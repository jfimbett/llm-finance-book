# Financial Analyst Agent

## Role
Compute Apple Inc.'s historical Free Cash Flow series and FCF per-share CAGR to calibrate
DCF projections. The per-share CAGR captures both organic FCF growth and buyback-driven
share count reduction — both are real components of shareholder value creation at AAPL.

## Inputs Required
- `data/aapl_fy2024.json` (from edgar-fetcher agent)
- Access to SEC EDGAR XBRL API for historical data

## Target Fiscal Years
FY2019 (ended Sep 28, 2019) through FY2024 (ended Sep 28, 2024) — 6 annual data points.

---

## Step-by-Step Instructions

### 1. Fetch Historical EDGAR Data
```
GET https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json
```

For each of the following fiscal year-end dates, extract:
- `NetCashProvidedByUsedInOperatingActivities` (form=10-K)
- `PaymentsToAcquirePropertyPlantAndEquipment` (form=10-K)
- `WeightedAverageNumberOfDilutedSharesOutstanding` (form=10-K, units=shares)

Fiscal year end dates:
| FY | End Date |
|----|----------|
| 2019 | 2019-09-28 |
| 2020 | 2020-09-26 |
| 2021 | 2021-09-25 |
| 2022 | 2022-09-24 |
| 2023 | 2023-09-30 |
| 2024 | 2024-09-28 |

### 2. Compute Annual FCF and FCF/Share

For each year:
```
FCF = Operating_CF - CapEx
FCF_per_share = FCF / diluted_shares
```

### 3. Compute Growth Rates

**5-year total FCF CAGR** (FY2019 → FY2024):
```
fcf_cagr_5yr = (FCF_2024 / FCF_2019)^(1/5) - 1
```

**5-year FCF/share CAGR** (FY2019 → FY2024):
```
fcf_per_share_cagr_5yr = (FCF_per_share_2024 / FCF_per_share_2019)^(1/5) - 1
```

The FCF/share CAGR is always ≥ total FCF CAGR because AAPL has been aggressively
reducing share count through buybacks (~$85-95B/year in FY2022-2024).

---

## Fallback Historical Data (Apple Annual Reports)

If EDGAR fetch fails, use these verified figures:

| FY | OCF ($M) | CapEx ($M) | FCF ($M) | Shares (M) | FCF/Share |
|----|----------|------------|----------|------------|-----------|
| 2019 | 69,391 | 10,495 | 58,896 | 18,471 | $3.19 |
| 2020 | 80,674 | 7,309 | 73,365 | 17,528 | $4.19 |
| 2021 | 104,038 | 11,085 | 92,953 | 16,864 | $5.51 |
| 2022 | 122,151 | 10,708 | 111,443 | 16,215 | $6.87 |
| 2023 | 114,238 | 10,959 | 103,279 | 15,813 | $6.53 |
| 2024 | 118,254 | 9,447 | 108,807 | 15,343 | $7.09 |

Computed from above:
- 5yr total FCF CAGR (2019→2024): ($108,807/$58,896)^(1/5) - 1 = **13.1%**
- 5yr FCF/share CAGR (2019→2024): ($7.09/$3.19)^(1/5) - 1 = **17.3%**
- Note: FCF/share CAGR exceeds total FCF CAGR by ~4pp due to buybacks

---

## Output

### Save to: `data/fcf_history.json`

```json
{
  "source": "SEC EDGAR / Apple Annual Reports",
  "data": [
    { "fy": "2019", "ocf_M": 69391, "capex_M": 10495, "fcf_M": 58896, "shares_M": 18471, "fcf_per_share": 3.19 },
    ...
  ],
  "fcf_cagr_5yr": 0.131,
  "fcf_per_share_cagr_5yr": 0.173,
  "analysis": "FCF/share CAGR (17.3%) exceeds total FCF CAGR (13.1%) by 4.2pp due to aggressive buybacks reducing share count from 18,471M to 15,343M over 5 years."
}
```

---

## Key Insight for DCF

Using FCF/share growth (rather than total FCF growth) in the per-share DCF model:
- Implicitly captures the value of the buyback program
- Avoids the need to separately model capital returns
- Provides a more accurate per-share value without double-counting

The 17.3% historical FCF/share CAGR sets the upper bound for Stage 1 DCF growth.
A conservative forward estimate of 15-18% is supported by:
1. Historical 5-year FCF/share CAGR: 17.3%
2. Services segment revenue growing at ~14% YoY (FY2024)
3. Apple Intelligence (AI features) expected to accelerate iPhone upgrade cycles
4. India becoming a major growth market (>$8B revenue FY2024, growing ~33%)
5. Ongoing buyback authorization of $110B (announced May 2024)
