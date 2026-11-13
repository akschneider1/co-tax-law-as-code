"""Score candidate spans against the hand-marked reference.

  python3 tools/evaluate.py CANDIDATES.json [MORE_RUNS.json ...]

For the first candidates file it prints, by span class, precision, recall and
F1 against extractions/extractions.json, counted two ways: exact (same
provision, class and characters) and overlapping (same provision and class,
any shared characters).

The hand marks are a reference, not the truth. Stanford RegLab found that 135
of 181 apparent false positives in a statutory benchmark were correct and
missing from the experts' list. So every disagreement is written to
extractions/adjudication.json with an empty decision for a person to fill in:
  candidate_right   the candidate is right and the reference is wrong or incomplete
  reference_right   the reference is right and the candidate is wrong
  both_defensible   either marking is acceptable
Decisions already in that file are kept, and a second table shows the scores
after applying them.

Integrity flags override the scores. A candidate span that is not word for
word in its provision (fabricated), or whose dates or number do not re-parse
to what it records (misparse), marks the whole file NOT RELIABLE.

With more than one candidates file, the files are treated as repeat runs and
the share of spans found in every run is reported.

The provisions shown to the model as examples (extractions/config.json) are
left out of every count. Standard library, Python 3.8+. Exit code 1 if any
integrity flag is raised.
"""
import json
import pathlib
import sys
from decimal import Decimal, InvalidOperation

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.textlib import (  # noqa: E402
    index, load_sections, parse_dollars, parse_effective_date, parse_percent, parse_period)

REFERENCE = ROOT / "extractions" / "extractions.json"
CONFIG = ROOT / "extractions" / "config.json"
ADJUDICATION = ROOT / "extractions" / "adjudication.json"
DECISIONS = ("candidate_right", "reference_right", "both_defensible")


def locate(groups, texts, skip, flags=None):
    """Return {(provision, class, start, end): span} for every span that is in the text.

    A span may carry its own 'start'. Otherwise repeated phrases are taken in
    order of appearance. Spans not found word for word are flagged.
    """
    found = {}
    for group in groups:
        provision = group["provision"]
        if provision in skip:
            continue
        text = texts.get(provision)
        cursor = {}
        for span in group["spans"]:
            phrase = span["text"]
            if text is None:
                start = -1
            elif "start" in span and text[span["start"]:span["start"] + len(phrase)] == phrase:
                start = span["start"]
            else:
                start = text.find(phrase, cursor.get(phrase, 0))
            if start < 0:
                if flags is not None:
                    flags.append(("fabricated", provision, span["class"], phrase))
                continue
            cursor[phrase] = start + len(phrase)
            found[(provision, span["class"], start, start + len(phrase))] = span
            if flags is not None:
                check_parse(provision, span, flags)
    return found


def check_parse(provision, span, flags):
    """Flag a period, value or threshold whose words do not parse to what it records."""
    try:
        if span["class"] == "period":
            recorded = span.get("normalized") or {}
            if parse_period(span["text"]) != (recorded.get("from"), recorded.get("to")):
                flags.append(("misparse", provision, "period", span["text"]))
        elif span["class"] == "value":
            if parse_percent(span["text"]) != Decimal(str(span.get("normalized"))):
                flags.append(("misparse", provision, "value", span["text"]))
        elif span["class"] == "threshold":
            if parse_dollars(span["text"]) != int(span.get("normalized")):
                flags.append(("misparse", provision, "threshold", span["text"]))
        elif span["class"] == "lifecycle":
            if parse_effective_date(span["text"]) != span.get("normalized"):
                flags.append(("misparse", provision, "lifecycle", span["text"]))
    except (ValueError, InvalidOperation, TypeError):
        flags.append(("misparse", provision, span["class"], span["text"]))


def overlaps(a, b):
    return a[0] == b[0] and a[1] == b[1] and a[2] < b[3] and b[2] < a[3]


def prf(tp, fp, fn):
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = (2 * precision * recall / (precision + recall)) if precision and recall else None
    return precision, recall, f1


def show(number):
    return " n/a" if number is None else "%.2f" % number


def score(reference, candidate, classes, credit_candidate=(), credit_reference=()):
    """Rows of (class, counts and scores), exact and overlapping.

    credit_candidate: candidate-only keys a person judged acceptable; they
    count as correct. credit_reference: reference-only keys judged wrong or
    optional; they are not counted as missed.
    """
    rows = []
    for name in list(classes) + ["all"]:
        ref = {k for k in reference if name in ("all", k[1])}
        cand = {k for k in candidate if name in ("all", k[1])}
        exact_tp = len(ref & cand)
        extra = {k for k in cand - ref if k in credit_candidate}
        forgiven = {k for k in ref - cand if k in credit_reference}
        exact = prf(exact_tp + len(extra), len(cand - ref) - len(extra), len(ref - cand) - len(forgiven))
        over_tp_c = sum(1 for c in cand if c in credit_candidate or any(overlaps(c, r) for r in ref))
        over_tp_r = sum(1 for r in ref if r in credit_reference or any(overlaps(r, c) for c in cand))
        p = over_tp_c / len(cand) if cand else None
        r = over_tp_r / len(ref) if ref else None
        f = (2 * p * r / (p + r)) if p and r else None
        rows.append((name, len(ref), len(cand), exact, (p, r, f)))
    return rows


def print_table(title, rows):
    print("\n" + title)
    print("  %-10s %5s %5s   %-17s   %-17s" % ("class", "ref", "cand", "exact  P    R    F1", "overlap P    R    F1"))
    for name, n_ref, n_cand, exact, over in rows:
        print("  %-10s %5d %5d      %s %s %s        %s %s %s"
              % (name, n_ref, n_cand, show(exact[0]), show(exact[1]), show(exact[2]),
                 show(over[0]), show(over[1]), show(over[2])))


def adjudication_key(side, key, span):
    return "%s|%s|%s|%d|%s" % (side, key[0], key[1], key[2], span["text"])


def main():
    paths = [pathlib.Path(a) for a in sys.argv[1:] if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    skip = set(config["example_provisions"])
    texts = {pid: p["text"] for pid, p in index(load_sections()).items() if p["text"]}
    reference_file = json.loads(REFERENCE.read_text(encoding="utf-8"))
    classes = list(reference_file["classes"])
    reference = locate(reference_file["groups"], texts, skip)

    runs, flags = [], []
    for position, path in enumerate(paths):
        data = json.loads(path.read_text(encoding="utf-8"))
        runs.append(locate(data["groups"], texts, skip, flags if position == 0 else []))
    candidate = runs[0]

    print("reference:  %s (%d spans outside the example provisions)" % (REFERENCE.name, len(reference)))
    print("candidates: %s (%d spans)" % (paths[0].name, len(candidate)))
    print("left out:   %d example provisions" % len(skip))
    print_table("Against the reference as it stands", score(reference, candidate, classes))

    # Disagreements go to a person. Earlier decisions are kept.
    previous = {}
    if ADJUDICATION.exists():
        for item in json.loads(ADJUDICATION.read_text(encoding="utf-8"))["items"]:
            previous[item["key"]] = item
    items = []
    for side, mine, theirs in (("candidate_only", candidate, reference), ("reference_only", reference, candidate)):
        for key in sorted(set(mine) - set(theirs)):
            item_key = adjudication_key(side, key, mine[key])
            old = previous.get(item_key, {})
            items.append({
                "key": item_key,
                "side": side,
                "provision": key[0],
                "class": key[1],
                "text": mine[key]["text"],
                "overlaps_other_side": any(overlaps(key, other) for other in theirs),
                "decision": old.get("decision"),
                "decided_by": old.get("decided_by"),
                "note": old.get("note"),
            })
    if items or ADJUDICATION.exists():
        ADJUDICATION.write_text(json.dumps({
            "about": "Disagreements between candidate spans and the hand-marked reference, for a person to decide. "
                     "Set decision to candidate_right, reference_right or both_defensible, and decided_by to your name. "
                     "Written by tools/evaluate.py, which keeps decisions already made.",
            "candidates": paths[0].name,
            "items": items,
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    decided = [i for i in items if i["decision"] in DECISIONS]
    print("\nDisagreements: %d (%d decided, %d waiting) -> %s"
          % (len(items), len(decided), len(items) - len(decided), ADJUDICATION.relative_to(ROOT)))
    if decided:
        by_key = {adjudication_key("candidate_only", k, candidate[k]): k for k in set(candidate) - set(reference)}
        by_key.update({adjudication_key("reference_only", k, reference[k]): k for k in set(reference) - set(candidate)})
        credit_candidate = {by_key[i["key"]] for i in decided
                            if i["side"] == "candidate_only" and i["decision"] != "reference_right"}
        credit_reference = {by_key[i["key"]] for i in decided
                            if i["side"] == "reference_only" and i["decision"] != "reference_right"}
        print_table("After applying the decisions made so far",
                    score(reference, candidate, classes, credit_candidate, credit_reference))

    if len(runs) > 1:
        union = set().union(*[set(r) for r in runs])
        everywhere = set(runs[0]).intersection(*[set(r) for r in runs[1:]])
        share = len(everywhere) / len(union) if union else 1.0
        print("\nStability over %d runs: %d of %d distinct spans appear in every run (%.2f)."
              % (len(runs), len(everywhere), len(union), share))

    if flags:
        print("\nINTEGRITY FLAGS (%d). These candidates are NOT RELIABLE, whatever the scores say:" % len(flags))
        for kind, provision, cls, phrase in flags:
            print("  %s: %s %s %r" % (kind, provision, cls, phrase[:80]))
        return 1
    print("\nNo integrity flags: every candidate span is word for word in its provision, "
          "and every date, number and amount re-parses to what it records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
