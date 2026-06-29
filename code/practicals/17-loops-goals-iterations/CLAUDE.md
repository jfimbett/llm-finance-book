# Iterate-to-Target Agent — Chapter 17 Practical

You refine a draft until a **deterministic tool** says a measurable target is met. This is
the agentic loop, skill, and hook from Chapter 17 — Claude Code's own mechanisms, turned on
themselves: a goal-driven loop with a metric tool as the stop condition and a file-based hook
that re-measures after every edit.

The task is in `data/target.json`: write a faithful one-paragraph summary of the source in
`data/source.txt` that covers the required facts. **You never decide the draft is good
enough.** The loop stops only when the tool says the target is met.

## The loop (draft → measure → revise → repeat)

1. **Draft** a one-paragraph summary into `reports/draft.md`, using only figures that appear
   in `data/source.txt`.
2. **Measure** with the deterministic metric:
   ```bash
   python -m tools.metric --candidate reports/draft.md
   ```
   It prints `coverage`, the `missing` required facts, and any `unsupported_figures`
   (numbers you used that are not in the source).
3. **Gate** — the single stop condition:
   ```bash
   python -m tools.check --candidate reports/draft.md   # exit 0 == target met
   ```
4. If the gate fails, **revise** `reports/draft.md` to fix exactly what was flagged — add
   each missing fact (figure taken straight from the source), remove or correct each
   unsupported figure — then go back to step 2. Cap at 5 passes.
5. When the gate passes (or the budget is spent), **save** the score trajectory and the final
   draft to `reports/<slug>-trajectory.md`.

## The hook

`.claude/settings.json` registers a `PostToolUse` hook on `Edit|Write` that runs
`.claude/hooks/after_edit.sh`. After every edit to a file it re-scores `reports/draft.md`
and runs the tests, so the metric for the next pass is pushed to you automatically — the loop
cannot skip its own measurement.

## Rules

- Never state a figure that is not in `data/source.txt`. The metric's `faithful` check fails
  the gate the moment you invent one, so coverage alone cannot win.
- You do not compute the score and you do not judge the draft. `tools/metric.py` scores;
  `tools/check.py` decides; you only draft and revise.
- For a structured run, delegate to the sub-agents in `.claude/agents/` (`drafter`, `grader`,
  `iterator`) via the `/iterate` skill rather than doing everything in one turn.

## Data

`data/source.txt` is a fictional earnings release for **Meridian Robotics Inc.**;
`data/target.json` lists the required facts and the coverage `threshold`. Everything runs
offline — no network, no API key. Tests: `python -m pytest -q`.
