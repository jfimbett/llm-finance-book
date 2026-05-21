# /release-chapter

## Purpose

Mark a chapter as released after it passes all quality gates: score threshold, clean references, proofreader pass, and successful compilation.

## When to Invoke

When a chapter is ready for students or readers — after all drafting, reviewing, and refinement is done.

## Inputs Required

- Chapter number/name (e.g., `01-intro`)

## Steps

1. **Quality score gate**: run `/score-content book/chapters/NN-name/chapter.tex`. If any dimension is below `quality_threshold`, abort and print "Gate FAILED: quality scores. Run /refine-until-threshold first."
2. **Reference gate**: run `/audit-cross-refs`. If broken refs or missing citations are found in the chapter, abort and print "Gate FAILED: broken references. Fix refs before releasing."
3. **Proofreader gate**: invoke the proofreader agent on `chapter.tex`. If the verdict is not `PASS`, fix all errors and re-run. Abort release if errors remain.
4. **Compilation gate**: run `/build-book`. If compilation fails, abort and print the error.
5. All gates passed: update `docs/STATUS.md` — set `Released = Yes` for this chapter.
6. Commit: `git add book/chapters/NN-name/ docs/STATUS.md && git commit -m "release(chNN): [topic name] chapter passes all quality gates"`

## Expected Output

Chapter committed with a release commit message. `docs/STATUS.md` updated with `Released = Yes`.

## Error Handling

- Any gate failure aborts the release process immediately. Print which gate failed and what the user needs to fix.
- Do not commit if any gate fails.
