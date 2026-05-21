# /commit-progress

## Purpose

Stage and commit all current changes with a structured conventional commit message.

## When to Invoke

After completing any meaningful unit of work — a draft, a review pass, a set of exercises.

## Inputs Required

- None — the skill reads `git status` to determine what changed.
- Optionally: commit type and scope provided by the user.

## Steps

1. Run `git status` to list all modified and untracked files.
2. If no changes: print "Nothing to commit" and exit.
3. Infer the commit type and scope from the changed files:
   - `.tex` files in `book/chapters/NN-*` → `feat(chNN)` or `refine(chNN)`
   - `.md` or `.tex` files in `course/lectures/NN-*` → `feat(lecNN)`
   - Files in `code/` → `feat(code-NN)`
   - Agent files in `.claude/agents/` → `chore(agents)`
   - Skill files in `.claude/skills/` → `chore(skills)`
   - Hook scripts in `.claude/hooks/` → `chore(hooks)`
   - `docs/` → `docs`
4. Propose a commit message: `type(scope): [brief summary of changes]`.
5. Ask the user to confirm or edit the proposed message.
6. Stage the changed files: `git add [files]`.
7. Run `git commit -m "[confirmed message]"`.

## Expected Output

A clean commit with a structured conventional commit message.

## Error Handling

- If pre-commit hooks (check-latex, gate-check, etc.) fail: print the hook's error output clearly and do NOT retry automatically. Ask the user to fix the underlying issue.
- If nothing is staged after `git add`: print "No stageable changes found."
