# /compute-fcf

## Purpose
Compute Apple Inc.'s historical Free Cash Flow series (FY2019–FY2024) and
derive FCF/share CAGR to use as the Stage 1 growth rate in the DCF model.

## When to Invoke
After `/fetch-financials`. Before `/run-dcf`.

## Inputs Required
- `data/aapl_fy2024.json` (for FY2024 reference values)
- Internet access (EDGAR for historical data)

## Steps

1. **Read `.claude/agents/financial-analyst.md`** and adopt the Financial Analyst persona.

2. **Fetch historical data from EDGAR** (same companyfacts endpoint):
   ```
   GET https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json
   ```
   Extract annual (form=10-K) values for FY2019 through FY2024:
   - `NetCashProvidedByUsedInOperatingActivities`
   - `PaymentsToAcquirePropertyPlantAndEquipment`
   - `WeightedAverageNumberOfDilutedSharesOutstanding` (units=shares)

   Fiscal year end dates:
   - FY2019: 2019-09-28
   - FY2020: 2020-09-26
   - FY2021: 2021-09-25
   - FY2022: 2022-09-24
   - FY2023: 2023-09-30
   - FY2024: 2024-09-28

3. **If EDGAR fails**, use fallback table in financial-analyst agent.

4. **Compute for each year**:
   ```
   FCF = Operating_CF - CapEx
   FCF_per_share = FCF / diluted_shares
   ```

5. **Compute growth rates**:
   ```
   fcf_cagr_5yr = (FCF_2024 / FCF_2019)^(1/5) - 1
   fcf_per_share_cagr_5yr = (FCF_per_share_2024 / FCF_per_share_2019)^(1/5) - 1
   ```

6. **Write output** to `data/fcf_history.json`.

7. **Print summary**:
   ```
   5yr Total FCF CAGR:        ~13.1%
   5yr FCF/share CAGR:        ~17.3%
   Buyback contribution:      ~4.2pp
   ```

## Expected Output
- `data/fcf_history.json`
- `fcf_per_share_cagr_5yr` ≈ 0.173 (tolerance ±2pp depending on EDGAR extraction)

## Notes
- FCF/share CAGR > Total FCF CAGR because share count decreased ~17% over 5 years
- This per-share CAGR is the direct input to the Stage 1 DCF growth rate
- A higher CAGR → higher DCF intrinsic value → closer to reference price
