# Exercises — Lecture 13: LLM Limitations and Evaluation Rigor in Finance

## Exercise 1 [B]
**Topic:** Calibration and Overconfidence

A financial analyst uses an LLM to generate probability estimates for whether a bond will default within one year. The model assigns 90% confidence to 100 bonds; in reality, only 60 of those bonds default. Explain what this pattern reveals about the model's calibration. Define Expected Calibration Error (ECE) in your own words and describe how a reliability diagram would look for this model. What practical steps could the analyst take to improve calibration before deploying the model in a credit risk workflow?

## Exercise 2 [I]
**Topic:** Evaluating an LLM Direction Predictor Beyond Classification Accuracy

You are given a dataset of daily news headlines for 50 S\&P 500 stocks together with their realized next-day return signs. The focus of this exercise is *evaluation rigor* applied to an LLM predictor — not the finance.

1. Prompt an LLM (zero-shot or few-shot) to read each day's headlines for a stock and emit a structured next-day direction prediction (`up`/`down`) **with a confidence score**, using constrained/structured decoding so the output is machine-readable. Compare its directional accuracy against a naive majority-class baseline.
2. Build a **reliability diagram** for the LLM's confidence scores and compute the **Expected Calibration Error** — are the stated confidences trustworthy, or systematically over-confident?
3. Simulate a long-short strategy that sizes positions by the LLM's confidence and compute the annualized Sharpe ratio, net of round-trip transaction costs of 10 basis points per trade.
4. Compare accuracy vs. Sharpe as evaluation metrics (2--3 sentences on why a higher-accuracy model can yield a *lower* Sharpe). Then explain why **temporal leakage** — the LLM having encountered these headlines or their outcomes during pre-training — is a first-order threat that would invalidate the result, and describe one safeguard.

Submit your code and a table summarizing accuracy, ECE, and net Sharpe across the 50 stocks.

## Exercise 3 [A]
**Topic:** Hallucination in Financial Contexts

Design a hallucination benchmark for financial LLMs. Your benchmark should:

1. Define at least three categories of financial hallucination (e.g., fabricated regulatory citations, incorrect earnings figures, phantom merger announcements).
2. Propose a data collection methodology that sources ground-truth facts from authoritative financial databases (SEC EDGAR, Bloomberg, Compustat).
3. Describe how you would score model outputs automatically and what human-review protocols would complement automated scoring.
4. Discuss the trade-off between benchmark contamination risk (the model may have seen the facts during pretraining) and the feasibility of using truly novel facts.

Write a 600--900 word report outlining the benchmark design, and include a sample of five test items with expected answers.
