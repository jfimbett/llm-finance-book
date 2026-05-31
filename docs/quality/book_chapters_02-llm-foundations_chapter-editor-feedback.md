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

---

## Revision Round 3 — Issues from Full Review Gate (8.4/10 PASS, 3 BLOCKERs → NEEDS_REVISION)

### BLOCKER

- [x] **B1 — Roadmap table off-by-one** (tab:roadmap, row "2"): Incremented all chapter rows by 1 (2→3 through 14→15). Updated the prose below the table to match (Chapters 3–5 for text sources, 6–7 for adaptation strategies, etc.).
- [x] **B2 — Three regulatory citations are comment placeholders**: Added `gdpr2016` and `sec2023ai` bib entries. The existing `euaiact2024` key was used (comments had a variant key name `eu-ai-act-2024`). Replaced all three `% [CITE: ...]` comment lines with live `\citep{}` calls.
- [x] **B3 — Llama 3 GPU memory citation is a comment**: Replaced `% [CITE: touvron2023llama]` comment with `\citep{touvron2023llama}` inline in the text.

---

## Revision Round 4 — Minor polish (final gate: 8.6/10 PASS, 0 BLOCKERs, peer MINOR_REVISION → READY_TO_RELEASE)

- [x] **m7 — M1/M2 inter-chapter refs**: Added "of Chapter~1" qualifier to `\ref{sec:classical-tfidf}` and "Chapter~1 (Section~\ref{sec:embeddings}) and" qualifier to the doc-repr reference, making inter-chapter nature explicit for standalone readers.
- [x] **m8 — M4 outlines API version**: Added `# requires: pip install outlines>=0.1` comment to grammar listing.
- [x] **m9 — M7 KD gradient rescaling missing citation**: Added `\citep{hinton2015distilling}` to the τ² gradient magnitude sentence.
- [x] **m10 — M8 math-mode e.g.**: Changed `($\text{e.g.}$, 70B...)` to `(e.g., 70B...)`.
- [x] **m11 — M9 Claude version**: Removed stale "3.7/4.x" version tag — now reads "Claude" (model-version-agnostic).
