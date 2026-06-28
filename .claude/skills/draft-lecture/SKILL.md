# /draft-lecture

## Purpose

Generate lecture notes, a 2-hour HTML slide deck, and a separate 1-hour practical session HTML slide deck from an existing book chapter, using the lecture-writer and pedagogy-reviewer agents.

## When to Invoke

After `/draft-chapter` has produced real content in the corresponding `chapter.tex`. Do not run on placeholder chapters.

## Inputs Required

- Lecture number/name (e.g., `01-intro`) — paired chapter must exist
- `book/chapters/NN-name/chapter.tex` — the source chapter with real content

## Steps

1. Read `book/chapters/NN-name/chapter.tex` and `TOPIC.md`.
2. Check that `chapter.tex` contains real content (not placeholder). If still placeholder, stop and prompt the user to run `/draft-chapter` first.
3. **Invoke the lecture-writer agent**: provide the full chapter content and ask it to produce:
   - `notes.md` content (comprehensive lecture notes for the full 2-hour session)
   - `index.html` content (2-hour main lecture HTML deck, ~20–25 slides)
   - `practical.html` content (1-hour practical session HTML deck, ~10–15 slides)
4. Write the returned notes content to `course/lectures/NN-name/notes.md`.
5. Write the returned lesson deck content to `course/slides-html/NN-name/index.html`.
6. Write the returned practical deck content to `course/slides-html/NN-name/practical.html`.
7. **Invoke the pedagogy-reviewer agent** on the new `notes.md`: ask it to check learning objectives, coverage, difficulty progression, and whether the practical session complements the lecture. Address any BLOCKER issues by re-invoking the lecture-writer agent with specific corrections.
8. **Invoke the editor agent** on `notes.md`: improve clarity without changing content.
9. Run `/score-content course/lectures/NN-name/notes.md` to get quality scores.
10. Validate both HTML decks: for each of `index.html` and `practical.html`, run `node course/slides-html/tools/validate.mjs <file>` from the repo root. Report OK/FAIL for each. On FAIL, fix the HTML before committing.
11. Commit: `git add course/lectures/NN-name/notes.md course/slides-html/NN-name/index.html course/slides-html/NN-name/practical.html && git commit -m "feat(lecNN): draft [topic name] lecture and practical"`

## Expected Output

- `course/lectures/NN-name/notes.md` — comprehensive notes covering all 2-hour lecture content
- `course/slides-html/NN-name/index.html` — 2-hour main lecture HTML deck (~20–25 slides) per AUTHORING.md
- `course/slides-html/NN-name/practical.html` — 1-hour practical session HTML deck (~10–15 slides) with hands-on exercises and worked examples
- Both decks validated without errors

## Error Handling

- If chapter is still placeholder: stop immediately and print "Run /draft-chapter for chapter NN-name first."
- If pedagogy-reviewer finds BLOCKERs: fix before committing (do not skip). MAJORs and ADVISORYs may be left as inline TODOs.
- If either HTML deck fails validation: print the error from the validator and stop before committing.
