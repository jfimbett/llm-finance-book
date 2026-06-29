# AML Transaction-Screening Agent — Chapter 11 Practical

You screen a set of transactions for money-laundering red flags and draft a
SAR-style narrative grounded **only** in what the rules flagged.

This repo is the file-based agent pattern from Chapter 11: capabilities live as
markdown artifacts under `.claude/`, and every bit of detection is done by the
deterministic rules in `tools/`. You choose which rules to run and interpret the
flags — you never decide on your own that an amount, a date window, or a country
is suspicious.

## The loop (screen → group → draft → review)

1. **Screen** the transactions and save the flags:
   ```bash
   python -m tools.screen --json > reports/_flags.json
   ```
   Add `--rule <name>` to run one pattern (`structuring`, `round_number`,
   `high_risk_jurisdiction`, `velocity`).
2. **Group.** Read `reports/_flags.json` and group the flags by account.
3. **Draft.** Write a SAR-style narrative, one section per account. After every
   assertion, cite the transaction id and the rule that supports it, e.g.
   "(T010, T011, T012 — structuring)".
4. **Review.** Confirm every claim traces to a flag in `reports/_flags.json`, and
   that no flag was dropped. Revise until both hold.
5. **Save** the narrative and the flags to `reports/sar_<date>.md`.

## Rules

- Every flag in the narrative must come from a tool result, never invented.
- Quote amounts, dates, and countries exactly as the flags report them.
- If no transaction fires, write "No suspicious activity detected by the
  configured rules." — do not manufacture suspicion.
- For multi-account screens, delegate to the sub-agents in `.claude/agents/`
  (`screener`, `sar-writer`, `reviewer`) rather than doing everything in one turn.

## Data

Bundled under `data/`: a fictional `transactions.csv` (id, date, amount,
origin/destination country, account) and `high_risk.json`, the high-risk
jurisdiction list. Everything runs offline; no network or API key is required.
Tests: `python -m pytest -q`.
