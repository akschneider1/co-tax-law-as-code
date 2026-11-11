"""Command line: compute the slice for one filer and show the trace.

Example:
    python3 calc.py --year 2025 --taxable-income 20000 --federal-eitc 4000
"""
import argparse
import json
import sys

from engine.co_rules import calculate
from engine.core import EngineError


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--year", type=int, required=True, help="income tax year, e.g. 2025")
    parser.add_argument("--taxable-income", required=True, help="Colorado taxable income, dollars")
    parser.add_argument("--federal-eitc", default="0", help="federal earned income credit, dollars")
    parser.add_argument("--residency", default="full_year", choices=["full_year", "part_year", "nonresident"])
    parser.add_argument("--json", action="store_true", help="print the full result as JSON")
    args = parser.parse_args()

    facts = {
        "tax_year": args.year,
        "residency": args.residency,
        "colorado_taxable_income": args.taxable_income,
        "federal_eitc": args.federal_eitc,
    }
    try:
        result = calculate(facts)
    except EngineError as exc:
        print("Cannot compute (%s): %s" % (exc.code, exc))
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    out = result["outputs"]
    print("Income tax before credits: $%s" % out["income_tax_before_credits"])
    print("Colorado EITC:             $%s" % out["co_eitc"])
    print("Net tax after EITC:        $%s  (negative = refund)" % out["net_tax_after_eitc"])
    print("\nHow each number was reached:")
    for step in result["trace"]:
        print("  %s = %s   [%s]" % (step["rule"], step["value"], step["detail"]))
        for cite in step["cites"]:
            print("      cites %s" % cite)
    if result["warnings"]:
        print("\nWarnings:")
        for warning in result["warnings"]:
            print("  - " + warning)
    print("\nUnofficial prototype. Not tax advice and not a statement of Colorado law.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
