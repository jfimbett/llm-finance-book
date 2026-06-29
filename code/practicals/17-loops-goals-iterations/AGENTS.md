# Iterate-to-Target Agent — agent instructions

Refine `reports/draft.md` until the deterministic gate `tools/check.py` says the target in
`data/target.json` is met. The tools measure and decide; you only draft and revise, and you
never invent a figure or judge the draft yourself.

Loop (budget: 5 passes):

1. Draft a one-paragraph summary of `data/source.txt` into `reports/draft.md`, using only
   figures from the source.
2. `python -m tools.metric --candidate reports/draft.md`  — reports coverage, missing facts,
   and any unsupported figures.
3. `python -m tools.check --candidate reports/draft.md`   — exit 0 means the target is met.
4. If it fails, edit `reports/draft.md` to add each missing fact (figure taken from the
   source) and remove/correct each unsupported figure; cite the source line. Repeat from 2.
5. Save the score trajectory and final draft to `reports/<slug>-trajectory.md`.

The loop stops only when the tool says the target is met. After every edit the PostToolUse
hook in `.claude/settings.json` (`.claude/hooks/after_edit.sh`) re-scores the draft and runs
the tests automatically. Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline, Cursor,
generic `AGENTS.md` runners) — Chapter 17's point that an agent's loop, skills, and hooks are
just files in the repo.
