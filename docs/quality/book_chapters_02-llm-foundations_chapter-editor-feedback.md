# Editor Feedback — Chapter 2: LLM Foundations

**Source:** Peer review (2026-05-31)
**Verdict:** MINOR_REVISION (overall 8.8/10, all dims ≥ 8)

---

## Round 1 — Open Issues

### MAJOR

- [x] **M1 — Undefined figure reference** (line ~823): `\ref{fig:transformer-architecture}` produces "??" — no figure environment exists; only a comment placeholder. Rewrote the remark to describe the Transformer architecture inline and reference the existing `fig:ch02-illustration` (sinusoidal PE figure).
- [x] **M2 — Grammar-based generation lacks code example** (line ~1542): Added a `minted` Python listing (`lst:ebnf-grammar`) demonstrating an `outlines` EBNF grammar constraint for a financial earnings record schema.
- [x] **M3 — SBERT mean-pool denominator wrong** (line ~235, eq. sbert-mean-pool): Fixed denominator from `n` to `\sum_{j=1}^{n} m_j` (number of non-padding tokens); added explanatory sentence in definition.

### MINOR

- [x] **m1 — Roadmap table header says "Ch. 1"** (lines 2542, 2547): Changed to "Chapter~2 foundations" and "Key Connection to Ch.~2".
- [x] **m2 — Self-referential benchmark sentence** (line 1215): Changed to "used later in this chapter as the primary benchmark".
- [x] **m3 — Five tables use captionof in bare center** (lines 1100, 1186, 1402, 1800, 1832): Converted all five to proper `\begin{table}[htbp]\centering\caption{...}` floats.
- [x] **m4 — Unnumbered subsections in Chapter Summary** (lines 2517, 2538): Converted both `\subsection*` to `\subsection` (numbered).
- [x] **m5 — RoBERTa citation key "liu2018" for 2019 paper** (line 871): Renamed key to `liu2019roberta` in both chapter.tex and bibliography.bib; also removed stale `note` field from bib entry.
- [x] **m6 — Reasoning model marginalisation notation** (line ~1041): Added inline note after Definition clarifying that Eq.~\eqref{eq:cot} shows exact marginalisation while inference uses a single Monte Carlo sample; references self-consistency decoding as the multi-sample approximation.

---

## Round 2 — Issues from Score Check (7.6/10, FAIL)

- [x] **S1 — Dangling internal reference** (line ~1073): `\ref{sec:limitations-hallucinations}` → `\ref{sec:hallucinations}` (correct label in this file).
- [x] **S2 — Missing exercises with difficulty tags** (completeness/pedagogy 7/10): Added `\textbf{[I]}` tag to existing exercise (ex:ch02-illustration). Added 5 new exercises: [B] scaled attention numerical example, [B] sampling strategy selection, [I] LoRA parameter budget, [I] SBERT embedding pipeline, [A] hallucination audit of RAG pipeline. Chapter now has 1 [I] (existing) + 2 [B] + 2 [I] + 1 [A] = 6 exercises with full coverage of all difficulty levels.
