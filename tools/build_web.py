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
import sys
from decimal import Decimal

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import engine.co_rules  # noqa: E402,F401  (registers the rules)
from engine.core import RULES, Parameters  # noqa: E402
from tools.textlib import (  # noqa: E402
    attach_cross_refs, load_sections, parse_dollars, parse_percent, parse_period)

YEARS = range(2022, 2028)


def covers(period, day):
    start, end = period
    return (start is None or start <= day) and (end is None or day <= end)


def ground(sections, extractions, errors):
    """Steps 1 and 2. Attach located, checked spans to their provisions."""
    by_id = {p["id"]: p for s in sections for p in s["provisions"]}
    for provision in by_id.values():
        provision["derive"] = None
    for group in extractions["groups"]:
        provision = by_id.get(group["provision"])
        if provision is None or provision["text"] is None:
            errors.append("extraction targets unknown or empty provision %s" % group["provision"])
            continue
        provision["parameter"] = group["parameter"]
        provision["derive"] = group.get("derive")
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
                elif span["class"] == "threshold":
                    parsed = parse_dollars(span["text"])
                    record["normalized"] = str(parsed)
                    if parsed != int(span["normalized"]):
                        errors.append("threshold mismatch in %s: text parses to %s, extraction says %s"
                                      % (group["provision"], parsed, span["normalized"]))
            except ValueError as exc:
                errors.append("%s: %s" % (group["provision"], exc))
            provision["spans"].append(record)
        provision["spans"].sort(key=lambda s: s["start"])
    return by_id


def periods_for(provision, by_id):
    """Period spans that govern a provision: its own, or the nearest ancestor's.

    A list item often carries the number while the lead-in above it carries
    the dates. Returns (owning provision id, [(span index, span)]).
    """
    current = provision
    while current is not None:
        found = [(i, s) for i, s in enumerate(current["spans"]) if s["class"] == "period"]
        if found:
            return current["id"], found
        current = by_id.get(current["parent"]) if current["parent"] else None
    return None, []


def schedule_from(provision):
    """A bracket schedule from one provision's marked rates and thresholds.

    Used only where the extraction group says "derive": "schedule". It relies
    on the schedule being graduated: the rates, in ascending order, are paired
    with zero and then each distinct threshold, in ascending order. Returns
    None if the counts do not fit.
    """
    rates = sorted({Decimal(s["normalized"]) for s in provision["spans"] if s["class"] == "value"})
    floors = [0] + sorted({int(s["normalized"]) for s in provision["spans"] if s["class"] == "threshold"})
    if len(rates) != len(floors):
        return None
    return [{"over": str(floor), "rate": str(rate)} for floor, rate in zip(floors, rates)]


def statute_value(by_id, parameter_id, day):
    """Step 3. What the ingested text alone says for this parameter on this day."""
    hits = []
    for provision in by_id.values():
        if provision["parameter"] != parameter_id:
            continue
        if provision.get("superseded_from") and day >= provision["superseded_from"]:
            continue
        values = [i for i, s in enumerate(provision["spans"]) if s["class"] == "value"]
        if not values:
            continue
        if provision.get("derive") == "schedule":
            value = schedule_from(provision)
            if value is None:
                continue
        else:
            value = provision["spans"][values[0]]["normalized"]
        owner, periods = periods_for(provision, by_id)
        for index, span in periods:
            period = (span["normalized"]["from"], span["normalized"]["to"])
            if covers(period, day):
                hits.append({
                    "provision": provision["id"],
                    "label": provision["label"],
                    "value": value,
                    # -1 where the dates are marked in a parent provision.
                    "period_span": index if owner == provision["id"] else -1,
                    "period_provision": owner,
                    "value_span": values[0],
                })
    return hits


def canonical(value):
    """A comparable form: a plain rate and a one-bracket schedule are the same claim."""
    if isinstance(value, list):
        return tuple((Decimal(b["over"]), Decimal(b["rate"])) for b in value)
    return ((Decimal(0), Decimal(value)),)


def build_parameters(parameters, by_id, errors):
    out = []
    for pid, data in sorted(parameters.by_id.items()):
        if data["value_type"] == "tax_table":
            continue  # a method, not a value stated in statute text; not shown in the viewer
        # Step 4: every statute claim in the parameter file must be grounded.
        for entry in data["values"]:
            for source in entry["sources"]:
                if "ref" not in source:
                    continue
                hits = statute_value(by_id, pid, entry["effective_from"])
                match = [h for h in hits if h["provision"] == source["ref"]
                         and canonical(h["value"]) == canonical(source["states"])]
                if not match:
                    errors.append("%s from %s: statute claim %s = %s is not supported by any extraction"
                                  % (pid, entry["effective_from"], source["ref"], json.dumps(source["states"])))

        years = []
        for year in YEARS:
            day = "%d-01-01" % year
            hits = statute_value(by_id, pid, day)
            if len({canonical(h["value"]) for h in hits}) > 1:
                errors.append("%s %d: provisions disagree: %s" % (pid, year, [h["provision"] for h in hits]))
            entry = next((e for e in data["values"]
                          if e["effective_from"] <= day and (e.get("effective_to") is None or day <= e["effective_to"])), None)
            years.append({
                "year": year,
                "statute": hits[0] if hits else None,
                "used": entry["value"] if entry else None,
                "status": entry["status"] if entry else "not_recorded",
                "other_sources": [s for s in entry["sources"] if s["kind"] != "statute"] if entry else [],
                "snapshot_only": bool(entry) and entry["status"] in ("statute_snapshot", "statutory_default"),
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
    sections = attach_cross_refs(load_sections())
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
