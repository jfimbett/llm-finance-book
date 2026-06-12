# Hallucination Audit Report — Chapter 03: Training and Fine-Tuning Large Language Models

**Verdict:** HALLUCINATIONS FOUND (6 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 3.3, FinBERT task results paragraph
- **Quoted text:** "Financial sentiment analysis: accuracy 88.5% (FinBERT) vs 80.7% (BERT). ESG category classification: macro-F1 78.3% vs 71.2%. Forward-looking statement detection: F1 91.3% vs 85.6%."
- **Why flagged:** Cited to `\citet{yang2020finbert}`, but the ESG classification and forward-looking statement detection tasks with those specific figures are not standard Yang et al. (2020) results. The original FinBERT paper focused on financial sentiment (FPB, FiQA, analyst-tone tasks), not ESG classification. The three-task framing with those numbers structurally resembles a synthesised result set invented to illustrate a point.
- **Severity:** HIGH
- **Recommended action:** Verify these three numbers against the actual Yang et al. (2020) paper. Replace with only results that appear verbatim in the cited paper. Add separate `\cite{}` keys for any other task-specific results.

**Finding 2**
- **Location:** Section 3.4, FinQA SOTA claim
- **Quoted text:** "Current state-of-the-art models achieve roughly 75% execution accuracy... compared with human accuracy of 91%."
- **Why flagged:** Precise current SOTA figure and human-performance ceiling with no `\cite{}`. SOTA figures become stale quickly; an undated claim with no citation cannot be verified.
- **Severity:** MEDIUM
- **Recommended action:** Add citation to the paper reporting 75% SOTA and 91% human accuracy (likely Chen et al. 2021 FinQA paper).

**Finding 3**
- **Location:** Section 3.3, BloombergGPT benchmarks paragraph
- **Quoted text:** "BloombergGPT outperforms GPT-NeoX-20B... by 10--20% on average"
- **Why flagged:** A specific performance-gap range without a `\cite{}` in this sentence. The claim reads as an editorial summary of the cited paper rather than a directly quoted result.
- **Severity:** LOW
- **Recommended action:** Add a parenthetical `\citep{wu2023bloomberggpt}` after this claim to make attribution unambiguous.

---

### H4 — Synthetic Real-World Examples

**Finding 4**
- **Location:** Example 3.7 (Two-stage adaptation for earnings sentiment)
- **Quoted text:** "On the held-out Financial PhraseBank test set, the two-stage approach achieves accuracy 94.2% versus 88.7% for Stage 2 fine-tuning alone and 79.3% for zero-shot prompting"
- **Why flagged:** Three precise performance figures for a specific configuration (LLaMA-2 7B, two-stage LoRA, FPB test set) with no `\cite{}`. The example is framed as illustrative ("Consider adapting…") but its conclusion reads as empirical fact. These exact numbers do not correspond to any recognisable published result for this configuration.
- **Severity:** HIGH
- **Recommended action:** Cite the source, or replace with clearly hypothetical values framed as illustration: "suppose Stage 1 yields roughly 94% versus 89% and 79% for the baselines."

---

### H3 — Invented Regulatory / Legal Claims

**Finding 5**
- **Location:** Section 3.5, MiFID II research independence subsection
- **Quoted text:** "A model used to generate research notes can violate research independence rules under MiFID II Article 37."
- **Why flagged:** "MiFID II Article 37" cited twice as the basis for research independence obligations with no `\cite{}`. MiFID II's research independence provisions are primarily in Article 37 of the Delegated Directive (Commission Delegated Directive (EU) 2017/593), not the main MiFID II text — the citation conflates the directive with its delegated acts.
- **Severity:** MEDIUM
- **Recommended action:** Add a `\cite{}` to the official regulatory text (Commission Delegated Directive 2017/593, Article 37), or qualify the reference explicitly.

---

### H6 — Undated "Recent" Claims

**Finding 6**
- **Location:** Section 3.4, FinQA SOTA paragraph
- **Quoted text:** "Current state-of-the-art models achieve roughly 75% execution accuracy"
- **Why flagged:** "Current state-of-the-art" is undated and uncited. The FinQA leaderboard advances rapidly; the figure may be substantially higher as of 2026.
- **Severity:** LOW
- **Recommended action:** Replace with "As of [year], state-of-the-art models achieved roughly X% execution accuracy \cite{key}" or anchor to the benchmark's introduction date.

---

## Code Hallucinations

No code hallucinations detected. The notebook uses clearly synthetic curve data generated from published Chinchilla power-law coefficients, with named model checkpoints used as approximate illustration points. No hardcoded financial price arrays, no fake API responses.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1 | Sec 3.3, FinBERT task results (88.5%, 78.3%, 91.3%) | HIGH |
| 2 | H1 | Sec 3.4, FinQA SOTA claim (75% / 91%) | MEDIUM |
| 3 | H1 | Sec 3.3, BloombergGPT vs GPT-NeoX margin (10–20%) | LOW |
| 4 | H4 | Example 3.7, two-stage LLaMA-2 results (94.2%, 88.7%, 79.3%) | HIGH |
| 5 | H3 | Sec 3.5, MiFID II Article 37 research independence (uncited) | MEDIUM |
| 6 | H6 | Sec 3.4, "Current state-of-the-art" FinQA (undated) | LOW |
