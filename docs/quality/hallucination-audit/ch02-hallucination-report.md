# Hallucination Audit Report — Chapter 02: Large Language Models: Architecture and Practice

**Verdict:** HALLUCINATIONS FOUND (2 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section~\ref{sec:sequential-rnn} (RNNs / vanishing gradients), paragraph beginning "These theoretical constraints have concrete consequences..."
- **Quoted text:** "An S\&P~500 earnings-call transcript is typically 8,000--12,000 tokens."
- **Why flagged:** A specific numeric range presented as an established empirical fact ("is typically") with no `\cite{}` key. The precision of the 8,000–12,000 band implies an underlying measurement/source that is not given. It is not a universally-known textbook constant (unlike "equity risk premium ≈ 5–7%"), and it feeds a downstream quantitative claim (the "$T - t \approx 9{,}900$ BPTT steps" argument), so the unsupported number propagates.
- **Recommended action:** Add a citation for the typical transcript length, or reframe explicitly as a rough order-of-magnitude ("on the order of ten thousand tokens, for illustration").

**Finding 2**
- **Location:** Section~\ref{sec:landscape} (The Modern LLM Landscape), opening `context` block beginning "In November 2022, a chatbot launched..."
- **Quoted text:** "It reportedly reached a hundred million users in approximately two months, making it one of the fastest-growing consumer applications on record."
- **Why flagged:** A specific adoption statistic (100M users / ~2 months) presented as fact. The "hundred million in two months" precision implies a specific source report that is absent. The hedges "reportedly"/"approximately" soften but do not supply the missing attribution, so the claim remains unverifiable as written.
- **Recommended action:** Add a citation for the user-growth figure, or downgrade to a non-numeric framing ("achieved unusually rapid mainstream adoption").

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1   | Sec on RNN vanishing gradients ("S&P 500 ... 8,000–12,000 tokens") | LOW |
| 2 | H1   | Sec~\ref{sec:landscape} context intro ("hundred million users in ~two months") | LOW |

**Severity guide:**
- HIGH: fabricated data attributed to a real entity with no disclaimer
- MEDIUM: uncited precision claim that could mislead a reader
- LOW: undated "recent" claim or soft imprecision

Note: precise numerics elsewhere in the chapter were *not* flagged because they are (a) deterministic computations shown in-text (e.g. $8\times4096^2 \approx 134$M attention entries; $405\text{B}\times2 = 810$ GB; LoRA $4096^2 = 16.8$M $\to 16\times8192 = 131$K), (b) carried a `\cite{}` key (BloombergGPT token counts, FinanceBench 81%, niszczota2023gpt 99%, chen2024uncertainty Sharpe ~20%, EU AI Act 2024/1689, GDPR 2016/679, BERT 15%/80/10/10 masking), (c) sat inside `example`/`remark`/`illustration` blocks or were tagged "illustrative"/"approximate" (BPE tokenisation example, merger-valuation EV/EBITDA 13.5×, cost tables, pricing table with "verify before budgeting"), or (d) are standard product specs / well-known model-landscape facts consistent with the latest-models convention (context-window history, parameter counts, prompt-caching ~10% cache-read rate).
