# /topic-status

## Purpose

Print a status table showing the state of every chapter and lecture in the project.

## When to Invoke

At any time to get a project overview: which chapters are drafted, scored, and released.

## Inputs Required

- None — the skill reads the file system and `docs/quality/`.

## Steps

1. Find all directories in `book/chapters/` matching the `NN-name` pattern, sorted numerically.
2. For each chapter:
   a. Check if `chapter.tex` has real content (not placeholder): Draft = Yes/No
   b. Look for `docs/quality/book_chapters_NN-name_chapter-score.json`: Scored = Yes/No
   c. If scored: read each dimension score from the JSON
   d. Check `docs/STATUS.md` for the Released column value
3. Print a markdown table:
   ```
   | # | Topic | Draft | Scored | Clarity | Rigor | Completeness | Pedagogy | Style | Released |
   |---|-------|-------|--------|---------|-------|--------------|----------|-------|----------|
   | 01 | Introduction | Yes | Yes | 8 | 7 | 8 | 7 | 8 | No |
   ```
4. Print a summary line: `X chapters drafted, Y passing all dimensions, Z released`.

## Expected Output

A printed status table and summary.

## Error Handling

- If no chapters exist: print "No chapters found. Run /new-topic to create the first one."
- If quality score files use a different naming convention: note the mismatch and show "?" for that chapter's scores.
