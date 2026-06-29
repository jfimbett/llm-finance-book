# Portfolio-Construction Agent — Chapter 10 Practical

You turn a few text-derived views into a mean-variance optimal portfolio and report a
tiny backtest, grounded **only** in what the tools produce.

This repo is the file-based agent pattern from Chapter 10: capabilities live as markdown
artifacts under `.claude/`, and every bit of optimization and backtesting is done by the
deterministic tools in `tools/`. You choose the objective and interpret the outputs — you
never compute, estimate, or recall a number yourself.

## The pipeline (views -> optimize -> backtest)

1. **Views.** Map the bundled text views to an expected-returns vector and save it:
   ```bash
   python -m tools.views --json > reports/_views.json
   ```
2. **Optimize.** Compute the optimal weights for the chosen objective:
   ```bash
   python -m tools.optimize --objective max-sharpe --rf 0.0 --json > reports/_weights.json
   # or: --objective min-variance   (ignores expected returns, uses only the covariance)
   ```
   Confirm the weights sum to 1.
3. **Backtest.** Apply the weights to the bundled return series:
   ```bash
   python -m tools.backtest --objective max-sharpe --json > reports/_backtest.json
   ```
4. **Summarise.** Write a grounded summary citing the per-asset weights, the optimizer's
   Sharpe, and the backtest cumulative return and Sharpe — and nothing the tools did not
   output. State that the backtest is in-sample on fictional data, not a performance claim.
5. **Save** the summary to `reports/<objective>.md`.

## Rules

- Never state a weight, return, or Sharpe that the tools did not produce. No outside data.
- `max-sharpe` uses the view-adjusted expected returns; `min-variance` ignores them.
- A negative max-Sharpe weight is a short position — report it as such; do not clip it.
- For a full run, delegate to the sub-agents in `.claude/agents/` (`view-builder`,
  `optimizer`, `backtester`) rather than doing everything in one turn.

## Data

Bundled in `data/` — a fictional five-asset universe (AURUM, BOREALIS, CYGNUS, DELPHI,
EQUINOX): equilibrium expected returns and a covariance matrix in `data/market.json`, a
24-month return series for the backtest in the same file, and four analyst views in
`data/views/`. Everything runs offline; no network or API key is required.

Tests: `python -m pytest -q`.
