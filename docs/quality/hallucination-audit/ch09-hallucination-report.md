# Hallucination Audit Report — Chapter 09: Financial NLP and Sentiment Analysis

**Verdict:** HALLUCINATIONS FOUND (6 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 9.5.2, batch inference paragraph
- **Quoted text:** "For a FinBERT-scale model (110M parameters) processing 512-token documents on a single A100 GPU, throughput is approximately 500--1,000 documents per second. For a 10M-document archive this implies 3--6 hours of GPU time per full pass."
- **Why flagged:** Precise hardware-performance claim (throughput range, GPU model, implied wall-clock time) with no `\cite{}`. GPU throughput figures are highly version- and configuration-dependent.
- **Severity:** MEDIUM
- **Recommended action:** Add citation to a benchmark paper or technical report, or soften to "on the order of hundreds of documents per second."

**Finding 2**
- **Location:** Section 9.5.2, streaming inference paragraph
- **Quoted text:** "the \texttt{onnxruntime} library with quantised model weights can achieve single-sentence latencies of 5--10 milliseconds on modern CPUs"
- **Why flagged:** Precise latency claim (5–10 ms) tied to a specific library and hardware class with no `\cite{}`. Implies a measured result.
- **Severity:** MEDIUM
- **Recommended action:** Add citation or rephrase as illustrative order-of-magnitude ("on the order of tens of milliseconds").

**Finding 3**
- **Location:** Example 9.2, final paragraph
- **Quoted text:** "A model trained this way consistently achieves macro-averaged F1 of 0.72--0.78 on held-out earnings call sentences, compared with 0.60--0.65 for the LM lexicon on the same data"
- **Why flagged:** Precise performance benchmarks stated as reliably reproducible ("consistently achieves") within an example framed as a practitioner workflow (not purely illustrative). No `\cite{}`.
- **Severity:** MEDIUM
- **Recommended action:** Cite a paper reporting these figures, or reframe: "In our experience, models of this type achieve macro F1 in the range 0.70–0.80 (illustrative; results will vary by corpus)."

**Finding 4**
- **Location:** Section 9.5.3, class balance paragraph
- **Quoted text:** "the 'neutral' class often comprises 50--60\% of financial sentences"
- **Why flagged:** Precise distributional claim without a `\cite{}`. The specificity (50–60%) implies a measurement across datasets that is not sourced.
- **Severity:** MEDIUM
- **Recommended action:** Add citation (e.g., to Malo et al. 2014 or another labelled financial sentiment dataset), or soften to "often the majority class."

**Finding 5**
- **Location:** Definition 9.3 (Fog Index), following sentence
- **Quoted text:** "10-K MD\&A sections typically score between 18 and 22."
- **Why flagged:** Precise empirical claim about the distribution of Fog Index scores in actual MD&A sections, stated without a `\cite{}`. `\citet{li2008annual}` and `\citet{lehavy2011benefit}` are cited nearby for related claims, making the absence here notable.
- **Severity:** MEDIUM
- **Recommended action:** Add citation (e.g., `\citet{li2008annual}` or a readability study that reports these values directly).

**Finding 6**
- **Location:** Section 9.1.2, Deduplication paragraph
- **Quoted text:** "A common threshold in practice is to mark as duplicates any two documents whose Jaccard similarity of character trigrams exceeds 0.7"
- **Why flagged:** A precise methodological standard ("0.7 threshold", "character trigrams") presented as established practice with no `\cite{}`. The phrasing "common threshold in practice" implies a documented convention rather than an illustrative example.
- **Severity:** LOW
- **Recommended action:** Cite a reference documenting this threshold, or reframe: "Practitioners commonly choose a threshold in the range 0.6–0.8 (the exact value is corpus-dependent)."

---

## Code Hallucinations

No code hallucinations detected. The notebook contains only a markdown header cell and a single stub cell (`# Your code here`). No executable code to audit.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1 | Sec 9.5.2, batch inference throughput (500–1,000 docs/s) | MEDIUM |
| 2 | H1 | Sec 9.5.2, ONNX latency (5–10 ms on modern CPUs) | MEDIUM |
| 3 | H1 | Example 9.2, F1 performance claim (0.72–0.78 vs 0.60–0.65) | MEDIUM |
| 4 | H1 | Sec 9.5.3, neutral class prevalence (50–60%) | MEDIUM |
| 5 | H1 | Definition 9.3, MD&A Fog Index range (18–22) | MEDIUM |
| 6 | H1 | Sec 9.1.2, Jaccard 0.7 deduplication threshold | LOW |
