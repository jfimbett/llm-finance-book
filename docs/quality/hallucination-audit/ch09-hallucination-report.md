# Hallucination Audit Report — Chapter 09: Financial NLP and Sentiment Analysis

**Verdict:** HALLUCINATIONS FOUND (3 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section~\ref{sec:ch09-evaluation} (Inter-Annotator Agreement), paragraph ending "...reflecting the genuine ambiguity of many financial sentences."
- **Quoted text:** "Published financial sentiment benchmarks typically report alphas between 0.65 and 0.78, reflecting the genuine ambiguity of many financial sentences."
- **Why flagged:** A specific numeric range (0.65–0.78) attributed to "published financial sentiment benchmarks" in general, with no `\cite{}` key. The precision implies an underlying source that is not given. Note that other quantitative dataset descriptions in the chapter (PhraseBank size, LM word-list counts, Fog ranges) are all properly cited, which makes this uncited range stand out.
- **Recommended action:** Add citations to the specific benchmarks whose alphas fall in this range, or reframe as an explicitly illustrative/approximate statement.

**Finding 2**
- **Location:** Section~\ref{sec:ch09-inference-at-scale} (Batch Inference), efficiency-optimisations bullet list.
- **Quoted text:** "Model distillation: replace a 110M-parameter model with a 33M-parameter distilled version with $<$5\% accuracy loss."
- **Why flagged:** Specific parameter count (33M) paired with a precise performance bound ("<5% accuracy loss") presented as established fact, with no `\cite{}`. This is the structural pattern of an uncited benchmark result (it resembles, but does not cite, known DistilBERT-style findings).
- **Recommended action:** Cite the distillation result being referenced (e.g., the DistilBERT paper) or soften to a clearly illustrative order-of-magnitude statement.

### H2 — Fabricated Benchmarks

**Finding 3**
- **Location:** Section~\ref{sec:ch09-evaluation}, Table~\ref{tab:krippendorff-benchmarks} ("Inter-annotator agreement on sentiment labels for financial text").
- **Quoted text:** Table caption "Source: selected published benchmarks." with rows including "Financial PhraseBank (66\% agreement) ... $\approx 0.72$", "Earnings call sentences (practitioner) ... 0.68--0.75", "FOMC statement sentences ... 0.70--0.78".
- **Why flagged:** A table of specific Krippendorff's-alpha values is attributed to unnamed "selected published benchmarks" with no per-row or aggregate `\cite{}` keys. Specific numeric benchmark values presented as sourced data without any retrievable citation is the H2 pattern; the "(practitioner)" row in particular has no identifiable source.
- **Recommended action:** Add citations for each non-trivial row (the Financial PhraseBank rows can point to `malo2014phrasebank`), or relabel the table as illustrative/hypothetical values rather than "published benchmarks."

---

## Code Hallucinations

None — this chapter has no companion notebook and no embedded code arrays.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1   | Sec ch09-evaluation (alpha range "0.65–0.78") | MEDIUM |
| 2 | H1   | Sec ch09-inference-at-scale (distillation "<5% loss") | LOW |
| 3 | H2   | Table tab:krippendorff-benchmarks | MEDIUM |

**Severity guide:**
- HIGH: fabricated data attributed to a real entity with no disclaimer
- MEDIUM: uncited precision claim that could mislead a reader
- LOW: undated "recent" claim or soft imprecision

**Note on items deliberately NOT flagged:** the LM lexicon worked example (scores −0.086, −0.17) and the FinBERT F1 figures (0.70–0.80 vs 0.60–0.65) are inside `\begin{example}` blocks explicitly marked illustrative; the per-million-sentence cost figure self-labels as "a rough order of magnitude for frontier models in 2024"; SEC filing deadlines (60–90 / 40–45 days, four business days) are standard, correct regulatory reference facts, not invented regulations; and all named papers/findings (LopezLiraTang2023, KirtacGermano2024, ko2024can, gilbazo2025tweeting, cookson2026bankrun, etc.) carry `\cite{}`/`\citet{}` keys and are out of scope per the "citations that exist" rule.
