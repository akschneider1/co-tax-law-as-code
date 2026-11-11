"""Small rules engine: dated parameters, cited rules, and a calculation trace.

Standard library only (Python 3.8+). Money is Decimal throughout.
"""
import datetime
import json
import pathlib
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARAMETER_DIR = ROOT / "parameters"

# Statuses a parameter value can carry, strongest first.
STATUSES = (
    "agency_published",             # stated by the administering agency
    "statute_snapshot",             # read from ingested statute text only
    "statutory_default",            # statute value that a later act or trigger may displace
    "reported_passed_uncertified",  # from news reports of an uncertified election
)


class EngineError(Exception):
    code = "engine_error"


class ParameterUnavailable(EngineError):
    code = "parameter_unavailable"


class OutOfScope(EngineError):
    code = "out_of_scope"


class InvalidFacts(EngineError):
    code = "invalid_facts"


def money(value):
    """Round to whole dollars, half up. Assumption: mirrors whole-dollar return entries."""
    return Decimal(value).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def to_decimal(value, name):
    try:
        result = Decimal(str(value))
    except Exception:
        raise InvalidFacts("%s must be a number, got %r" % (name, value))
    if result < 0:
        raise InvalidFacts("%s must not be negative" % name)
    return result


class Parameters:
    """Loads every parameters/*.json file and resolves values by date."""

    def __init__(self, directory=PARAMETER_DIR):
        self.by_id = {}
        for path in sorted(pathlib.Path(directory).glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            self.by_id[data["id"]] = data

    def entry(self, param_id, on_date):
        if param_id not in self.by_id:
            raise ParameterUnavailable("no parameter named %s" % param_id)
        for entry in self.by_id[param_id]["values"]:
            start = datetime.date.fromisoformat(entry["effective_from"])
            end = entry.get("effective_to")
            end = datetime.date.fromisoformat(end) if end else datetime.date.max
            if start <= on_date <= end:
                return entry
        raise ParameterUnavailable(
            "%s has no recorded value on %s" % (param_id, on_date.isoformat())
        )


# Registry of rules, filled by the @rule decorator. validate.py reads it.
RULES = {}


def rule(rule_id, cites, params=()):
    """Register a rule with the statute provisions and parameters it relies on."""

    def decorate(func):
        func.rule_id = rule_id
        func.cites = tuple(cites)
        func.params = tuple(params)
        RULES[rule_id] = func
        return func

    return decorate


class Context:
    """One calculation: facts in, results plus a trace and warnings out."""

    def __init__(self, facts, parameters):
        self.facts = facts
        self.parameters = parameters
        self.trace = []
        self.warnings = []

    def param(self, param_id, on_date):
        entry = self.parameters.entry(param_id, on_date)
        if entry["status"] != "agency_published":
            self.warn("%s: status is %s" % (param_id, entry["status"]))
        if not any(s["kind"] == "statute" for s in entry.get("sources", [])):
            self.warn("%s: no ingested statute text supports this value; the cited provisions do not state it" % param_id)
        for key in ("caveat", "conflict_note"):
            if entry.get(key):
                self.warn("%s: %s" % (param_id, entry[key]))
        return entry

    def warn(self, message):
        if message not in self.warnings:
            self.warnings.append(message)

    def record(self, func, value, detail):
        self.trace.append(
            {
                "rule": func.rule_id,
                "value": str(value),
                "detail": detail,
                "cites": list(func.cites),
                "parameters": list(func.params),
            }
        )
        return value
