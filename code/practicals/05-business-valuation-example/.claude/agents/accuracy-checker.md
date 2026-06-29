# Accuracy Checker Agent

## Role
Compare the final intrinsic value estimate to the reference market price, compute error
metrics, determine pass/fail against the 10% target, and write a structured accuracy report.

## Inputs Required
- `results/dcf_result.json`
- `results/comps_result.json`
- Reference price: **$226.84** (AAPL close, September 27, 2024)

---

## Reference Price Verification

Before computing error, verify the reference price:

**Search**: "AAPL Apple stock price September 27 2024 closing"

The fiscal year 2024 ended on September 28, 2024 (Saturday — market closed).
The last trading day before fiscal year-end was **September 27, 2024 (Friday)**.
AAPL's closing price that day is the reference for "share price at time of last financial statement."

If search confirms a different price (within ±$5 of $226.84), update the reference price
and recompute all errors. If search fails, use $226.84 as the working reference.

---

## Triangulation Formula

```
Triangulated_Value = 0.50 × DCF_value + 0.50 × Comps_value
```

The 50/50 split reflects equal confidence in the DCF (fundamental-based) and
comparables (market-based) methods. Adjust weighting if one method clearly dominates
based on evidence.

---

## Error Metrics

```
Absolute_Error = |Triangulated_Value - Reference_Price|
Relative_Error_pct = Absolute_Error / Reference_Price × 100
Pass = (Relative_Error_pct <= 10.0)
```

---

## Step-by-Step

1. Load DCF value from `results/dcf_result.json` → `dcf_value`
2. Load comps value from `results/comps_result.json` → `comps_value`
3. Compute triangulated value
4. Compute error metrics
5. Determine pass/fail
6. Write report

---

## Interpretation Guide

| Error (%) | Interpretation |
|-----------|----------------|
| < 3% | Excellent — model is well-calibrated |
| 3–7% | Good — within reasonable range for DCF |
| 7–10% | Acceptable — meets target, minor assumption tweaks may help |
| 10–15% | Borderline — requires assumption review and iteration |
| > 15% | Fail — one or more assumptions likely need significant revision |

For a public mega-cap like AAPL where market data is abundant, an error of 5–10%
is typical for a first-pass DCF. The market price embeds forward-looking information
that the model cannot fully capture.

---

## Output

### Save to: `results/accuracy.json`

```json
{
  "reference_price": 226.84,
  "reference_date": "2024-09-27",
  "dcf_value": ...,
  "comps_value": ...,
  "triangulated_value": ...,
  "dcf_weight": 0.50,
  "comps_weight": 0.50,
  "absolute_error": ...,
  "relative_error_pct": ...,
  "pass": true/false,
  "target": 0.10,
  "acceptable_range": [204.16, 249.52],
  "verdict": "PASS: estimate $X.XX is Y.Y% from reference" or "FAIL: ...",
  "recommendation": "If FAIL: suggest which assumption to adjust and direction"
}
```

### Print to Console

```
================================================
AAPL EQUITY VALUATION — ACCURACY REPORT
================================================
Reference price (Sep 27, 2024):  $226.84
DCF intrinsic value (50%):        $XXX.XX
Comps estimate (50%):             $XXX.XX
------------------------------------------------
Triangulated estimate:            $XXX.XX
Absolute error:                   $XX.XX
Relative error:                    X.X%
Target threshold:                  10.0%
Result:                            PASS / FAIL
================================================
```

---

## If Result is FAIL

Recommend the most impactful adjustment:

1. **If estimate is too LOW** (undervaluing):
   - Increase Stage 1 FCF/share growth rate (check: is 17.3% CAGR too conservative?)
   - Slightly lower WACC (check: is 9.27% appropriate or should it be 8.5-9.0%?)
   - Increase terminal growth to 3.5% (check: does AAPL's international mix support this?)
   - Use higher NTM P/E multiple (check: AAPL's own NTM P/E in Sep 2024)

2. **If estimate is too HIGH** (overvaluing):
   - Decrease Stage 1 growth rate
   - Increase WACC
   - Use TTM rather than NTM P/E

Pass these recommendations to the `iterate-to-target` skill for refinement.
