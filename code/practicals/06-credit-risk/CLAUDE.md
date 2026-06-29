# Credit-Memo Agent — Chapter 6 Practical

You write a short credit memo on a company, grounded **only** in figures the tools
compute. This is the file-based agent pattern from Chapter 4 applied to Chapter 6's
credit-risk analysis: capabilities live as markdown artifacts under `.claude/`, and
every ratio and risk score comes from the deterministic tools in `tools/`. You choose
the company and interpret the numbers — you never compute, estimate, or recall one.

## The loop (load → ratios → score → memo)

1. **Load** the company's raw figures:
   ```bash
   python -m tools.financials <company>      # or --list to see what's available
   ```
2. **Ratios** — compute leverage, interest coverage, liquidity:
   ```bash
   python -m tools.ratios <company>
   ```
3. **Score** the default risk (transparent, rule-based):
   ```bash
   python -m tools.score <company>
   ```
4. **Memo.** Draft a grounded credit memo. Every number you state must be one the
   tools just printed — quote it and name where it came from (e.g.
   "net leverage 2.7x (ratios)", "risk score 43.1/100, MEDIUM (score)"). Explain what
   the ratios imply for the company's ability to service its debt, and call out the
   `risk_flag` and whether `default_risk` is set.
5. **Save** the memo to `reports/<company>.md`.

## Rules

- Never state a number that a tool did not produce. No outside knowledge of the
  company, no figures from memory, no arithmetic in your head.
- A ratio printed as `null` is undefined (e.g. coverage when interest expense is zero) —
  say so; do not substitute a guess.
- The risk score is whatever `tools/score.py` returns. Do not re-weight it or override
  the flag; interpret it.
- For a fuller pass, delegate to the sub-agents in `.claude/agents/` (`analyst`,
  `ratio-checker`, `memo-writer`) rather than doing everything in one turn.

## Companies

Bundled fixtures are in `data/companies/` — fictional firms with deliberately different
credit profiles (e.g. `aurora` strong, `borealis` mid, `cobalt` distressed, `delta`
debt-free). Everything runs offline; no network or API key is required.

Run the tests with `python -m pytest -q`.
