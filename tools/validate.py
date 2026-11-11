"""Check that the three layers agree with each other.

  text        every provision id is unique; content hashes match text/manifest.json
  parameters  date ranges are ordered and do not overlap; statute refs resolve;
              a value that any source contradicts must carry a conflict_note
  sources     every stored copy in sources/ matches its recorded hash; every
              quote that names a stored copy appears in it word for word; an
              agency_published value has at least one agency quote checked so
  rules       every cited provision id and parameter id exists

Run with --stamp to (re)write text/manifest.json after an intended text change.
Run with --strict to also fail on any value that rests on the statute snapshot
alone, which is known to be out of date.
Exit code 1 on any error. Acknowledged conflicts are listed but are not errors.
"""
import datetime
import hashlib
import json
import pathlib
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import engine.co_rules  # noqa: E402,F401  (registers the rules)
from engine.core import RULES, STATUSES, Parameters  # noqa: E402
from tools.snapshot_source import load_manifest, normalise, snapshot_text  # noqa: E402

TEXT_DIR = ROOT / "text"
MANIFEST = TEXT_DIR / "manifest.json"


def content_hash(text):
    normalised = " ".join(text.split())
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()


def load_text(errors):
    """Return {provision id: sha256 of its content, or None if it has none}."""
    index = {}
    for path in sorted(TEXT_DIR.glob("*.xml")):
        root = ET.parse(str(path)).getroot()
        for element in [root] + list(root.iter("provision")):
            pid = element.get("id")
            if not pid:
                errors.append("%s: element without id" % path.name)
                continue
            if pid in index:
                errors.append("%s: duplicate id %s" % (path.name, pid))
            content = element.find("content")
            index[pid] = content_hash(content.text) if content is not None else None
    return index


def check_manifest(index, errors, stamp):
    hashes = {pid: h for pid, h in index.items() if h}
    if stamp:
        MANIFEST.write_text(json.dumps(hashes, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("stamped %d content hashes into %s" % (len(hashes), MANIFEST.name))
        return
    if not MANIFEST.exists():
        errors.append("text/manifest.json missing; run with --stamp")
        return
    recorded = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for pid in sorted(set(hashes) | set(recorded)):
        if hashes.get(pid) != recorded.get(pid):
            errors.append("text changed or unrecorded since last stamp: %s" % pid)


def check_parameters(parameters, index, errors):
    conflicts = []
    for pid, data in sorted(parameters.by_id.items()):
        previous_end = None
        for entry in data["values"]:
            label = "%s from %s" % (pid, entry["effective_from"])
            start = datetime.date.fromisoformat(entry["effective_from"])
            end = entry.get("effective_to")
            end = datetime.date.fromisoformat(end) if end else datetime.date.max
            if end < start:
                errors.append("%s: ends before it starts" % label)
            if previous_end is not None and start <= previous_end:
                errors.append("%s: overlaps or precedes the previous entry" % label)
            previous_end = end

            if entry.get("status") not in STATUSES:
                errors.append("%s: unknown status %r" % (label, entry.get("status")))
            if not entry.get("sources"):
                errors.append("%s: no source" % label)

            disagreeing = []
            for source in entry.get("sources", []):
                if "ref" in source and source["ref"] not in index:
                    errors.append("%s: text ref does not resolve: %s" % (label, source["ref"]))
                if "states" in source and source["states"] != entry["value"]:
                    disagreeing.append(source)
            if disagreeing:
                if not entry.get("conflict_note"):
                    errors.append("%s: a source contradicts the value and no conflict_note explains it" % label)
                for source in disagreeing:
                    conflicts.append((label, entry["value"], source))
    return conflicts


def check_sources(parameters, errors):
    """Check stored copies and the quotes that rest on them.

    Returns (rows, snapshot_only). Each row is one non-statute source with a
    computed status: 'verified' (its quote is in the stored copy) or
    'unverified' (no stored copy, so nothing was checked).
    """
    manifest = load_manifest()
    texts = {}
    for source_id, record in sorted(manifest.items()):
        path = ROOT / "sources" / (source_id + ".txt")
        if not path.exists():
            errors.append("sources/%s.txt is missing" % source_id)
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != record["text_sha256"]:
            errors.append("sources/%s.txt does not match the hash in sources/manifest.json" % source_id)
        texts[source_id] = snapshot_text(source_id)

    rows, snapshot_only = [], []
    for pid, data in sorted(parameters.by_id.items()):
        for entry in data["values"]:
            label = "%s from %s" % (pid, entry["effective_from"])
            agency_verified = False
            for source in entry.get("sources", []):
                if source["kind"] == "statute":
                    continue
                status = "unverified"
                snapshot = source.get("snapshot")
                if snapshot:
                    if snapshot not in texts:
                        errors.append("%s: source names unknown stored copy %r" % (label, snapshot))
                    elif not source.get("quote"):
                        errors.append("%s: source names stored copy %s but records no quote" % (label, snapshot))
                    elif normalise(source["quote"]) not in texts[snapshot]:
                        errors.append("%s: quote not found in sources/%s.txt: %r" % (label, snapshot, source["quote"]))
                    else:
                        status = "verified"
                        agency_verified = agency_verified or source["kind"] == "agency"
                rows.append((label, source["kind"], status, snapshot or source.get("url", "")))
            if entry.get("status") == "agency_published" and not agency_verified:
                errors.append("%s: status is agency_published but no agency quote is checked against a stored copy" % label)
            if entry.get("status") in ("statute_snapshot", "statutory_default"):
                snapshot_only.append(label)
    return rows, snapshot_only


def check_rules(parameters, index, errors):
    for rule_id, func in sorted(RULES.items()):
        for cite in func.cites:
            if cite not in index:
                errors.append("rule %s cites unknown provision %s" % (rule_id, cite))
        for param in func.params:
            if param not in parameters.by_id:
                errors.append("rule %s uses unknown parameter %s" % (rule_id, param))


def main():
    errors = []
    index = load_text(errors)
    check_manifest(index, errors, stamp="--stamp" in sys.argv)
    parameters = Parameters()
    conflicts = check_parameters(parameters, index, errors)
    source_rows, snapshot_only = check_sources(parameters, errors)
    check_rules(parameters, index, errors)

    print("text:       %d provisions, %d with content" % (len(index), sum(1 for h in index.values() if h)))
    print("parameters: %d files, %d dated values" % (
        len(parameters.by_id), sum(len(d["values"]) for d in parameters.by_id.values())))
    print("rules:      %d" % len(RULES))

    if conflicts:
        print("\nAcknowledged conflicts between a source and the value used (%d):" % len(conflicts))
        for label, value, source in conflicts:
            where = source.get("ref") or source.get("url")
            print("  %s\n      used %s; %s source %s states %s" % (
                label, json.dumps(value), source["kind"], where, json.dumps(source["states"])))

    verified = sum(1 for row in source_rows if row[2] == "verified")
    print("\nSources other than statute text: %d, of which %d have a quote checked against a stored copy"
          % (len(source_rows), verified))
    for label, kind, status, where in source_rows:
        if status != "verified":
            print("  unverified: %s, %s source %s" % (label, kind, where))

    if snapshot_only:
        print("\nValues resting on the statute snapshot alone, which is known to be out of date (%d):"
              % len(snapshot_only))
        for label in snapshot_only:
            print("  " + label)
        if "--strict" in sys.argv:
            errors.append("--strict: %d value(s) rest on the statute snapshot alone" % len(snapshot_only))

    if errors:
        print("\nERRORS (%d):" % len(errors))
        for error in errors:
            print("  " + error)
        return 1
    print("\nOK: layers are consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
