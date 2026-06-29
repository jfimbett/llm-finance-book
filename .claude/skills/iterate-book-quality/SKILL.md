# /iterate-book-quality

## Purpose

Drive a chapter (or a list of chapters) to **≥90 on every dimension** by looping:
editor-plan → `chapter-surgeon` patch → re-run relevant checks → re-score, until pass,
max iterations, or a blocker that needs human/external verification. This is the
**editing arm** — it modifies `chapter.tex`. Run `/audit-chapter-quality` first.

## When to Invoke

- After `/audit-book-quality` or `/audit-chapter-quality` finds a chapter below 90.

## Inputs Required

- A chapter identifier (slug / number / reading index), or `--all-failing` to iterate
  every chapter whose `score.json` has `pass:false`.
- The chapter's existing audit outputs in
  `docs/quality/book-quality/chapters/<read#>-<slug>/`. If missing, run
  `/audit-chapter-quality` for that chapter first.
- `max_refine_iterations` from `TOPIC.md` (default 5), adapted to 0–100.

## Steps

For each target chapter:

1. **Load context.** Read `editor-plan.md`, `score.json`, and the chapter. Identify
   dimensions < 90 and the MUST_FIX tasks that target them.
2. **Guardrails before editing:**
   - Respect `DO_NOT_CHANGE` / `KEEP*` zones from the constructive review.
   - Book-wide items (single-source-of-truth, cross-chapter repetition) are NOT edited
     blindly here — they stay in `IMPLEMENTATION_BACKLOG.md` unless the editor-plan
     assigns this chapter as the SSOT and gives a local instruction.
3. **Apply patches.** For each MUST_FIX, invoke `chapter-surgeon` with the editor's
   exact Location/Problem/Fix. The surgeon returns a minimal BEFORE/AFTER patch; apply
   it with Edit. Constraints: preserve labels (unless fixing a known collision), use
   `\ref`/`\Cref{ch:...}` not hard-coded numbers, never add a citation key absent from
   `bibliography.bib`, never invent paper claims. Record each applied change in
   `change-log.md` with iteration number, task id, and a one-line diff summary.
4. **Re-run only the relevant checks** (cheap): the auditor(s) owning the touched
   dimensions (e.g. `citation-description-auditor` after a cite fix; `cross-ref-checker`
   after a ref fix). Avoid full re-audit unless many dimensions changed.
5. **Re-score.** Update `score.json` (increment `iteration`). Recompute per-dimension
   and chapter `pass`.
6. **Loop control.** If chapter passes → stop, log success. Else if `iteration >=
   max_refine_iterations` → stop, write `MAX ITERATIONS REACHED — human review` to
   `change-log.md`. Else if remaining blockers are all `NEEDS_EXTERNAL_VERIFICATION` /
   human-decision (e.g. delete stale `.bib`, reorder `\include`) → stop and surface
   them. Else regenerate the editor-plan for the still-failing dimensions and repeat
   from step 3.
7. **Compile check.** After the last patch of a chapter, run a draft `pdflatex` (or
   `scripts/build-book.sh` if cheap) to confirm the chapter still compiles. Revert/fix
   if it broke.

## Expected Output

- Edited `chapter.tex` (auto-committed by the hook).
- Updated `score.json`, appended `change-log.md`, refreshed `editor-plan.md`.
- Console:
  ```
  === Iterate: <read#> <slug> ===
  Iter 1: fixed T1 (citation_accuracy), T2 (completeness) → re-score
  ...
  Result: PASS (all dims ≥90)  |  MAX_ITER  |  BLOCKED (needs external verification: …)
  ```

## Error Handling

- No editor-plan: run `/audit-chapter-quality` first, then resume.
- `chapter-surgeon` returns `CANNOT APPLY`: log it, route the task back to `audit-editor`
  for a sharper instruction, do not force the edit.
- Compile breaks after a patch: revert that patch, mark the task BLOCKED, continue others.
- A fix would require inventing a citation or paper claim: refuse, mark
  `NEEDS_EXTERNAL_VERIFICATION`, leave the dimension below 90.
- Never edit content a chapter does not own (book-wide repetition) without an explicit
  editor SSOT assignment.
