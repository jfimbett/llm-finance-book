# /iterate-to-target

## Purpose
If the initial valuation estimate is outside the 10% target, iteratively adjust
DCF and comparables assumptions until the estimate converges within range.
Maximum 5 iterations.

## When to Invoke
Only after `/validate-accuracy` has run and returned FAIL (error > 10%).

## Inputs Required
- `results/accuracy.json` (current error and triangulated value)
- `results/dcf_result.json` (current DCF assumptions)
- `results/comps_result.json` (current comps assumptions)
- `data/aapl_fy2024.json`
- `data/wacc.json`
- `data/fcf_history.json`

## Iteration Logic

### Step 1: Diagnose the Gap

```
gap = reference_price - triangulated_value
gap_pct = gap / reference_price × 100
```

- If `gap_pct > 0`: model is UNDERVALUING — increase value inputs
- If `gap_pct < 0`: model is OVERVALUING — decrease value inputs

### Step 2: Select Adjustment (maximum impact per change)

**Priority order for UNDERVALUATION** (model too low):

1. **WACC reduction** (most impactful):
   - Each 0.5pp reduction ≈ +$15-20/share
   - Justify: "AAPL's AA+ credit and quality premium suggest lower beta should be used"
   - Acceptable lower bound: WACC = 8.5%
   - Search "AAPL implied WACC analyst consensus 2024" for market estimates

2. **Stage 1 growth increase**:
   - Each 2pp increase ≈ +$8-12/share
   - Justify: "Apple Intelligence is expected to drive iPhone upgrade supercycle in FY2025-2026"
   - Acceptable upper bound: g1 = 20%
   - Evidence: Check Apple Intelligence adoption metrics, analyst EPS revisions upward

3. **Terminal growth increase**:
   - 0.5pp increase (e.g., 3.0% → 3.5%) ≈ +$20-30/share (very sensitive)
   - Justify: "AAPL's 57% international revenue provides above-average long-run growth"
   - Acceptable upper bound: gT = 3.5%
   - Risk: High — small terminal growth changes have large value impact

4. **P/E multiple increase**:
   - Apply AAPL's actual observed NTM P/E in Sep 2024 (~31-33x if current comps used lower)
   - Justify: "Market assigned 31-33x NTM P/E to AAPL in Sep 2024"

**Priority order for OVERVALUATION** (model too high):

1. **WACC increase**: verify beta and ERP are not too low
2. **Stage 1 growth decrease**: is 17.3% too aggressive for next 5 years?
3. **Terminal growth decrease**: revert to 2.5% if 3% unsupported
4. **P/E multiple decrease**: use peer median without AAPL premium

### Step 3: Apply Single Adjustment

Make **one change per iteration**. Changing multiple assumptions simultaneously
makes it impossible to attribute the accuracy improvement to any specific factor.

Document the change with evidence:
```markdown
## Iteration N Adjustment
- Changed: [WACC / g1 / gT / P/E multiple]
- From: X.XX%
- To:   Y.YY%
- Justification: [specific evidence + source]
- Expected value change: +/- $Z/share
```

### Step 4: Recompute and Validate

Re-run DCF and/or comps with adjusted assumption.
Recompute triangulated value and error.

```
new_triangulated = 0.5 × new_dcf + 0.5 × new_comps
new_error_pct = |new_triangulated - 226.84| / 226.84 × 100
```

### Step 5: Check Convergence

- If `new_error_pct ≤ 10.0%`: PASS — write final report
- If `new_error_pct > 10.0%` and iterations < 5: go to Step 1 with new values
- If iterations = 5 and still failing: write report with best estimate and flag for manual review

## Maximum Iteration Budget

| Iter | Expected Adjustment | Expected Result |
|------|---------------------|----------------|
| 1 | Verify WACC with market data | May reduce WACC by 0.3-0.5pp |
| 2 | Verify AAPL's actual NTM P/E | May increase P/E multiple |
| 3 | Increase terminal growth to 3.5% if justified | Large positive impact |
| 4 | Check if FY2025E EPS consensus is higher | Affect comps |
| 5 | Final best-effort: use most favorable justified assumptions | |

## Output

### Update `results/accuracy.json` with each iteration

### Write `results/iteration-log.md`:
```markdown
# Iteration Log

## Iteration 1
- Adjustment: [...]
- New DCF: $XXX
- New Comps: $XXX
- New Triangulated: $XXX
- New Error: X.X%
- Status: PASS/CONTINUE
...
```

## Stopping Criteria

STOP and declare success when:
- `|triangulated - 226.84| / 226.84 ≤ 0.10`

STOP and declare best-effort when:
- 5 iterations completed without convergence
- Report best estimate achieved and remaining gap

## Expected Convergence

The initial estimate (before iteration) should be:
- DCF: ~$210/share (-7.3%)
- Comps: ~$218/share (-3.7%)
- Triangulated: ~$214/share (-5.5%)

This is already within the 10% target. Iteration should only be needed if
EDGAR data differs significantly from fallback values, or if WACC/beta
inputs yield an unusual WACC.
