# /draft-exercises

## Purpose

Generate exercises and verified model solutions for a lecture using the exercise-designer and math-checker agents.

## When to Invoke

After `/draft-lecture` has produced real lecture notes for the corresponding topic.

## Inputs Required

- Lecture number/name (e.g., `01-intro`)
- `course/lectures/NN-name/notes.md` — the source lecture notes

## Steps

1. Read `course/lectures/NN-name/notes.md` and `TOPIC.md`.
2. Check that `notes.md` contains real content. If placeholder, stop and prompt to run `/draft-lecture` first.
3. **Invoke the exercise-designer agent**: provide the lecture notes and audience level from `TOPIC.md`. Ask for one [B], one [I], and one [A] exercise with model solutions.
4. Write exercises content to `course/lectures/NN-name/exercises.md`.
5. Write solutions content to `course/lectures/NN-name/solutions.md`.
6. **Invoke the math-checker agent** on `solutions.md`: verify all solutions are mathematically correct. If FAIL, re-invoke the exercise-designer agent with the specific failing solutions for correction. Repeat until PASS.
7. Commit: `git add course/lectures/NN-name/exercises.md && git commit -m "feat(lecNN): add exercises and solutions"`
   Note: `solutions.md` is gitignored — it will not appear in the commit.

## Expected Output

`exercises.md` with 3+ exercises (one per difficulty tier), `solutions.md` with verified model solutions.

## Error Handling

- If lecture notes are placeholder: stop and prompt to run `/draft-lecture` first.
- If math-checker fails solutions after 2 iterations: commit exercises without solutions and flag as `[SOLUTIONS_NEED_REVIEW]` in commit message.
