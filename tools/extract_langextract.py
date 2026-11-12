"""Mark spans with LangExtract instead of by hand.

Checked against LangExtract 1.7.2 with --dry-run, which runs the library's
whole pipeline (prompting, chunking, parsing, alignment) with a stand-in
model that answers from the hand marks. It has NOT been run against a real
model: no model key was available. A dry run tests the plumbing, not a model.

Needs Python 3.10+, `pip install -r requirements-langextract.txt`, and a key:
    --ask-key                           prompts for it in the terminal, hidden, for this run only
or  export LANGEXTRACT_API_KEY=...      (Gemini, the default)
or  export OPENAI_API_KEY=...           with --model gpt-4o and langextract[openai]
or  export ANTHROPIC_API_KEY=...        with --model claude-opus-5-5 and `pip install anthropic`
                                        (COTAX_CLAUDE_API_KEY is read first, if set)
or a local Ollama model                 with --model gemma2:2b --model-url http://localhost:11434

What it does
  1. Uses the hand-marked provisions named in extractions/config.json as the
     few-shot examples.
  2. Asks the model to mark spans in every other provision that has text,
     sending with each one the context a reader needs (tools/textlib.py
     context_for): heading, lead-ins, definitions, provisos, cross-references.
     Pass --no-context to leave it out, to measure what it is worth.
  3. Keeps a span only if LangExtract aligned it exactly and the characters at
     that position are the span's words. Fuzzy alignment is switched off.
     Each kept span records where it starts. Dropped spans are counted by
     reason.
  4. Saves each provision's result in extractions/cache/, keyed by the text,
     the prompt, the context and the model, so unchanged provisions are not
     sent again. --replay uses the cache only and fails on a miss, so a
     published run can be reproduced without a key.
  5. Writes extractions/candidates.langextract.json in the same format as the
     hand-marked file.

Then:
    python3 tools/evaluate.py extractions/candidates.langextract.json
    python3 tools/build_web.py --extractions extractions/candidates.langextract.json
The first scores the candidates and lists disagreements for a person to
decide. The second re-parses every date and number and rebuilds the viewer.
"""
import argparse
import getpass
import hashlib
import json
import os
import pathlib
import sys
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.textlib import attach_cross_refs, context_for, index, load_sections  # noqa: E402

HAND_MARKED = ROOT / "extractions" / "extractions.json"
CONFIG = ROOT / "extractions" / "config.json"
CACHE = ROOT / "extractions" / "cache"
OUTPUT = ROOT / "extractions" / "candidates.langextract.json"

PROMPT = textwrap.dedent("""\
    You are marking up one provision of a tax statute. Extract spans in order of
    appearance, using the exact words of the text, in the same capitals. Do not
    paraphrase. Do not let spans overlap. Use only these classes:
      period     the tax years the provision covers. Attributes: "from" and "to"
                 as ISO dates, inclusive, or "" when open-ended. "before January 1,
                 2023" means to 2022-12-31.
      value      the number the provision sets, as written. Attribute: "decimal",
                 the number as a fraction, so "twenty percent" is "0.20".
      threshold  an income amount where a rate starts or stops, as written.
                 Attribute: "dollars", the amount in digits.
      base       what the number is applied to.
      who        who the provision applies to.
      exception  a cross-reference that can displace the provision.
      effect     a consequence other than a number, such as a refund or a repeal.
    Mark every separate period phrase as its own span. If the provision sets no
    number, extract no value span.
    Many provisions cover only tax years that have ended, or are repealed by a
    later provision. Mark them exactly as you would a current one: a period
    that has ended is still a period. Never skip a provision because it has
    expired.
    The context before the examples is there to help you read the provision.
    Extract spans from the provision only, never from the context.""")


def attributes_for(span):
    normalized = span.get("normalized")
    if span["class"] == "period":
        return {"from": normalized["from"] or "", "to": normalized["to"] or ""}
    if span["class"] == "value":
        return {"decimal": normalized}
    if span["class"] == "threshold":
        return {"dollars": normalized}
    return {}


def build_examples(lx, provisions, hand, example_ids):
    examples = []
    for group in hand["groups"]:
        if group["provision"] not in example_ids:
            continue
        text = provisions[group["provision"]]
        ordered = sorted(group["spans"], key=lambda s: text.find(s["text"]))
        examples.append(lx.data.ExampleData(
            text=text,
            extractions=[
                lx.data.Extraction(
                    extraction_class=span["class"],
                    extraction_text=span["text"],
                    attributes=attributes_for(span),
                )
                for span in ordered
            ],
        ))
    return examples


def to_span(extraction, classes, text, dropped):
    """Convert one LangExtract extraction to this project's span format, or None.

    A span is kept only if the library located it exactly and the characters
    at that position are its words. The position is kept, so a phrase that
    occurs twice in a provision is not confused with its first occurrence.
    """
    cls = extraction.extraction_class
    if cls not in classes:
        dropped["unknown class"] += 1
        return None
    interval = extraction.char_interval
    if interval is None or interval.start_pos is None:
        dropped["not located in the text"] += 1
        return None
    status = getattr(extraction.alignment_status, "value", extraction.alignment_status)
    if status != "match_exact":
        dropped["not an exact match (%s)" % status] += 1
        return None
    start, end = interval.start_pos, interval.end_pos
    if text[start:end] != extraction.extraction_text:
        dropped["words differ from the text at that position"] += 1
        return None
    span = {"class": cls, "text": extraction.extraction_text, "start": start}
    attrs = extraction.attributes or {}
    if cls == "period":
        span["normalized"] = {"from": attrs.get("from") or None, "to": attrs.get("to") or None}
    elif cls == "value":
        span["normalized"] = str(attrs.get("decimal", ""))
    elif cls == "threshold":
        span["normalized"] = str(attrs.get("dollars", ""))
    return span


def without_overlaps(spans, dropped):
    kept, taken = [], []
    for span in sorted(spans, key=lambda s: s["start"]):
        start, end = span["start"], span["start"] + len(span["text"])
        if any(start < e and s < end for s, e in taken):
            dropped["overlaps an earlier span"] += 1
            continue
        taken.append((start, end))
        kept.append(span)
    return kept


def cache_key(text, context, examples_text, model, passes, run=1):
    digest = hashlib.sha256()
    parts = [text, PROMPT, context or "", examples_text, model, str(passes)]
    if run != 1:
        parts.append("run:%d" % run)  # run 1 keeps the key it had before repeat runs existed
    for part in parts:
        digest.update(part.encode("utf-8"))
        digest.update(b"\x00")
    return digest.hexdigest()


def stand_in_model(lx, provisions, hand):
    """A model that answers from the hand marks, for --dry-run.

    It lets the library's prompting, parsing and alignment be exercised with
    no key. It says nothing about how a real model would do.
    """
    from langextract.core import base_model, types

    marks = {g["provision"]: g["spans"] for g in hand["groups"]}

    class StandIn(base_model.BaseLanguageModel):
        def infer(self, batch_prompts, **kwargs):
            for prompt in batch_prompts:
                # The provision is the last thing in the prompt; take the longest text it ends with.
                body = prompt.rstrip()
                body = body[:body.rfind("\n")].rstrip() if "\n" in body else body
                hits = [pid for pid, text in provisions.items() if body.endswith(text)]
                pid = max(hits, key=lambda h: len(provisions[h])) if hits else None
                text = provisions.get(pid, "")
                ordered = sorted(marks.get(pid, []), key=lambda s: text.find(s["text"]))
                items = []
                for span in ordered:
                    items.append({span["class"]: span["text"],
                                  span["class"] + "_attributes": attributes_for(span)})
                yield [types.ScoredOutput(score=1.0, output=json.dumps({"extractions": items}))]

    return StandIn()


def claude_model(model_id):
    """A LangExtract model that calls Claude through the official Anthropic SDK.

    LangExtract ships no Anthropic provider, so this supplies one: it sends
    each prompt LangExtract builds as a single user message and hands the
    reply back for LangExtract to parse and align. Needs `pip install
    anthropic` and ANTHROPIC_API_KEY (or another credential the SDK finds).
    """
    import re

    import anthropic
    from langextract.core import base_model, types

    # Name the API host outright. Some environments set ANTHROPIC_BASE_URL for
    # their own tooling, and the key for this run belongs to api.anthropic.com.
    # COTAX_CLAUDE_API_KEY, if set, is used in preference to ANTHROPIC_API_KEY. It exists for
    # environments where ANTHROPIC_API_KEY is reserved for the tooling that hosts the session.
    client = anthropic.Anthropic(base_url="https://api.anthropic.com",
                                 api_key=os.environ.get("COTAX_CLAUDE_API_KEY") or None)

    # Claude Haiku 5.5 has no server-side refusal fallback, so it is not asked for one.
    state = {"fallbacks": "haiku" not in model_id}

    class Claude(base_model.BaseLanguageModel):
        def infer(self, batch_prompts, **kwargs):
            for prompt in batch_prompts:
                request = dict(model=model_id, max_tokens=16000, output_config={"effort": "medium"},
                               messages=[{"role": "user", "content": prompt}])
                response = None
                if state["fallbacks"]:
                    try:
                        # If a safety classifier declines, let the API retry on its default fallback model.
                        response = client.beta.messages.create(
                            betas=["server-side-fallback-2026-07-01"], fallbacks="default", **request)
                    except anthropic.BadRequestError:
                        # This model or account does not take the fallback setting; go on without it.
                        state["fallbacks"] = False
                if response is None:
                    response = client.messages.create(**request)
                if response.stop_reason == "refusal":
                    raise RuntimeError("Claude declined the request (stop_reason refusal)")
                if response.stop_reason == "max_tokens":
                    raise RuntimeError("Claude's reply was cut off at max_tokens")
                if response.model != model_id:
                    raise RuntimeError("the reply came from %s, not %s; not recorded as a %s result"
                                       % (response.model, model_id, model_id))
                text = "".join(block.text for block in response.content if block.type == "text").strip()
                fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
                yield [types.ScoredOutput(score=1.0, output=fenced.group(1) if fenced else text)]

    return Claude()


class CacheMiss(Exception):
    """Raised in replay mode when a provision's result is not in the cache."""


def load_langextract():
    """Import LangExtract and report its version, or raise ImportError."""
    import langextract as lx
    try:
        from importlib.metadata import version
        lx_version = version("langextract")
    except Exception:
        lx_version = "version unknown"
    return lx, lx_version


def setup(lx):
    """Everything a run needs that does not depend on the model."""
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    example_ids = tuple(config["example_provisions"])
    hand = json.loads(HAND_MARKED.read_text(encoding="utf-8"))
    sections = attach_cross_refs(load_sections())
    provisions = {pid: p["text"] for pid, p in index(sections).items() if p["text"]}
    examples = build_examples(lx, provisions, hand, example_ids)
    examples_text = json.dumps([[e.text, [(x.extraction_class, x.extraction_text) for x in e.extractions]]
                                for e in examples], ensure_ascii=False)
    return {
        "config": config, "example_ids": example_ids, "hand": hand, "sections": sections,
        "provisions": provisions, "examples": examples, "examples_text": examples_text,
        "targets": [pid for pid in sorted(provisions) if pid not in example_ids],
    }


def model_options(lx, env, model, model_url=None, dry_run=False):
    """Return (name recorded for the model, keyword arguments for lx.extract)."""
    options = {"model_url": model_url} if model_url else {}
    if dry_run:
        options["model"] = stand_in_model(lx, env["provisions"], env["hand"])
        return "stand-in (hand marks)", options
    if model.startswith("claude-"):
        options["model"] = claude_model(model)
    else:
        options["model_id"] = model
    return model, options


def mark_provision(lx, lx_version, env, provision_id, model_name, options,
                   passes=1, with_context=True, run=1, replay=False, use_cache=True):
    """Mark one provision. Returns (raw extractions, True if they came from the cache).

    run numbers repeat runs: run 1 and run 2 of the same provision are cached
    separately, so a repeat run is a fresh call and can be compared with the first.
    """
    text = env["provisions"][provision_id]
    context = context_for(provision_id, env["sections"]) if with_context else None
    key = cache_key(text, context, env["examples_text"], model_name, passes, run)
    cache_file = CACHE / (key + ".json")
    if use_cache and cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))["extractions"], True
    if replay:
        raise CacheMiss(provision_id)
    result = lx.extract(
        text_or_documents=text,
        prompt_description=PROMPT,
        examples=env["examples"],
        additional_context=context,
        extraction_passes=passes,
        # One provision is one unit: never split it, or a span across the split is lost.
        max_char_buffer=len(text) + 1000,
        # Verbatim only: no fuzzy matching, no partial matches.
        resolver_params={"enable_fuzzy_alignment": False, "accept_match_lesser": False},
        show_progress=False,
        **options
    )
    raw = [{
        "extraction_class": e.extraction_class,
        "extraction_text": e.extraction_text,
        "attributes": e.attributes,
        "start": e.char_interval.start_pos if e.char_interval else None,
        "end": e.char_interval.end_pos if e.char_interval else None,
        "alignment_status": getattr(e.alignment_status, "value", e.alignment_status),
    } for e in result.extractions]
    if use_cache:
        CACHE.mkdir(exist_ok=True)
        cache_file.write_text(json.dumps({
            "provision": provision_id, "model": model_name, "langextract": lx_version,
            "passes": passes, "with_context": context is not None, "run": run, "extractions": raw,
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return raw, False


def group_for(env, provision_id, raw, dropped):
    """Turn raw extractions into this project's group of checked spans, or None if none survive."""
    text = env["provisions"][provision_id]
    spans = [to_span(_Raw(r), env["hand"]["classes"], text, dropped) for r in raw]
    spans = without_overlaps([s for s in spans if s], dropped)
    if not spans:
        return None
    sets_value = any(s["class"] == "value" for s in spans)
    section = next(s["id"] for s in env["sections"] if provision_id.startswith(s["id"] + "/"))
    group = {
        "provision": provision_id,
        "parameter": env["config"]["parameter_by_section"].get(section) if sets_value else None,
        "spans": spans,
    }
    if any(s["class"] == "threshold" for s in spans) and sum(s["class"] == "value" for s in spans) > 1:
        group["derive"] = "schedule"  # several rates with thresholds: a bracket schedule
    return group


def main():
    parser = argparse.ArgumentParser(description="Mark statute spans with LangExtract.")
    parser.add_argument("--model", default="gemini-3.5-flash",
                        help="model id: a Gemini, OpenAI or Ollama model LangExtract knows, or a Claude model "
                             "such as claude-opus-5-5, which is called through the Anthropic SDK")
    parser.add_argument("--model-url", default=None, help="for a local Ollama model")
    parser.add_argument("--passes", type=int, default=1,
                        help="extraction passes per provision; later passes add spans, they are not a vote")
    parser.add_argument("--run", type=int, default=1,
                        help="which repeat run this is; each run number is cached separately, so run 2 "
                             "calls the model again and can be compared with run 1")
    parser.add_argument("--no-context", action="store_true", help="send each provision without its context")
    parser.add_argument("--replay", action="store_true", help="use cached results only; fail on a miss")
    parser.add_argument("--dry-run", action="store_true",
                        help="use a stand-in model that answers from the hand marks; tests the plumbing only")
    parser.add_argument("--output", default=str(OUTPUT), help="where to write the candidates")
    parser.add_argument("--ask-key", action="store_true",
                        help="prompt for the model key in the terminal, without showing it; it is used for "
                             "this run only and is not saved anywhere")
    args = parser.parse_args()

    if sys.version_info < (3, 10):
        print("LangExtract needs Python 3.10 or later; this is %s." % sys.version.split()[0])
        return 2
    try:
        lx, lx_version = load_langextract()
    except ImportError:
        print("LangExtract is not installed: pip install -r requirements-langextract.txt")
        return 2

    if args.ask_key:
        if not sys.stdin.isatty():
            print("--ask-key needs an interactive terminal; set the key as an environment variable instead.")
            return 2
        variable = ("ANTHROPIC_API_KEY" if args.model.startswith("claude-") else
                    "OPENAI_API_KEY" if args.model.startswith(("gpt-", "o1", "o3", "o4")) else "LANGEXTRACT_API_KEY")
        os.environ[variable] = getpass.getpass("Model key for %s (input is hidden): " % args.model).strip()

    env = setup(lx)
    try:
        model_name, options = model_options(lx, env, args.model, args.model_url, args.dry_run)
    except ImportError:
        print("The Anthropic SDK is not installed: pip install anthropic")
        return 2

    from collections import Counter
    groups, dropped, sent, cached = [], Counter(), 0, 0
    stopped = None
    for provision_id in env["targets"]:
        try:
            raw, was_cached = mark_provision(
                lx, lx_version, env, provision_id, model_name, options, passes=args.passes,
                with_context=not args.no_context, run=args.run, replay=args.replay, use_cache=not args.dry_run)
        except CacheMiss:
            print("cache miss for %s; run without --replay to call the model" % provision_id)
            return 1
        except Exception as exc:  # a provider error: quota, network, bad key
            # Results so far are in the cache, so the next run resumes here.
            stopped = "%s: %s" % (provision_id, " ".join(str(exc).split())[:300])
            break
        cached += was_cached
        sent += not was_cached
        group = group_for(env, provision_id, raw, dropped)
        if group is None:
            continue
        groups.append(group)
        print("%-58s %d spans kept" % (provision_id, len(group["spans"])))

    # The examples are hand-marked; carry them over so the file is complete.
    hand, example_ids = env["hand"], env["example_ids"]
    groups.extend(g for g in hand["groups"] if g["provision"] in example_ids)
    output = pathlib.Path(args.output)
    output.write_text(json.dumps({
        "about": ("DRY RUN: produced by a stand-in that answers from the hand marks. Not a model result."
                  if args.dry_run else
                  "INCOMPLETE: the run stopped before every provision was sent. Unreviewed."
                  if stopped else "Candidate spans marked by a model through LangExtract. Unreviewed."),
        "complete": stopped is None,
        "extracted_by": "LangExtract %s with %s%s; %d provisions hand-marked as examples. Not reviewed by a lawyer."
                        % (lx_version, model_name, ", no context" if args.no_context else "", len(example_ids)),
        "classes": hand["classes"],
        "groups": sorted(groups, key=lambda g: g["provision"]),
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\nwrote %s: %d provisions sent, %d from cache" % (output.name, sent, cached))
    if dropped:
        print("spans dropped:")
        for reason, count in sorted(dropped.items()):
            print("  %d  %s" % (count, reason))
    else:
        print("no spans dropped")
    if stopped:
        print("\nSTOPPED before finishing, at %s" % stopped)
        print("The output is incomplete. Results so far are cached; run the same command again to resume.")
        return 1
    print("next: python3 tools/evaluate.py %s" % output)
    return 0


class _Raw:
    """Gives a cached extraction the attributes to_span reads."""

    class _Interval:
        def __init__(self, start, end):
            self.start_pos, self.end_pos = start, end

    def __init__(self, raw):
        self.extraction_class = raw["extraction_class"]
        self.extraction_text = raw["extraction_text"]
        self.attributes = raw["attributes"]
        self.alignment_status = raw["alignment_status"]
        self.char_interval = self._Interval(raw["start"], raw["end"]) if raw["start"] is not None else None


if __name__ == "__main__":
    sys.exit(main())
