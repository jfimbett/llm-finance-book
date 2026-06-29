# /book-quality-regression

## Purpose

The final/regression gate. After an editing sweep, re-run the objective book-wide checks
and re-aggregate the scorecard to confirm nothing regressed and to evaluate the
**book-level pass condition**. Run last, after `/iterate-book-quality`.

## When to Invoke

- After a round of `/iterate-book-quality` edits, before declaring the book done.
- Periodically, to detect regressions introduced by ordinary edits.

## Inputs Required

- `book/` (compilable), `docs/quality/book-quality/` (existing audit outputs),
  `docs/quality/RUBRIC.md`.

## Steps

1. **Build the book.** Run `scripts/build-book.sh` (pdflatex + biber + pdflatex). Capture
   errors. Record `compiles: true/false` and any LaTeX errors.
2. **Bibliography checks (fresh).** Run `/audit-bibliography`. Confirm: no duplicate keys
   (e.g. `wei2022emergent`), no stub entries (`xu2024stock`), all cited keys resolve, no
   stale `.bib` confusion. Record results — **do not trust the old
   `docs/quality/bibliography-audit.md`; regenerate it.**
3. **Cross-reference checks.** Run `/audit-cross-refs` + the `check-refs.sh` logic:
   every `\ref`/`\eqref`/`\cite` resolves; no duplicate labels (e.g. `def:calibration`);
   no dangling figure refs (`fig:ch11-rag-pipeline`). Also scan for hard-coded
   "Chapter N" prose references that should be `\Cref{ch:...}`.
4. **Concept-ordering re-check.** Re-run `concept-ordering-auditor` book-wide; confirm no
   new use-before-definition was introduced; refresh `CONCEPT_DEPENDENCY_MAP.md` and
   `REPETITION_MAP.md`.
5. **Repetition re-check.** Confirm single-source-of-truth assignments hold and later
   occurrences are `\ref`-based reminders, not re-derivations.
6. **Code/figure re-check** (where applicable): re-run `code-figure-auditor`; confirm no
   new dangling figure refs and that touched figures still match prose.
7. **Re-score aggregation.** Re-read every chapter `score.json` (re-run
   `/audit-chapter-quality` for any chapter edited since its last score). Recompute
   `BOOK_SCORE.json` / `BOOK_SCORE.md`.
8. **Evaluate book pass.** `book.pass = true` iff: every chapter passes; every book-level
   dimension ≥ 90; `compiles:true`; no broken refs; no unresolved cites; no duplicate
   labels; no stale critical reports. Otherwise list exactly what blocks it.
9. **Write the final report** and print the console summary.

## Expected Output

- Refreshed `BOOK_SCORE.json`, `BOOK_SCORE.md`, `CONCEPT_DEPENDENCY_MAP.md`,
  `REPETITION_MAP.md`, fresh `docs/quality/bibliography-audit.md`.
- A `docs/quality/book-quality/REGRESSION_REPORT.md` capturing build/bib/ref/order/score
  results for this pass.
- Console:
  ```
  === Book Quality Regression ===
  Compiles:            YES
  Duplicate bib keys:  0
  Broken refs/cites:   0
  Duplicate labels:    0
  Use-before-def:      0
  Chapters passing:    16/16
  Book-level pass:     YES / NO (blocked by: …)
  ```

## Error Handling

- Build fails: record the LaTeX error, set `compiles:false`, book `pass:false`, point at
  the offending file/line, and stop before claiming pass.
- A check tool is unavailable: mark that gate `unverified`, set book `pass:false`, continue.
- This skill may edit only generated reports — never `chapter.tex`. Fixes go through
  `/iterate-book-quality`.
- Do not declare the book done unless every gate is green this run (no trusting stale reports).
