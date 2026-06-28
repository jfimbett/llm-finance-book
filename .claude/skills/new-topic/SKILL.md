# /new-topic

## Purpose

Scaffold a new numbered chapter/lecture/notebook unit, or a lettered appendix, with all required placeholder files.

## When to Invoke

When the user wants to add a new topic (chapter or appendix) to the book/course. Run before `/draft-chapter` or `/draft-lecture`.

## Inputs Required

- **Type**: chapter or appendix — ask the user if not clear from context
- **Chapter**: topic number (e.g., `02`) and short name (e.g., `linear-algebra`)
- **Appendix**: topic letter (e.g., `A`) and short name (e.g., `math-review`)
- `TOPIC.md` — for project configuration
- Optional: a raw section outline provided by the user in the invocation arguments

---

## Steps — Chapter Mode (default)

1. Ask the user for the topic number (two digits, e.g., `02`) and short name (kebab-case, e.g., `linear-algebra`) if not already provided in the invocation.
2. Check that `book/chapters/NN-name/` does not already exist — if it does, ask the user whether to overwrite or choose a different number.
3. **Run the outline-curator agent** (`.claude/agents/outline-curator.md`) on the user-provided section list (or on a minimal default outline if none was given). Apply the refined outline from the agent's output — use its approved sections as the section structure for all files created in steps 4–9. If the agent returns `STATUS: NEEDS_REVISION`, address the outstanding items and re-run the agent until `STATUS: APPROVED`.
4. Create `book/chapters/NN-name/chapter.tex` using the approved outline: one `\section{}` per top-level section, one `\subsection{}` per subsection, each with a `[Placeholder]` body and correct `\label` tags.
5. Create `book/chapters/NN-name/figures/.gitkeep`.
6. Create `course/lectures/NN-name/notes.md` with header `# Lecture N: [Topic Name]`, learning objectives derived from the approved outline (one per major section), and one `## N. [Section]` heading per top-level section with a `[Placeholder]` body. Include a **Further Reading** footer pointing to the companion book chapter.
7. Create stub HTML slide decks under `course/slides-html/NN-name/`: both `index.html` (lesson) and `practical.html` (practical session), each containing the required boilerplate from `course/slides-html/AUTHORING.md` — a title slide plus one section-divider slide per top-level section from the approved outline. Load shared assets via `../assets/slides.css` and `../assets/slides.js`.
8. Create `course/lectures/NN-name/exercises.md` with three placeholder exercises (one `[B]` beginner, one `[I]` intermediate, one `[A]` advanced), each tied to a section from the approved outline.
9. Create `course/lectures/NN-name/solutions.md` with three placeholder solutions matching the exercises.
10. Create `code/notebooks/NN-name/demo.ipynb` and `code/notebooks/NN-name/exercises.ipynb` — minimal valid notebooks with one markdown cell each describing the chapter topic.
11. Update `docs/STATUS.md` — append a new row: `| NN | [Topic Name] | No | No | — | — | — | — | — | No |`

**Step 12: Update `book/main.tex` to include the new chapter**

Open `book/main.tex` and find the `% Add new chapters here` comment. Add the following line immediately before it:

```latex
\include{chapters/NN-name/chapter}
```

Replace `NN-name` with the actual chapter directory segment (e.g., `02-linear-algebra`). This ensures the chapter is compiled when you run `/build-book`.

13. **Re-run outline-curator on the created `chapter.tex`** as a final check: read the section/subsection headings from the file, pass them to the agent, and verify `STATUS: APPROVED`. If not, fix the file and repeat until approved.
14. Run `bash scripts/validate-scaffold.sh` to verify the new directories exist.
15. Stage and commit: `git add book/chapters/NN-name course/lectures/NN-name course/slides-html/NN-name code/notebooks/NN-name docs/STATUS.md book/main.tex && git commit -m "chore: scaffold topic NN-name"`

---

## Steps — Appendix Mode

Use this mode when the user asks to create an appendix (e.g., "add appendix A on math review").

1. Ask the user for the appendix letter (single uppercase letter, e.g., `A`) and short name (kebab-case, e.g., `math-review`) if not already provided.
2. Check that `book/appendices/A-name/` does not already exist — if it does, ask the user whether to overwrite or choose a different letter.
3. **Run the outline-curator agent** on the user-provided section list (or a minimal default outline). Apply the approved outline. If the agent returns `STATUS: NEEDS_REVISION`, fix and re-run until `STATUS: APPROVED`.
4. Create `book/appendices/A-name/chapter.tex` using the approved outline: one `\section{}` per top-level section, one `\subsection{}` per subsection, each with a `[Placeholder]` body and correct `\label` tags. The file starts with `\chapter{[Appendix Title]}` (no number prefix — LaTeX handles lettering via `\appendix`).
5. Create `book/appendices/A-name/figures/.gitkeep`.
6. **No course lecture files** — appendices are book-only (no notes.md, index.html/practical.html under course/slides-html/, exercises.md, solutions.md, or notebooks).
7. Update `docs/STATUS.md` — append a new row in the appendices section: `| A | [Appendix Name] | No | No | — | — | — | — | — | No |`. If an appendices section doesn't exist yet, add a `## Appendices` header before it.

**Step 8: Update `book/main.tex` to include the new appendix**

Open `book/main.tex` and find the `% Add new appendices here` comment (it is under the `\appendix` command in the backmatter area). Add the following line immediately before that comment:

```latex
\include{appendices/A-name/chapter}
```

Replace `A-name` with the actual appendix directory segment (e.g., `A-math-review`).

9. **Re-run outline-curator on the created `chapter.tex`** as a final check. Verify `STATUS: APPROVED`.
10. Stage and commit: `git add book/appendices/A-name docs/STATUS.md book/main.tex && git commit -m "chore: scaffold appendix A-name"`

---

## Expected Output

**Chapter**: Three new directories with section-structured placeholder files. `docs/STATUS.md` updated. Changes committed.

**Appendix**: One new directory (`book/appendices/A-name/`) with `chapter.tex` and `figures/`. `docs/STATUS.md` updated. Changes committed.

## Error Handling

- If the topic/appendix identifier already exists: stop and ask the user to confirm overwrite or choose a different identifier.
- If `docs/STATUS.md` cannot be found: create it with the standard header before appending the row.
- If the scaffold validation fails after creation: report which paths are missing.
- If the outline-curator returns `STATUS: NEEDS_REVISION` after three iterations: surface the remaining issues to the user and ask for guidance before proceeding.
