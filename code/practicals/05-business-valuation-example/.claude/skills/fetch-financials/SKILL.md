# /fetch-financials

## Purpose
Retrieve Apple Inc. FY2024 10-K financial data from SEC EDGAR and save to `data/aapl_fy2024.json`.

## When to Invoke
First step of any valuation run. Must complete before any other skill.

## Inputs Required
- Internet access (SEC EDGAR free API)
- Write access to `data/` directory

## Steps

1. **Read `.claude/agents/edgar-fetcher.md`** and adopt the Edgar Fetcher persona.

2. **Fetch XBRL company facts**:
   ```
   GET https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json
   ```
   Note: This file is ~50-80MB. Allow up to 60 seconds for download.

3. **Extract FY2024 values** (filter: `form="10-K"`, `end="2024-09-28"`):
   - Revenues
   - OperatingIncomeLoss
   - NetIncomeLoss
   - NetCashProvidedByUsedInOperatingActivities
   - PaymentsToAcquirePropertyPlantAndEquipment
   - DepreciationDepletionAndAmortization
   - LongTermDebt (or LongTermDebtNoncurrent)
   - CashAndCashEquivalentsAtCarryingValue
   - EarningsPerShareDiluted
   - WeightedAverageNumberOfDilutedSharesOutstanding

4. **Convert units**: All USD values are in full dollars; divide by 1,000,000 for millions.
   Shares are in individual units; divide by 1,000,000 for millions.

5. **Compute derived metrics**:
   - `free_cash_flow_M = operating_cf_M - capex_M`
   - `ebitda_M = operating_income_M + da_M`
   - `net_debt_M = total_debt_M - cash_M`

6. **If EDGAR fails** (timeout, parse error, unexpected structure):
   Use fallback values from `.claude/agents/edgar-fetcher.md` (Apple press release Oct 31, 2024).
   Set `data_source = "Apple Q4 FY2024 press release fallback"`.

7. **Write output** to `data/aapl_fy2024.json` (format in edgar-fetcher agent).

8. **Verify** by printing key metrics:
   ```
   Revenue:   $391.0B ± 2%
   FCF:       $108.8B ± 2%
   EPS:       $6.11 ± 5%
   Shares:    15,343M ± 2%
   ```
   If values deviate significantly from these ranges, log a warning and check EDGAR extraction logic.

## Expected Output
- File: `data/aapl_fy2024.json`
- Key fields: `free_cash_flow_M`, `eps_diluted`, `diluted_shares_M`, `ebitda_M`, `net_debt_M`

## Error Handling
- EDGAR timeout: retry once after 10s, then use fallback
- Missing concept: try alternate concept name (see edgar-fetcher agent for aliases)
- Wrong fiscal year: verify `end` date matches `2024-09-28`
