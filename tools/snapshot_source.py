"""Keep a text copy of an agency page or document that a parameter quotes.

  python3 tools/snapshot_source.py ID URL [--file PATH] [--title T] [--publisher P]

Fetches URL (or reads PATH, a copy already downloaded from URL), converts it
to plain text, and writes sources/ID.txt plus an entry in sources/manifest.json
with the url, retrieval date and hashes of both the original and the text.

tools/validate.py then checks every quote in parameters/*.json that names a
snapshot against the stored text. A snapshot records what a page said on one
day. It does not notice later changes; re-run this to refresh it.

HTML is converted with the standard library. PDF needs the `pdftotext`
program (poppler); this is the only step in the project that does.
"""
import argparse
import datetime
import hashlib
import html
import json
import pathlib
import re
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
MANIFEST = SOURCES / "manifest.json"


def html_to_text(raw):
    text = re.sub(r"(?is)<(script|style|svg|noscript).*?</\1>", "", raw)
    text = re.sub(r"(?i)<(br|/p|/div|/li|/tr|/h\d|/td|/th)[^>]*>", "\n", text)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    lines = [" ".join(line.split()) for line in text.splitlines()]
    return "\n".join(line for line in lines if line) + "\n"


def pdf_to_text(path):
    try:
        done = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        raise SystemExit("pdftotext is not installed; it is needed to convert a PDF")
    return done.stdout.decode("utf-8", errors="replace")


def normalise(text):
    """Collapse whitespace, so a quote matches across line breaks and table cells."""
    return " ".join(text.split())


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}


def snapshot_text(source_id):
    """Normalised text of one stored snapshot, or None if it is not stored."""
    path = SOURCES / (source_id + ".txt")
    return normalise(path.read_text(encoding="utf-8")) if path.exists() else None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("id")
    parser.add_argument("url")
    parser.add_argument("--file", help="a copy already downloaded from the url")
    parser.add_argument("--title", default="")
    parser.add_argument("--publisher", default="")
    parser.add_argument("--retrieved", default=datetime.date.today().isoformat())
    args = parser.parse_args()

    if args.file:
        raw = pathlib.Path(args.file).read_bytes()
    else:
        with urllib.request.urlopen(args.url, timeout=120) as response:
            raw = response.read()

    is_pdf = raw[:5] == b"%PDF-"
    if is_pdf:
        scratch = SOURCES / (args.id + ".pdf.tmp")
        SOURCES.mkdir(exist_ok=True)
        scratch.write_bytes(raw)
        try:
            text = pdf_to_text(scratch)
        finally:
            scratch.unlink()
    else:
        text = html_to_text(raw.decode("utf-8", errors="replace"))

    SOURCES.mkdir(exist_ok=True)
    (SOURCES / (args.id + ".txt")).write_text(text, encoding="utf-8")
    manifest = load_manifest()
    manifest[args.id] = {
        "url": args.url,
        "title": args.title,
        "publisher": args.publisher,
        "retrieved": args.retrieved,
        "original_type": "pdf" if is_pdf else "html",
        "original_sha256": hashlib.sha256(raw).hexdigest(),
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "converted_with": "pdftotext -layout" if is_pdf else "tools/snapshot_source.py html_to_text",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("stored sources/%s.txt (%d characters)" % (args.id, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
