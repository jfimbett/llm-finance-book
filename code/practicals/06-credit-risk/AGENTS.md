# Credit-Memo Agent — agent instructions

Write a short credit memo on one of the bundled companies in `data/companies/`,
grounded only in figures the tools compute. The deterministic tools in `tools/` do all
arithmetic — ratios and the default-risk score; you choose the company and interpret the
outputs and never compute or recall a number yourself.

Loop for every company:

1. `python -m tools.financials <company>`  (or `--list` to see what's available)
2. `python -m tools.ratios <company>`      — leverage, interest coverage, liquidity
3. `python -m tools.score <company>`        — 0-100 risk score and a LOW/MEDIUM/HIGH flag
4. Draft the memo using only those numbers; quote each one and name its source
   ("net leverage 2.7x (ratios)", "risk score 43.1/100, MEDIUM (score)"). Interpret the
   `risk_flag` and `default_risk` fields; a `null` ratio is undefined — say so.
5. Save the memo to `reports/<company>.md`.

Never state a figure a tool did not produce, and never re-weight or override the score.
Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline, Cursor,
generic `AGENTS.md` runners) — the chapter's point that an agent's capabilities are just
markdown artifacts.
