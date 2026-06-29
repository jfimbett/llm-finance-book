# WACC Estimator Agent

## Role
Estimate Apple Inc.'s Weighted Average Cost of Capital (WACC) as of September 28, 2024
using CAPM for the cost of equity and verified market data for all inputs.
Every input must be justified with a data source.

## Inputs Required
- `data/aapl_fy2024.json` (total debt, diluted shares)
- Web access to verify market inputs

---

## CAPM Formula

```
WACC = Equity_weight × Cost_of_Equity + Debt_weight × After_tax_Cost_of_Debt

Cost_of_Equity = Risk_Free_Rate + Beta × Equity_Risk_Premium
After_tax_Cost_of_Debt = Pre_tax_Cost_of_Debt × (1 - Effective_Tax_Rate)
```

---

## Step-by-Step Inputs

### 1. Risk-Free Rate (Rf)
**Source**: US 10-year Treasury yield around September 27-28, 2024.

Context: The Federal Reserve cut the federal funds rate by 50bps on September 18, 2024
(first cut since 2020). The 10-year Treasury yield was ~3.75-3.80% in late September 2024,
having declined from its Oct 2023 peak of 5.0%.

**Verify by searching**: "10 year treasury yield September 27 2024"
**Expected value**: 3.75% – 3.80%
**Use**: **3.78%** (0.0378)

### 2. Beta (β)
**Source**: AAPL 5-year monthly beta vs S&P 500 as of late 2024.

AAPL's beta has historically ranged from 1.1 to 1.35 depending on the measurement window.
As of mid-2024, AAPL's 5-year monthly beta was approximately 1.24 (available from
Bloomberg, Yahoo Finance Pro, or Macrotrends).

**Verify by searching**: "Apple AAPL beta 5 year monthly 2024"
**Expected value**: 1.20 – 1.30
**Use**: **1.24**

### 3. Equity Risk Premium (ERP)
**Source**: Damodaran's implied ERP for the US market.

Aswath Damodaran (NYU Stern) publishes monthly implied ERP estimates for the US.
As of January 2025 (closest estimate to Sep 2024 fiscal year-end):
- Damodaran's US implied ERP: approximately 4.60%
- URL: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/implprem.html

**Verify**: search "Damodaran implied equity risk premium US January 2025"
**Expected value**: 4.5% – 5.0%
**Use**: **4.60%** (0.046)

### 4. Cost of Equity (CAPM)

```
CoE = Rf + β × ERP = 3.78% + 1.24 × 4.60% = 3.78% + 5.70% = 9.48%
```

### 5. Pre-Tax Cost of Debt
**Source**: AAPL's bond yields in secondary market, late 2024.

AAPL has ~$95-101B in total long-term debt, issued primarily between 2013 and 2023
at coupons ranging from 1.375% (2013) to 4.5% (2023). The weighted average coupon
is approximately 2.8-3.0%. However, secondary market yield-to-maturity for AAPL bonds
in Sep 2024 was approximately 4.3% (reflecting higher rate environment).

For WACC: use **book-value weighted coupon** rather than market yield, as it represents
the actual cost of existing debt (the new-issuance rate would be 4.3%+ but is not
representative of the outstanding debt structure).

**Use**: **2.90%** (0.029) — weighted average coupon on outstanding bonds
**Alternative**: 4.3% if modeling marginal cost of new debt

### 6. Effective Tax Rate
From AAPL FY2024 income statement: Net income / Pre-tax income.
Apple's effective tax rate has been stable at ~24-25% for several years.
FY2024: Net income $93,736M, Pre-tax income ~$123,000M → effective rate ~24.1%

**Use**: **24.1%** (0.241)

### 7. After-Tax Cost of Debt

```
After_tax_CoD = 2.90% × (1 - 0.241) = 2.90% × 0.759 = 2.20%
```

### 8. Capital Structure Weights

As of September 27, 2024 (reference date):
- Market cap = $226.84/share × 15,343M shares = **$3,480.3B**
- Total debt = **$101.3B** (from FY2024 balance sheet)
- Total capital = $3,480.3B + $101.3B = **$3,581.6B**

```
Equity weight = 3,480.3 / 3,581.6 = 97.17%
Debt weight   =   101.3 / 3,581.6 =  2.83%
```

Note: AAPL's capital structure is overwhelmingly equity-funded at market values.
The debt weighting is minimal and has a small impact on WACC.

### 9. WACC Calculation

```
WACC = 97.17% × 9.48% + 2.83% × 2.20%
     = 9.211% + 0.062%
     = 9.27%
```

**Final WACC: 9.27%** (round to **9.3%** for model inputs)

---

## Sensitivity Analysis

| Rf | Beta | ERP | WACC |
|----|------|-----|------|
| 3.50% | 1.20 | 4.40% | 8.78% |
| 3.78% | 1.24 | 4.60% | **9.27%** |
| 4.00% | 1.30 | 4.80% | 9.93% |

The key driver of WACC uncertainty is Beta (ranges from 1.1-1.35 across sources)
and ERP (ranges from 4.0-5.5% depending on methodology).

---

## Output

### Save to: `data/wacc.json`

```json
{
  "risk_free_rate": 0.0378,
  "risk_free_rate_source": "US 10yr Treasury yield, Sep 27 2024",
  "beta": 1.24,
  "beta_source": "5yr monthly beta vs S&P 500",
  "erp": 0.046,
  "erp_source": "Damodaran implied ERP, Jan 2025",
  "cost_of_equity": 0.0948,
  "pre_tax_cost_of_debt": 0.029,
  "effective_tax_rate": 0.241,
  "after_tax_cost_of_debt": 0.022,
  "equity_weight": 0.9717,
  "debt_weight": 0.0283,
  "wacc": 0.0927,
  "wacc_pct": "9.27%",
  "notes": "CAPM-based WACC; book-value weighted coupon for CoD"
}
```
