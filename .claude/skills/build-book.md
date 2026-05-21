# /build-book

## Purpose

Compile the full LaTeX book to PDF using pdflatex + biber.

## When to Invoke

To check compilation or produce the final PDF. Run from the repository root; the skill handles the `cd book/` internally.

## Inputs Required

- `book/main.tex` must exist
- pdflatex and biber must be installed

## Steps

1. Verify `book/main.tex` exists. If not, print an error and exit.
2. Change to the `book/` directory.
3. Run: `pdflatex -interaction=nonstopmode main.tex`
4. Run: `biber main`
5. Run: `pdflatex -interaction=nonstopmode main.tex` (second pass for cross-references)
6. Run: `pdflatex -interaction=nonstopmode main.tex` (third pass for final references)
7. Check `book/main.log` for lines starting with `! ` (LaTeX errors). If found, print each error line and exit with status 1.
8. If clean: print `Book compiled successfully — output: book/main.pdf`.

## Expected Output

`book/main.pdf` if compilation succeeds. Clear error output if it fails.

## Error Handling

- If `pdflatex` is not found: print "Install TeX Live or MiKTeX and ensure pdflatex is in PATH."
- If `biber` is not found: print "Install biber (included in TeX Live full installation)."
- If compilation fails with errors: print the specific error lines from `main.log`.
