# /release-chapter

## Purpose

Mark a chapter or appendix as released after it passes all quality gates: score threshold, clean references, proofreader pass, and successful compilation.

## When to Invoke

When a chapter or appendix is ready for students or readers — after all drafting, reviewing, and refinement is done.

## Inputs Required

- Chapter identifier (e.g., `01-intro`) or appendix identifier (e.g., `A-math-review`)

## Path Resolution

Determine the target file and commit scope from the identifier format:

- **Chapter** (numeric prefix, e.g., `01-intro`): path = `book/chapters/01-intro/`, score file = `book_chapters_01-intro_chapter-score.json`, commit scope = `chNN`
- **Appendix** (single uppercase letter prefix, e.g., `A-math-review`): path = `book/appendices/A-math-review/`, score file = `book_appendices_A-math-review_chapter-score.json`, commit scope = `appA`

## Steps

1. Resolve the path and commit scope using the identifier (see Path Resolution above).
2. **Quality score gate**: run `/score-content [resolved path]/chapter.tex`. If any dimension is below `quality_threshold`, abort and print "Gate FAILED: quality scores. Run /refine-until-threshold first."
3. **Reference gate**: run `/audit-cross-refs`. If broken refs or missing citations are found, abort and print "Gate FAILED: broken references. Fix refs before releasing."
4. **Proofreader gate**: invoke the proofreader agent on `chapter.tex`. If the verdict is not `PASS`, fix all errors and re-run. Abort release if errors remain.
5. **Compilation gate**: run `/build-book`. If compilation fails, abort and print the error.
6. All gates passed: update `docs/STATUS.md` — set `Released = Yes` for this entry.
7. Commit:
   - Chapter: `git add book/chapters/NN-name/ docs/STATUS.md && git commit -m "release(chNN): [topic name] chapter passes all quality gates"`
   - Appendix: `git add book/appendices/A-name/ docs/STATUS.md && git commit -m "release(appA): [topic name] appendix passes all quality gates"`

## Expected Output

Chapter or appendix committed with a release commit message. `docs/STATUS.md` updated with `Released = Yes`.

## Error Handling

- Any gate failure aborts the release process immediately. Print which gate failed and what the user needs to fix.
- Do not commit if any gate fails.
