# Hallucination Audit Report — Chapter 04: LLM Agents and Finance Applications

**Verdict:** HALLUCINATIONS FOUND (8 text, 0 code)

---

## Text Hallucinations

### H1 — Phantom Statistics

**Finding 1**
- **Location:** Section 4.4, Example 4.8 (Chunking a 10-K for RAG)
- **Quoted text:** "15 top-level item chunks, 340 paragraph-level chunks (mean 180 tokens each), 28 table chunks... A query about iPhone revenue growth retrieves the relevant paragraph... with 94% recall on a manually labelled evaluation set."
- **Why flagged:** Precise numeric figures attributed to Apple's 2023 10-K processing with no `\cite{}`. Implies a real experiment was run; if illustrative, must be labelled as such.
- **Severity:** HIGH
- **Recommended action:** Add citation to the source experiment, or reframe as explicitly illustrative with approximate placeholder values.

**Finding 2**
- **Location:** Section 4.4, Hybrid Search subsection
- **Quoted text:** "Empirically, $\alpha \approx 0.7$ (favouring dense retrieval) works well for question-answering tasks... while $\alpha \approx 0.3$ is preferable for keyword-heavy regulatory lookup tasks."
- **Why flagged:** Precise parameter values presented as empirical findings without any `\cite{}`.
- **Severity:** MEDIUM
- **Recommended action:** Add citation to a paper reporting these values, or reframe as a starting-point heuristic.

**Finding 3**
- **Location:** Section 4.4, Vector Databases subsection, Example 4.5
- **Quoted text:** "This combination of semantic search and metadata filtering reduces irrelevant retrievals by approximately 60% compared to unconstrained semantic search."
- **Why flagged:** Precise quantitative benefit claim implying a study that is not cited.
- **Severity:** MEDIUM
- **Recommended action:** Cite the source, or replace with qualitative language ("substantially reduces irrelevant retrievals").

**Finding 4**
- **Location:** Section 4.4, Chunking subsection
- **Quoted text:** "This strategy outperforms fixed-size chunking by approximately 15--20% on downstream question-answering benchmarks over 10-K filings."
- **Why flagged:** Precise performance advantage range on an unspecified benchmark with no `\cite{}`.
- **Severity:** MEDIUM
- **Recommended action:** Cite the benchmark study, or replace with qualitative guidance.

**Finding 5**
- **Location:** Section 4.4, RAG Evaluation subsection
- **Quoted text:** "A faithfulness score below 0.85 should trigger automatic review rather than automated publication."
- **Why flagged:** The 0.85 threshold is stated as an operational prescription without citation. Its precision creates the false appearance of an established standard.
- **Severity:** LOW
- **Recommended action:** Reframe as a suggested heuristic: "below a practitioner-chosen threshold (e.g., 0.85)."

**Finding 6**
- **Location:** Section 4.5, Example 4.9 (Earnings Call Pipeline Output)
- **Quoted text:** "Revenue guidance: '$89–$90 billion for Q1 2024' (vs. consensus $90.7B; mild negative surprise; sourced from CEO remarks at transcript minute 12:43)… deflection score 0.72 (high). Total pipeline latency: 3.2 minutes for a 90-minute transcript."
- **Why flagged:** Specific financial figures, transcript timestamps, speaker attributions, deflection score, and pipeline latency attributed to Apple's Q4 2023 earnings call. Presented as real pipeline output without any citation or "hypothetical" disclaimer.
- **Severity:** HIGH
- **Recommended action:** Add explicit illustrative disclaimer at the start of the example, or if these are real numbers, cite the transcript and pipeline paper.

**Finding 7**
- **Location:** Section 4.3, Frameworks subsection
- **Quoted text:** "LangChain's integration layer provides pre-built connectors for over 100 data sources and APIs."
- **Why flagged:** Uncited, potentially outdated count of LangChain integrations with no date anchor.
- **Severity:** LOW
- **Recommended action:** Remove the count or add a date-anchored citation.

---

### H3 — Invented Regulatory / Legal Claims

**Finding 8**
- **Location:** Section 4.6, Audit Trails subsection
- **Quoted text:** "MiFID II's record-keeping obligations (Article 25)..."
- **Why flagged:** "Article 25" cited as establishing record-keeping obligations without a `\cite{}`. MiFID II Article 25 concerns suitability and appropriateness obligations, not record-keeping (record-keeping is primarily Article 16). Citing the wrong article without a source is a structural H3 hallucination.
- **Severity:** HIGH
- **Recommended action:** Verify correct article reference (Article 16 concerns record-keeping) and add citation `\cite{mifid2}` or equivalent.

---

## Code Hallucinations

No code hallucinations detected. The notebook fetches live news data via `yf.Ticker(sym).news`, imports only real PyPI libraries, and does not hardcode arrays implying real historical prices.

---

## Summary Table

| # | Type | Location | Severity |
|---|------|----------|----------|
| 1 | H1 | Sec 4.4, Example 4.8 — chunk counts and 94% recall | HIGH |
| 2 | H1 | Sec 4.4, Hybrid Search — α = 0.7 / α = 0.3 empirical values | MEDIUM |
| 3 | H1 | Sec 4.4, Example 4.5 — "reduces irrelevant retrievals by ~60%" | MEDIUM |
| 4 | H1 | Sec 4.4, Chunking — "outperforms fixed-size chunking by 15–20%" | MEDIUM |
| 5 | H1 | Sec 4.4, RAG Evaluation — faithfulness threshold 0.85 | LOW |
| 6 | H1/H4 | Sec 4.5, Example 4.9 — Apple Q4 2023 pipeline output with timestamps, deflection 0.72, latency 3.2 min | HIGH |
| 7 | H1/H6 | Sec 4.3, Frameworks — "over 100 data sources" (LangChain, undated) | LOW |
| 8 | H3 | Sec 4.6, Audit Trails — "MiFID II Article 25" record-keeping (likely wrong article, uncited) | HIGH |
