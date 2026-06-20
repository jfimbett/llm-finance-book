# Change Log — 1 01-intro

| Date | Iteration | Task | Change | Dimensions moved |
|------|-----------|------|--------|------------------|
| 2026-06-20 | 0 | — | **Audit only — no edits applied** (dry run of the book-quality goal system). | — |
| 2026-06-20 | 1 | T1 | Collapsed §6 (RNN/LSTM) and §7 (attention) from full derivations-with-proofs to intuition-only previews; removed the vanishing-gradient theorem+proof, full LSTM gate equations, scaled-dot-product definition, √d_k proposition+proof, and multi-head definition; replaced with forward `\ref` to ch02 (`thm:vanish-explode`, `def:lstm`, `sec:sequential-lstm`, `def:scaled-dot-product-attn`, `thm:sqrt-dk-scaling`, `sec:transformer-mha`, `def:mha`, `sec:transformer`). Net −119 lines (214 deletions, 95 insertions). | non_repetition 68→93, notation_crossref 60→91, progressive_learning 88→92 |
| 2026-06-20 | 1 | T1 | Removed 9 ch01 `\label`s that collided with ch02 (`eq:rnn-jacobian`, `def:lstm`, `eq:lstm-{forget,input,candidate,cell,output,hidden}`, `eq:multihead`); renamed `def:mlm`→`def:mlm-intro` to clear the ch03 collision. | notation_crossref |
| 2026-06-20 | 1 | T2 | Dropped the `ke2019predicting` "attention-based model / attention weights" mischaracterization from `rem:attention-finance`; reworded to a generic attention-interpretability remark (no citation invented). | citation_accuracy 84→87 |
| 2026-06-20 | 1 | paired | Fixed Looking-Ahead cross-ref: "derived from first principles in §\ref{sec:attention} of that chapter" pointed at ch01's own label; retargeted to `\ref{sec:transformer}` (ch02). | notation_crossref |

> Iteration 1 verified by a two-pass `pdflatex` build (exit 0, 620 pages): none of the
> §6-§7 / MLM labels are multiply-defined. Root-cause blockers (non_repetition,
> notation_crossref) now pass. Chapter still **NOT PASS** overall — open below-90 dims:
> concept_ordering (85), citation_accuracy (87), completeness (88), correctness (88),
> code_figure_correctness (82), reproducibility (55). These were intentionally out of
> scope for this controlled SSOT-only iteration.
