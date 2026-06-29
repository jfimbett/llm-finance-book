# Portfolio-Construction Agent — agent instructions

Build a mean-variance optimal portfolio from the bundled text views and report a tiny
backtest, grounded only in tool output. The deterministic tools in `tools/` do all the
optimization and backtesting; you choose the objective and interpret outputs and never
compute or recall numbers yourself.

Pipeline for every run:

1. `python -m tools.views --json > reports/_views.json`
2. `python -m tools.optimize --objective max-sharpe --rf 0.0 --json > reports/_weights.json`
   (use `--objective min-variance` to ignore expected returns). Confirm weights sum to 1.
3. `python -m tools.backtest --objective max-sharpe --json > reports/_backtest.json`
4. Write a summary citing only the per-asset weights, the optimizer Sharpe, and the
   backtest cumulative return and Sharpe; flag any short (negative) weight; state that the
   backtest is in-sample on fictional data.
5. Save the summary to `reports/<objective>.md`.

Never state a weight, return, or Sharpe the tools did not produce. Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline, Cursor,
generic `AGENTS.md` runners) — Chapter 10's point that an agent's capabilities are just
markdown artifacts.
