import math

from tools._common import load_financials, list_companies
from tools.ratios import compute_ratios, ratios_for


def test_ratio_math_on_fixture():
    # Aurora: revenue 2000, ebitda 600, debt 400, interest 30, ca 900, cl 300, cash 350.
    r = ratios_for("aurora")
    assert r["leverage"] == round(400 / 600, 3)            # gross debt / EBITDA
    assert r["net_leverage"] == round((400 - 350) / 600, 3)  # net debt / EBITDA
    assert r["interest_coverage"] == round(600 / 30, 3)    # EBITDA / interest = 20
    assert r["current_ratio"] == round(900 / 300, 3)       # = 3.0
    assert r["cash_to_debt"] == round(350 / 400, 3)
    assert r["net_debt"] == 400 - 350


def test_all_fixtures_have_complete_required_figures():
    for slug in list_companies():
        fin = load_financials(slug)
        # compute_ratios must run without raising on every bundled company
        compute_ratios(fin)


def test_zero_interest_yields_null_coverage_not_infinity():
    # Delta has no debt and no interest expense.
    r = ratios_for("delta")
    assert r["interest_coverage"] is None     # undefined, not inf / not a fabricated number
    assert r["cash_to_debt"] is None          # division by zero debt
    # the ratios that ARE defined still compute
    assert r["current_ratio"] == round(600 / 200, 3)
    assert r["net_debt"] == 0 - 300


def test_zero_current_liabilities_is_handled():
    fin = load_financials("aurora").copy()
    fin["current_liabilities"] = 0
    r = compute_ratios(fin)
    assert r["current_ratio"] is None
    assert not math.isnan(r["leverage"])
