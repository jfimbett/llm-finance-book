# Hallucination Audit Report — Chapter 14: Financial Text Summarization and Information Extraction

**Verdict:** HALLUCINATIONS FOUND (4 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 14.3.2, Example `ex:earnings-gpt4`
- **Quoted text:** "Evaluation on a set of 100 earnings releases, scored by a financial analyst against ground truth, finds that the constrained prompt reduces number errors by approximately 40% relative to an unconstrained paraphrase prompt. However, the approach does not eliminate hallucination entirely: in roughly 8% of cases the model paraphrases a nuanced forward guidance statement in a way that changes its meaning."
- **Why flagged:** Two precise uncited numeric claims ("reduces number errors by ~40%", "roughly 8% of cases") attributed to "a set of 100 earnings releases." No `\cite{}`. The example block is labelled only as "Earnings Report Summarization with GPT-4," not as hypothetical. The specificity of sample size (100), error-reduction magnitude (40%), and failure rate (8%) implies a real study that is not cited.
- **Severity:** HIGH
- **Recommended action:** Add citation to the source, or reframe as explicitly illustrative: "In a hypothetical evaluation… suppose the constrained prompt reduced number errors by roughly 40%, with approximately 8% of cases showing paraphrase errors."

---

### H4 — Synthetic Real-World Examples

**Finding 2**
- **Location:** Section 14.1.2, Example `ex:entities-earnings-call`
- **Quoted text:** "In Q3 2023, **Microsoft** reported revenue of **\$56.5 billion**, representing a **13%** increase year-over-year. **CEO Satya Nadella** noted that **Azure** cloud revenue grew **29%**, driven by enterprise adoption of **Copilot** products."
- **Why flagged:** Verbatim-style attribution to a real company (Microsoft), real named executive (Satya Nadella), and real products (Azure, Copilot) with specific financial figures. No `\cite{}` key. These figures are close to Microsoft's actual Q3 FY2023 reported numbers, but without citation they cannot be confirmed and could be misremembered. The example is inside `\begin{example}` but presents itself as factual transcript content, not as illustrative.
- **Severity:** HIGH
- **Recommended action:** Add citation to the actual earnings call transcript or SEC filing, or replace the real company with a generic stand-in and adjust figures accordingly.

**Finding 3**
- **Location:** Section 14.3.2, consistency discussion paragraph
- **Quoted text:** "If an abstractive model summarises an earnings call as reporting 'revenue of \$57 billion' when the actual figure was \$56.5 billion…"
- **Why flagged:** Reuses the specific Microsoft-sized figure from Finding 2 as a concrete "actual figure" without being framed as purely hypothetical. Compounds the ambiguity of Finding 2.
- **Severity:** MEDIUM
- **Recommended action:** If Finding 2 is reframed as generic, update this figure to match. If kept, label explicitly as illustrative.

---

### H6 — Undated "Recent" Claims

**Finding 4**
- **Location:** Section 14.3.4, long-document processing paragraph
- **Quoted text:** "…more recently, commercial models with 128K or 1M token contexts---can process an entire S-1 in a single forward pass."
- **Why flagged:** "More recently" is an undated temporal claim. The 1M-token context figure is stated without an explicit date or citation. Context window sizes are rapidly evolving.
- **Severity:** LOW
- **Recommended action:** Add explicit date anchor ("as of 2024") or citation to specific model(s) (e.g., Gemini 1.5 Pro's 1M-token context), or reframe as "at the time of writing, models with extended context windows up to 1M tokens."

---

## Code Hallucinations

No code hallucinations detected. The notebook contains only a markdown cell and a single stub cell (`# Your code here`).

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1 | Sec 14.3.2, Example `ex:earnings-gpt4` — "~40% error reduction", "~8% of cases" | HIGH |
| 2 | H4 | Sec 14.1.2, Example `ex:entities-earnings-call` — Microsoft/Satya Nadella/Azure figures, uncited | HIGH |
| 3 | H4 | Sec 14.3.2, "\$56.5 billion actual figure" reuse | MEDIUM |
| 4 | H6 | Sec 14.3.4, "more recently, commercial models with 128K or 1M token contexts" | LOW |
