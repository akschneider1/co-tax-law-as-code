"""Shared helpers for the statute text layer. Standard library, Python 3.8+.

  load_sections        the provisions of every text/*.xml file, in document order
  find_cross_refs      every cross-reference in a provision, resolved against
                       what has actually been ingested
  context_for          the surrounding material a reader (or a model) needs to
                       understand one provision: heading, lead-ins, definitions,
                       references and following provisos
  parse_period / parse_percent / parse_dollars   deterministic readers for date
                       phrases and number words, used to re-check model and
                       hand extractions. Case does not matter: ballot measures
                       print new text in capitals.
"""
import datetime
import hashlib
import pathlib
import re
import xml.etree.ElementTree as ET
from decimal import Decimal

ROOT = pathlib.Path(__file__).resolve().parent.parent

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
DATE = r"([A-Za-z]+) (\d{1,2}), (\d{4})"


def content_hash(text):
    return hashlib.sha256(" ".join(text.split()).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- parsers

SCALES = {"thousand": 1000, "million": 1000000}


def words_to_int(words):
    """'twenty-five' -> 25; 'seven hundred fifty thousand' -> 750000."""
    total = current = 0
    for token in words.lower().replace("-", " ").split():
        if token in UNITS:
            current += UNITS[token]
        elif token in TENS:
            current += TENS[token]
        elif token == "hundred":
            current = (current or 1) * 100
        elif token in SCALES:
            total += (current or 1) * SCALES[token]
            current = 0
        else:
            raise ValueError("unknown number word %r" % token)
    return total + current


def parse_percent(text):
    """'twenty-five percent' -> 0.25; 'four and forty one-hundredths percent' -> 0.044."""
    match = re.fullmatch(r"(.+?)(?: and (.+?) one-hundredths)? percent", text.lower())
    if not match:
        raise ValueError("not a percentage phrase: %r" % text)
    whole = Decimal(words_to_int(match.group(1)))
    hundredths = Decimal(words_to_int(match.group(2))) if match.group(2) else Decimal(0)
    return (whole + hundredths / 100) / 100


def parse_dollars(text):
    """'twenty five thousand dollars' -> 25000."""
    match = re.fullmatch(r"(.+) dollars", text.lower())
    if not match:
        raise ValueError("not a dollar amount in words: %r" % text)
    return words_to_int(match.group(1))


def _date(groups):
    month, day, year = groups
    if month.capitalize() not in MONTHS:
        raise ValueError("unknown month %r" % month)
    return datetime.date(int(year), MONTHS[month.capitalize()], int(day))


def parse_period(text):
    """Return (from, to) as ISO strings or None, from the statute's date phrasing."""
    start = end = None
    after = re.search(r"on or after " + DATE, text, re.IGNORECASE)
    before = re.search(r"(?:before|prior to) " + DATE, text, re.IGNORECASE)
    single = re.search(r"commencing on " + DATE, text, re.IGNORECASE)
    if after:
        start = _date(after.groups())
    if before:
        end = _date(before.groups()) - datetime.timedelta(days=1)
    if single and not after and not before:
        start = _date(single.groups())
        end = datetime.date(start.year, 12, 31)
    if start is None and end is None:
        raise ValueError("no date phrase recognised in %r" % text)
    return (start.isoformat() if start else None, end.isoformat() if end else None)


# ---------------------------------------------------------------- loading

def load_sections():
    """Every section, with its provisions flattened in document order."""
    sections = []
    for path in sorted((ROOT / "text").glob("*.xml")):
        root = ET.parse(str(path)).getroot()
        meta = root.find("meta")
        provisions = []

        def walk(element, label, depth, parent_id):
            for child in element.findall("provision"):
                child_label = label + child.get("num")
                content = child.find("content")
                text = " ".join(content.text.split()) if content is not None else None
                provisions.append({
                    "id": child.get("id"),
                    "label": child_label,
                    "depth": depth,
                    "parent": parent_id,
                    "status": child.get("status"),
                    # Set where a later instrument ends this provision's effect.
                    "superseded_from": child.get("superseded-from"),
                    "superseded_by": child.get("superseded-by"),
                    "superseded_basis": child.get("superseded-basis"),
                    "text": text,
                    "words": len(text.split()) if text else 0,
                    "sha256": content_hash(text) if text else None,
                    "spans": [],
                    "parameter": None,
                })
                walk(child, child_label, depth + 1, child.get("id"))

        walk(root, "", 0, None)
        sections.append({
            "id": root.get("id"),
            # The enacted section a measure's proposed text would change, if any.
            "amends": root.get("amends"),
            "citation": meta.findtext("citation"),
            "heading": meta.findtext("heading"),
            "source": dict(meta.find("source").attrib),
            "authority": meta.findtext("authority"),
            "note": meta.findtext("note"),
            "provisions": provisions,
        })
    return sections


def index(sections):
    return {p["id"]: p for s in sections for p in s["provisions"]}


# ---------------------------------------------------------------- cross-references

_PARENS = r"((?: ?\([0-9A-Za-z.]+\))*)"
_CRS = re.compile(r"sections? (\d+-\d+(?:\.\d+)?-\d+(?:\.\d+)?)" + _PARENS, re.IGNORECASE)
_IRC = re.compile(r"section (\d+[A-Za-z]?)" + _PARENS + r" of the internal revenue code", re.IGNORECASE)
_GROUP = r"(?:\([0-9A-Za-z.]+\))+"
_INTERNAL = re.compile(r"subsections? (" + _GROUP + r"(?:(?:, and |, or |, | and | or )" + _GROUP + r")*) of this section",
                       re.IGNORECASE)


def _path(parens):
    return "/".join(re.findall(r"\(([0-9A-Za-z.]+)\)", parens))


def find_cross_refs(section_id, text, known_ids, amends=None):
    """Locate cross-references in one provision and say whether each target is ingested.

    status: 'ingested'      the target provision's text is in text/
            'not_ingested'  a Colorado provision this project has not read
            'external'      federal law, outside the project's scope
    """
    known_sections = {"/".join(i.split("/")[:5]) for i in known_ids}
    refs = []

    def add(start, end, target, kind):
        if kind == "irc":
            status = "external"
        elif target in known_ids:
            status = "ingested"
        else:
            status = "not_ingested"
        refs.append({"start": start, "end": end, "text": text[start:end], "target": target,
                     "kind": kind, "status": status,
                     "section_ingested": "/".join(target.split("/")[:5]) in known_sections})

    for match in _IRC.finditer(text):
        target = "/us/usc/t26/s" + match.group(1) + ("/" + _path(match.group(2)) if match.group(2) else "")
        add(match.start(), match.end(), target, "irc")
    for match in _CRS.finditer(text):
        target = "/us/co/crs/" + match.group(1) + ("/" + _path(match.group(2)) if match.group(2) else "")
        add(match.start(), match.start() + len(match.group(0).rstrip()), target, "crs")
    for match in _INTERNAL.finditer(text):
        for group in re.finditer(_GROUP, match.group(1)):
            target = section_id + "/" + _path(group.group(0))
            if target not in known_ids and amends and amends + "/" + _path(group.group(0)) in known_ids:
                # A measure's "this section" is the enacted section it amends.
                target = amends + "/" + _path(group.group(0))
            add(match.start(1) + group.start(), match.start(1) + group.end(), target, "internal")
    refs.sort(key=lambda r: r["start"])
    return refs


def attach_cross_refs(sections):
    """Add a 'refs' list to every provision that has text."""
    known = set(index(sections))
    for section in sections:
        for provision in section["provisions"]:
            provision["refs"] = (find_cross_refs(section["id"], provision["text"], known, section.get("amends"))
                                 if provision["text"] else [])
    return sections


# ---------------------------------------------------------------- context

_DEFINITION = re.compile(r"[\"\u201c]([^\"\u201d]{2,60})[\"\u201d],? (?:means|has the same meaning|includes)")
_PROVISO = re.compile(r"\bthis (?:sub)?section\b|\bprovided, that\b|\bnotwithstanding\b", re.IGNORECASE)


def find_definitions(sections):
    """Terms defined in the ingested text: [(term, defining provision id, text)].

    Only quoted terms followed by 'means', 'includes' or 'has the same meaning'
    are found. A definition's scope ('as used in this section') is not parsed;
    context_for limits each definition to the section that contains it.
    """
    found = []
    for section in sections:
        for provision in section["provisions"]:
            for match in _DEFINITION.finditer(provision["text"] or ""):
                found.append((match.group(1), provision["id"], provision["text"]))
    return found


def context_for(provision_id, sections):
    """Plain-text context for one provision, so it can be read on its own.

    Follows the four kinds of context STARA attaches to each unit (Surani et
    al., ICAIL 2025, section 3.1), which its ablation found to be the largest
    single gain in extraction accuracy:
      1. a heading: citation and position
      2. lead-ins: the text of parent provisions that this one completes
      3. definitions of quoted terms used in the provision, if the same
         section defines them
      4. provisos: later sibling provisions that modify this one, such as a
         repeal clause
    Cross-referenced text is added too, or a warning where it was not read.
    """
    by_id = index(sections)
    section = next(s for s in sections if provision_id.startswith(s["id"] + "/"))
    provision = by_id[provision_id]
    lines = ["Section: %s. %s" % (section["citation"], section["heading"]),
             "Provision: %s%s" % (section["citation"], provision["label"])]

    parents, parent = [], provision["parent"]
    while parent:
        if by_id[parent]["text"]:
            parents.append("%s %s" % (by_id[parent]["label"], by_id[parent]["text"]))
        parent = by_id[parent]["parent"]
    for line in reversed(parents):
        lines.append("Lead-in from parent provision: " + line)

    text = provision["text"] or ""
    for term, where, definition in find_definitions([section]):
        if where != provision_id and term.lower() in text.lower():
            lines.append("Definition of \"%s\" (%s): %s" % (term, by_id[where]["label"], definition))

    siblings = [p for p in section["provisions"] if p["parent"] == provision["parent"]]
    position = siblings.index(provision)
    for later in siblings[position + 1:]:
        if later["text"] and later["words"] <= 60 and _PROVISO.search(later["text"]):
            lines.append("Following provision %s: %s" % (later["label"], later["text"]))

    if provision.get("superseded_from"):
        lines.append("Note: this provision's effect ends before %s (%s)."
                     % (provision["superseded_from"], provision.get("superseded_basis") or "basis not recorded"))

    for ref in provision.get("refs", []):
        if ref["status"] == "ingested" and by_id[ref["target"]]["text"]:
            lines.append("Referenced %s: %s" % (ref["text"], by_id[ref["target"]]["text"]))
        elif ref["status"] == "not_ingested":
            lines.append("Referenced %s: text not available. Do not guess what it says." % ref["text"])
    return "\n".join(lines)
