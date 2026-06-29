# Practical 13 — LLM Limitations and Rigorous Evaluation (Claude Code / Cline)

**Large Language Models in Finance · Chapter 13**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive an **evaluation-harness** agent. It scores a
bundled model's answers against a gold finance QA set and reports honest metrics —
accuracy and token-F1 plus calibration — surfacing the cases where the model is
**confidently wrong**.

The agent never computes a metric or decides whether an answer is right: the deterministic
tools in `tools/` do all scoring and calibration, and the agent only chooses the eval set
and interprets the numbers.

## Setup

```bash
pip install -r requirements.txt   # pytest + numpy; the tools need nothing else
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts under
`.claude/`: three sub-agents (`scorer`, `calibration-analyst`, `reviewer`) and one
command, `/evaluate`.

## Run

```
/evaluate
```

The harness scores the answers, measures Expected Calibration Error, flags every
confident-but-wrong answer, and saves a report to `reports/`. Everything is offline — the
eval set is a bundled fictional finance QA set for **NovaCorp Inc.** (`data/`).

You can also run the steps by hand:

```bash
python -m tools.score --gold data/gold.json --pred data/candidates_overconfident.json --out reports/_scored.json
python -m tools.calibration --scored reports/_scored.json
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Score answers (exact-match + token-F1) | `scorer` | `tools/score.py` |
| Measure ECE, flag confident-wrong cases | `calibration-analyst` | `tools/calibration.py` |
| Write the honest report | `reviewer` | — (reads `reports/_scored.json`) |

## What the eval set shows

`data/` ships two candidate models answering the same 10 questions:

- `candidates_overconfident.json` — gets only half right, but states ~0.9 confidence on
  almost everything. Five of its answers are **confident and wrong**. High ECE.
- `candidates_calibrated.json` — more accurate, and it hedges (low confidence) exactly on
  the answers it gets wrong. Low ECE, no confident-wrong cases.

Same harness, very different trustworthiness — that is the lesson: accuracy alone hides
whether a model knows when it is wrong.

## Things to try

- `/evaluate data/candidates_calibrated.json` and compare the two reports.
- Lower the confident-wrong threshold (`--confident-threshold 0.6`) and watch more items
  get flagged.
- Edit a `confidence` in a candidate file and re-run — see ECE move.
- Add a new question to `data/gold.json` plus a matching prediction, then re-score.
- Make the overconfident model claim 0.99 on a wrong answer and watch ECE rise.

## Tests

```bash
python -m pytest -q        # fully offline, deterministic
```
