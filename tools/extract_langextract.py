"""Mark spans with LangExtract instead of by hand.

UNTESTED: written against the LangExtract README (v1.7.2) but never run, because
the machine it was written on had Python 3.8 and no model API key.

Needs Python 3.10+, `pip install -r requirements-langextract.txt`, and a key:
    export LANGEXTRACT_API_KEY=...      (Gemini, the default)
or  export OPENAI_API_KEY=...           with --model gpt-4o and langextract[openai]
or a local Ollama model                 with --model gemma2:2b --model-url http://localhost:11434

What it does
  1. Uses two hand-marked provisions from extractions/extractions.json as the
     few-shot examples.
  2. Asks the model to mark spans in every other provision that has text.
  3. Drops any span that is not verbatim in the provision, or that overlaps one
     already kept, and says how many it dropped.
  4. Writes extractions/candidates.langextract.json in the same format as the
     hand-marked file, and reports where the model and the hand marks differ.

The output is a set of candidates. Check it with:
    python3 tools/build_web.py --extractions extractions/candidates.langextract.json
which re-parses every date and number from the text and fails on any mismatch.
"""
import argparse
import json
import pathlib
import sys
import textwrap
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
HAND_MARKED = ROOT / "extractions" / "extractions.json"
OUTPUT = ROOT / "extractions" / "candidates.langextract.json"

# Provisions used as few-shot examples; everything else is a target.
EXAMPLE_PROVISIONS = ("/us/co/crs/39-22-104/1.7/b", "/us/co/crs/39-22-123.5/2/a/I")

# Which parameter a section's value-setting provisions feed.
PARAMETER_BY_SECTION = {
    "/us/co/crs/39-22-104": "co.income_tax.rate_schedule",
    "/us/co/crs/39-22-123.5": "co.eitc.match_rate",
}

PROMPT = textwrap.dedent("""\
    You are marking up one provision of a tax statute. Extract spans in order of
    appearance, using the exact words of the text. Do not paraphrase. Do not let
    spans overlap. Use only these classes:
      period     the tax years the provision covers. Attributes: "from" and "to"
                 as ISO dates, inclusive, or "" when open-ended. "before January 1,
                 2023" means to 2022-12-31.
      value      the number the provision sets, as written. Attribute: "decimal",
                 the number as a fraction, so "twenty percent" is "0.20".
      base       what the number is applied to.
      who        who the provision applies to.
      exception  a cross-reference that can displace the provision.
      effect     a consequence other than a number, such as a refund or a repeal.
    Mark every separate period phrase as its own span. If the provision sets no
    number, extract no value span.""")


def load_provisions():
    """Return {provision id: whitespace-normalised text} for provisions with text."""
    provisions = {}
    for path in sorted((ROOT / "text").glob("*.xml")):
        for element in ET.parse(str(path)).getroot().iter("provision"):
            content = element.find("content")
            if content is not None:
                provisions[element.get("id")] = " ".join(content.text.split())
    return provisions


def attributes_for(span):
    normalized = span.get("normalized")
    if span["class"] == "period":
        return {"from": normalized["from"] or "", "to": normalized["to"] or ""}
    if span["class"] == "value":
        return {"decimal": normalized}
    return {}


def build_examples(lx, provisions, hand):
    examples = []
    for group in hand["groups"]:
        if group["provision"] not in EXAMPLE_PROVISIONS:
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


def to_span(extraction, classes):
    """Convert one LangExtract extraction to this project's span format."""
    cls = extraction.extraction_class
    if cls not in classes:
        return None
    span = {"class": cls, "text": extraction.extraction_text}
    attrs = extraction.attributes or {}
    if cls == "period":
        span["normalized"] = {"from": attrs.get("from") or None, "to": attrs.get("to") or None}
    elif cls == "value":
        span["normalized"] = str(attrs.get("decimal", ""))
    return span


def keep_grounded(text, spans):
    """Keep spans that are verbatim and do not overlap an earlier kept span."""
    kept, taken, dropped = [], [], 0
    for span in spans:
        start = text.find(span["text"])
        end = start + len(span["text"])
        if start < 0 or any(start < e and s < end for s, e in taken):
            dropped += 1
            continue
        taken.append((start, end))
        kept.append(span)
    return kept, dropped


def section_of(provision_id):
    return next((s for s in PARAMETER_BY_SECTION if provision_id.startswith(s + "/")), None)


def compare(hand, candidates):
    """Print where the model's spans differ from the hand-marked ones."""
    def keyed(groups):
        return {g["provision"]: {(s["class"], s["text"]) for s in g["spans"]} for g in groups}

    mine, theirs = keyed(hand["groups"]), keyed(candidates)
    print("\nModel against hand marks (hand-marked provisions that were not examples):")
    for provision in sorted(set(mine) - set(EXAMPLE_PROVISIONS)):
        got = theirs.get(provision, set())
        missing, extra = mine[provision] - got, got - mine[provision]
        verdict = "same" if not missing and not extra else "%d missing, %d extra" % (len(missing), len(extra))
        print("  %-36s %s" % (provision, verdict))
        for cls, text in sorted(missing):
            print("      missing %-9s %r" % (cls, text[:70]))
        for cls, text in sorted(extra):
            print("      extra   %-9s %r" % (cls, text[:70]))


def main():
    parser = argparse.ArgumentParser(description="Mark statute spans with LangExtract.")
    parser.add_argument("--model", default="gemini-3.5-flash", help="LangExtract model id")
    parser.add_argument("--model-url", default=None, help="for a local Ollama model")
    parser.add_argument("--passes", type=int, default=1, help="extraction passes per provision")
    args = parser.parse_args()

    if sys.version_info < (3, 10):
        print("LangExtract needs Python 3.10 or later; this is %s." % sys.version.split()[0])
        return 2
    try:
        import langextract as lx
    except ImportError:
        print("LangExtract is not installed: pip install -r requirements-langextract.txt")
        return 2

    hand = json.loads(HAND_MARKED.read_text(encoding="utf-8"))
    provisions = load_provisions()
    examples = build_examples(lx, provisions, hand)
    options = {"model_url": args.model_url} if args.model_url else {}

    groups, dropped_total = [], 0
    for provision_id, text in sorted(provisions.items()):
        if provision_id in EXAMPLE_PROVISIONS:
            continue
        result = lx.extract(
            text_or_documents=text,
            prompt_description=PROMPT,
            examples=examples,
            model_id=args.model,
            extraction_passes=args.passes,
            **options
        )
        spans = [to_span(e, hand["classes"]) for e in result.extractions]
        spans, dropped = keep_grounded(text, [s for s in spans if s])
        dropped_total += dropped
        if not spans:
            continue
        sets_value = any(s["class"] == "value" for s in spans) and any(s["class"] == "period" for s in spans)
        groups.append({
            "provision": provision_id,
            "parameter": PARAMETER_BY_SECTION.get(section_of(provision_id)) if sets_value else None,
            "spans": spans,
        })
        print("%-40s %d spans kept, %d dropped" % (provision_id, len(spans), dropped))

    # The examples are hand-marked; carry them over so the file is complete.
    groups.extend(g for g in hand["groups"] if g["provision"] in EXAMPLE_PROVISIONS)
    OUTPUT.write_text(json.dumps({
        "about": "Candidate spans marked by a model through LangExtract. Unreviewed.",
        "extracted_by": "LangExtract %s with %s; two provisions hand-marked as examples. Not reviewed by a lawyer."
                        % (getattr(lx, "__version__", "version unknown"), args.model),
        "classes": hand["classes"],
        "groups": sorted(groups, key=lambda g: g["provision"]),
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\nwrote %s (%d spans dropped as not verbatim or overlapping)" % (OUTPUT.relative_to(ROOT), dropped_total))
    compare(hand, groups)
    return 0


if __name__ == "__main__":
    sys.exit(main())
