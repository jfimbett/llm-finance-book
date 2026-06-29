---
name: screen
description: Screen the bundled transactions for AML red flags and draft a grounded SAR narrative. Usage /screen [--rule <name>]
---

# /screen

Run the full screen -> group -> draft -> review loop and save a report.

1. **Screen** (screener agent):
   `python -m tools.screen --json > reports/_flags.json`
   Add `--rule <name>` to limit to one pattern (`structuring`, `round_number`,
   `high_risk_jurisdiction`, `velocity`).
2. **Group** (screener agent): read `reports/_flags.json` and group the flags by
   account, listing each transaction's id, amount, date, and the rule reason.
3. **Draft** (sar-writer agent): write a SAR-style narrative, one section per
   account, citing the transaction id and rule behind every assertion. State
   nothing that is not in `reports/_flags.json`.
4. **Review** (reviewer agent): confirm every claim is backed by a flag and that
   no flag was dropped. If a claim is unsupported, send it back to the sar-writer
   to remove or correct; if a flag was missed, add it. Loop at most 3 times.
5. **Save** to `reports/sar_<date>.md`:
   - the rule set and thresholds used,
   - the flagged transactions grouped by account,
   - the SAR narrative with per-claim citations.

If no transaction fires, write "No suspicious activity detected by the configured
rules." and stop — do not manufacture suspicion.

Try these to start:
- `/screen` — screen everything; expect structuring, round-number, high-risk, and velocity flags.
- `/screen --rule structuring` — isolate the smurfing pattern on ACC201.
- `/screen --rule high_risk_jurisdiction` — see only the high-risk-country hits.
