from tools._common import load_financials
from tools.score import score_company, score_for, risk_components


def test_weaker_company_scores_higher_risk_than_stronger():
    # Aurora (low leverage, 20x coverage, 3.0 current) vs Cobalt (6.8x net leverage,
    # <1x coverage, 0.57 current). The distressed retailer must score higher risk.
    strong = score_for("aurora")["risk_score"]
    medium = score_for("borealis")["risk_score"]
    weak = score_for("cobalt")["risk_score"]
    assert strong < medium < weak


def test_score_is_monotone_when_every_input_worsens():
    # Build a strictly-weaker twin: more debt, less EBITDA, more interest,
    # fewer current assets, more current liabilities, less cash. Every sub-score
    # can only rise, so the blended score must strictly increase.
    base = {
        "company": "base", "name": "Base Co",
        "revenue": 1000, "ebitda": 300, "total_debt": 600, "interest_expense": 60,
        "current_assets": 500, "current_liabilities": 400, "cash": 100,
    }
    worse = {
        **base, "company": "worse", "name": "Worse Co",
        "ebitda": 200, "total_debt": 800, "interest_expense": 90,
        "current_assets": 380, "current_liabilities": 460, "cash": 40,
    }
    cb, cw = risk_components(base), risk_components(worse)
    for k in ("leverage", "coverage", "liquidity"):
        assert cw[k] >= cb[k], k
    assert score_company(worse)["risk_score"] > score_company(base)["risk_score"]


def test_high_risk_company_is_flagged_for_default():
    res = score_for("cobalt")
    assert res["risk_flag"] == "HIGH"
    assert res["default_risk"] is True


def test_strong_company_is_low_risk():
    res = score_for("aurora")
    assert res["risk_flag"] == "LOW"
    assert res["default_risk"] is False


def test_zero_interest_company_carries_no_coverage_risk():
    # Delta: no debt, no interest -> leverage and coverage risk both zero, score low.
    comp = risk_components(load_financials("delta"))
    assert comp["coverage"] == 0.0
    assert comp["leverage"] == 0.0
    assert score_for("delta")["risk_flag"] == "LOW"


def test_no_earnings_pins_leverage_and_coverage_to_max():
    fin = load_financials("borealis").copy()
    fin["ebitda"] = 0   # no earnings to service debt
    comp = risk_components(fin)
    assert comp["leverage"] == 1.0
    assert comp["coverage"] == 1.0
