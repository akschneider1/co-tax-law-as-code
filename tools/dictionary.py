"""The data dictionary: what may be marked, what each provision type needs,
and what every parameter must record. Standard library, Python 3.8+.

dictionary/dictionary.json is the single statement of the rules. This module
reads it for three users:
  tools/validate.py             enforces it on the reference marks and parameters
  tools/extract_langextract.py  builds the model's instructions from it
  demo/server.py                reports what a model run left out
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATH = ROOT / "dictionary" / "dictionary.json"

INHERIT_FROM_ABOVE = ("period", "who", "base", "exception")
INHERIT_FROM_BELOW = ("value", "threshold")


def load():
    return json.loads(PATH.read_text(encoding="utf-8"))


def active_classes(dictionary):
    """{class name: record} for the classes that are marked and sent to a model."""
    return {name: record for name, record in dictionary["classes"].items() if record["status"] == "active"}


def legend(dictionary):
    """{class name: short label}, for the viewer's legend."""
    return {name: record["label"] for name, record in active_classes(dictionary).items()}


def _meets(requirement, spans):
    """True if any span satisfies 'class' or 'class:kind'."""
    cls, _, kind = requirement.partition(":")
    for span in spans:
        if span["class"] == cls and (not kind or (span.get("attrs") or {}).get("kind") == kind):
            return True
    return False


def missing_requirements(dictionary, provision_id, marks, parents, check_kinds=True):
    """Requirements of a provision's type that its marks do not meet.

    marks: {provision id: list of spans}. parents: {provision id: parent id or None}.
    A requirement can be met by the provision itself; by a provision above it,
    for the classes a lead-in may carry; or by a provision below it, for the
    classes a list item may carry. With check_kinds False only the class is
    required, which suits model output that carries no 'kind'.
    """
    type_name = dictionary["provision_assignments"].get(provision_id)
    if type_name is None:
        return ["no provision type is assigned"]
    above, current = [], parents.get(provision_id)
    while current:
        above.extend(marks.get(current, []))
        current = parents.get(current)
    below = [span for pid, spans in marks.items() if pid.startswith(provision_id + "/") for span in spans]
    missing = []
    for requirement in dictionary["provision_types"][type_name]["requires"]:
        wanted = requirement if check_kinds else requirement.partition(":")[0]
        cls = wanted.partition(":")[0]
        pool = list(marks.get(provision_id, []))
        if cls in INHERIT_FROM_ABOVE:
            pool += above
        if cls in INHERIT_FROM_BELOW:
            pool += below
        if not _meets(wanted, pool):
            missing.append(wanted)
    return missing


def check_marks(dictionary, groups, parents, provision_ids, errors):
    """Check a set of reference marks against the dictionary. Returns a summary."""
    classes = dictionary["classes"]
    types = dictionary["provision_types"]
    for pid, type_name in sorted(dictionary["provision_assignments"].items()):
        if type_name not in types:
            errors.append("dictionary: %s is assigned unknown type %r" % (pid, type_name))
        if pid not in provision_ids:
            errors.append("dictionary: a type is assigned to %s, which is not an ingested provision" % pid)
    for pid in sorted(provision_ids):
        if pid not in dictionary["provision_assignments"]:
            errors.append("dictionary: provision %s has text but no assigned type" % pid)
    for name, record in types.items():
        for requirement in record["requires"] + record["optional"]:
            cls, _, kind = requirement.partition(":")
            if cls not in classes:
                errors.append("dictionary: type %s names unknown class %r" % (name, cls))
            elif kind and kind not in classes[cls]["attributes"].get("kind", []):
                errors.append("dictionary: type %s names unknown kind %r for %s" % (name, kind, cls))

    marks = {}
    for group in groups:
        marks[group["provision"]] = group["spans"]
        for span in group["spans"]:
            record = classes.get(span["class"])
            if record is None:
                errors.append("%s: span class %r is not in the dictionary" % (group["provision"], span["class"]))
                continue
            if record["status"] != "active":
                errors.append("%s: span class %r is defined but not active" % (group["provision"], span["class"]))
            for key, value in (span.get("attrs") or {}).items():
                allowed = record["attributes"].get(key)
                if allowed is None:
                    errors.append("%s: %s has no attribute %r" % (group["provision"], span["class"], key))
                elif value not in allowed:
                    errors.append("%s: %s.%s is %r, not one of %s"
                                  % (group["provision"], span["class"], key, value, ", ".join(allowed)))
    for pid in sorted(marks):
        for requirement in missing_requirements(dictionary, pid, marks, parents):
            errors.append("%s: its type, %s, requires %s, which is not marked"
                          % (pid, dictionary["provision_assignments"].get(pid), requirement))
    return {"marked": len(marks), "unmarked": len(provision_ids) - len(marks)}


def check_parameter(dictionary, data, errors):
    """Check one parameter file's descriptive fields against the dictionary."""
    record = dictionary["parameter_record"]
    pid = data.get("id", "?")
    for field in record["required_fields"]:
        if field not in data:
            errors.append("%s: missing the field %r" % (pid, field))
    if data.get("unit") not in record["unit"]:
        errors.append("%s: unit is %r, not one of %s" % (pid, data.get("unit"), ", ".join(record["unit"])))
    if data.get("shape") not in record["shape"]:
        errors.append("%s: shape is %r, not one of %s" % (pid, data.get("shape"), ", ".join(record["shape"])))
    resolutions = data.get("resolution") or []
    if not resolutions:
        errors.append("%s: no resolution is recorded" % pid)
    for resolution in resolutions:
        if resolution not in record["resolution"]:
            errors.append("%s: resolution %r is not in the dictionary" % (pid, resolution))
    if not isinstance(data.get("keys"), list):
        errors.append("%s: keys must be a list" % pid)


def prompt(dictionary):
    """The instructions sent to a model, built from the active classes and the boundary rules."""
    asks = {
        "period": 'Attributes: "from" and "to" as ISO dates, inclusive, or "" when open-ended.',
        "value": 'Attribute: "decimal", the number as a fraction, so "twenty percent" is "0.20".',
        "threshold": 'Attribute: "dollars", the amount in digits.',
        "lifecycle": 'Attribute: "date", the ISO date the text is repealed or takes effect.',
    }
    lines = ["You are marking up one provision of a tax statute. Extract spans in order of appearance.",
             "Use only these classes:"]
    for name, record in active_classes(dictionary).items():
        lines.append("  %s: %s%s" % (name, record["definition"], " " + asks[name] if name in asks else ""))
    lines.append("Rules:")
    for rule in dictionary["boundary_rules"]:
        lines.append("  - " + rule)
    lines += [
        "  - If the provision sets no number, extract no value span.",
        "  - Never skip a provision because it covers past tax years or is repealed by a later provision.",
        "The context before the examples is there to help you read the provision.",
        "Extract spans from the provision only, never from the context.",
    ]
    return "\n".join(lines)
