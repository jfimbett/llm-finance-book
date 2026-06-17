# /draft-lecture

## Purpose

Generate lecture notes, a 2-hour Beamer slide deck, and a separate 1-hour practical session slide deck from an existing book chapter, using the lecture-writer and pedagogy-reviewer agents.

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
   - `slides.tex` content (2-hour main lecture Beamer deck, ~20–25 frames)
   - `practical.tex` content (1-hour practical session Beamer deck, ~10–15 frames)
4. Write the returned notes content to `course/lectures/NN-name/notes.md`.
5. Write the returned slides content to `course/lectures/NN-name/slides.tex`.
6. Write the returned practical content to `course/lectures/NN-name/practical.tex`.
7. **Invoke the pedagogy-reviewer agent** on the new `notes.md`: ask it to check learning objectives, coverage, difficulty progression, and whether the practical session complements the lecture. Address any BLOCKER issues by re-invoking the lecture-writer agent with specific corrections.
8. **Invoke the editor agent** on `notes.md`: improve clarity without changing content.
9. Run `/score-content course/lectures/NN-name/notes.md` to get quality scores.
10. Compile both slide decks: for each of `slides.tex` and `practical.tex`, run `pdflatex -interaction=nonstopmode` from its directory. Report OK/FAIL for each.
11. Commit: `git add course/lectures/NN-name/notes.md course/lectures/NN-name/slides.tex course/lectures/NN-name/practical.tex && git commit -m "feat(lecNN): draft [topic name] lecture and practical"`

## Expected Output

- `notes.md` — comprehensive notes covering all 2-hour lecture content
- `slides.tex` — 2-hour main lecture Beamer deck (~20–25 frames)
- `practical.tex` — 1-hour practical session Beamer deck (~10–15 frames) with hands-on exercises and worked examples
- Both PDFs compiled without errors

## Error Handling

- If chapter is still placeholder: stop immediately and print "Run /draft-chapter for chapter NN-name first."
- If pedagogy-reviewer finds BLOCKERs: fix before committing (do not skip). MAJORs and ADVISORYs may be left as inline TODOs.
- If either PDF fails to compile: print the first error from the `.log` file and stop before committing.
