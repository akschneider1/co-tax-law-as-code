"""Colorado slice: individual income tax rate and the state earned income tax credit.

Each rule cites the statute provision ids in text/ that it implements. Facts the
slice does not compute (Colorado taxable income, the federal credit, residency)
come in as inputs.
"""
import datetime
from decimal import Decimal

from .core import (
    Context,
    InvalidFacts,
    OutOfScope,
    Parameters,
    money,
    rule,
    to_decimal,
)


def tax_year_start(facts):
    year = facts.get("tax_year")
    if not isinstance(year, int):
        raise InvalidFacts("tax_year must be an integer year")
    return datetime.date(year, 1, 1)


@rule(
    "co.income_tax.before_credits",
    cites=["/us/co/crs/39-22-104/1.7/c", "/us/co/crs/39-22-104/2"],
    params=["co.income_tax.rate_schedule"],
)
def income_tax_before_credits(ctx):
    """Tax = rate schedule applied to Colorado taxable income.

    39-22-104(2) requires federal taxable income to be modified under (3) and (4)
    before the rate applies. Those modifications are not modelled: the caller
    supplies Colorado taxable income after them.
    """
    income = to_decimal(ctx.facts.get("colorado_taxable_income"), "colorado_taxable_income")
    entry = ctx.param("co.income_tax.rate_schedule", tax_year_start(ctx.facts))
    brackets = [(Decimal(b["over"]), Decimal(b["rate"])) for b in entry["value"]]

    tax = Decimal("0")
    parts = []
    for index, (floor, rate) in enumerate(brackets):
        ceiling = brackets[index + 1][0] if index + 1 < len(brackets) else None
        if income <= floor:
            break
        slice_top = income if ceiling is None else min(income, ceiling)
        amount = (slice_top - floor) * rate
        tax += amount
        parts.append("%s x %s" % (slice_top - floor, rate))
    detail = " + ".join(parts) if parts else "no taxable income"
    return ctx.record(income_tax_before_credits, money(tax), detail)


@rule(
    "co.eitc.amount",
    cites=[
        "/us/co/crs/39-22-123.5/2",
        "/us/co/crs/39-22-123.5/2.5",
        "/us/co/crs/39-22-123.5/2.7",
    ],
    params=["co.eitc.match_rate"],
)
def co_eitc(ctx):
    """Credit = match rate x federal earned income credit.

    The federal amount is an input: the credit claimed on the federal return, or
    the credit that would have been allowed under (2.5) or (2.7). The same
    percentage applies to all three in the ingested text.
    """
    federal = to_decimal(ctx.facts.get("federal_eitc", 0), "federal_eitc")
    if federal == 0:
        return ctx.record(co_eitc, Decimal("0"), "no federal credit")
    entry = ctx.param("co.eitc.match_rate", tax_year_start(ctx.facts))
    rate = Decimal(entry["value"])
    return ctx.record(co_eitc, money(federal * rate), "%s x %s" % (federal, rate))


@rule(
    "co.income_tax.net_of_eitc",
    cites=["/us/co/crs/39-22-123.5/4"],
)
def net_tax(ctx, tax, credit):
    """Refundable: credit above the tax due is refunded, so the net can be negative."""
    return ctx.record(net_tax, tax - credit, "%s - %s" % (tax, credit))


def calculate(facts, parameters=None):
    """Run the slice for one filer. Returns outputs, trace and warnings."""
    ctx = Context(facts, parameters or Parameters())

    residency = facts.get("residency", "full_year")
    if residency != "full_year":
        # Part-year credit is apportioned under 39-22-123.5(5) and 39-22-110(1);
        # nonresident tax is apportioned too. Neither is modelled.
        raise OutOfScope("only full-year residents are modelled, got %r" % residency)

    tax = income_tax_before_credits(ctx)
    credit = co_eitc(ctx)
    net = net_tax(ctx, tax, credit)
    return {
        "outputs": {
            "income_tax_before_credits": str(tax),
            "co_eitc": str(credit),
            "net_tax_after_eitc": str(net),
        },
        "trace": ctx.trace,
        "warnings": ctx.warnings,
    }
