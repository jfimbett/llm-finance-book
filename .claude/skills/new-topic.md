# /new-topic

## Purpose

Scaffold a new numbered chapter/lecture/notebook unit with all required placeholder files.

## When to Invoke

When the user wants to add a new topic to the course. Run before `/draft-chapter` or `/draft-lecture`.

## Inputs Required

- Topic number (e.g., `02`) and short name (e.g., `linear-algebra`) — ask the user if not provided
- `TOPIC.md` — for project configuration

## Steps

1. Ask the user for the topic number (two digits, e.g., `02`) and short name (kebab-case, e.g., `linear-algebra`) if not already provided in the invocation.
2. Check that `book/chapters/NN-name/` does not already exist — if it does, ask the user whether to overwrite or choose a different number.
3. Create `book/chapters/NN-name/chapter.tex` with a placeholder matching the intro chapter template (replace "Introduction" with the topic name, update `\label{ch:NN-name}` and all section labels).
4. Create `book/chapters/NN-name/figures/.gitkeep`.
5. Create `course/lectures/NN-name/notes.md` with a placeholder header `# Lecture N: [Topic Name]`, blank learning objectives, and three placeholder sections.
6. Create `course/lectures/NN-name/slides.tex` with a blank Beamer template (title, one section frame).
7. Create `course/lectures/NN-name/exercises.md` with three placeholder exercises (one per difficulty level).
8. Create `course/lectures/NN-name/solutions.md` with three placeholder solutions.
9. Create `code/notebooks/NN-name/demo.ipynb` and `code/notebooks/NN-name/exercises.ipynb` — minimal valid notebooks with one markdown cell each.
10. Update `docs/STATUS.md` — append a new row: `| NN | [Topic Name] | No | No | — | — | — | — | — | No |`
11. Run `bash scripts/validate-scaffold.sh` to verify the new directories exist.
12. Stage and commit: `git add book/chapters/NN-name course/lectures/NN-name code/notebooks/NN-name docs/STATUS.md && git commit -m "chore: scaffold topic NN-name"`

## Expected Output

Three new directories (`book/chapters/NN-name/`, `course/lectures/NN-name/`, `code/notebooks/NN-name/`) with placeholder files. `docs/STATUS.md` updated with a new row. Changes committed.

## Error Handling

- If the topic number already exists: stop and ask the user to confirm overwrite or pick a new number.
- If `docs/STATUS.md` cannot be found: create it with the standard header before appending the row.
- If the scaffold validation fails after creation: report which paths are missing.
