---
name: iterate
description: Refine a draft summary until the deterministic target metric is met. Usage /iterate [max_passes]
---

# /iterate [max_passes]

Drive the goal-driven loop: draft → measure → revise the missing facts → repeat, until
`tools.check` says the target in `data/target.json` is met. Default budget: 5 passes.

1. **Draft** (drafter agent): read `data/source.txt` and write a first one-paragraph
   summary to `reports/draft.md`, using only figures from the source.

2. **Measure** (grader agent):
   ```bash
   python -m tools.metric --candidate reports/draft.md
   python -m tools.check  --candidate reports/draft.md   # exit 0 == target met
   ```

3. **Gate.** If `tools.check` exits 0, stop — record the final score and break.

4. **Revise** (iterator agent): edit `reports/draft.md` to address *exactly* what the metric
   reported — add each `missing` fact (figure taken from the source), and remove or correct
   each `unsupported_figure`. Cite the source line for every number you add.

5. **Repeat** from step 2. Stop when the gate passes or after `max_passes` revisions.

6. **Save the trajectory** to `reports/<slug>-trajectory.md`:
   - one row per pass: `pass | coverage | faithful | missing facts | gate`,
   - the final draft text,
   - whether the target was met and on which pass.

The point of the practical: **you never judge the draft yourself.** The loop stops only when
the tool says the target is met. After each edit the PostToolUse hook in
`.claude/settings.json` re-runs the metric automatically (see `.claude/hooks/after_edit.sh`),
so the feedback for the next pass is already on screen.

Try:
- `/iterate`        ← default 5-pass budget
- `/iterate 2`      ← tight budget; likely stops below target, reports the best score
