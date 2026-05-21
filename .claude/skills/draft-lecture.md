# /draft-lecture

## Purpose

Generate lecture notes and Beamer slides from an existing book chapter, using the lecture-writer and pedagogy-reviewer agents.

## When to Invoke

After `/draft-chapter` has produced real content in the corresponding `chapter.tex`. Do not run on placeholder chapters.

## Inputs Required

- Lecture number/name (e.g., `01-intro`) — paired chapter must exist
- `book/chapters/NN-name/chapter.tex` — the source chapter with real content

## Steps

1. Read `book/chapters/NN-name/chapter.tex` and `TOPIC.md`.
2. Check that `chapter.tex` contains real content (not placeholder). If still placeholder, stop and prompt the user to run `/draft-chapter` first.
3. **Invoke the lecture-writer agent**: provide the full chapter content and ask it to produce notes.md content and slides.tex content, identifying the 3–5 core lecture ideas.
4. Write the returned notes content to `course/lectures/NN-name/notes.md`.
5. Write the returned slides content to `course/lectures/NN-name/slides.tex`.
6. **Invoke the pedagogy-reviewer agent** on the new `notes.md`: ask it to check learning objectives, coverage, and difficulty progression. Address any BLOCKER issues by re-invoking the lecture-writer agent with specific corrections.
7. **Invoke the editor agent** on `notes.md`: improve clarity without changing content.
8. Run `/score-content course/lectures/NN-name/notes.md` to get quality scores.
9. Commit: `git add course/lectures/NN-name/notes.md course/lectures/NN-name/slides.tex && git commit -m "feat(lecNN): draft [topic name] lecture"`

## Expected Output

Populated `notes.md` and `slides.tex` with real lecture content, quality-scored, committed.

## Error Handling

- If chapter is still placeholder: stop immediately and print "Run /draft-chapter for chapter NN-name first."
- If pedagogy-reviewer finds BLOCKERs: fix before committing (do not skip). MAJORs and ADVISORYs may be left as inline TODOs.
