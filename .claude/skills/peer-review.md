# /peer-review

## Purpose

Simulate a formal academic peer review of a chapter or lecture set using the peer-reviewer agent.

## When to Invoke

When a chapter draft is mature and needs a formal evaluation before release. Best run after `/score-content` passes.

## Inputs Required

- File path: a `chapter.tex` or the lecture directory (e.g., `course/lectures/01-intro/`)

## Steps

1. Verify the file/directory contains real content (not placeholder). If placeholder, stop and prompt to run `/draft-chapter` or `/draft-lecture` first.
2. If a lecture directory is given, read `notes.md` and `exercises.md` together.
3. **Invoke the peer-reviewer agent**: provide the full content and ask for a referee report with a verdict (ACCEPT / MINOR_REVISION / MAJOR_REVISION / REJECT) and numbered comments.
4. Print the full referee report.
5. Save the report to `docs/quality/[chapter-or-lecture]-peer-review.md`.
6. Commit: `git add docs/quality/ && git commit -m "docs(chNN): add peer review report"`

## Expected Output

A printed referee report with summary, verdict, and numbered major/minor comments. Report saved to `docs/quality/`.

## Error Handling

- If content is placeholder: stop immediately.
- If the `docs/quality/` directory does not exist: create it before saving.
