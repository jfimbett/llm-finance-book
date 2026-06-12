# Hallucination Audit Report — Chapter 05: LLMs for Business Valuation

**Verdict:** HALLUCINATIONS FOUND (4 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 5.7, benchmarking paragraph ("Preliminary evidence from internal experiments...")
- **Quoted text:** "LLM-assisted extraction achieves coverage rates above 90% for S&P 500 constituents and above 75% for Russell 2000 companies, with MAVE broadly comparable to the spread between analyst price targets and realised prices (typically 20--40\% on an annualised basis)"
- **Why flagged:** Three precise numeric claims (90%, 75%, 20–40%) attributed to "internal experiments and published literature," but the sole `\cite{zhang2024financebench}` following the sentence cites a financial QA benchmark that does not report EDGAR coverage rates or MAVE statistics for valuation pipelines. The coverage-rate figures are particularly suspect as round numbers from uncredited "internal experiments."
- **Severity:** HIGH
- **Recommended action:** Provide a verifiable citation for the coverage-rate figures, replace with a citation to an actual extraction pipeline paper, or reframe as explicitly illustrative.

**Finding 2**
- **Location:** Section 5.7, cost paragraph
- **Quoted text:** "the cost per company is in the range \$0.50--\$3.00. At scale---a universe of 3{,}000 companies refreshed quarterly---the budget is thus \$6{,}000--\$36{,}000 per quarter"
- **Why flagged:** Specific dollar ranges for "typical 2024 frontier-model pricing" without any citation or footnote. API pricing changes frequently. Additionally, the arithmetic appears inconsistent: 3,000 × $0.50–$3.00 = $1,500–$9,000, not $6,000–$36,000. (Note for math-checker agent: arithmetic error present.)
- **Severity:** MEDIUM
- **Recommended action:** Add a footnote with a specific pricing reference and access date, or reframe as an illustrative back-of-envelope calculation.

**Finding 3**
- **Location:** Section 5.7, latency paragraph
- **Quoted text:** "Each LLM call introduces 1--5 seconds of network and inference latency... end-to-end latency per company can be reduced to 15--30 seconds."
- **Why flagged:** Specific latency figures without any citation. Architecture- and provider-dependent and subject to rapid change.
- **Severity:** LOW
- **Recommended action:** Reframe as "on the order of seconds" and cite a specific benchmark or technical report, or label as illustrative.

---

### H4 — Synthetic Real-World Examples

**Finding 4**
- **Location:** Figure caption (fig:ch05-illustration)
- **Quoted text:** "DCF sensitivity heatmap for Apple Inc.\ (AAPL)... evaluated at the most recently reported free cash flow."
- **Why flagged:** Caption names Apple Inc. (AAPL) as the subject of a DCF analysis using "the most recently reported free cash flow" with no date or citation to a specific filing. The displayed values will change with every filing and cannot be verified by a reader without knowing the source date. (Note: the companion notebook correctly fetches live data via `yfinance` with a labeled fallback — the problem is specific to the figure caption.)
- **Severity:** MEDIUM
- **Recommended action:** Amend caption to state the fiscal year and FCF value used, add a `\cite{}` to the relevant EDGAR filing, or add a parenthetical "(illustrative; values depend on the FCF and date used)."

---

## Code Hallucinations

No code hallucinations detected. The notebook uses live `yfinance` data with labeled fallbacks that explicitly acknowledge their approximate nature. No hardcoded arrays presented as verified historical data.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1 | Sec 5.7, benchmarking paragraph — coverage rates (90%, 75%) from "internal experiments" | HIGH |
| 2 | H1 | Sec 5.7, cost paragraph — \$0.50–\$3.00/company without citation | MEDIUM |
| 3 | H1 | Sec 5.7, latency paragraph — 1–5 sec / 15–30 sec figures | LOW |
| 4 | H4 | Figure caption `fig:ch05-illustration` — AAPL FCF with no date or filing citation | MEDIUM |
