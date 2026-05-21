# /build-slides

## Purpose

Compile all Beamer slide files across all lectures.

## When to Invoke

To produce PDF slides for all lectures, or to check that slides compile after editing.

## Inputs Required

- At least one `slides.tex` file in `course/lectures/`

## Steps

1. Find all `course/lectures/*/slides.tex` files.
2. If none found: print "No slides files found" and exit.
3. For each `slides.tex`: change to its directory and run `pdflatex -interaction=nonstopmode slides.tex`.
4. Check the corresponding `.log` file for `! ` errors.
5. Report: `OK lecture/NN-name/slides` or `FAIL lecture/NN-name/slides — [error summary]` for each.
6. Print summary: `N of M lectures compiled successfully`.

## Expected Output

One PDF per lecture slides file. Summary of pass/fail per lecture.

## Error Handling

- If a lecture's slides fail: continue compiling the remaining lectures (do not stop on first failure).
- If pdflatex is not found: print the install instructions and exit.
