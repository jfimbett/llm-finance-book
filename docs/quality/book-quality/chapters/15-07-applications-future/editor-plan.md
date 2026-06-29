# Editor Plan — Ch. 07 Applications & Future Trends (reading index 15)

Audit only — this plan is NOT applied. Edits are targeted and minimal; protect
KEEP-tagged content from constructive-review.md.

## MUST_FIX (blocks pass)

1. **Resolve `def:calibration` label collision** (`chapter.tex:400`).
   Rename this chapter's fairness label to `def:calibration-within-group`
   (and update the in-chapter range ref at `chapter.tex:379`
   `Definitions~\ref{def:demographic-parity}--\ref{def:calibration}`). Leave
   credit-risk's `def:calibration` (06-credit-risk/chapter.tex:382) untouched.
   → unblocks notation_crossref.

2. **Fix the stub-notebook pointers** (`chapter.tex:243`, `chapter.tex:334`).
   Either (a) repoint both lines to `code/notebooks/07-applications-future/exercises.ipynb`
   (where the EDGAR monitor / skill code actually lives), or (b) populate `demo.ipynb`
   with the promised earnings-pipeline + OpenClaw-skill code. Do NOT leave prose claiming
   "complete Python implementation" while the file is a placeholder.
   → unblocks code_figure_correctness, reproducibility.

3. **Correct "Six chapters ago"** (`chapter.tex:38`). Replace the numeric count with a
   non-numeric framing ("This book opened with a question...") or the correct
   reading-order count. → unblocks correctness.

4. **Fix `tab:chapter-map`** (`chapter.tex:56-82`). Either (a) renumber the table to the
   `main.tex` reading order and add the missing chapters, or (b) drop the leading "Ch. N"
   numeric column and key rows by `\Cref{ch:...}` titles only, so the table cannot
   contradict the TOC. → unblocks correctness, progressive_learning.

## SHOULD_FIX (raises a dimension toward 90)

5. Soften / verify the FinanceBench "roughly 80%" claim (`chapter.tex:147`); if it cannot
   be sourced, hedge it or cite the specific configuration. → citation_accuracy.

6. Add `\Cref{ch:credit-risk}` at `chapter.tex:363` ("The credit chapter introduced
   bias...") for a real hyperlink. → notation_crossref.

7. Verify figure benchmark numbers against original papers (GPT-4 FinQA 0.68;
   BloombergGPT FPB 0.85) or mark them illustrative in the caption itself, not only in the
   notebook note. → code_figure_correctness / citation_accuracy.

## OPTIONAL

8. Introduce at least one `deepdive` box for the under-the-hood material (RRF math,
   SHAP-on-embeddings projection, KL-divergence drift detector) to restore the
   context/deepdive layering the rest of the book uses. → concept_separation.

## DO_NOT_CHANGE (protected)

- The deployment-pattern and architecture-family definitions + decision tables
  (`def:deployment-patterns`, `def:arch-families`, `tab:deployment-heuristics`,
  `tab:arch-decision`) — single source of truth.
- The fairness definitions and impossibility proposition (381-416) content — correct;
  only the *label* changes (MUST_FIX #1), not the math or prose.
- SR 11-7 three-lines + checklist (453-469); GDPR/MiFID treatment (480-489).
- The honest figure caveats in `exercises.ipynb` cell [1] — keep the warnings.
- Open-research-problems + "Path Forward" close (562-590).

## BOOK_WIDE_ITEMS

- B1. Duplicate label `def:calibration` (ch06 ↔ ch07). [cross-chapter]
- B2. Stale pre-reorder folder numbering surviving in prose/tables ("Six chapters ago",
  `tab:chapter-map` Ch.1–7). Audit other near-final chapters for the same artifact.
- B3. External verification of SSRN working-paper citations and the FinanceBench 80% /
  benchmark figures. [citation]
