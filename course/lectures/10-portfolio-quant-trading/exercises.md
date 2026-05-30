# Exercises — Lecture 10: Portfolio Optimization and Quantitative Trading

## Exercise 1 [B]
**Topic:** Classical Portfolio Theory and Its Limits

The Black-Litterman model combines a market equilibrium prior with investor-specified views to produce a posterior return estimate. Suppose you have access to an LLM that has analyzed 50 recent earnings call transcripts and produced a bullish view on the technology sector with a confidence score of 0.75.

(a) Explain in your own words how this LLM-derived view could be incorporated into the Black-Litterman framework. What inputs would you need to specify, and what assumptions must hold for the integration to be meaningful?

(b) Identify two limitations of classical mean-variance optimization that LLMs cannot resolve, even with access to large volumes of textual data. Justify your answer.

## Exercise 2 [I]
**Topic:** Backtesting with LLM Signals

You have constructed a daily sentiment score from a financial news LLM for 100 S&P 500 stocks over a five-year period (2019–2023). You want to backtest a long-short strategy that goes long the top-decile sentiment stocks and short the bottom-decile each month.

Write Python code (using `pandas` and `numpy`) that implements a walk-forward backtest of this strategy. Your implementation must:

(a) Refit the signal ranking each month using only data available up to that point (no look-ahead).

(b) Compute monthly portfolio returns net of a round-trip transaction cost of 10 basis points per trade.

(c) Report the annualized Sharpe ratio and maximum drawdown of the strategy.

Discuss one additional pitfall beyond look-ahead bias that could invalidate your backtest results, and explain how you would address it.

## Exercise 3 [A]
**Topic:** Risk Management Applications

Tail risk events — such as sudden credit spread blowouts or liquidity crises — are often preceded by shifts in financial language detectable in regulatory filings, central bank communications, and news corpora.

Design a real-time tail risk monitoring system that uses a large language model to score daily textual inputs and trigger portfolio alerts. Your design should address:

(a) The choice of textual sources, their update frequency, and how you would construct a composite tail-risk score from heterogeneous inputs.

(b) How you would calibrate the alert threshold to control the false-positive rate, using historical crisis episodes (e.g., COVID-19 March 2020, SVB collapse March 2023) as your evaluation benchmark.

(c) The market microstructure considerations that would govern how quickly you act on an alert, given that other participants may be processing the same signals.

Critically evaluate the limits of such a system: under what conditions would it fail to detect or respond to a tail event in time to be useful?
