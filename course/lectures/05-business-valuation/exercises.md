# Exercises — Lecture 5: LLMs for Business Valuation

---

## Exercise 1 [B] — EDGAR Extraction with the SEC API

Using the SEC EDGAR full-text search API (`https://efts.sec.gov/LATEST/search-index?q=...`), write a Python function that:

1. Retrieves the most recent 10-K filing for a given company ticker (e.g., `AAPL`).
2. Extracts the income statement table as a pandas DataFrame using an LLM call (you may use the OpenAI or Anthropic API).
3. Returns the DataFrame with columns: `Year`, `Revenue`, `Operating_Income`, `Net_Income`.

**Hints:** Use the `requests` library to fetch filing index pages. Pass the raw HTML table text to the LLM and ask it to output structured JSON.

---

## Exercise 2 [I] — Forecasting Free Cash Flow with Chain-of-Thought Prompting

Given historical FCF figures for a company (provided as a CSV), design a chain-of-thought prompt that asks an LLM to:

1. Identify the trend and key drivers behind FCF growth.
2. Project FCF for the next 5 years under a base-case assumption.
3. Justify each projection year with a one-sentence rationale.

Then implement a terminal value calculation (Gordon Growth Model) and compute the enterprise value, using the LLM-generated projections as inputs. Compare your LLM-based estimate to a naive linear extrapolation.

**Deliverable:** A Jupyter notebook with both the prompt design and the valuation computation.

---

## Exercise 3 [A] — Embedding-Based Comparable Selection and Valuation

Build a comparable company selection system using financial statement embeddings:

1. Download 10-K filings for 50 S&P 500 companies using the EDGAR pipeline from Exercise 1.
2. Embed the Management Discussion & Analysis (MD&A) section of each filing using a sentence-transformer model.
3. Given a target company, retrieve the top-5 most similar companies by cosine similarity.
4. Apply a trading multiples valuation (EV/EBITDA) using the selected comparables and compare against the DCF estimate from Exercise 2.
5. Critically evaluate: do embedding-selected peers produce tighter or wider valuation ranges than sector-based peers? Provide statistical evidence.

**Deliverable:** A report (≤ 4 pages) with methodology, results, and a discussion of LLM/embedding limitations in comparable selection.
