# Hallucination Audit Report — Chapter 04: LLM Agents and Finance Applications

**Verdict:** HALLUCINATIONS FOUND (5 text, 0 code)

There is no notebook for this chapter; every in-text code listing has been replaced by a prose pointer to `code/practicals/04-llm-agents/`, so no C1–C5 code rules apply. The chapter is otherwise heavily hallucination-proofed: nearly all precise figures sit inside `\begin{example}`, `\begin{remark}[Illustrative output]`, or `\begin{illustration}` blocks, or carry a `\cite{}`/`\citet{}` key (e.g., the Apple Q4-2023 pipeline numbers, the portfolio Q&A weights, the chunking recall figures, the TradingAgents/FinVerse/FinanceBench/kim2024financial result claims). Those are correctly out of scope. The findings below are the residual uncited specifics.

---

## Text Hallucinations

### H4 — Synthetic Real-World Examples / Invented Product

**Finding 1**
- **Location:** Section "Deployment, Safety, and Governance" → "Latency, Cost, and Reliability in Production," paragraph beginning "The primary tools for managing latency" (line 1408).
- **Quoted text:** "a small, fast model (e.g., \texttt{gpt-5.6-luna}, Claude Haiku 4.5) handles routine classification..."
- **Why flagged:** `gpt-5.6-luna` has the signature of an invented model name — an oddly specific version number plus a codename that does not correspond to any known OpenAI model. It is presented as a real, namable product alongside the genuine "Claude Haiku 4.5." This is invented specificity, not an illustrative placeholder.
- **Recommended action:** Replace with a verified current small/fast model name (per the latest-models policy, look it up rather than recall it), or genericise to "a small, fast model (e.g., a Haiku- or mini-tier model)."

**Finding 2**
- **Location:** Section "Tool Use and Function Calling," opening `\begin{context}` block, sentence beginning "When Morgan Stanley deployed an internal LLM assistant..." (line 322).
- **Quoted text:** "When Morgan Stanley deployed an internal LLM assistant for financial advisors, one of the earliest challenges was not language quality but factual grounding."
- **Why flagged:** A named real institution is used as a factual deployment example with no `\cite{}` and no "for illustration" framing. The claim is plausibly true but the specificity (named firm, specific use case) implies a verifiable source that is absent.
- **Recommended action:** Add a citation to the public reporting of the Morgan Stanley/OpenAI advisor assistant, or reframe generically ("when a large wealth manager deployed an internal LLM assistant").

**Finding 3**
- **Location:** Section "Finance-Specific Agent Applications," opening `\begin{context}` block, sentence beginning "These applications are not hypothetical..." (line 1123).
- **Quoted text:** "firms including Goldman Sachs, JPMorgan, Bloomberg, and numerous hedge funds have deployed LLM-based systems for tasks ranging from document analysis to automated report generation."
- **Why flagged:** Multiple named real institutions asserted as factual deployers of LLM systems, with no citation and no illustrative framing. Matches the H4 pattern (named institutions presented as established fact).
- **Recommended action:** Cite specific public sources for each named deployment, or soften to "several major banks and data vendors have publicly described LLM-based systems."

### H1 — Phantom Statistics

**Finding 4**
- **Location:** Section "Retrieval-Augmented Generation in Finance" → "Vector Databases and Embedding Retrieval," paragraph beginning "The most widely deployed ANN algorithm..." (lines 906–908).
- **Quoted text:** "For corpora up to roughly one million vectors, IVF-HNSW provides an excellent balance of query speed (typically under 10 milliseconds) and recall (typically above 95\% for top-10 retrieval)."
- **Why flagged:** Three precise performance figures (1M vectors, <10 ms, >95% recall) presented as established benchmarks. The nearby `\cite{johnson2019billion}` attaches to FAISS in general, not to these specific numbers; no source substantiates them. The "typically/roughly" hedging softens but does not source the claim.
- **Recommended action:** Attach a citation that actually reports these latency/recall figures, or reframe as an explicit order-of-magnitude rule of thumb without the specific 10 ms / 95% values.

**Finding 5**
- **Location:** Section "Tool Use and Function Calling" → "Tool Selection, Reliability, and Error Recovery," final paragraph (line 503).
- **Quoted text:** "...without mentally enumerating all 30,000 available Bloomberg functions."
- **Why flagged:** A precise count ("30,000") of Bloomberg terminal functions stated as fact with no citation. Uncitable precision of exactly the type H1 targets, even though it is used inside an analogy.
- **Recommended action:** Cite the figure or hedge it ("the tens of thousands of available Bloomberg functions").

---

## Code Hallucinations

None — there is no notebook for this chapter and all in-chapter code listings are replaced by prose references to `code/practicals/04-llm-agents/`. C1–C5 not applicable.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H4   | Sec "Latency, Cost..." (l.1408), `gpt-5.6-luna` | MEDIUM |
| 2 | H4   | Sec "Tool Use" context (l.322), Morgan Stanley | LOW |
| 3 | H4   | Sec "Finance-Specific Apps" context (l.1123), GS/JPM/Bloomberg | LOW |
| 4 | H1   | Sec "Vector Databases" (l.906–908), FAISS 10 ms / 95% / 1M | LOW |
| 5 | H1   | Sec "Tool Selection" (l.503), 30,000 Bloomberg functions | LOW |

**Severity guide:**
- HIGH: fabricated data attributed to a real entity with no disclaimer
- MEDIUM: uncited precision claim / invented product that could mislead a reader
- LOW: uncited named-institution claim or soft, hedged precision
