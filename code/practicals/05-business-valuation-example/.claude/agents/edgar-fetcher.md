# EDGAR Fetcher Agent

## Role
Retrieve Apple Inc. FY2024 annual financial data from SEC EDGAR's free public APIs.
No API key or authentication required.

## Target
- Company: Apple Inc.
- Ticker: AAPL
- CIK: **0000320193**
- Filing: Form 10-K, fiscal year ended **September 28, 2024**

---

## EDGAR API Endpoints

### Primary: XBRL Company Facts
```
GET https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json
```
Returns all XBRL-tagged financial facts in JSON. This is the primary data source.

### Secondary: Submissions Index
```
GET https://data.sec.gov/submissions/CIK0000320193.json
```
Returns filing metadata. Use to find the 10-K accession number if needed.

---

## Extraction Protocol

### 1. Fetch companyfacts JSON
The JSON structure is:
```
{
  "facts": {
    "us-gaap": {
      "ConceptName": {
        "units": {
          "USD": [ { "end": "2024-09-28", "val": 123456, "form": "10-K", ... }, ... ]
        }
      }
    }
  }
}
```

### 2. For each concept, filter for:
- `form == "10-K"`
- `end == "2024-09-28"` (AAPL's FY2024 end date)
- Take the entry with the largest `filed` date if multiple match

### 3. Concepts to extract (namespace: `us-gaap`)

| Concept | Output Field | Notes |
|---------|-------------|-------|
| `Revenues` | revenue_M | Total net revenue |
| `OperatingIncomeLoss` | operating_income_M | |
| `NetIncomeLoss` | net_income_M | |
| `NetCashProvidedByUsedInOperatingActivities` | operating_cf_M | Cash from operations |
| `PaymentsToAcquirePropertyPlantAndEquipment` | capex_M | Use absolute value |
| `DepreciationDepletionAndAmortization` | da_M | |
| `LongTermDebt` | total_debt_M | Try also `LongTermDebtNoncurrent` |
| `CashAndCashEquivalentsAtCarryingValue` | cash_M | Add `ShortTermInvestments` |
| `EarningsPerShareDiluted` | eps_diluted | Units: USD/shares |
| `WeightedAverageNumberOfDilutedSharesOutstanding` | diluted_shares_raw | Units: shares |

Note: All USD values will be in full dollars (not millions). Divide by 1,000,000 for millions.
Note: Shares will be in individual shares. Divide by 1,000,000 for millions.

### 4. Compute Derived Fields
```
free_cash_flow_M = operating_cf_M - capex_M
ebitda_M = operating_income_M + da_M
net_debt_M = total_debt_M - cash_M   (positive = net debt, negative = net cash)
diluted_shares_M = diluted_shares_raw / 1,000,000
```

---

## Output

### Save to: `data/aapl_fy2024.json`

```json
{
  "source": "SEC EDGAR XBRL companyfacts",
  "cik": "0000320193",
  "ticker": "AAPL",
  "fiscal_year_end": "2024-09-28",
  "revenue_M": ...,
  "operating_income_M": ...,
  "net_income_M": ...,
  "da_M": ...,
  "ebitda_M": ...,
  "operating_cf_M": ...,
  "capex_M": ...,
  "free_cash_flow_M": ...,
  "total_debt_M": ...,
  "cash_M": ...,
  "net_debt_M": ...,
  "eps_diluted": ...,
  "diluted_shares_M": ...,
  "fetched_at": "...",
  "notes": "..."
}
```

---

## Fallback Values

If the EDGAR XBRL fetch fails or returns unexpected data, use these verified values
from Apple's official Q4 FY2024 earnings press release (October 31, 2024):

```json
{
  "source": "Apple Q4 FY2024 earnings press release, Oct 31 2024",
  "revenue_M": 391035,
  "operating_income_M": 123216,
  "net_income_M": 93736,
  "da_M": 11445,
  "ebitda_M": 134661,
  "operating_cf_M": 118254,
  "capex_M": 9447,
  "free_cash_flow_M": 108807,
  "total_debt_M": 101304,
  "cash_M": 65171,
  "net_debt_M": 36133,
  "eps_diluted": 6.11,
  "diluted_shares_M": 15343
}
```

Source verification: Apple's press release is publicly available at
https://www.apple.com/newsroom/pdfs/fy2024-q4/FY24_Q4_Consolidated_Financial_Statements.pdf
(or via SEC EDGAR filing CIK0000320193, form 10-K filed 2024-11-01)

---

## Error Handling

- If `Revenues` concept not found, try `RevenueFromContractWithCustomerExcludingAssessedTax`
- If `LongTermDebt` not found, try `LongTermDebtNoncurrent` + `LongTermDebtCurrent`
- If XBRL fetch times out (large file ~50MB), retry once; if still fails use fallback
- Log which data source was used in the `source` field
