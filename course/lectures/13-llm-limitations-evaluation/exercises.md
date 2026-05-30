# Exercises — Lecture 13: LLM Limitations and Evaluation Rigor in Finance

## Exercise 1 [B]
**Topic:** Calibration and Overconfidence

A financial analyst uses an LLM to generate probability estimates for whether a bond will default within one year. The model assigns 90% confidence to 100 bonds; in reality, only 60 of those bonds default. Explain what this pattern reveals about the model's calibration. Define Expected Calibration Error (ECE) in your own words and describe how a reliability diagram would look for this model. What practical steps could the analyst take to improve calibration before deploying the model in a credit risk workflow?

## Exercise 2 [I]
**Topic:** Stock Movement Prediction and Evaluation Beyond Classification Accuracy

Using the Yahoo Finance API (or a provided dataset of daily closing prices for 50 S\&P 500 stocks), implement the following evaluation pipeline:

1. Compute a naive baseline that predicts the next-day direction as the majority class in the training window.
2. Implement a simple ARIMA(1,1,0) model and record its directional accuracy.
3. Simulate a long-short strategy based on ARIMA predictions and compute the annualized Sharpe ratio assuming round-trip transaction costs of 10 basis points per trade.
4. Compare directional accuracy against Sharpe ratio as evaluation metrics. Discuss in 2--3 sentences why a model with higher accuracy may yield a lower Sharpe ratio.

Submit your code and a table summarizing results across the 50 stocks.

## Exercise 3 [A]
**Topic:** Hallucination in Financial Contexts

Design a hallucination benchmark for financial LLMs. Your benchmark should:

1. Define at least three categories of financial hallucination (e.g., fabricated regulatory citations, incorrect earnings figures, phantom merger announcements).
2. Propose a data collection methodology that sources ground-truth facts from authoritative financial databases (SEC EDGAR, Bloomberg, Compustat).
3. Describe how you would score model outputs automatically and what human-review protocols would complement automated scoring.
4. Discuss the trade-off between benchmark contamination risk (the model may have seen the facts during pretraining) and the feasibility of using truly novel facts.

Write a 600--900 word report outlining the benchmark design, and include a sample of five test items with expected answers.
