# Hallucination Audit Report — Chapter 07: Other Applications in Finance and Future Trends

**Verdict:** HALLUCINATIONS FOUND (4 text, 1 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 7.1.3, "Choosing the Right LLM Architecture" paragraph
- **Quoted text:** "the FinanceBench benchmark \cite{zhang2024financebench} shows that frontier models answer approximately 80% of financial QA questions correctly on the first attempt"
- **Why flagged:** The 80% figure is cited to `\cite{zhang2024financebench}`, but FinanceBench is also referenced elsewhere in the chapter under a different citation key (`\citep{xie2023pixiu}`, labelled as "FinBench survey"). The text conflates two distinct benchmarks under one citation key. If `zhang2024financebench` is FinanceBench (a QA benchmark), the 80% figure needs verification against the actual paper; the citation-key inconsistency must also be resolved.
- **Severity:** MEDIUM
- **Recommended action:** Verify that `zhang2024financebench` resolves to the FinanceBench paper and that 80% matches its reported figures. Ensure the two citation keys refer to distinct papers.

**Finding 2**
- **Location:** Section 7.3.4, "Deploying and Maintaining a Production Research Assistant" paragraph
- **Quoted text:** "\citet{BaloghDidisheim2025} demonstrate that LLM predictive accuracy in financial tasks follows an inverted U-shaped pattern as a function of context length"
- **Why flagged:** `\citet{}` key is present, so the citation is not absent. However, the additional claim about the "cognitive limitations" framing and the specific inverted-U result is a distinctive enough finding that the citation should be verified as a real working paper before publication. If BaloghDidisheim2025 is fabricated, this becomes a HIGH finding.
- **Severity:** MEDIUM
- **Recommended action:** Verify `BaloghDidisheim2025` is a real working paper with these specific findings. Flag for bibliography verification.

---

### H3 — Invented Regulatory / Legal Claims

**Finding 3**
- **Location:** Section 7.4.3, GDPR paragraph
- **Quoted text:** "GDPR Article 22 provides individuals with the right not to be subject to a decision based solely on automated processing... Articles 13 and 14 further require that individuals be informed at data collection time..."
- **Why flagged:** Specific article numbers (22, 13, 14) described without any `\cite{}` key on any GDPR claim. The substance appears correct (these are standard GDPR provisions), but the chapter applies no regulatory citation style at all for GDPR references.
- **Severity:** LOW
- **Recommended action:** Add `\cite{gdpr2016}` (Regulation (EU) 2016/679) to accompany GDPR article references throughout the chapter.

**Finding 4**
- **Location:** Section 7.4.3, MiFID II record-keeping paragraph
- **Quoted text:** "the prompt, the model version, the output, and the time of generation" must be logged under MiFID II for LLM-generated outputs.
- **Why flagged:** The enumeration of LLM-specific fields (prompt, model version, output, timestamp) as a MiFID II record-keeping requirement is stated as settled law with no `\cite{}`. MiFID II imposes communications record-keeping obligations, but the LLM-specific enumerated fields are an interpretive extrapolation, not explicit statutory text.
- **Severity:** MEDIUM
- **Recommended action:** Add a citation to MiFID II (Directive 2014/65/EU, Article 16) and soften the LLM-specific enumeration to "in the view of practitioners" or "consistent with MiFID II record-keeping obligations."

---

## Code Hallucinations

### C1 — Synthetic Real-Data Arrays

**Finding 5**
- **Location:** `exercises.ipynb`, illustration cell (benchmark data dict)
- **Code fragment:**
  ```python
  models = {
      "BERT-base":     [0.11, 0.73, 0.64],
      "FinBERT":       [0.13, 0.87, 0.76],
      "GPT-3.5":       [0.52, 0.78, 0.79],
      "GPT-4":         [0.68, 0.83, 0.84],
      "BloombergGPT":  [0.23, 0.85, 0.75],
  }
  ```
  The comment cites "Chen et al. 2021 (FinQA); Shah et al. 2022 (FPB); Xie et al. 2023 (FinBench survey); original model papers."
- **Why flagged:** Two specific values are not straightforwardly traceable from the stated sources: **GPT-4 on FinQA: 0.68** — GPT-4's FinQA score is not reported in the OpenAI technical report ("original model papers"); source is unclear. **BloombergGPT on FPB: 0.85** — the Wu et al. (2023) BloombergGPT paper reports FPB accuracy of 0.511 on its primary metric; 0.85 is substantially higher and difficult to reconcile with the cited paper. The disclaimer ("hardcoded from published papers") is present but source traceability is incomplete.
- **Severity:** MEDIUM
- **Recommended action:** Add line-level source attribution for each cell value (e.g., "GPT-4 FinQA: 0.68 (source: [paper/table])"). Replace any value that cannot be traced to a specific paper and table with the verified figure or remove it.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1 | Sec 7.1.3, FinanceBench 80% claim / citation-key inconsistency | MEDIUM |
| 2 | H1 | Sec 7.3.4, BaloghDidisheim2025 inverted-U context length finding | MEDIUM |
| 3 | H3 | Sec 7.4.3, GDPR Articles 22/13/14 — no `\cite{}` | LOW |
| 4 | H3 | Sec 7.4.3, MiFID II LLM-specific logging fields as settled law | MEDIUM |
| 5 | C1 | Notebook illustration cell — GPT-4 FinQA 0.68 and BloombergGPT FPB 0.85 unverifiable from stated sources | MEDIUM |
