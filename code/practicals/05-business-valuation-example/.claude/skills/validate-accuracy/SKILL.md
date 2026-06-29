# /validate-accuracy

## Purpose
Triangulate DCF and comps estimates, compute accuracy vs reference price,
and determine pass/fail against the 10% target.

## When to Invoke
After both `/run-dcf` and `/run-comps` complete.

## Inputs Required
- `results/dcf_result.json`
- `results/comps_result.json`
- Reference price: $226.84

## Steps

1. **Read `.claude/agents/accuracy-checker.md`** and adopt the Accuracy Checker persona.

2. **Optionally verify reference price**:
   Search: "AAPL closing price September 27 2024"
   If search returns a price within ±$5 of $226.84, update reference accordingly.
   If search fails or is ambiguous, proceed with $226.84.

3. **Load values**:
   ```
   dcf_value = dcf_result.intrinsic_value_per_share
   comps_value = comps_result.triangulated_comps_value
   reference = 226.84
   ```

4. **Compute triangulated estimate** (50% DCF, 50% Comps):
   ```
   triangulated = 0.50 × dcf_value + 0.50 × comps_value
   ```

5. **Compute accuracy**:
   ```
   abs_error = |triangulated - reference|
   rel_error_pct = abs_error / reference × 100
   pass = (rel_error_pct <= 10.0)
   acceptable_range = [reference × 0.90, reference × 1.10]
               = [$204.16, $249.52]
   ```

6. **Print accuracy report** to console.

7. **Write results** to `results/accuracy.json`.

8. **If PASS**: write `results/final-report.md` with full valuation summary.

9. **If FAIL**: recommend adjustments and set flag for `/iterate-to-target`.

## Expected Numerical Result

With DCF = $210.23, Comps = $218.51:
```
Triangulated = 0.5 × 210.23 + 0.5 × 218.51 = $214.37/share
Error = |214.37 − 226.84| / 226.84 = 5.5%  ✓ PASS
```

Note: $214.37 is within the $204.16–$249.52 acceptable range.

## Output Files

### `results/accuracy.json`
```json
{
  "reference_price": 226.84,
  "dcf_value": 210.23,
  "comps_value": 218.51,
  "triangulated_value": 214.37,
  "dcf_weight": 0.50,
  "comps_weight": 0.50,
  "absolute_error": 12.47,
  "relative_error_pct": 5.5,
  "acceptable_range": [204.16, 249.52],
  "pass": true,
  "verdict": "PASS: $214.37 is 5.5% below reference $226.84"
}
```

### Console Report
```
================================================
AAPL EQUITY VALUATION — ACCURACY REPORT
================================================
Reference price (Sep 27, 2024):  $226.84
DCF intrinsic value  (50%):      $210.23
Comps estimate       (50%):      $218.51
------------------------------------------------
Triangulated estimate:           $214.37
Absolute error:                   $12.47
Relative error:                     5.5%
Target threshold:                  10.0%
Acceptable range:        [$204.16, $249.52]
Result:                             PASS ✓
================================================
```

## Error Handling

- If `dcf_result.json` is missing: run `/run-dcf` first
- If `comps_result.json` is missing: run `/run-comps` first
- If both values are far from target: check EDGAR data loaded correctly
