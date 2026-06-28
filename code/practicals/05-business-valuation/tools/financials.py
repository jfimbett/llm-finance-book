import argparse

from _common import cik_pad, data_dir, die, emit, read_json, write_json

TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax",
                "Revenues", "SalesRevenueNet"],
    "ebit": ["OperatingIncomeLoss"],
    "da": ["DepreciationDepletionAndAmortization",
           "DepreciationAmortizationAndAccretionNet",
           "DepreciationAndAmortization"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment",
              "PaymentsToAcquireProductiveAssets"],
    "current_assets": ["AssetsCurrent"],
    "current_liabilities": ["LiabilitiesCurrent"],
    "long_term_debt": ["LongTermDebtNoncurrent", "LongTermDebt"],
    "debt_current": ["LongTermDebtCurrent", "DebtCurrent"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue",
             "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"],
    "net_income": ["NetIncomeLoss"],
    "pretax_income": [
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
    "tax_expense": ["IncomeTaxExpenseBenefit"],
    "shares": ["CommonStockSharesOutstanding",
               "WeightedAverageNumberOfDilutedSharesOutstanding",
               "EntityCommonStockSharesOutstanding"],
}


def _annual_rows(facts, tag):
    gaap = facts.get("facts", {}).get("us-gaap", {})
    node = gaap.get(tag)
    if not node:
        return []
    units = node["units"]
    unit = "USD" if "USD" in units else ("shares" if "shares" in units else next(iter(units)))
    rows = [u for u in units[unit] if str(u.get("form", "")).startswith("10-K")]
    rows.sort(key=lambda u: u.get("end", ""))
    return rows


def latest_annual(facts, tags, unit="USD"):
    for tag in tags:
        rows = _annual_rows(facts, tag)
        if rows:
            return rows[-1]["val"]
    return None


def _two_latest(facts, tags):
    for tag in tags:
        rows = _annual_rows(facts, tag)
        if len(rows) >= 2:
            return rows[-1]["val"], rows[-2]["val"]
        if len(rows) == 1:
            return rows[-1]["val"], None
    return None, None


def _num(facts, tags, default=0.0):
    val = latest_annual(facts, tags)
    return float(val) if val is not None else default


def delta_nwc(facts):
    ca1, ca0 = _two_latest(facts, TAGS["current_assets"])
    cl1, cl0 = _two_latest(facts, TAGS["current_liabilities"])
    if None in (ca1, ca0, cl1, cl0):
        return 0.0
    return (ca1 - cl1) - (ca0 - cl0)


def _fiscal_year(facts):
    for tag in TAGS["revenue"]:
        rows = _annual_rows(facts, tag)
        if rows:
            return rows[-1].get("fy")
    return None


def normalize(facts, ticker=None):
    rev = latest_annual(facts, TAGS["revenue"])
    if rev is None or rev <= 0:
        die("could not find positive annual revenue in company facts")
    ebit = _num(facts, TAGS["ebit"])
    da = _num(facts, TAGS["da"])
    capex = _num(facts, TAGS["capex"])
    ltd = _num(facts, TAGS["long_term_debt"])
    dc = _num(facts, TAGS["debt_current"])
    cash = _num(facts, TAGS["cash"])
    ni = _num(facts, TAGS["net_income"])
    shares = latest_annual(facts, TAGS["shares"])
    if not shares or shares <= 0:
        die("could not find shares outstanding in company facts")
    pretax = latest_annual(facts, TAGS["pretax_income"])
    tax_exp = latest_annual(facts, TAGS["tax_expense"])
    if pretax and pretax > 0 and tax_exp is not None:
        tax_rate = max(0.0, min(0.45, tax_exp / pretax))
    else:
        tax_rate = 0.21
    return {
        "cik": cik_pad(facts.get("cik", 0)),
        "ticker": ticker,
        "entity": facts.get("entityName"),
        "fiscal_year": _fiscal_year(facts),
        "revenue": float(rev),
        "ebit": float(ebit),
        "da": float(da),
        "capex": float(capex),
        "delta_nwc": float(delta_nwc(facts)),
        "total_debt": float(ltd + dc),
        "cash": float(cash),
        "shares": float(shares),
        "net_income": float(ni),
        "ebitda": float(ebit + da),
        "tax_rate": float(tax_rate),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cik", required=True)
    ap.add_argument("--ticker")
    a = ap.parse_args()
    facts_path = data_dir(a.cik) / "companyfacts.json"
    if not facts_path.exists():
        die(f"{facts_path} not found — run edgar_fetch.py first")
    out = normalize(read_json(facts_path), ticker=a.ticker)
    write_json(data_dir(a.cik) / "financials.json", out)
    emit(out)


if __name__ == "__main__":
    main()
