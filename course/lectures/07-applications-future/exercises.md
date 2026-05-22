# Exercises — Lecture 7: Other Applications in Finance and Future Trends

---

## Exercise 1 [B] — Automating an Earnings Call Pipeline

Using an LLM API of your choice, build a simple three-step automated workflow that:

1. Accepts the plain-text transcript of an earnings call as input.
2. Extracts the five most important management statements about future guidance (revenue outlook, margin targets, capex plans, headcount, key risks) and returns them as a structured JSON object.
3. Generates a one-paragraph analyst summary suitable for inclusion in a morning briefing note.

Test your pipeline on a publicly available earnings call transcript (e.g., from Seeking Alpha or the SEC EDGAR 8-K search). Report the total token usage and wall-clock time.

---

## Exercise 2 [I] — RAG Research Assistant with Bias Audit

Build a retrieval-augmented generation (RAG) research assistant over a corpus of 10-K filings:

1. Download 10-K filings for 20 companies spanning at least three GICS sectors using the EDGAR pipeline from Chapter 5.
2. Chunk and embed the MD&A sections using a sentence-transformer model; store vectors in a FAISS index.
3. Implement a query interface: given a natural-language question (e.g., "Which companies cite climate risk as a material factor?"), retrieve the top-5 relevant passages and synthesise an answer.
4. **Bias audit**: run the same query for companies from two different GICS sectors (e.g., Energy vs. Technology). Does the assistant show asymmetric retrieval or answer quality? Quantify using cosine similarity distributions of retrieved passages.

**Deliverable:** Jupyter notebook with the full pipeline and a one-page bias audit report.

---

## Exercise 3 [A] — Model Risk Management Documentation for an LLM System

You are the model risk manager at a mid-size asset management firm. The quant team has built an LLM-assisted earnings-forecast system (similar to Chapter 5 but for EPS rather than FCF). Prepare a Model Risk Management (MRM) document following the SR 11-7 framework that:

1. Describes the model purpose, intended use, and limitations.
2. Identifies at least four material risks (e.g., hallucination, data staleness, distributional shift, adversarial inputs) and maps them to mitigations.
3. Proposes a backtesting protocol: specify the benchmark, time window, performance metrics, and pass/fail thresholds.
4. Defines an ongoing monitoring plan: what metrics are tracked in production, at what frequency, and what triggers a model review?

**Deliverable:** A 3–5 page MRM document in the style of a regulatory submission.
