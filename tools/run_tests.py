"""Run tests/cases.json against the engine. Exit code 1 if any case fails."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.co_rules import calculate  # noqa: E402
from engine.core import EngineError, Parameters  # noqa: E402


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
            ok = error is None and got == case["expect"]
            shown = "error %s" % error if error else got
            wanted = case["expect"]

        print("%s  %s" % ("PASS" if ok else "FAIL", case["id"]))
        if not ok:
            failures += 1
            print("      expected: %s" % (wanted,))
            print("      got:      %s" % (shown,))

    total = len(corpus["cases"])
    print("\n%d of %d cases passed" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
