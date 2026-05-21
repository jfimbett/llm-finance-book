# /score-content

## Purpose

Score a single content file on 5 dimensions and write a JSON quality report to `docs/quality/`.

## When to Invoke

After any content draft is complete, before committing, or when checking quality status. Also triggered automatically by the `score-on-save.sh` hook.

## Inputs Required

- File path: a `.tex` or `.md` content file (e.g., `book/chapters/01-intro/chapter.tex`)
- `TOPIC.md` — for `quality_threshold`

## Steps

1. Verify the file exists at the given path. If not, print an error and exit.
2. Read `quality_threshold` from `TOPIC.md` YAML front matter. Default to 7 if not found.
3. **Invoke the scorer agent**: provide the file content and threshold. The scorer reads the file, applies the 5-dimension rubric, and returns scores + justifications.
4. The scorer writes the JSON report to `docs/quality/[sanitized-filename]-score.json` where `[sanitized-filename]` is the file path with `/` replaced by `_` and the file extension removed, then `-score` appended. Example: `book/chapters/01-intro/chapter.tex` → `book_chapters_01-intro_chapter-score.json`.
5. Print the summary table returned by the scorer:
   ```
   === Quality Score: [filename] ===
   Clarity:      N/10  — <justification>
   Rigor:        N/10  — <justification>
   Completeness: N/10  — <justification>
   Pedagogy:     N/10  — <justification>
   Style:        N/10  — <justification>
   Overall:      N.N/10
   Status:       PASS / FAIL (threshold: N)
   ```
6. Run `bash .claude/hooks/update-status.sh` (or manually update `docs/STATUS.md` if the hook is not yet installed) to refresh the chapter status table.

## Expected Output

A JSON file at `docs/quality/[filename]-score.json` and a printed summary. `docs/STATUS.md` refreshed.

## Error Handling

- If the file is a placeholder (contains "invoke /draft-" text): print a warning "File appears to be a placeholder — score may not be meaningful" and proceed.
- If `TOPIC.md` is missing: default threshold to 7 and warn the user.
- If `docs/quality/` does not exist: create it before writing the report.
