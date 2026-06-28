# Hallucination Audit Report — Chapter 14: Financial Text Summarization and Information Extraction

**Verdict:** HALLUCINATIONS FOUND (2 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 14.1 (`sec:ch14-information-extraction-problem`), opening paragraph beginning "Financial markets run on information."
- **Quoted text:** "A portfolio manager cannot personally read every 10-K filed by the 6,000-plus companies in the Russell 3000."
- **Why flagged:** Uncited invented specificity. The Russell 3000 by construction tracks approximately 3,000 companies (the count is encoded in the index name); the precise-sounding "6,000-plus" figure has no `\cite{}` and contradicts the index definition, implying a source that does not exist.
- **Recommended action:** Correct to "roughly 3,000 companies in the Russell 3000," or reframe generically ("the thousands of companies in a broad equity index").

### H6 — Undated "Recent" Claims

**Finding 2**
- **Location:** Section 14.3.4 (`sec:ch14-long-document-challenges`), final bullet "Long-context models."
- **Quoted text:** "...and, as of 2024, commercial models with extended context windows of 128K to 1M tokens---such as Gemini 1.5 Pro---can process an entire S-1 in a single forward pass."
- **Why flagged:** "As of 2024 ... such as [named current product]" soft-currency claim naming a specific commercial model and capability with no `\cite{}`. Matches the H6 pattern (point-in-time SOTA assertion that cannot be verified from the text and will date quickly).
- **Recommended action:** Add a citation/source for the Gemini 1.5 Pro context-window figure, or generalize ("contemporary long-context commercial models with windows up to ~1M tokens") without anchoring to an undated "as of 2024" SOTA naming.

---

## Code Hallucinations

None — there is no notebook for this chapter, and the chapter contains no executable code cells (only an illustrative natural-language prompt in a `verbatim` block within an `example` environment).

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1   | Sec 14.1 (Russell 3000 count) | MEDIUM |
| 2 | H6   | Sec 14.3.4 (Gemini 1.5 Pro, "as of 2024") | LOW |

**Severity guide:**
- HIGH: fabricated data attributed to a real entity with no disclaimer
- MEDIUM: uncited precision claim that could mislead a reader
- LOW: undated "recent" claim or soft imprecision

**Notes on items deliberately NOT flagged:** The Microsoft Q3 2023 figures (Ex. `ex:entities-earnings-call`) sit in an `example` block and carry an explicit footnote attribution; the GPT-5 earnings-summary metrics (Ex. `ex:earnings-gpt4`) are explicitly framed as "As an illustration, suppose..."; the "$57B vs $56.5 billion (illustrative)" and "$142 to $168" target-price line are labeled illustrative/generic templates; and all dataset/benchmark statistics (EDGAR-Corpus ~6.5B tokens, ECTSum 2,425 pairs, FinQA ~50%/over 70%, kryscinski 25–30%, FINER-139) carry `\cite{}`/`\citep{}` keys and are therefore out of scope per the "What NOT to Flag" rules.
