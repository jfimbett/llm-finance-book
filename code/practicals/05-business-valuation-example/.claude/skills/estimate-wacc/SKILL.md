# /estimate-wacc

## Purpose
Estimate Apple Inc.'s WACC as of September 28, 2024 using CAPM.
All inputs must be verified with external data sources.

## When to Invoke
After `/fetch-financials`. Parallel to `/compute-fcf`.

## Inputs Required
- `data/aapl_fy2024.json` (total debt, diluted shares)
- Internet access for market data verification

## Steps

1. **Read `.claude/agents/wacc-estimator.md`** and adopt the WACC Estimator persona.

2. **Look up Risk-Free Rate**:
   Search: "US 10-year Treasury yield September 27 2024"
   Expected: ~3.75–3.85%
   Alternatively: check FRED https://fred.stlouisfed.org/series/DGS10

3. **Look up Beta**:
   Search: "Apple AAPL beta 5 year monthly 2024"
   Expected: ~1.20–1.30
   Note: Yahoo Finance shows "Beta (5Y Monthly)" on the Statistics page

4. **Look up Equity Risk Premium**:
   Search: "Damodaran implied equity risk premium US 2024 2025"
   Expected: ~4.5–5.0%
   Primary source: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/implprem.html

5. **Compute Cost of Equity**:
   ```
   CoE = Rf + Beta × ERP
   ```

6. **Establish Cost of Debt**:
   AAPL's outstanding bonds were issued at 1.375%–4.5% coupons (2013–2023).
   Weighted average coupon ≈ 2.85–2.95%.
   Use 2.90% unless EDGAR filing shows different interest expense / debt ratio.

7. **Get Tax Rate**:
   From `data/aapl_fy2024.json` or compute:
   Apple's effective tax rate FY2024: ~24.1%

8. **Compute Capital Structure Weights**:
   ```
   Market_cap = $226.84 × diluted_shares_M (from aapl_fy2024.json)
   Total_capital = Market_cap + total_debt_M
   Equity_weight = Market_cap / Total_capital
   Debt_weight = total_debt_M / Total_capital
   ```

9. **Compute WACC**:
   ```
   WACC = Equity_weight × CoE + Debt_weight × CoD × (1 - tax_rate)
   ```

10. **Write output** to `data/wacc.json` (format in wacc-estimator agent).

## Expected Output
- `data/wacc.json`
- WACC in range **8.8% – 9.8%** (central estimate ~9.27%)
- If WACC falls outside this range, re-verify beta and ERP sources

## Sensitivity Check
After computing, confirm sensitivity is reasonable:
- If WACC changes by ±0.5pp, DCF intrinsic value should change by ~$15-20/share
- A WACC of 9.27% should give a DCF value around $205-215/share
- If result is dramatically different, check that all units are in decimal (not percent)
