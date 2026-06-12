# Hallucination Audit Report — Chapter 02: Large Language Models: Architecture and Practice

**Verdict:** HALLUCINATIONS FOUND (5 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 2.3 (The Transformer Architecture), opening paragraph
- **Quoted text:** "Published at NeurIPS 2017, it has since accumulated more than 100,000 citations"
- **Why flagged:** A precise citation count asserted as established fact with no `\cite{}`. Citation counts for living papers are dynamic; the specific 100,000 threshold cannot be verified from any citable source.
- **Severity:** LOW
- **Recommended action:** Replace with qualitative characterisation ("one of the most cited papers in computer science") or add a source with an access date.

**Finding 2**
- **Location:** Section 2.4 (The Modern LLM Landscape), opening paragraph
- **Quoted text:** "Within sixty days it had a hundred million users---the fastest consumer adoption of any product in history."
- **Why flagged:** Two uncited precision claims: (a) "sixty days" to reach 100M users, and (b) "the fastest consumer adoption of any product in history." No `\cite{}` key. The superlative "fastest in history" is an extraordinary claim requiring a citable source.
- **Severity:** MEDIUM
- **Recommended action:** Add citation to the Reuters/UBS study (January 2023), or soften to "reportedly reached a hundred million users in approximately two months, making it one of the fastest-growing consumer applications on record \cite{source}."

**Finding 3**
- **Location:** Section 2.6 (Working with LLMs via API), cost/latency bullet points
- **Quoted text:** "Time-to-first-token for GPT-4o is typically 1--3 seconds; for Claude 3 Haiku under 500 ms. Locally-hosted Llama 3 (8B, single A100 GPU) can achieve sub-100 ms first-token latency."
- **Why flagged:** Three specific latency benchmarks stated as engineering facts without any `\cite{}` or date qualifier. Latency figures are highly environment-dependent.
- **Severity:** MEDIUM
- **Recommended action:** Add a citation to a benchmark source, add a date qualifier, or soften to indicative ranges.

**Finding 4**
- **Location:** Section 2.6 (Working with LLMs via API), cost/latency bullet points
- **Quoted text:** "This can reduce total API cost by 80--95\% on typical workloads."
- **Why flagged:** Precise percentage range ("80–95%") on "typical workloads" with no `\cite{}`. "Typical workloads" is too vague to be independently verifiable.
- **Severity:** MEDIUM
- **Recommended action:** Cite a source for this range, or soften to "can reduce API costs substantially."

---

### H3 — Invented Regulatory / Legal Claims

**Finding 5**
- **Location:** Section 2.8 (Limitations and Responsible Use), Regulatory and Ethical Considerations
- **Quoted text:** "AI systems used for credit scoring, insurance risk assessment, pricing of life insurance products, and AI-assisted securities pricing fall into the high-risk category (Annex III)."
- **Why flagged:** EU AI Act Annex III does not explicitly classify "AI-assisted securities pricing" as high-risk. Annex III covers biometric identification, critical infrastructure, education, employment, essential services, law enforcement, migration, administration of justice, and democratic processes. The `\citep{euaiact2024}` citation is present but the specific Annex III attribution to securities pricing appears to be a hallucinated precision detail overextending the cited regulation.
- **Severity:** HIGH
- **Recommended action:** Verify the exact Annex III categories against the published regulation text and correct or remove the "AI-assisted securities pricing" characterisation. Replace with accurately cited language from Annex III.

---

## Code Hallucinations

No code hallucinations detected. The notebook implements a sinusoidal positional encoding visualisation using `numpy` and `matplotlib`. All imports are real PyPI packages. No hardcoded financial data, no phantom file paths.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1 | Sec 2.3, "100,000 citations" claim | LOW |
| 2 | H1 | Sec 2.4, "sixty days / fastest in history" | MEDIUM |
| 3 | H1 | Sec 2.6, latency benchmarks (GPT-4o, Haiku, Llama 3) | MEDIUM |
| 4 | H1 | Sec 2.6, "80–95% cost reduction on typical workloads" | MEDIUM |
| 5 | H3 | Sec 2.8, Annex III attribution for "AI-assisted securities pricing" | HIGH |
