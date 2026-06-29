# /audit-chapter-quality

## Purpose

Run the full multi-agent book-quality audit on **one** chapter: constructive review +
skeptical review + specialized auditors, merged by the audit-editor into a prioritized
plan and a 0–100, 14-dimension scorecard. **Audit only — makes no chapter edits.**
Use `/iterate-book-quality` to apply the plan.

## When to Invoke

- To audit or re-audit a single chapter against [`docs/quality/RUBRIC.md`](../../../docs/quality/RUBRIC.md).
- As the per-chapter unit invoked by `/audit-book-quality`.

## Inputs Required

- A chapter identifier: a folder slug (`05-business-valuation`), a folder number, or a
  reading index. Resolve it to a `chapter.tex` path **and** a reading index using the
  `\include` order in `book/main.tex` (NOT folder order).
- `TOPIC.md`, `docs/quality/RUBRIC.md`, `docs/quality/score-schema.json`.

## Steps

1. **Resolve chapter & reading index.** Parse `book/main.tex`. Map the identifier to
   `book/chapters/NN-slug/chapter.tex` and its reading index. Compute the output dir
   `docs/quality/book-quality/chapters/<read#>-<slug>/` (zero-padded read#, e.g. `09-05-business-valuation` → use `<read#>-<slug>` = `9-05-business-valuation`). Create it.
2. **Dispatch reviewers/auditors in parallel** (one message, multiple agents — do not
   wait between them). Pass each the chapter text, its reading index, `TOPIC.md`, and
   `RUBRIC.md`:
   - `constructive-reviewer` → `constructive-review.md`
   - `skeptical-reviewer` → `skeptical-review.md`
   - `concept-ordering-auditor` (chapter scope, but reads `main.tex` for order)
   - `finance-auditor`
   - `citation-description-auditor` (also reads `book/bibliography.bib`)
   - `code-figure-auditor` (also reads paired `code/notebooks/NN-slug/` + `figures/`)
   - Reuse as needed for correctness: `math-checker`, `fact-checker`,
     `hallucination-detector`, `cross-ref-checker`, `consistency-checker`.
   Save the two review files; keep auditor outputs for the editor.
3. **Editor merge.** Run `audit-editor` on the two reviews + auditor outputs → write
   `editor-plan.md` (MUST_FIX / SHOULD_FIX / OPTIONAL / DO_NOT_CHANGE + book-wide items).
4. **Score.** Produce `score.json` conforming to `docs/quality/score-schema.json`:
   14 dimensions, 0–100, each with `evidence`, `blocking_issues`, `recommended_action`.
   `pass` per dimension = `score >= 90` (or `score: null` for N/A). Chapter `pass` =
   all non-null dimensions ≥ 90. Set `iteration: 0` for an initial audit.
5. **Touch the change-log.** If `change-log.md` does not exist, create it with a header
   and an "Audit only — no edits applied" entry dated today.
6. **Print a summary** (see below).

## Expected Output

Under `docs/quality/book-quality/chapters/<read#>-<slug>/`:
`constructive-review.md`, `skeptical-review.md`, `editor-plan.md`, `score.json`,
`change-log.md`. Console summary:

```
=== Chapter Quality Audit: <read#> <slug> ===
Dimension              Score  Pass
correctness             88     ✗
concept_separation      92     ✓
...
Chapter pass: NO — below 90 on: correctness, completeness
MUST_FIX tasks: 3   Book-wide items routed to backlog: 2
Outputs: docs/quality/book-quality/chapters/<read#>-<slug>/
```

## Error Handling

- Identifier not resolvable in `main.tex`: print the reading-order table and stop.
- Placeholder chapter (<100 lines or contains `% PLACEHOLDER`): mark SKIPPED, write a
  minimal `score.json` with `pass:false` and a note, and stop.
- A reviewer/auditor returns no structured output: record that dimension's score as
  `null` with `recommended_action: "re-run auditor"` and continue; do not fabricate.
- This skill never edits `chapter.tex`. If asked to fix, defer to `/iterate-book-quality`.
