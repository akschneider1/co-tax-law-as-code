"""Turn the Department of Revenue's printed tax tables into official test rows.

Reads the stored copies of the 104 Books in sources/ and writes
tests/tax_tables.json: for each tax year, every table row that could be read,
as [over, not_over, tax]. tools/run_tests.py checks the engine's form-table
amount against each row at both ends of its band.

A row is read only if its three figures sit on one line of the converted text
and its band is one the table is known to use. Rows the conversion split
across lines are counted as unread, not guessed.

  python3 tools/make_table_tests.py          write tests/tax_tables.json
  python3 tools/make_table_tests.py --check  fail if the file differs from the sources
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "tests" / "tax_tables.json"
YEARS = (2022, 2023, 2024, 2025)
FIRST_BANDS = {(0, 10), (10, 30), (30, 50), (50, 75), (75, 100)}
TOP = 50000
ROW = re.compile(r"\$([\d,]+)[ \t]+\$([\d,]+)[ \t]+\$([\d,]+)(?![\d,])")


def read_rows(year):
    """Rows of one year's table, from the stored copy of that year's 104 Book."""
    text = (ROOT / "sources" / ("dor-104-book-%d.txt" % year)).read_text(encoding="utf-8")
    start = text.index("%d Colorado Income Tax Table with tax rate" % year)
    rows = {}
    for match in ROW.finditer(text[start:]):
        low, high, tax = (int(g.replace(",", "")) for g in match.groups())
        if (low, high) in FIRST_BANDS or (low % 100 == 0 and high == low + 100 and 100 <= low < TOP):
            if rows.get((low, high), tax) != tax:
                raise SystemExit("%d: band %d to %d is printed with two different taxes" % (year, low, high))
            rows[(low, high)] = tax
    return [[low, high, tax] for (low, high), tax in sorted(rows.items())]


def build():
    expected = len(FIRST_BANDS) + (TOP - 100) // 100
    tables = []
    for year in YEARS:
        rows = read_rows(year)
        tables.append({
            "tax_year": year,
            "source": "dor-104-book-%d" % year,
            "rows_in_table": expected,
            "rows_read": len(rows),
            "rows": rows,
        })
    return {
        "about": "Official test rows: the Department of Revenue's printed Colorado Income Tax Table for each year, "
                 "read from the stored copy of that year's 104 Book by tools/make_table_tests.py. Each row is "
                 "[taxable income over, but not over, tax]. Do not edit by hand.",
        "basis": "official",
        "tables": tables,
    }


def dump(data):
    # One table row per line keeps the file readable and diffs small.
    text = json.dumps(data, indent=1)
    text = re.sub(r"\[\s+(\d+),\s+(\d+),\s+(\d+)\s+\]", r"[\1, \2, \3]", text)
    return text + "\n"


def main():
    text = dump(build())
    if "--check" in sys.argv:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != text:
            print("tests/tax_tables.json does not match the stored sources; run tools/make_table_tests.py")
            return 1
        print("tests/tax_tables.json matches the stored sources")
        return 0
    OUTPUT.write_text(text, encoding="utf-8")
    for table in json.loads(text)["tables"]:
        print("%d: %d of %d rows read" % (table["tax_year"], table["rows_read"], table["rows_in_table"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
