# /draft-code

## Purpose

Generate companion Python code (reusable `src/` modules and demonstration notebooks) for a lecture or chapter using the code-writer and code-reviewer agents.

## When to Invoke

After lecture notes exist for the topic. Can be run any time after `/draft-lecture`.

## Inputs Required

- Lecture/chapter number (e.g., `01-intro`)
- `course/lectures/NN-name/notes.md` or `book/chapters/NN-name/chapter.tex` — the content to base code on

## Steps

1. Read `notes.md` (preferred) or `chapter.tex` and `TOPIC.md`.
2. Identify 2–4 algorithms, methods, or concepts in the content that benefit from hands-on code.
3. **Invoke the code-writer agent**: provide the identified concepts and ask for: (a) Python functions/classes for `code/src/`, (b) `demo.ipynb` cells demonstrating each concept, (c) `exercises.ipynb` exercise stubs with assert tests.
4. Write the returned module code to `code/src/<module_name>.py`.
5. Update `code/notebooks/NN-name/demo.ipynb` with the returned cells.
6. Update `code/notebooks/NN-name/exercises.ipynb` with exercise stubs (create file if it doesn't exist).
7. **Invoke the code-reviewer agent** on the new `code/src/<module_name>.py`: address any BUG findings before committing. WARNING findings should be fixed; SUGGESTION findings are optional.
8. Commit: `git add code/src/ code/notebooks/NN-name/ && git commit -m "feat(code-NN): add companion code for [topic]"`

## Expected Output

One or more functions in `code/src/`, filled `demo.ipynb`, and `exercises.ipynb` with exercise stubs and tests.

## Error Handling

- If code-reviewer returns BUG findings: fix all bugs before committing. Do not commit broken code.
- If `code/src/` already has a module with the same name: check with the user before overwriting.
