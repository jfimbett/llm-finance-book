# /audit-bibliography

## Purpose

Check `bibliography.bib` for missing required fields, duplicate keys, uncited entries, and undefined cite keys.

## When to Invoke

Before final book compilation, or after adding new references.

## Inputs Required

- `book/bibliography.bib`
- All `.tex` files in `book/` (to find `\cite{}` usages)

## Steps

1. Parse `bibliography.bib`: collect all entry keys and check each entry for required fields:
   - `@article`: author, title, journal, year
   - `@book`: author, title, publisher, year
   - `@inproceedings`: author, title, booktitle, year
2. Collect all `\cite{KEY}` usages from all `.tex` files in `book/`.
3. Find duplicate BibTeX keys (same key defined twice in `.bib`).
4. Find entries in `.bib` with missing required fields.
5. Find `.bib` entries never cited in any `.tex` file (uncited entries).
6. Find `\cite{KEY}` references with no matching `.bib` entry (undefined keys).
7. Print a four-section report and save to `docs/quality/bibliography-audit.md`.

## Expected Output

Four-section report: missing fields / duplicates / uncited entries / undefined cite keys. Saved to `docs/quality/`.

## Error Handling

- If `bibliography.bib` is empty or missing: print a warning and exit 0.
- If `docs/quality/` does not exist: create it before saving.
