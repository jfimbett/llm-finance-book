# /session-summary

## Purpose

Print a summary of what changed in the current AI session: commits made, quality score changes, and open items.

## When to Invoke

At the end of a work session, or triggered automatically by the `session-log.sh` hook when the session ends.

## Inputs Required

- None — the skill reads git history and quality reports.

## Steps

1. Run `git log --oneline --since="8 hours ago"` to list commits made in this session.
2. Read all JSON files in `docs/quality/` modified today to identify score changes.
3. List files that were modified but not yet committed (`git status`).
4. Print a structured summary:
   ```
   === Session Summary ===
   Commits (last 8h): N
   [list each commit message]
   
   Score changes:
   [file]: N.N → N.N (PASS/FAIL)
   
   Uncommitted changes:
   [list modified files]
   
   Still below threshold:
   [list files with failing dimensions]
   ```
5. The `session-log.sh` hook also appends a one-line version of this summary to `docs/SESSION_LOG.md`.

## Expected Output

A printed session summary.

## Error Handling

- If no commits today: print "No commits in this session."
- If `docs/quality/` is empty: skip score changes section.
