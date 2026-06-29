# Practical 10 — Portfolio Optimization and Quantitative Trading (Claude Code / Cline)

**Large Language Models in Finance · Chapter 10**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive a portfolio-construction agent that turns a handful
of text-derived views into a mean-variance optimal portfolio and reports a tiny backtest —
the views -> optimize -> backtest pipeline from the chapter, built with the file-based
agents/skills pattern.

The agent never does the algebra or recalls a figure from memory: the deterministic tools
in `tools/` do all the optimization and backtesting, and the agent only chooses the
objective and interprets the outputs.

## Setup

```bash
pip install -r requirements.txt   # numpy + pytest; the tools are NumPy + standard library
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts under
`.claude/`: three sub-agents (`view-builder`, `optimizer`, `backtester`) and one command,
`/portfolio`.

## Run

```
/portfolio max-sharpe
```

The agent maps the bundled text views to an expected-returns vector, computes the optimal
weights, backtests them on the bundled return series, and saves a cited report to
`reports/`. Everything is offline — the data is a fictional five-asset universe in
`data/`.

You can also run the steps by hand:

```bash
python -m tools.views --json
python -m tools.optimize --objective max-sharpe --rf 0.0
python -m tools.backtest --objective max-sharpe
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Map text views to an expected-returns vector | `view-builder` | `tools/views.py` |
| Solve for mean-variance optimal weights | `optimizer` | `tools/optimize.py` (closed-form) |
| Backtest the weights on the return series | `backtester` | `tools/backtest.py` |

## The data

`data/market.json` holds a fictional five-asset universe — AURUM, BOREALIS, CYGNUS,
DELPHI, EQUINOX — with equilibrium expected returns, a 5x5 covariance matrix, and a
24-month return series. `data/views/` holds four short analyst notes (bullish on AURUM and
DELPHI, bearish on BOREALIS, neutral on EQUINOX; CYGNUS has no note). Everything is
invented for the exercise.

## The two objectives

- **`max-sharpe`** — the tangency portfolio `w ∝ Σ⁻¹(μ − r_f)`, normalised to sum to 1.
  Uses the **view-adjusted** expected returns, so it tilts toward the bullish names and
  shorts the bearish one.
- **`min-variance`** — the global minimum-variance portfolio `w ∝ Σ⁻¹1`. Ignores expected
  returns entirely and concentrates in the low-volatility anchor.

## Things to try

- Run `/portfolio min-variance` and compare the weights to `max-sharpe`: the views move
  one but not the other.
- Edit a note in `data/views/` from "bullish" to "bearish" and re-run — watch that asset's
  weight flip from long to short under `max-sharpe`.
- Raise `--rf` and watch the tangency portfolio rotate toward higher-return assets.
- Backtest an explicit equal-weight book with
  `python -m tools.backtest --weights 0.2 0.2 0.2 0.2 0.2` and compare its Sharpe to the
  optimized one. The backtest is in-sample on fictional data — illustrative, not a
  performance claim.

## Tests

```bash
python -m pytest -q        # fully offline
```
