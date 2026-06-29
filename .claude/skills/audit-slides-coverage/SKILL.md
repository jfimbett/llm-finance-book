# /audit-slides-coverage

## Purpose

Detect where the **HTML slide decks teach less than the book chapter** — core concepts that
are missing or under-explained on the slides — using the `slides-coverage-auditor` agent in
parallel across all chapters. The audience for this audit is the **slides-only student**:
someone who attends lectures and studies the slides but never opens the book. The book is
allowed to go deeper; this skill flags only *load-bearing* gaps, not legitimate book-only
depth. **Audit only — makes no edits to slides or chapters.**

## When to Invoke

- After drafting or revising slide decks, to check they still track the book.
- Before releasing a lecture, to confirm a slides-only student can follow it.
- Whenever you suspect the slides have drifted thinner than the book.

## Inputs

- `book/chapters/NN-slug/chapter.tex` for each chapter (the source of truth, collected
  automatically).
- `course/slides-html/NN-slug/index.html` (lesson deck) and `course/slides-html/NN-slug/practical.html`
  (practical deck, if present), matched by the chapter slug.
- `TOPIC.md` for audience/level.

## Arguments

- **No argument** → audit **all** chapters in parallel (default).
- **A chapter identifier** (`ch08`, `08`, or `08-domain-specific-llms`) → audit just that
  one chapter. Resolve it to the `NN-slug` folder before dispatching.

## Steps

1. **Discover chapters.** Glob `book/chapters/*/chapter.tex`, sorted by chapter number. If
   none exist, print "No chapters found — run /draft-chapter first" and exit. If an argument
   was given, filter to the single matching chapter.

2. **Match each chapter to its slide decks.** For `book/chapters/NN-slug/`, locate
   `course/slides-html/NN-slug/index.html` and `course/slides-html/NN-slug/practical.html`.
   - If `index.html` is missing, mark the chapter `NO SLIDES` and skip dispatching it
     (note it in the summary).
   - If `practical.html` is missing, proceed with the lesson deck only and note it.

3. **Ensure output directory.** Create `docs/quality/slides-coverage/` if it does not exist.

4. **Dispatch agents in parallel.** For each chapter with at least a lesson deck, spawn one
   `slides-coverage-auditor` agent in the **same message** (all concurrent — do not wait
   between dispatches). Give each agent:
   - the path to `book/chapters/NN-slug/chapter.tex`,
   - the paths to `course/slides-html/NN-slug/index.html` and `practical.html` (note which
     exist),
   - `TOPIC.md` for audience context,
   - an instruction to follow the `slides-coverage-auditor` spec exactly and return either
     the `WELL-COVERED` verdict block or the full Markdown report verbatim as its final
     message.

5. **Collect results.** For each chapter:
   - `WELL-COVERED` → record as well-covered (no file written).
   - `GAPS FOUND` → save the full report to
     `docs/quality/slides-coverage/chNN-slides-coverage.md` (two-digit `NN`).
   Parse the critical/minor counts from each report's verdict line for the summary.

6. **Print a summary table.**

   ```
   === Slides Coverage Audit Summary ===

   | Chapter | Title                | Slides-only verdict        | Critical | Minor |
   |---------|----------------------|----------------------------|----------|-------|
   | ch01    | Introduction         | can follow end to end      |    0     |   0   |
   | ch02    | LLM Foundations      | falls off at attention     |    3     |   2   |
   ...

   Total chapters audited: N
   Chapters with gaps:     M   (Critical: X, Minor: Y across all chapters)
   Reports saved to: docs/quality/slides-coverage/
   ```

   Fill Critical/Minor from each agent's verdict line (0 for WELL-COVERED). Use the agent's
   one-line "Slides-only student" sentence for the verdict column.

7. **Aggregate report.** Write `docs/quality/slides-coverage/SUMMARY.md` with:
   - the summary table above,
   - a "Chapters Requiring Attention" section: each chapter with gaps, its critical/minor
     counts, the slides-only-student verdict, and its report path, ordered by critical count
     (most urgent first),
   - a "Well-Covered Chapters" section listing chapters that passed,
   - a "Top cross-chapter patterns" section (optional): recurring kinds of gaps you notice
     (e.g., "worked examples consistently book-only," "limitations sections rarely on slides").

8. **Commit.**
   ```
   git add docs/quality/slides-coverage/
   git commit -m "docs: slides coverage audit report"
   ```

## Expected Output

- Per-chapter reports `docs/quality/slides-coverage/chNN-slides-coverage.md` (only for
  chapters with gaps).
- `docs/quality/slides-coverage/SUMMARY.md`.
- Summary table printed to console.

## Error Handling

- Placeholder chapter (`chapter.tex` < 100 lines or contains `% PLACEHOLDER`): skip and mark
  `SKIPPED` in the summary.
- Lesson deck missing (`index.html` absent): mark `NO SLIDES` and skip; this is itself worth
  surfacing (a chapter with no lesson deck is the largest possible coverage gap).
- Practical deck missing: proceed with the lesson deck only; note "lesson-only" in the
  summary for that chapter.
- An agent returns no structured output (neither a verdict block nor a report): mark the
  chapter `ERROR` in the summary and continue; do not fabricate findings.
- `docs/quality/` does not exist: create the full path before saving.
- This skill never edits slides or chapters. If asked to apply fixes, report the gaps and
  defer the slide edits to a separate, explicit request.
