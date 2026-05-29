# /topic-status

## Purpose

Print a status table showing the state of every chapter, lecture, and appendix in the project.

## When to Invoke

At any time to get a project overview: which chapters and appendices are drafted, scored, and released.

## Inputs Required

- None — the skill reads the file system and `docs/quality/`.

## Steps

1. Find all directories in `book/chapters/` matching the `NN-name` pattern, sorted numerically.
2. Also find all directories in `book/appendices/` matching the `A-name` pattern (single uppercase letter prefix), sorted alphabetically.
3. For each chapter and appendix:
   a. Check if `chapter.tex` has real content (not placeholder): Draft = Yes/No
   b. Look for the quality score JSON in `docs/quality/`:
      - Chapter: `book_chapters_NN-name_chapter-score.json`
      - Appendix: `book_appendices_A-name_chapter-score.json`
      Scored = Yes/No
   c. If scored: read each dimension score from the JSON
   d. Check `docs/STATUS.md` for the Released column value
4. Print a markdown table for chapters:
   ```
   ## Chapters

   | # | Topic | Draft | Scored | Clarity | Rigor | Completeness | Pedagogy | Style | Released |
   |---|-------|-------|--------|---------|-------|--------------|----------|-------|----------|
   | 01 | Introduction | Yes | Yes | 8 | 7 | 8 | 7 | 8 | No |
   ```
5. Print a second table for appendices (skip if none exist):
   ```
   ## Appendices

   | # | Topic | Draft | Scored | Clarity | Rigor | Completeness | Pedagogy | Style | Released |
   |---|-------|-------|--------|---------|-------|--------------|----------|-------|----------|
   | A | Math Review | Yes | No | - | - | - | - | - | No |
   ```
6. Print a summary line: `X chapters drafted, Y passing all dimensions, Z released. A appendices drafted, B passing all dimensions, C released.`

## Expected Output

Printed status tables (one for chapters, one for appendices) and a summary line.

## Error Handling

- If no chapters exist: print "No chapters found. Run /new-topic to create the first one."
- If no appendices exist: omit the appendices table entirely.
- If quality score files use a different naming convention: note the mismatch and show "?" for that entry's scores.
