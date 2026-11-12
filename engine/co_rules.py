"""Colorado slice: individual income tax rate and the state earned income tax credit.

Each rule cites the provision ids in text/ that it implements, by tax year where
the provision in force changes. Facts the slice does not compute (Colorado
taxable income, the federal credit, residency) come in as inputs.

Optional facts:
  tax_method                        'statute' (default) or 'form': which tax
                                    amount the net figure is built on
  federal_eitc_basis                'claimed' (default), 'no_work_ssn', 'under_25'
  taxable_principal_residence_gain  from tax year 2027; must be 0 or absent
"""
import datetime
from decimal import Decimal

from .core import (
    Context,
    InvalidFacts,
    OutOfScope,
    ParameterUnavailable,
    Parameters,
    money,
    rule,
    to_decimal,
)

MEASURE = "/us/co/measure/2026/amendment-87/39-22-104"

# How the caller arrived at the federal credit, and the provision that allows
# a Colorado credit on that basis. The under-25 basis starts with tax year 2022
# in the ingested text of (2.7).
EITC_BASES = {
    "claimed": ("/us/co/crs/39-22-123.5/2", None),
    "no_work_ssn": ("/us/co/crs/39-22-123.5/2.5", None),
    "under_25": ("/us/co/crs/39-22-123.5/2.7", 2022),
}


def tax_year_start(facts):
    year = facts.get("tax_year")
    if not isinstance(year, int):
        raise InvalidFacts("tax_year must be an integer year")
    return datetime.date(year, 1, 1)


@rule(
    "co.income_tax.before_credits",
    cites=[
        ("/us/co/crs/39-22-104/1.7/c", None, 2026),
        (MEASURE + "/1.8/a", 2027, None),
        (MEASURE + "/1.8/a/VI", 2027, None),
        "/us/co/crs/39-22-104/2",
    ],
    params=["co.income_tax.rate_schedule"],
)
def income_tax_before_credits(ctx):
    """Tax = rate schedule applied to Colorado taxable income.

    39-22-104(2) requires federal taxable income to be modified under (3) and (4)
    before the rate applies. Those modifications are not modelled: the caller
    supplies Colorado taxable income after them.

    From tax year 2027 the measure's proposed (1.8)(b) taxes certain gain on
    the sale of a principal residence at a separate rate. That is not
    modelled, so a filer who reports such gain is refused.
    """
    income = to_decimal(ctx.facts.get("colorado_taxable_income"), "colorado_taxable_income")
    if ctx.facts["tax_year"] >= 2027:
        gain = ctx.facts.get("taxable_principal_residence_gain")
        if gain is None:
            ctx.warn("co.income_tax.before_credits: assumes no taxable gain from selling a principal residence; "
                     "proposed 39-22-104(1.8)(b) taxes that gain at a separate rate and is not modelled")
        elif to_decimal(gain, "taxable_principal_residence_gain") > 0:
            raise OutOfScope("taxable gain from selling a principal residence is taxed under proposed "
                             "39-22-104(1.8)(b), which is not modelled")
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
    "co.income_tax.form_table",
    cites=[],
    params=["co.income_tax.tax_table", "co.income_tax.rate_schedule"],
)
def income_tax_form_table(ctx, statutory_tax):
    """Tax as the Department of Revenue's form arrives at it.

    At or below $50,000 of taxable income the form uses a printed table: the
    rate applied to the middle of the income band, in whole dollars. Above
    that, the form's worksheet applies the rate to the income, which is the
    statutory amount. Returns None for a year with no recorded table.
    """
    income = to_decimal(ctx.facts.get("colorado_taxable_income"), "colorado_taxable_income")
    day = tax_year_start(ctx.facts)
    try:
        table = ctx.parameters.entry("co.income_tax.tax_table", day)["value"]
    except ParameterUnavailable:
        return ctx.record(income_tax_form_table, None, "no tax table is recorded for this tax year")
    if income > Decimal(table["at_or_below"]):
        return ctx.record(income_tax_form_table, statutory_tax,
                          "over %s: the form's worksheet applies the rate to the income" % table["at_or_below"])
    if income == 0:
        return ctx.record(income_tax_form_table, Decimal("0"), "no taxable income")
    schedule = ctx.parameters.entry("co.income_tax.rate_schedule", day)["value"]
    if len(schedule) != 1:
        return ctx.record(income_tax_form_table, None, "the table method is recorded for a single rate only")
    rate = Decimal(schedule[0]["rate"])

    edges = [Decimal(e) for e in table["band_edges_below_100"]]
    width = Decimal(table["band_width"])
    if income <= edges[-1]:
        low = max(e for e in edges[:-1] if e < income)
        high = min(e for e in edges[1:] if e >= income)
    else:
        # Bands are "over low, but not over high".
        high = (income / width).to_integral_value(rounding="ROUND_CEILING") * width
        low = high - width
    middle = (low + high) / 2
    return ctx.record(income_tax_form_table, money(middle * rate),
                      "band over %s, not over %s: %s x %s" % (low, high, middle, rate))


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

    The federal amount is an input. The fact federal_eitc_basis says what it is:
      claimed      the credit claimed on the federal return, (2)
      no_work_ssn  the credit that would have been allowed but for the lack of
                   a social security number valid for employment, (2.5)
      under_25     the credit that would have been allowed to a filer under 25
                   without a qualifying child, (2.7)
    The same percentage applies to all three. For the last two the engine
    cannot check the amount, because it does not compute the federal credit.
    """
    federal = to_decimal(ctx.facts.get("federal_eitc", 0), "federal_eitc")
    basis = ctx.facts.get("federal_eitc_basis", "claimed")
    if basis not in EITC_BASES:
        raise InvalidFacts("federal_eitc_basis must be one of %s, got %r" % (", ".join(sorted(EITC_BASES)), basis))
    provision, first_year = EITC_BASES[basis]
    if first_year and ctx.facts["tax_year"] < first_year:
        raise OutOfScope("the %s basis is allowed from tax year %d" % (basis, first_year))
    if federal == 0:
        return ctx.record(co_eitc, Decimal("0"), "no federal credit", cites=[provision])
    if basis != "claimed":
        ctx.warn("co.eitc.amount: the federal amount is the credit that would have been allowed (%s), "
                 "worked out by the caller; the engine does not compute or check it" % basis)
    entry = ctx.param("co.eitc.match_rate", tax_year_start(ctx.facts))
    rate = Decimal(entry["value"])
    return ctx.record(co_eitc, money(federal * rate), "%s x %s (%s)" % (federal, rate, basis), cites=[provision])


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

    method = facts.get("tax_method", "statute")
    if method not in ("statute", "form"):
        raise InvalidFacts("tax_method must be 'statute' or 'form', got %r" % (method,))
    tax_year_start(facts)

    tax = income_tax_before_credits(ctx)
    form_tax = income_tax_form_table(ctx, tax)
    if method == "form" and form_tax is None:
        raise ParameterUnavailable("tax_method is 'form' but no form amount can be computed for this tax year")
    credit = co_eitc(ctx)
    net = net_tax(ctx, form_tax if method == "form" else tax, credit)
    return {
        "outputs": {
            "income_tax_before_credits": str(tax),
            "income_tax_form_table": None if form_tax is None else str(form_tax),
            "co_eitc": str(credit),
            "net_tax_after_eitc": str(net),
        },
        "trace": ctx.trace,
        "warnings": ctx.warnings,
    }
