# Practical 17 — Loops, Goals, and Iterations (Claude Code / Cline)

**Large Language Models in Finance · Chapter 17 (capstone)**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive an **iterate-to-target** agent: it refines a draft
financial summary until a **measurable target is met**, demonstrating the chapter's three
mechanisms together — a goal-driven **loop**, a **skill** (`/iterate`) that runs it, and a
**hook** that re-measures after every edit.

The agent never decides the draft is good enough. A deterministic tool computes the score and
a separate gate decides whether the target is met; the agent only drafts, reads the number,
and revises. **The loop stops only when the tool says the target is met.**

## Setup

```bash
pip install -r requirements.txt   # only pytest; the tools are standard-library + numpy-free
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts under
`.claude/`: three sub-agents (`drafter`, `grader`, `iterator`), one command `/iterate`, and a
hook wired in `.claude/settings.json`.

## The task

`data/source.txt` is a fictional earnings release for **Meridian Robotics Inc.**
`data/target.json` defines the goal: a one-paragraph summary that **covers the required
facts** (revenue, margin, backlog, free cash flow, guidance) with **coverage ≥ 0.8**, using
only figures that actually appear in the source.

## Run

```
/iterate
```

The agent drafts `reports/draft.md`, scores it, and — while below target — revises to add
exactly the facts the metric reports as missing, looping up to 5 times. It saves the score
trajectory to `reports/<slug>-trajectory.md`.

You can also run the steps by hand:

```bash
# score a candidate against the source and the required facts
python -m tools.metric --candidate-text "Revenue rose 22% to 2.4 billion dollars. Operating margin expanded to 17%."

# the gate — exit 0 means the target is met, exit 1 means keep iterating
python -m tools.check --candidate reports/draft.md
```

## The loop

| Step | Agent | Tool |
|------|-------|------|
| Write / revise the draft | `drafter`, `iterator` | — (edits `reports/draft.md`) |
| Score coverage + faithfulness | `grader` | `tools/metric.py` |
| Decide pass/fail vs the threshold | `grader` | `tools/check.py` |

`tools/metric.py` returns two reproducible quantities. **coverage** is the fraction of
required facts whose anchor phrases all appear in the draft — the number the loop drives up.
**faithful** is `False` if the draft uses any figure not in the source, so the agent cannot
hit the target by inventing numbers; it has to pull them from the source. The gate
(`tools/check.py`) passes only when `coverage ≥ threshold` **and** `faithful`.

## The hook

`.claude/settings.json` registers a `PostToolUse` hook on `Edit|Write`:

```json
"hooks": {
  "PostToolUse": [
    { "matcher": "Edit|Write",
      "hooks": [ { "type": "command", "command": "bash .claude/hooks/after_edit.sh" } ] }
  ]
}
```

After every edit, the harness runs `.claude/hooks/after_edit.sh`, which re-scores
`reports/draft.md` (`python -m tools.metric`) and runs the test suite. The feedback for the
next pass is **pushed by the harness, not pulled by the model** — the loop cannot skip its own
measurement. This is the file-based hook pattern from the chapter: a hook is just a script the
runner invokes on an event, declared in `settings.json`.

## Things to try

- Start with a one-line draft and watch `coverage` climb 0.2 at a time as the agent adds each
  missing fact — the metric *names* exactly which fact is still absent.
- Add a number that is **not** in the source (say "a 45% segment margin"). Coverage may be
  1.0, but `faithful` flips to `False` and the gate refuses — the agent must remove it.
- Raise `threshold` in `data/target.json` to 1.0 and re-run: now every fact is mandatory.
- Add a sixth required fact to `data/target.json` and watch the loop take one more pass.
- Run `/iterate 2` to give a tight budget and watch it stop below target, reporting the best
  score reached instead of pretending success.

## Tests

```bash
python -m pytest -q        # fully offline
```

The suite checks the loop's invariants: coverage rises as missing facts are added, the gate
passes only at/above threshold, a draft missing a required fact is flagged below target, and a
fabricated figure breaks faithfulness even at full coverage.
