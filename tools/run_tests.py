"""Run tests/cases.json and the official tax table rows against the engine.

Exit code 1 if any case or table row fails.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.co_rules import calculate  # noqa: E402
from engine.core import EngineError, Parameters  # noqa: E402
from tools import make_table_tests  # noqa: E402


def main():
    corpus = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))
    parameters = Parameters()
    failures = 0
    for case in corpus["cases"]:
        try:
            got = calculate(case["facts"], parameters)["outputs"]
            error = None
        except EngineError as exc:
            got, error = None, exc.code

        if "expect_error" in case:
            ok = error == case["expect_error"]
            shown = "error %s" % error if error else "outputs %s" % got
            wanted = "error %s" % case["expect_error"]
        else:
            # Only the outputs a case names are compared.
            ok = error is None and all(got.get(k) == v for k, v in case["expect"].items())
            shown = "error %s" % error if error else got
            wanted = case["expect"]

        print("%s  %s" % ("PASS" if ok else "FAIL", case["id"]))
        if not ok:
            failures += 1
            print("      expected: %s" % (wanted,))
            print("      got:      %s" % (shown,))

    total = len(corpus["cases"])
    print("\n%d of %d cases passed" % (total - failures, total))

    table_failures = run_tax_tables(parameters)
    return 1 if failures or table_failures else 0


def run_tax_tables(parameters):
    """Check the form-table amount against every row of the printed tax tables.

    Each row is tried at both ends of its band: one dollar over the lower
    figure, and at the upper figure. Only failures are listed.
    """
    path = ROOT / "tests" / "tax_tables.json"
    if not path.exists():
        print("tests/tax_tables.json is missing; run tools/make_table_tests.py")
        return 1
    if make_table_tests.dump(make_table_tests.build()) != path.read_text(encoding="utf-8"):
        print("tests/tax_tables.json does not match the stored sources; run tools/make_table_tests.py")
        return 1
    failures = 0
    print("\nOfficial tax table rows (Department of Revenue 104 Books):")
    for table in json.loads(path.read_text(encoding="utf-8"))["tables"]:
        checked = bad = 0
        for low, high, tax in table["rows"]:
            for income in (low + 1, high):
                facts = {"tax_year": table["tax_year"], "colorado_taxable_income": income}
                got = calculate(facts, parameters)["outputs"]["income_tax_form_table"]
                checked += 1
                if got != str(tax):
                    bad += 1
                    print("  FAIL %d income %d: table says %d, engine says %s" % (table["tax_year"], income, tax, got))
        failures += bad
        print("  %d: %d of %d checks passed (%d of %d rows read from the table)"
              % (table["tax_year"], checked - bad, checked, table["rows_read"], table["rows_in_table"]))
    return failures


if __name__ == "__main__":
    sys.exit(main())
