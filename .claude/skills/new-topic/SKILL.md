# /new-topic

## Purpose

Scaffold a new numbered chapter/lecture/notebook unit with all required placeholder files.

## When to Invoke

When the user wants to add a new topic to the course. Run before `/draft-chapter` or `/draft-lecture`.

## Inputs Required

- Topic number (e.g., `02`) and short name (e.g., `linear-algebra`) — ask the user if not provided
- `TOPIC.md` — for project configuration
- Optional: a raw section outline provided by the user in the invocation arguments

## Steps

1. Ask the user for the topic number (two digits, e.g., `02`) and short name (kebab-case, e.g., `linear-algebra`) if not already provided in the invocation.
2. Check that `book/chapters/NN-name/` does not already exist — if it does, ask the user whether to overwrite or choose a different number.
3. **Run the outline-curator agent** (`.claude/agents/outline-curator.md`) on the user-provided section list (or on a minimal default outline if none was given). Apply the refined outline from the agent's output — use its approved sections as the section structure for all files created in steps 4–9. If the agent returns `STATUS: NEEDS_REVISION`, address the outstanding items and re-run the agent until `STATUS: APPROVED`.
4. Create `book/chapters/NN-name/chapter.tex` using the approved outline: one `\section{}` per top-level section, one `\subsection{}` per subsection, each with a `[Placeholder]` body and correct `\label` tags.
5. Create `book/chapters/NN-name/figures/.gitkeep`.
6. Create `course/lectures/NN-name/notes.md` with header `# Lecture N: [Topic Name]`, learning objectives derived from the approved outline (one per major section), and one `## N. [Section]` heading per top-level section with a `[Placeholder]` body. Include a **Further Reading** footer pointing to the companion book chapter.
7. Create `course/lectures/NN-name/slides.tex` with a Beamer template: title frame plus one `\section` frame per top-level section from the approved outline.
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
15. Stage and commit: `git add book/chapters/NN-name course/lectures/NN-name code/notebooks/NN-name docs/STATUS.md book/main.tex && git commit -m "chore: scaffold topic NN-name"`

## Expected Output

Three new directories (`book/chapters/NN-name/`, `course/lectures/NN-name/`, `code/notebooks/NN-name/`) with section-structured placeholder files derived from an outline-curator-approved outline. `docs/STATUS.md` updated with a new row. Changes committed.

## Error Handling

- If the topic number already exists: stop and ask the user to confirm overwrite or pick a new number.
- If `docs/STATUS.md` cannot be found: create it with the standard header before appending the row.
- If the scaffold validation fails after creation: report which paths are missing.
- If the outline-curator returns `STATUS: NEEDS_REVISION` after three iterations: surface the remaining issues to the user and ask for guidance before proceeding.
