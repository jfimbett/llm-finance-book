# Skeptical Review — Ch. 13 (read #14) LLM Limitations and Rigorous Evaluation

Format: `SEVERITY · dimension_key · file:line — issue`. Scope tagged local vs book-wide.
File = `book/chapters/13-llm-limitations-evaluation/chapter.tex` unless noted.
Audit only — no edits applied.

## BLOCKER

- BLOCKER · citation_hygiene · book/bibliography.bib:1727 and :3175 — **Duplicate BibTeX
  key `wei2022emergent`.** Two `@article{wei2022emergent,...}` entries (identical content,
  one with `note={arXiv:2206.07682}`, one without). `biber`/`bibtex` will warn/error and
  silently pick one. Scope: **book-wide** (not cited by this chapter, but it is the
  designated owner-position for the eval/limitations bib block per audit brief). Fix:
  delete one entry, keep the one with the arXiv note. Confirmed only-duplicate in the
  whole `.bib` via `uniq -d`.

## MAJOR

- MAJOR · concept_ordering · cross-chapter — **Forward/backward inversion of the
  calibration SSOT.** This chapter (read #14) is intended as the single source of truth
  for calibration/ECE/reliability diagrams (`def:ch13-perfect-calibration`, line 44; ECE
  `eq:ch13-ece`, line 62). But ch06 credit-risk (read #10, EARLIER) already defines
  calibration (`def:calibration`, 06-credit-risk/chapter.tex:381), reliability diagrams,
  Platt scaling, isotonic regression, ECE, and Brier score (06:376–419). A reader meets
  the full calibration apparatus four chapters before this "foundational" treatment.
  Scope: **book-wide (cross-chapter-ordering)**. Neither chapter cross-references the
  other (this ch13 has only `\ref{ch:llm-training-finetuning}` line 674 and
  `\ref{ch:portfolio-quant-trading}` line 967; grep of ch06 finds no ref to ch13).

- MAJOR · non_repetition · book-repetition — **Two parallel calibration definitions and
  duplicated recalibration menu.** `def:ch13-perfect-calibration` (line 44,
  $\Pr(Y{=}1\mid\hat p{=}p)=p$) is the same proposition as `def:calibration`
  (06-credit-risk:381, $\mathbb{E}[Y\mid\hat P{=}p]=p$). Platt scaling (line 221) and
  isotonic regression (line 215) are re-introduced here with the same two citations
  (`platt1999probabilistic`, `zadrozny2002transforming`) already used in ch06 (06:393,
  06:404). Reliability-diagram prose is near-duplicated (line 53 vs 06:391). One concept
  must be the SSOT and the other a `\Cref`; currently both re-derive. Scope: **book-wide**.

- MAJOR · citation_accuracy · chapter.tex:631-637 — **Fama-French factors mis-cited.**
  Lines 631–636 define the market/SMB/HML factor regression and attribute the
  "Fama-French ... market, size, and value factors" to `\cite{fama1970efficient}`
  (line 636). `fama1970efficient` is the 1970 Efficient Capital Markets / EMH paper; the
  three-factor model is Fama & French (1993). Wrong paper for the proposition. The bib
  appears to lack a `famafrench1993` key. Scope: local (citation), but fix may require a
  new bib entry. Mark `NEEDS_EXTERNAL_VERIFICATION` for the exact replacement key.

## MINOR

- MINOR · correctness · chapter.tex:118 — **Display typo in ECE worked example.** Line 118
  writes the first bin weight as `0.012 \cdot 0.03` where it should be `0.12 \cdot 0.03`
  (= 120/1000). The product printed (`0.0036`) and the final ECE (`0.115`, line 120) are
  both correct, so this is a transcription typo in the intermediate display only.
  Verified independently: ECE = 0.115, $\sum|B_m| = 1000$.

- MINOR · notation_crossref · chapter.tex:709-714 — **Dangling symbol in Almgren-Chriss
  impact.** Prose (line 713–714) defines "$P$ the price" but the stated temporary-impact
  expression $\eta\cdot(q/V)$ per share (line 711–712) contains no $P$. Either drop the
  $P$ definition or write the impact in price units. `almgren2001optimal` resolves.

- MINOR · citation_hygiene · book/bibliography.bib (zhang2024financebench) —
  **`% [CHECK]` flag still live.** Entry carries an inline `% [CHECK] verify author list
  and title spelling`. Author list (`Islam, Shariful and ...`) and title
  ("A New Benchmark for Financial Question Answering") need external verification against
  the FinanceBench paper (arXiv:2311.11944). Cited at lines 853, 858. Scope: citation.
  → `NEEDS_EXTERNAL_VERIFICATION`.

- MINOR · citation_hygiene · book/bibliography.bib (ziemke2024temporal) — **Stub-like
  author field.** `author = {Ziemke, Matthias and others}` — bare "and others" with a
  single named author; this is the primary reference for the temporal-leakage section
  (cited lines 268, 941) and arXiv:2510.05533 dated 2024 should have a verifiable author
  list. → `NEEDS_EXTERNAL_VERIFICATION` (also: a 2025 arXiv id (2510 = Oct 2025) with
  `year={2024}` is internally inconsistent — verify date).

- MINOR · citation_accuracy · chapter.tex:856-858 — FinanceBench claim "models struggle
  substantially with multi-step numerical questions" is sourced only to
  `zhang2024financebench` with no specific hallucination-rate number; acceptable but the
  earlier sentence (line 857) says "Hallucination rates ... are high even for frontier
  models" without a figure. Soft claim; verify against source or hedge. → minor.

## NIT

- NIT · notation_crossref · chapter.tex:674 — Inline parenthetical "(parameter-efficient
  fine-tuning, e.g., LoRA; see Chapter~\ref{ch:llm-training-finetuning})" inside a
  `definition` body is dense; fine but consider a `remark`.
- NIT · pedagogy · chapter.tex:617 — Fundamental law `IR ≈ IC·√N` attributed to
  `grinold1999active`; standard attribution is Grinold (1989) / Grinold & Kahn. The
  `grinold1999active` key (Active Portfolio Management, 2nd ed.) does cover it, so
  acceptable; no change required.

## Dimensions with NO blocking issues found (positive)

- finance_orientation, finance_examples, completeness, progressive_learning, pedagogy:
  no issues rising above NIT. See constructive review.
- code_figure_correctness: chapter uses **no** figures or `\includegraphics`; worked
  numeric tables/examples verified correct (ECE example). N/A for figures.
- reproducibility: chapter is prose+math; `demo.ipynb` is a 2-cell stub (see editor plan)
  but the chapter does not depend on it. Treated as N/A-leaning with one note.
