---
name: credit
description: Draft a grounded credit memo on a bundled company, with computed ratios and a default-risk score. Usage /credit <company>
---

# /credit <company>

Run the full load → ratios → score → memo loop and save a report.

1. **Load** (analyst agent):
   `python -m tools.financials <company>`  (run `--list` first if unsure of the slug)
2. **Ratios** (analyst agent):
   `python -m tools.ratios <company>`  — leverage, net leverage, interest coverage,
   current ratio, cash-to-debt.
3. **Score** (analyst agent):
   `python -m tools.score <company>`  — the 0-100 `risk_score`, the `risk_flag`
   (LOW/MEDIUM/HIGH), `default_risk`, and the per-dimension `components`.
4. **Write** (memo-writer agent): draft the memo from those numbers only — profile,
   leverage & coverage, liquidity, default risk, verdict — citing the source of every
   figure (`(ratios)` / `(score)`). Describe any `null` ratio as undefined.
5. **Check** (ratio-checker agent): re-run the tools and confirm every number in the memo
   matches a tool output; send it back to the writer if anything was invented, re-rounded,
   re-weighted, or has the flag overridden. Loop at most 3 times.
6. **Save** to `reports/<company>.md`:
   - the company and the headline figures,
   - the leverage / coverage / liquidity read,
   - the risk score, flag, and default-risk call,
   - a one-line verdict.

Try these to start:
- `/credit aurora`   ← strong: low leverage, 20x coverage, ample liquidity.
- `/credit cobalt`   ← distressed: high leverage, sub-1x coverage, current ratio below 1.
- `/credit delta`    ← debt-free: interest coverage is undefined (no interest expense).
