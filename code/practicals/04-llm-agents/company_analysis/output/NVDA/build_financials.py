import json, datetime, collections

RAW = "/Users/juan/Documents/company_analysis/output/NVDA/raw/companyfacts.json"
OUT = "/Users/juan/Documents/company_analysis/output/NVDA/02_financials.json"

d = json.load(open(RAW))
gaap = d["facts"]["us-gaap"]

def dparse(s):
    return datetime.date.fromisoformat(s)

def fy_label(end):
    # NVIDIA fiscal year ends late January; end-year == FY label
    return end.year

def annual_flow(concept, unit="USD"):
    """Full-year duration facts from 10-Ks, keyed by fiscal year (end-year)."""
    out = {}
    node = gaap.get(concept)
    if not node or unit not in node["units"]:
        return out
    for f in node["units"][unit]:
        if f.get("form") != "10-K":
            continue
        if "start" not in f:
            continue
        start = dparse(f["start"]); end = dparse(f["end"])
        days = (end - start).days
        if days < 330 or days > 400:
            continue
        fy = fy_label(end)
        prev = out.get(fy)
        if prev is None or f["filed"] > prev["filed"]:
            out[fy] = {"val": f["val"], "filed": f["filed"], "end": f["end"]}
    return {k: v["val"] for k, v in out.items()}

def annual_instant(concept, unit="USD"):
    """Instant (balance-sheet) facts from 10-Ks, keyed by fiscal year."""
    out = {}
    node = gaap.get(concept)
    if not node or unit not in node["units"]:
        return out
    for f in node["units"][unit]:
        if f.get("form") != "10-K":
            continue
        if "start" in f:
            continue
        end = dparse(f["end"])
        # balance sheet date late Jan -> FY = end.year
        fy = fy_label(end)
        prev = out.get(fy)
        if prev is None or f["filed"] > prev["filed"]:
            out[fy] = {"val": f["val"], "filed": f["filed"], "end": f["end"]}
    return {k: v["val"] for k, v in out.items()}

notes = []

# ---- Income statement (flows) ----
flow_concepts = {
    "revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"],
    "cost_of_revenue": ["CostOfRevenue", "CostOfGoodsAndServicesSold"],
    "gross_profit": "GrossProfit",
    "operating_income": "OperatingIncomeLoss",
    "net_income": "NetIncomeLoss",
    "rd_expense": "ResearchAndDevelopmentExpense",
    "income_tax_expense": "IncomeTaxExpenseBenefit",
    "pretax_income": "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
    "sbc": "ShareBasedCompensation",
    "effective_tax_rate": ("EffectiveIncomeTaxRateContinuingOperations", "pure"),
}
# cash flow (flows)
cf_concepts = {
    "operating_cash_flow": "NetCashProvidedByUsedInOperatingActivities",
    "investing_cash_flow": "NetCashProvidedByUsedInInvestingActivities",
    "financing_cash_flow": "NetCashProvidedByUsedInFinancingActivities",
    "capex": ["PaymentsToAcquireProductiveAssets", "PaymentsToAcquirePropertyPlantAndEquipment"],
    "buybacks": "PaymentsForRepurchaseOfCommonStock",
    "dividends_paid": "PaymentsOfDividends",
}
# balance sheet (instants)
bs_concepts = {
    "cash_and_equivalents": "CashAndCashEquivalentsAtCarryingValue",
    "marketable_securities_current": ["MarketableSecuritiesCurrent", "AvailableForSaleSecuritiesDebtMaturitiesWithinOneYearFairValue"],
    "accounts_receivable": "AccountsReceivableNetCurrent",
    "inventory": "InventoryNet",
    "assets_current": "AssetsCurrent",
    "assets_total": "Assets",
    "liabilities_current": "LiabilitiesCurrent",
    "liabilities_total": "Liabilities",
    "stockholders_equity": "StockholdersEquity",
    "long_term_debt_noncurrent": "LongTermDebtNoncurrent",
    "long_term_debt_current": "LongTermDebtCurrent",
    "long_term_debt_total": "LongTermDebt",
    "accounts_payable": "AccountsPayableCurrent",
    "deferred_revenue_current": "ContractWithCustomerLiabilityCurrent",
}
# per share & shares
ps_concepts = {
    "eps_basic": ("EarningsPerShareBasic", "USD/shares"),
    "eps_diluted": ("EarningsPerShareDiluted", "USD/shares"),
    "dividends_per_share": ("CommonStockDividendsPerShareDeclared", "USD/shares"),
    "shares_diluted": ("WeightedAverageNumberOfDilutedSharesOutstanding", "shares"),
    "shares_basic": ("WeightedAverageNumberOfSharesOutstandingBasic", "shares"),
}

series = {}
def add(name, spec, kind):
    # spec may be: "Concept" | ("Concept","unit") | ["C1","C2"] | [("C1","u"),("C2","u")]
    if isinstance(spec, list):
        candidates = spec
    else:
        candidates = [spec]
    merged = {}
    used = []
    for cand in candidates:
        if isinstance(cand, tuple):
            concept, unit = cand
        else:
            concept, unit = cand, "USD"
        data = annual_flow(concept, unit) if kind == "flow" else annual_instant(concept, unit)
        if data:
            used.append(concept)
        for y, v in data.items():
            merged.setdefault(y, v)  # first candidate wins per year
    if not merged:
        names = ", ".join(c[0] if isinstance(c, tuple) else c for c in candidates)
        notes.append(f"Missing/empty concept for '{name}' (tried: {names}).")
    elif len(candidates) > 1 and len(used) > 1:
        notes.append(f"'{name}' merged across tags {used} (NVIDIA changed XBRL tag across years).")
    series[name] = merged

for n, s in flow_concepts.items(): add(n, s, "flow")
for n, s in cf_concepts.items(): add(n, s, "flow")
for n, s in bs_concepts.items(): add(n, s, "instant")
for n, s in ps_concepts.items():
    concept, unit = s
    # EPS and dividends-per-share are flows (duration); shares are duration too
    add(n, s, "flow")

# ---- Stock-split normalization (per-share consistency) ----
# NVIDIA: 10-for-1 split effective June 10, 2024 (FY2025); 4-for-1 effective July 2021 (FY2022).
# Filings up to FY2024 (covering FY<=2022 comparatives) report FY2022 on the PRE-10:1 basis,
# while FY2023+ comparatives in later filings are POST-10:1. Normalize all per-share/share
# data to the current (post-June-2024) basis so series and EPS CAGR are comparable.
split_factor = {2022: 10}  # multiply shares by factor; divide per-share amounts by factor
per_share_divide = ["eps_basic", "eps_diluted", "dividends_per_share"]
share_multiply = ["shares_diluted", "shares_basic"]
as_reported_fy2022 = {}
for fy, fac in split_factor.items():
    for nm in per_share_divide:
        if series.get(nm, {}).get(fy) is not None:
            as_reported_fy2022.setdefault(nm, {})[fy] = series[nm][fy]
            series[nm][fy] = round(series[nm][fy] / fac, 4)
    for nm in share_multiply:
        if series.get(nm, {}).get(fy) is not None:
            as_reported_fy2022.setdefault(nm, {})[fy] = series[nm][fy]
            series[nm][fy] = series[nm][fy] * fac

# Determine fiscal years to cover: last 5 by revenue availability
all_years = sorted(series["revenue"].keys())
years = all_years[-5:]

# Restrict series to selected years (keep all reported but expose chosen window)
def window(dmap):
    return {str(y): dmap.get(y) for y in years}

series_out = {k: window(v) for k, v in series.items()}

# ---- Derived metrics ----
def g(name, y):
    return series[name].get(y)

derived = {"by_year": {}, "cagr": {}}
prev_year = {years[i]: years[i-1] for i in range(1, len(years))}

for y in years:
    row = {}
    rev = g("revenue", y)
    ni = g("net_income", y)
    gp = g("gross_profit", y)
    oi = g("operating_income", y)
    ocf = g("operating_cash_flow", y)
    capex = g("capex", y)
    eq = g("stockholders_equity", y)
    at = g("assets_total", y)
    ca = g("assets_current", y)
    cl = g("liabilities_current", y)
    rd = g("rd_expense", y)
    ltd = g("long_term_debt_total", y) or g("long_term_debt_noncurrent", y)

    def margin(num):
        return round(num / rev, 4) if (num is not None and rev) else None
    row["gross_margin"] = margin(gp)
    row["operating_margin"] = margin(oi)
    row["net_margin"] = margin(ni)
    row["rd_intensity"] = margin(rd)
    # FCF
    fcf = (ocf - capex) if (ocf is not None and capex is not None) else None
    row["free_cash_flow"] = fcf
    row["fcf_margin"] = round(fcf / rev, 4) if (fcf is not None and rev) else None
    # returns (using end-of-year balances; simple ROE/ROA)
    row["roe"] = round(ni / eq, 4) if (ni is not None and eq) else None
    row["roa"] = round(ni / at, 4) if (ni is not None and at) else None
    # liquidity
    row["current_ratio"] = round(ca / cl, 4) if (ca and cl) else None
    # leverage
    row["debt_to_equity"] = round(ltd / eq, 4) if (ltd is not None and eq) else None
    # net cash = cash + marketable sec - total debt
    cash = g("cash_and_equivalents", y)
    msc = g("marketable_securities_current", y)
    if cash is not None or msc is not None:
        invest = (cash or 0) + (msc or 0)
        debt = ltd or 0
        row["net_cash_position"] = invest - debt
    else:
        row["net_cash_position"] = None
    # growth YoY
    if y in prev_year:
        py = prev_year[y]
        prev_rev = g("revenue", py)
        prev_ni = g("net_income", py)
        row["revenue_growth_yoy"] = round(rev / prev_rev - 1, 4) if (rev and prev_rev) else None
        row["net_income_growth_yoy"] = round(ni / prev_ni - 1, 4) if (ni and prev_ni) else None
        prev_fcf = derived["by_year"].get(py, {}).get("free_cash_flow")
    else:
        row["revenue_growth_yoy"] = None
        row["net_income_growth_yoy"] = None
    derived["by_year"][str(y)] = row

# CAGR over the window (first to last available)
def cagr(name):
    ys = [y for y in years if series[name].get(y) not in (None, 0)]
    if len(ys) < 2:
        return None
    first, last = ys[0], ys[-1]
    v0, v1 = series[name][first], series[name][last]
    n = last - first
    if v0 <= 0 or v1 <= 0 or n == 0:
        return None
    return round((v1 / v0) ** (1 / n) - 1, 4)

derived["cagr"] = {
    "period": f"FY{years[0]}-FY{years[-1]}",
    "revenue": cagr("revenue"),
    "net_income": cagr("net_income"),
    "gross_profit": cagr("gross_profit"),
    "operating_income": cagr("operating_income"),
    "eps_diluted": cagr("eps_diluted"),
    "free_cash_flow": None,  # filled below
}
# FCF CAGR
fcf_by_year = {y: derived["by_year"][str(y)]["free_cash_flow"] for y in years}
fcf_years = [y for y in years if fcf_by_year[y] not in (None, 0) and fcf_by_year[y] > 0]
if len(fcf_years) >= 2:
    f0, f1 = fcf_years[0], fcf_years[-1]
    derived["cagr"]["free_cash_flow"] = round((fcf_by_year[f1] / fcf_by_year[f0]) ** (1/(f1-f0)) - 1, 4)

# Notes on conventions
notes.append("Fiscal years aligned by period end-date (NVIDIA FY ends late January; e.g., FY2026 = period ending 2026-01-25). The XBRL 'fy' field was NOT used as it was inconsistent across restated filings.")
notes.append("Annual flows filtered to 10-K facts with a ~365-day duration; for each fiscal year the latest 'filed' value was kept (captures restatements/retrospective revisions).")
notes.append("Revenue concept = RevenueFromContractWithCustomerExcludingAssessedTax. Cost of revenue = CostOfGoodsAndServicesSold.")
notes.append("ROE/ROA use end-of-period equity/assets (not average), so they are point-in-time approximations.")
notes.append("net_cash_position = cash_and_equivalents + marketable_securities_current - total long-term debt; excludes non-current marketable securities if any.")
notes.append("Per-share and share-count series are split-adjusted to the CURRENT basis (post June-10-2024 10-for-1 split). FY2022 as-reported (pre-10:1) values were: eps_diluted=3.85, eps_basic=3.91, dividends_per_share=0.16, shares_diluted=2,535,000,000, shares_basic=2,496,000,000. These were converted (per-share /10, shares x10) so the series and EPS CAGR are comparable; FY2023-FY2026 were already on the current basis.")
notes.append("marketable_securities_current: FY2022-FY2025 from MarketableSecuritiesCurrent; FY2026 not tagged under that concept, so the within-one-year available-for-sale debt-securities fair value (AvailableForSaleSecuritiesDebtMaturitiesWithinOneYearFairValue) is used as the current-investments proxy. NVIDIA also holds large non-current equity stakes (EquitySecuritiesFVNINoncurrent ~$22.3B in FY2026) and non-current marketable securities not included in net_cash_position.")
notes.append("deferred_revenue_current = ContractWithCustomerLiabilityCurrent (NVIDIA's deferred-revenue/contract-liability tag).")
notes.append("All USD values as reported (full dollars, not millions). Shares in absolute counts. EPS reflects post stock-split reporting as filed.")

meta = {
    "ticker": "NVDA",
    "cik": "0001045810",
    "company_name": d.get("entityName", "NVIDIA CORP"),
    "latest_filing_date": "2026-02-25",
    "latest_report_date": "2026-01-25",
    "fiscal_years_covered": [f"FY{y}" for y in years],
    "fiscal_year_convention": "FY label = calendar year of fiscal year-end (late January).",
}

out = {"meta": meta, "series": series_out, "derived": derived, "notes": notes}
json.dump(out, open(OUT, "w"), indent=2)
print("Years covered:", years)
print("Wrote", OUT)
# quick sanity print
for y in years:
    print(f"FY{y}: rev={series['revenue'].get(y)}, ni={series['net_income'].get(y)}, gm={derived['by_year'][str(y)]['gross_margin']}, eps_dil={series['eps_diluted'].get(y)}")
print("Missing notes:", [n for n in notes if n.startswith('Missing')])
