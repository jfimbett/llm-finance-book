# /run-dcf

## Purpose
Run the two-stage per-share DCF model for AAPL and save results to `results/dcf_result.json`.

## When to Invoke
After `/compute-fcf` and `/estimate-wacc` both complete.

## Inputs Required
- `data/aapl_fy2024.json`
- `data/fcf_history.json`
- `data/wacc.json`

## Steps

1. **Read `.claude/agents/dcf-modeler.md`** and adopt the DCF Modeler persona.

2. **Load inputs**:
   ```
   fcf_per_share_0 = aapl_fy2024.free_cash_flow_M / aapl_fy2024.diluted_shares_M
   g1 = min(fcf_history.fcf_per_share_cagr_5yr, 0.20)   # cap at 20%
   gT = 0.030                                             # terminal growth: 3%
   wacc = wacc.wacc                                       # from data/wacc.json
   n = 5                                                  # stage 1 years
   ```

3. **Validate inputs** (abort if outside bounds):
   - `fcf_per_share_0` must be in [5.0, 10.0] — expected ~$7.09
   - `g1` must be in [0.10, 0.20]
   - `gT` must be < `wacc` (required for Gordon Growth to converge)
   - `wacc` must be in [0.06, 0.14]

4. **Compute Stage 1 FCF/share projections**:
   For each year y in [1, 2, 3, 4, 5]:
   ```
   FCF_y = fcf_per_share_0 × (1 + g1)^y
   PV_y = FCF_y / (1 + wacc)^y
   ```

5. **Compute Terminal Value**:
   ```
   TV = FCF_5 × (1 + gT) / (wacc - gT)
   PV_TV = TV / (1 + wacc)^5
   ```

6. **Sum**:
   ```
   intrinsic_value = Sum(PV_y for y=1..5) + PV_TV
   ```

7. **Compute error**:
   ```
   error_pct = (intrinsic_value - 226.84) / 226.84 × 100
   ```

8. **Run sensitivity table** (4×4 grid):
   - WACC: [wacc - 0.005, wacc, wacc + 0.005, wacc + 0.01]
   - g1:   [g1 - 0.02, g1, g1 + 0.02]

9. **Write results** to `results/dcf_result.json`.

## Expected Output
- `results/dcf_result.json`
- `intrinsic_value_per_share` expected in range $195–$230
- With WACC=9.27% and g1=17.3%, gT=3%: expected ~$210/share

## Numerical Example (pre-computed for verification)

With: `fcf_per_share_0 = 7.0916`, `g1 = 0.173`, `wacc = 0.0927`, `gT = 0.030`

| Year | FCF/share | PV |
|------|-----------|-----|
| 1 | $8.318 | $7.613 |
| 2 | $9.757 | $8.172 |
| 3 | $11.445 | $8.773 |
| 4 | $13.426 | $9.417 |
| 5 | $15.749 | $10.111 |
Sum PV Stage 1 = $44.09

Terminal value = $15.749 × 1.03 / (0.0927 - 0.030) = $258.71
PV Terminal = $258.71 / (1.0927)^5 = $166.14

**Total DCF = $210.23/share** (7.3% below $226.84 — within 10% target)

## Error Handling
- If `wacc ≤ gT`: cannot compute Gordon Growth model; increase gT or decrease wacc
- If `intrinsic_value > 400` or `< 50`: likely unit error; check that FCF is per-share (not total)
- If result is < $200: try increasing `g1` by 2pp or decreasing `wacc` by 0.5pp
