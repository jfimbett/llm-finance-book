# Change Log — Chapter 3 (reading order) · `02-llm-foundations`

Chapter file: `book/chapters/02-llm-foundations/chapter.tex`
Reading index: 3 · Slug: `02-llm-foundations` · Date: 2026-06-20 · Iteration: 0

Audit only — no edits applied. (2026-06-20)

## Iteration 1 (2026-06-20) — no edits to this chapter

ch02 was held as the **single source of truth** and left unedited. The paired
SSOT edit to ch01 removed ch01's duplicate RNN/LSTM/attention/√d_k/multi-head
derivations and the 9 labels that collided with this chapter, so ch02 is now the
sole owner of those definitions (verified by two-pass `pdflatex`, exit 0, 620 pages).
Cross-chapter scores improved: **notation_crossref 48→68, non_repetition 55→78**.
Both remain < 90 due to ch02's own out-of-scope issues (7 other cross-chapter
duplicate labels, 15 hard-coded `Chapter~N` refs, stub `demo.ipynb`, `tab:roadmap`).
