---
name: portfolio
description: Build a mean-variance optimal portfolio from the text views and report a tiny backtest. Usage /portfolio [max-sharpe|min-variance]
---

# /portfolio [max-sharpe|min-variance]

Run the full views -> optimize -> backtest pipeline and save a grounded report. Default
objective is `max-sharpe`; pass `min-variance` to ignore expected returns.

1. **Views** (view-builder agent):
   `python -m tools.views --json > reports/_views.json`
   Read the view-adjusted expected returns and which note moved each asset.
2. **Optimize** (optimizer agent):
   `python -m tools.optimize --objective <objective> --rf 0.0 --json > reports/_weights.json`
   Confirm the weights sum to 1; read the expected return, volatility and Sharpe.
3. **Backtest** (backtester agent):
   `python -m tools.backtest --objective <objective> --json > reports/_backtest.json`
   Read the cumulative return and annualised Sharpe over the bundled return series.
4. **Summarise.** Write a grounded summary that cites only numbers from the three JSON
   files: the per-asset weights, the in-sample Sharpe from the optimizer, and the backtest
   cumulative return and Sharpe. State that the backtest is in-sample on fictional data and
   not a performance claim. Do not state any number the tools did not produce.
5. **Save** to `reports/<objective>.md`:
   - the chosen objective,
   - the view-adjusted expected returns and the tilts that produced them,
   - the optimal weights (and a note on any short position),
   - the backtest cumulative return and Sharpe.

Try these to start:
- `/portfolio max-sharpe`   -> tilts toward the bullish views (AURUM, DELPHI), shorts the bearish one (BOREALIS).
- `/portfolio min-variance` -> ignores the views; concentrates in the low-volatility anchor (EQUINOX).
