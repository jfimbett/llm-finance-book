# Hallucination Audit Report — Chapter 13: LLM Limitations and Rigorous Evaluation in Finance

**Verdict:** HALLUCINATIONS FOUND (5 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 13.3.2, meta-analysis paragraph
- **Quoted text:** "A meta-analysis of 84 empirical studies \cite{zhao2025frontiers} finds that the 59% average accuracy figure is ubiquitous across different LLMs, different markets, and different time periods."
- **Why flagged:** The "84 empirical studies" count is a precise numeric detail that is highly characteristic of a hallucinated number appended to what may be a real citation. The surrounding 59% average figure is cited to `\cite{xu2024stock}` which appears plausible, but the specific meta-analysis count of 84 must be verified against the actual paper.
- **Severity:** MEDIUM
- **Recommended action:** Verify that `zhao2025frontiers` is a real meta-analysis and that 84 is the actual study count. If unverifiable, remove the count or replace with the verified figure.

**Finding 2**
- **Location:** Sections 13.4.1 and 13.4.3
- **Quoted text:** "find that GPT-4 class models answer incorrectly 15--30\% of the time on precise numerical questions" (attributed to `\cite{kang2023hallucination}`)
- **Why flagged:** `kang2023hallucination` is an unusual citation key; no widely-cited 2023 paper by "Kang" on LLM hallucination in finance is a standard reference. The paper is cited three times with specific claims about a "dedicated benchmark of numerical queries from public filings." If this citation is fabricated, both the citation and the 15–30% statistics are phantom.
- **Severity:** HIGH
- **Recommended action:** Confirm `kang2023hallucination` resolves to a real published paper. If it does not resolve, this becomes a combined phantom-citation + phantom-statistic finding requiring removal or replacement.

---

### H2 — Fabricated Benchmarks

**Finding 3**
- **Location:** Section 13.4.3, FinanceBench paragraph
- **Quoted text:** "the benchmark's analysis reports that models hallucinate or compute incorrectly on 20--40\% of multi-step numerical questions" (attributed to FinanceBench, `\cite{zhang2024financebench}`)
- **Why flagged:** FinanceBench is a real benchmark. However, the specific "20–40%" range is suspiciously wide (a 20-percentage-point spread) and the phrasing "hallucinate or compute incorrectly" conflates two different error types. The range should be verifiable from the cited paper's tables; if the figure is not in that paper, it is a phantom statistic attached to a real benchmark name.
- **Severity:** MEDIUM
- **Recommended action:** Verify the exact figure from `zhang2024financebench` and replace with the actual reported number or add a page/table citation.

---

### H3 — Invented Regulatory / Legal Claims

**Finding 4**
- **Location:** Section 13.1.3, calibration remark
- **Quoted text:** "Financial practitioners should re-estimate calibration parameters at least quarterly, treating them as part of the model monitoring workflow mandated by SR~11-7 guidance \cite{sr117}."
- **Why flagged:** SR 11-7 is a real 2011 Federal Reserve guidance document. However, SR 11-7 does not specifically mandate quarterly recalibration of LLM confidence scores — it predates LLMs by over a decade. The phrase "mandated by SR 11-7" overstates what the guidance requires, fabricating a specific obligation that does not exist in SR 11-7's text.
- **Severity:** MEDIUM
- **Recommended action:** Soften to "consistent with the model monitoring principles in SR 11-7 guidance" or "in the spirit of SR 11-7's model validation requirements."

---

### H6 — Undated "Recent" Claims

**Finding 5**
- **Location:** Section 13.3.1, efficient markets paragraph
- **Quoted text:** "The alpha from simple text-based signals has declined significantly as these strategies became more widely known and deployed."
- **Why flagged:** "Has declined significantly" is a precise directional claim about alpha decay with no citation and no date range. Stated with empirical confidence implying a specific study or measurement that is not provided.
- **Severity:** LOW
- **Recommended action:** Add citation (e.g., to academic work on NLP alpha decay), or reframe as "many practitioners believe the alpha from simple text-based signals has declined."

---

## Code Hallucinations

No code hallucinations detected. The notebook contains only a markdown header cell and a single stub cell (`# Your code here`).

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1 | Sec 13.3.2, "84 empirical studies" count in meta-analysis | MEDIUM |
| 2 | H1+H5 | Sec 13.4.1 & 13.4.3, `kang2023hallucination` — 15–30% figure, citation unverified | HIGH |
| 3 | H2 | Sec 13.4.3, FinanceBench 20–40% hallucination rate | MEDIUM |
| 4 | H3 | Sec 13.1.3, SR 11-7 "mandated" quarterly recalibration | MEDIUM |
| 5 | H6 | Sec 13.3.1, "alpha has declined significantly" (uncited) | LOW |
