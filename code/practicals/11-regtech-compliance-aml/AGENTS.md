# AML Transaction-Screening Agent — agent instructions

Screen the bundled transactions in `data/` for money-laundering red flags and
draft a SAR-style narrative grounded only in what the rules flagged. The
deterministic rules in `tools/` do all detection; you choose which rules to run
and interpret the flags, and you never judge an amount, date, or country yourself.

Loop for every screening:

1. `python -m tools.screen --json > reports/_flags.json` (add `--rule <name>` to
   limit to `structuring`, `round_number`, `high_risk_jurisdiction`, or `velocity`).
2. Read `reports/_flags.json` and group the flags by account.
3. Write a SAR narrative; after every assertion cite the transaction id and the
   rule, e.g. "(T010, T011, T012 — structuring)".
4. Check that every claim traces to a flag and that no flag was dropped; revise
   until both hold.
5. Save the narrative + flags to `reports/sar_<date>.md`.

Every flag in the narrative must come from a tool result, never invented. If no
transaction fires, write "No suspicious activity detected by the configured
rules." Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline,
Cursor, generic `AGENTS.md` runners) — Chapter 11's point that an agent's
capabilities are just markdown artifacts.
