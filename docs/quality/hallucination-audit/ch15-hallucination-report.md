# Hallucination Audit Report — Chapter 15: LLMs and Privacy: Local Deployments and Text De-identification

**Verdict:** HALLUCINATIONS FOUND (2 text, 0 code)

---

## Text Hallucinations

### H4 — Synthetic Real-World Examples

**Finding 1**
- **Location:** Section~\ref{sec:ch15-privacy-imperative}, opening `\begin{context}` block, paragraph beginning "It is January 2023..."
- **Quoted text:** "Samsung engineers make global headlines weeks later when source code submitted to ChatGPT is retained for training."
- **Why flagged:** A named real company (Samsung) is paired with a specific factual event and an implied date ("weeks later" after January 2023), presented as established fact with no `\cite{}`. This matches the H4 pattern of a real-world entity used as a factual example without a citation. It sits in a `context` box, but unlike `remark`/`example` blocks it is not framed as hypothetical or illustrative — it asserts a real incident. (The adjacent "a major bank" story is generic/hypothetical and correctly not flagged.)
- **Recommended action:** Add a citation to a public report of the incident, or reframe explicitly as illustrative.

### H6 — Undated "Recent" Claims

**Finding 2**
- **Location:** Section~\ref{sec:ch15-quantisation}, paragraph beginning "The primary cost of local deployment..."
- **Quoted text:** "The best available open-weight models as of 2025 are competitive with GPT-3.5-class performance on general benchmarks, but lag behind the frontier (GPT-5 / Claude Opus 4.8) on complex reasoning..."
- **Why flagged:** A comparative capability claim qualified only by "as of 2025," with no citation or benchmark reference. It is a soft, time-bound assertion of relative model performance that cannot be verified and will date quickly — the H6 pattern.
- **Recommended action:** Anchor to a cited benchmark/leaderboard, or soften to a qualitative, clearly time-stamped statement.

---

## Code Hallucinations

None — there is no notebook for this chapter, so no C1–C5 findings apply.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H4   | Sec 15.1 context box (Samsung) | LOW |
| 2 | H6   | Sec 15.3 quantisation (GPT-3.5 comparison) | LOW |

**Severity guide:**
- HIGH: fabricated data attributed to a real entity with no disclaimer
- MEDIUM: uncited precision claim that could mislead a reader
- LOW: undated "recent" claim or soft imprecision

Note: numerous precise claims in this chapter (GDPR Art. 83 fine thresholds, MiFID II retention periods, DORA applicability date, AWQ salient-weight fraction, Llama VRAM footprints, Carlini extraction results) are all either backed by `\cite{}` keys or are standard stylized facts, and were correctly not flagged.
