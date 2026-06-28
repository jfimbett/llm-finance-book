# Hallucination Audit Report — Chapter 08: Domain-Specific Financial Large Language Models

**Verdict:** HALLUCINATIONS FOUND (2 text, 0 code)

---

## Text Hallucinations

### H2 — Fabricated Benchmarks

**Finding 1**
- **Location:** Section~\ref{sec:ch08-benchmarks} (FinQA paragraph), sentence beginning "On the public leaderboard, the best fine-tuned specialist systems..."
- **Quoted text:** "On the public leaderboard, the best fine-tuned specialist systems achieve execution accuracy around 68--72\%, while general-purpose zero-shot GPT-4 class models achieve approximately 55--60\%."
- **Why flagged:** Specific leaderboard performance ranges with no `\cite{}` on the numbers. The only citation in the paragraph (`\citet{chen2021finqa}`, the 2021 dataset paper) is attached to the introduction of FinQA, not to these results — and it cannot be the source of a "GPT-4 class" figure, since GPT-4 postdates the cited paper by roughly two years. The precision ("68--72\%", "55--60\%") implies a leaderboard source that is not given.
- **Recommended action:** Add a citation to the specific leaderboard / evaluation paper reporting these GPT-4-era numbers, or reframe explicitly as illustrative orders of magnitude without specific percentages.

**Finding 2**
- **Location:** Section~\ref{sec:ch08-limitations-general-purpose}, paragraph "\textit{Table parsing failures.}"
- **Quoted text:** "On the FinQA benchmark \cite{chen2021finqa}, ... general-purpose models in the GPT-3 class (175B parameters) achieve accuracy below 60\%, while fine-tuned specialist systems exceed 80\%."
- **Why flagged:** The `\cite{chen2021finqa}` is attached to "the FinQA benchmark" (the dataset), not to the performance figures. The "exceed 80\%" specialist figure is uncitable from the 2021 dataset paper and directly contradicts this same chapter's later statement that "the best fine-tuned specialist systems achieve execution accuracy around 68--72\%" (Section~\ref{sec:ch08-benchmarks}). An internal contradiction between two precise benchmark figures is a hallmark of invented specificity.
- **Recommended action:** Reconcile the two passages to a single sourced figure, and cite the specific result for the specialist/GPT-3 accuracy numbers rather than relying on the dataset citation.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H2   | Sec ch08-benchmarks (FinQA leaderboard sentence) | MEDIUM |
| 2 | H2   | Sec ch08-limitations-general-purpose (table parsing) | MEDIUM |

**Severity guide:**
- HIGH: fabricated data attributed to a real entity with no disclaimer
- MEDIUM: uncited precision claim that could mislead a reader
- LOW: undated "recent" claim or soft imprecision
