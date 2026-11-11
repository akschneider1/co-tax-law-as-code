"""Ground the parameters in the statute text and build the web viewer.

Bottom-up, in four steps:
  1. locate every extracted span verbatim in its provision (character offsets)
  2. re-parse period and value spans with deterministic code and compare with
     the 'normalized' value recorded in extractions/extractions.json
  3. derive, for each tax year, the value the statute text alone gives
  4. check every statute claim in parameters/*.json against step 3

Writes web/index.html from web/template.html, with the data inlined.
Pass --extractions PATH to check and view a different set of spans, such as
the candidates written by tools/extract_langextract.py. Exit code 1 if any span is not found, any parse disagrees,
or any parameter's statute claim is not supported by an extraction.
"""
import datetime
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from decimal import Decimal

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import engine.co_rules  # noqa: E402,F401  (registers the rules)
from engine.core import RULES, Parameters  # noqa: E402

YEARS = range(2022, 2028)

UNITS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19,
}
TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90,
}
MONTHS = {
    name: number for number, name in enumerate(
        ["January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"], start=1)
}
DATE = r"([A-Z][a-z]+) (\d{1,2}), (\d{4})"


def words_to_int(words):
    total = 0
    for token in words.replace("-", " ").split():
        if token in UNITS:
            total += UNITS[token]
        elif token in TENS:
            total += TENS[token]
        else:
            raise ValueError("unknown number word %r" % token)
    return total


def parse_percent(text):
    """'twenty-five percent' -> 0.25; 'four and forty one-hundredths percent' -> 0.044."""
    match = re.fullmatch(r"(.+?)(?: and (.+?) one-hundredths)? percent", text)
    if not match:
        raise ValueError("not a percentage phrase: %r" % text)
    whole = Decimal(words_to_int(match.group(1)))
    hundredths = Decimal(words_to_int(match.group(2))) if match.group(2) else Decimal(0)
    return (whole + hundredths / 100) / 100


def to_date(match_groups):
    month, day, year = match_groups
    return datetime.date(int(year), MONTHS[month], int(day))


def parse_period(text):
    """Return (from, to) as ISO strings or None, from the statute's date phrasing."""
    start = end = None
    after = re.search(r"on or after " + DATE, text)
    before = re.search(r"(?:before|prior to) " + DATE, text)
    single = re.search(r"commencing on " + DATE, text)
    if after:
        start = to_date(after.groups())
    if before:
        end = to_date(before.groups()) - datetime.timedelta(days=1)
    if single and not after and not before:
        start = to_date(single.groups())
        end = datetime.date(start.year, 12, 31)
    if start is None and end is None:
        raise ValueError("no date phrase recognised in %r" % text)
    return (start.isoformat() if start else None, end.isoformat() if end else None)


def covers(period, day):
    start, end = period
    return (start is None or start <= day) and (end is None or day <= end)


def load_sections():
    sections = []
    for path in sorted((ROOT / "text").glob("*.xml")):
        root = ET.parse(str(path)).getroot()
        meta = root.find("meta")
        provisions = []

        def walk(element, label, depth):
            for child in element.findall("provision"):
                child_label = label + child.get("num")
                content = child.find("content")
                provisions.append({
                    "id": child.get("id"),
                    "label": child_label,
                    "depth": depth,
                    "status": child.get("status"),
                    "text": " ".join(content.text.split()) if content is not None else None,
                    "spans": [],
                    "parameter": None,
                })
                walk(child, child_label, depth + 1)

        walk(root, "", 0)
        sections.append({
            "id": root.get("id"),
            "citation": meta.findtext("citation"),
            "heading": meta.findtext("heading"),
            "source": dict(meta.find("source").attrib),
            "authority": meta.findtext("authority"),
            "note": meta.findtext("note"),
            "provisions": provisions,
        })
    return sections


def ground(sections, extractions, errors):
    """Steps 1 and 2. Attach located, checked spans to their provisions."""
    by_id = {p["id"]: p for s in sections for p in s["provisions"]}
    for group in extractions["groups"]:
        provision = by_id.get(group["provision"])
        if provision is None or provision["text"] is None:
            errors.append("extraction targets unknown or empty provision %s" % group["provision"])
            continue
        provision["parameter"] = group["parameter"]
        taken = []
        for span in group["spans"]:
            start = provision["text"].find(span["text"])
            if start < 0:
                errors.append("span not found verbatim in %s: %r" % (group["provision"], span["text"]))
                continue
            end = start + len(span["text"])
            if any(start < e and s < end for s, e in taken):
                errors.append("overlapping span in %s: %r" % (group["provision"], span["text"]))
                continue
            taken.append((start, end))

            record = {"start": start, "end": end, "class": span["class"], "normalized": None}
            try:
                if span["class"] == "period":
                    parsed = parse_period(span["text"])
                    record["normalized"] = {"from": parsed[0], "to": parsed[1]}
                    declared = (span["normalized"]["from"], span["normalized"]["to"])
                    if parsed != declared:
                        errors.append("period mismatch in %s: text parses to %s, extraction says %s"
                                      % (group["provision"], parsed, declared))
                elif span["class"] == "value":
                    parsed = parse_percent(span["text"])
                    record["normalized"] = str(parsed.normalize())
                    if parsed != Decimal(span["normalized"]):
                        errors.append("value mismatch in %s: text parses to %s, extraction says %s"
                                      % (group["provision"], parsed, span["normalized"]))
            except ValueError as exc:
                errors.append("%s: %s" % (group["provision"], exc))
            provision["spans"].append(record)
        provision["spans"].sort(key=lambda s: s["start"])
    return by_id


def statute_value(by_id, parameter_id, day):
    """Step 3. What the ingested text alone says for this parameter on this day."""
    hits = []
    for provision in by_id.values():
        if provision["parameter"] != parameter_id:
            continue
        values = [i for i, s in enumerate(provision["spans"]) if s["class"] == "value"]
        for index, span in enumerate(provision["spans"]):
            if span["class"] != "period" or not values:
                continue
            period = (span["normalized"]["from"], span["normalized"]["to"])
            if covers(period, day):
                hits.append({
                    "provision": provision["id"],
                    "label": provision["label"],
                    "value": provision["spans"][values[0]]["normalized"],
                    "period_span": index,
                    "value_span": values[0],
                })
    return hits


def as_rate(value):
    """A one-bracket schedule and a plain rate are the same statute claim."""
    if isinstance(value, list):
        return Decimal(value[0]["rate"]) if len(value) == 1 else None
    return Decimal(value)


def build_parameters(parameters, by_id, errors):
    out = []
    for pid, data in sorted(parameters.by_id.items()):
        # Step 4: every statute claim in the parameter file must be grounded.
        for entry in data["values"]:
            for source in entry["sources"]:
                if source["kind"] != "statute":
                    continue
                hits = statute_value(by_id, pid, entry["effective_from"])
                match = [h for h in hits if h["provision"] == source["ref"]
                         and Decimal(h["value"]) == as_rate(source["states"])]
                if not match:
                    errors.append("%s from %s: statute claim %s = %s is not supported by any extraction"
                                  % (pid, entry["effective_from"], source["ref"], json.dumps(source["states"])))

        years = []
        for year in YEARS:
            day = "%d-01-01" % year
            hits = statute_value(by_id, pid, day)
            if len({h["value"] for h in hits}) > 1:
                errors.append("%s %d: provisions disagree: %s" % (pid, year, [h["provision"] for h in hits]))
            entry = next((e for e in data["values"]
                          if e["effective_from"] <= day and (e.get("effective_to") is None or day <= e["effective_to"])), None)
            years.append({
                "year": year,
                "statute": hits[0] if hits else None,
                "used": entry["value"] if entry else None,
                "status": entry["status"] if entry else "not_recorded",
                "other_sources": [s for s in entry["sources"] if s["kind"] != "statute"] if entry else [],
                "conflict_note": entry.get("conflict_note") if entry else None,
                "caveat": entry.get("caveat") if entry else None,
            })
        out.append({
            "id": pid,
            "description": data["description"],
            "value_type": data["value_type"],
            "gaps": data.get("gaps", []),
            "years": years,
        })
    return out


def main():
    errors = []
    sections = load_sections()
    source = ROOT / "extractions" / "extractions.json"
    if "--extractions" in sys.argv:
        source = pathlib.Path(sys.argv[sys.argv.index("--extractions") + 1]).resolve()
    print("extractions: %s" % source.name)
    extractions = json.loads(source.read_text(encoding="utf-8"))
    by_id = ground(sections, extractions, errors)
    parameters = build_parameters(Parameters(), by_id, errors)
    rules = [{"id": rid, "cites": list(f.cites), "parameters": list(f.params),
              "summary": (f.__doc__ or "").strip().splitlines()[0]}
             for rid, f in sorted(RULES.items())]

    span_count = sum(len(p["spans"]) for p in by_id.values())
    print("spans located verbatim: %d" % span_count)
    print("parameters derived for tax years %d to %d: %d" % (YEARS[0], YEARS[-1], len(parameters)))
    if errors:
        print("\nERRORS (%d):" % len(errors))
        for error in errors:
            print("  " + error)
        return 1

    data = {
        "generated": datetime.date.today().isoformat(),
        "uswds": (ROOT / "web" / "assets" / "uswds" / "VERSION").read_text().strip(),
        "classes": extractions["classes"],
        "extracted_by": extractions["extracted_by"],
        "sections": sections,
        "parameters": parameters,
        "rules": rules,
    }
    # The data is inlined so the page opens by double-click; styles load from web/assets/.
    template = (ROOT / "web" / "template.html").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    target = ROOT / "web" / "index.html"
    target.write_text(template.replace("/*COTAX_DATA*/", "window.COTAX = " + payload + ";"), encoding="utf-8")
    print("wrote %s" % target.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
