# /audit-book-quality

## Purpose

Book-wide quality audit: fan out `/audit-chapter-quality` across **every chapter in
`main.tex` reading order** (modelled on `/audit-hallucinations`), then build the
cross-chapter book-level reports and the aggregate scorecard. **Audit only — no edits.**

## When to Invoke

- The first phase of the book-quality goal system, before any editing.
- A full re-audit after an editing sweep (or use `/book-quality-regression`).

## Inputs Required

- `book/main.tex` (reading order), all `book/chapters/*/chapter.tex`,
  `book/bibliography.bib`, `TOPIC.md`, `docs/quality/RUBRIC.md`, `score-schema.json`.

## Steps

1. **Derive reading order** from `book/main.tex` `\include` list. Build the
   reading-index ↔ slug table. If it differs from `RUBRIC.md`, update `RUBRIC.md`'s
   table and note it.
2. **Ensure output dir** `docs/quality/book-quality/` and `.../chapters/`.
3. **Fan out per chapter.** For each chapter in reading order, run the
   `/audit-chapter-quality` unit. Run independent chapters **in parallel** (batch the
   agent dispatches; do not serialize). Each produces its five per-chapter files.
4. **Book-level cross-chapter passes** (run once, across all chapters):
   - `concept-ordering-auditor` book-wide → `CONCEPT_DEPENDENCY_MAP.md` and the
     repetition analysis → `REPETITION_MAP.md` (single-source-of-truth assignments for
     attention, transformers, LoRA, RAG, calibration, regulatory frameworks, SHAP,
     AUROC, WACC/CAPM).
   - `finance-auditor` roll-up → `FINANCE_EXAMPLES_MAP.md` (incl. orphaned
     `exercises/valuation_example/` integration target).
   - `citation-description-auditor` book-wide → `CITATION_DESCRIPTION_AUDIT.md`
     (hygiene + description accuracy; seed issues: `wei2022emergent` dup, `xu2024stock`
     stub, `fama1970efficient` mis-cite, `kang2023hallucination` verify, stale `.bib`).
   - `code-figure-auditor` roll-up → `CODE_FIGURE_AUDIT.md`.
5. **Aggregate scorecard.** Write `BOOK_SCORE.json` (scope `book`): per book-level
   dimension 0–100 + `pass`, plus an array of chapter pass/fail. Book `pass` requires
   all of: every chapter passes; every book-level dimension ≥ 90; book compiles; no
   broken refs; no unresolved cites; no duplicate labels; no stale critical reports.
   (Compile/ref/cite/label checks are confirmed by `/book-quality-regression`; if not
   yet run, mark them `unverified` and book `pass:false`.)
6. **Backlog.** Merge every chapter's book-wide items + the seed-issue list into
   `IMPLEMENTATION_BACKLOG.md`, prioritized (BLOCKER→MAJOR→MINOR), each with target
   dimension, owning chapter/SSOT, and recommended action.
7. **Write `BOOK_SCORE.md`** (human-readable summary table + below-90 heatmap) and
   **print** the console summary.

## Expected Output

Under `docs/quality/book-quality/`: per-chapter dirs (5 files each) + `BOOK_SCORE.json`,
`BOOK_SCORE.md`, `CONCEPT_DEPENDENCY_MAP.md`, `REPETITION_MAP.md`,
`FINANCE_EXAMPLES_MAP.md`, `CITATION_DESCRIPTION_AUDIT.md`, `CODE_FIGURE_AUDIT.md`,
`IMPLEMENTATION_BACKLOG.md`. Console:

```
=== Book Quality Audit (reading order) ===
| Read# | Slug | Pass | Below-90 dimensions |
| 1 | 01-intro | NO | non_repetition, completeness |
...
Chapters passing: M/16
Book-level pass: NO
Backlog items: N (BLOCKER B, MAJOR J, MINOR M)
Next: /iterate-book-quality <chNN>  then  /book-quality-regression
```

## Error Handling

- No chapters found: print "run /draft-chapter first" and stop.
- A chapter unit errors: mark it ERROR in the table, continue the others.
- Keep this skill **read-only** w.r.t. `chapter.tex` and `bibliography.bib`. Heavy jobs
  (compile, notebook execution) are deferred to `/book-quality-regression`.
- Auto-commit: the PostToolUse hook may commit the written reports; that is expected.
