# /audit-cross-refs

## Purpose

Find broken LaTeX references (`\ref{}`, `\cite{}`) and unpaired chapter/lecture directories.

## When to Invoke

Before compiling the book, after editing any `.tex` file, or when the `check-refs.sh` hook reports issues.

## Inputs Required

- All `.tex` files in `book/` (collected automatically)
- `book/bibliography.bib`

## Steps

1. **Invoke the cross-ref-checker agent**: provide all `.tex` content and the `bibliography.bib` content. Ask for a three-section report: broken `\ref{}`, missing `\cite{}`, and unpaired directories.
2. Print the broken references list with file and line information.
3. Print the missing citations list.
4. Print the unpaired chapter/lecture list.
5. Print a summary: `N broken refs, N missing citations, N unpaired directories`.
6. If any issues found: exit with a non-zero status code to signal blocking.

## Expected Output

Three-section report printed to console. Non-zero exit code if issues found.

## Error Handling

- If `bibliography.bib` does not exist: warn and skip the citation check.
- If no `.tex` files exist yet: print "No LaTeX files to audit" and exit 0.
