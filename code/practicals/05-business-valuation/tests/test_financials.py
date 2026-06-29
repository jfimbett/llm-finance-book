import json
from pathlib import Path

import financials

FIX = Path(__file__).parent / "fixtures" / "companyfacts_TEST.json"


def load():
    return json.loads(FIX.read_text())


def test_normalize_picks_latest_revenue():
    out = financials.normalize(load(), ticker="TEST")
    assert out["revenue"] == 1100
    assert out["fiscal_year"] == 2024


def test_normalize_computes_ebitda_and_delta_nwc():
    out = financials.normalize(load(), ticker="TEST")
    # ebitda = ebit + da = 300 + 90
    assert out["ebitda"] == 390
    # delta_nwc = (560-320) - (500-300) = 240 - 200 = 40
    assert out["delta_nwc"] == 40


def test_normalize_tax_rate_from_expense_over_pretax():
    out = financials.normalize(load(), ticker="TEST")
    # 60 / 300 = 0.2
    assert abs(out["tax_rate"] - 0.20) < 1e-9


def test_normalize_total_debt_and_shares():
    out = financials.normalize(load(), ticker="TEST")
    assert out["total_debt"] == 400
    assert out["shares"] == 100


def test_normalize_preserves_negative_ebit_and_net_income():
    facts = {
        "cik": 1,
        "entityName": "LOSS CO",
        "facts": {"us-gaap": {
            "Revenues": {"units": {"USD": [
                {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 500}]}},
            "OperatingIncomeLoss": {"units": {"USD": [
                {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": -80}]}},
            "NetIncomeLoss": {"units": {"USD": [
                {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": -120}]}},
            "CommonStockSharesOutstanding": {"units": {"shares": [
                {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 10}]}},
        }},
    }
    out = financials.normalize(facts, ticker="LOSS")
    assert out["ebit"] == -80
    assert out["net_income"] == -120
