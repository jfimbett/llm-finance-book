# /audit-notation

## Purpose

Check notation consistency across all book chapters using the consistency-checker agent.

## When to Invoke

After writing 2+ chapters, or before any release. Run whenever new notation is introduced.

## Inputs Required

- All `chapter.tex` files in `book/chapters/` (collected automatically)

## Steps

1. Find all `chapter.tex` files: `find book/chapters -name "chapter.tex" | sort`.
2. If no chapters exist or all are placeholders: print "No chapters to audit" and exit.
3. **Invoke the consistency-checker agent**: provide all chapter content. Ask for a symbol table, terminology table, and conflict list.
4. Print the symbol table (markdown table format).
5. Print the terminology table.
6. Print the conflict list.
7. Save the full output to `docs/quality/notation-audit.md`.
8. If conflicts are found: print `ACTION REQUIRED: N notation conflicts found — resolve before release`.
9. Commit: `git add docs/quality/notation-audit.md && git commit -m "docs: notation audit report"`

## Expected Output

Symbol table, terminology table, and conflict list saved to `docs/quality/notation-audit.md` and printed.

## Error Handling

- If `docs/quality/` does not exist: create it.
- If all chapters are placeholders: exit with a note to run `/draft-chapter` first.
