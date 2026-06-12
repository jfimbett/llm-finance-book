# Hallucination Audit Report — Chapter 10: Portfolio Optimization and Quantitative Trading with LLMs

**Verdict:** HALLUCINATIONS FOUND (2 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 10.3.2, paragraph beginning "In simulations based on the FinRL framework..."
- **Quoted text:** "In simulations based on the FinRL framework \citep{liu2022finrl}, adding news-alert features reduces implementation shortfall by approximately 8--12\% relative to a baseline RL agent without text augmentation"
- **Why flagged:** The `\citep{liu2022finrl}` citation identifies the software framework, not a paper reporting this specific simulation result. The 8–12% figure is a precise quantitative performance claim with no cited source for the actual experiment. The hedging language does not resolve the missing attribution — it signals the authors ran this simulation themselves, but the result is neither self-contained (simulation details not given) nor cited to an external source.
- **Severity:** MEDIUM
- **Recommended action:** (a) Cite a specific paper reporting this 8–12% result, (b) replace with "in our own simulations using the FinRL framework, described in the companion notebook, we find..." and provide the simulation code, or (c) reframe as qualitative: "can meaningfully reduce implementation shortfall."

**Finding 2**
- **Location:** Section 10.3.1, transaction costs paragraph
- **Quoted text:** "For US large-cap equities, this is on the order of 1--3 basis points per trade; for small-caps, 10--50 basis points is common."
- **Why flagged:** Both figures are stated without a `\cite{}`. While the large-cap figure is a well-known stylized fact, the small-cap range (10–50 bp) spans an order of magnitude and implies specific empirical grounding. When paired in an uncited sentence, the small-cap range reads as an implied empirical finding.
- **Severity:** LOW
- **Recommended action:** Add citation (e.g., `\citet{grinold2000active}` or a microstructure study) or reframe as "commonly in the range of single-digit basis points for large-caps and tens of basis points for small-caps (see, e.g., \citet{grinold2000active})."

---

## Code Hallucinations

No code hallucinations detected. The companion notebook contains only a markdown header cell and a single stub cell (`# Your code here`).

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1 | Sec 10.3.2, FinRL simulation — 8–12% implementation shortfall reduction | MEDIUM |
| 2 | H1 | Sec 10.3.1, bid-ask spread figures (large-cap/small-cap equities) | LOW |
