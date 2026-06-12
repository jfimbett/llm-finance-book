# Hallucination Audit Report — Chapter 01: Introduction

**Verdict:** HALLUCINATIONS FOUND (5 text, 0 code)

---

## Text Hallucinations

### H6 — Undated "Recent" Claims

**Finding 1**
- **Location:** Section 1.8 (Token Costs and Latency Trade-offs), Table~\ref{tab:api-costs}
- **Quoted text:** `representative pricing and latency benchmarks as of 2024` — `gpt-4o` at $2.50/$10.00 per M tokens, 60 tokens/s, P99 1.2s; `gpt-4o-mini` at $0.15/$0.60, 120 tokens/s, P99 0.4s; `claude-sonnet` at $3.00/$15.00, 80 tokens/s, P99 1.0s; `claude-haiku` at $0.25/$1.25, 200 tokens/s, P99 0.3s; `LLaMA-3 70B (on-prem)` at 45 tokens/s, P99 0.8s.
- **Why flagged:** Table carries soft qualifier "as of 2024" but no `\cite{}` key. Every numeric entry (input price, output price, tokens/s, P99 latency) is asserted with false precision. Token prices for OpenAI and Anthropic change frequently; throughput and P99 figures vary sharply across deployment configurations, regions, and load. The `claude-sonnet` figures ($3.00/$15.00) do not match published pricing of any named Claude Sonnet release in 2024 without a specific model-version citation.
- **Severity:** HIGH
- **Recommended action:** Replace the hardcoded table with cited sources (e.g., `\cite{openai2024pricing}`, `\cite{anthropic2024pricing}`), or add a prominent note that figures are illustrative orders of magnitude and instruct readers to verify current rates, citing at least one empirical throughput study.

---

### H3 — Invented Regulatory / Legal Claims

**Finding 2**
- **Location:** Section 1.9.4 (The Regulatory Landscape), Remark `rem:eu-ai-act`
- **Quoted text:** "The EU AI Act, entering into force August 2024, classifies AI systems into four risk tiers. General-purpose LLM APIs (Article 51–52) must comply with transparency obligations..."
- **Why flagged:** Specific article numbers (Article 51–52) cited as establishing obligations, with no `\cite{}` key. Article numbering in the AI Act shifted substantially between draft and final text; asserting "Article 51–52" without a citation to the official OJ text creates the risk that the article numbers are outdated or misattributed.
- **Severity:** HIGH
- **Recommended action:** Add a `\cite{}` key for Regulation (EU) 2024/1689 and verify that Article 51–52 corresponds to the final enacted text. If uncertain, cite at chapter level and remove the specific article numbers.

**Finding 3**
- **Location:** Section 1.9.4 (The Regulatory Landscape), Remark `rem:sec-guidance`
- **Quoted text:** "In July 2023 the US Securities and Exchange Commission proposed rules requiring investment advisers and broker-dealers to eliminate or neutralise conflicts of interest when using 'predictive data analytics,' including LLMs, in investor interactions."
- **Why flagged:** Specific SEC rulemaking with specific month and quoted language ("predictive data analytics") but no `\cite{}` key. The proposed rule (Release No. IA-6383) is real; the absence of citation makes the specific framing unverifiable and risks the quoted terminology being subtly wrong.
- **Severity:** MEDIUM
- **Recommended action:** Add `\cite{sec2023predictive}` linking to SEC Proposed Rules Release IA-6383, and verify that "predictive data analytics" is verbatim from the release.

---

### H1 — Phantom Statistics

**Finding 4**
- **Location:** Section 1.8, lines 1869–1873
- **Quoted text:** "classifying one million headlines with a 100-token context costs roughly $250 vs. $15"
- **Why flagged:** Dollar figures derived from the uncited table in Finding 1, inheriting its uncited precision. The downstream dollar figures presented as established fact amplify the H6/H1 risk.
- **Severity:** MEDIUM
- **Recommended action:** Frame as illustrative arithmetic dependent on the preceding table and apply the same citation fix as Finding 1.

---

### H2 — Fabricated Benchmarks

**Finding 5**
- **Location:** Section 1.5 (History: LSTM-era)
- **Quoted text:** "They achieved state-of-the-art performance on financial sentiment benchmarks such as FiQA and Financial Phrase Bank throughout 2016–2018."
- **Why flagged:** No `\cite{}`. FiQA as a shared task was introduced in 2018 (FiQA-2018 at WWW'18); LSTM models being state-of-the-art on FiQA "throughout 2016–2018" is temporally implausible given the benchmark did not exist in its benchmark form until 2018.
- **Severity:** MEDIUM
- **Recommended action:** Cite the FiQA shared task paper (Maia et al., 2018) and narrow the claim to Financial PhraseBank with an appropriate citation (e.g., Malo et al., 2014), removing the cross-benchmark generalisation.

---

## Code Hallucinations

No code hallucinations detected. All cells use live API calls to `yfinance` for real data; only well-established, real libraries are imported; no hardcoded financial statements or phantom file paths.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H6/H1 | Sec 1.8, Table `tab:api-costs` — API pricing/latency table | HIGH |
| 2 | H3 | Sec 1.9.4, Remark `rem:eu-ai-act` — Article 51–52 reference | HIGH |
| 3 | H3 | Sec 1.9.4, Remark `rem:sec-guidance` — SEC July 2023 rulemaking | MEDIUM |
| 4 | H1 | Sec 1.8 — derived cost computation $250 vs. $15 | MEDIUM |
| 5 | H2 | Sec 1.5 — LSTM SOTA claim on FiQA 2016–2018 | MEDIUM |
