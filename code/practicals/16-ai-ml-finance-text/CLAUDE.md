# Text-to-Signal Pipeline — Chapter 16 Practical

You run an end-to-end text-as-data machine-learning pipeline: labelled financial sentences
become features, a classifier learns from them, and you report the out-of-sample accuracy.

This repo is the file-based agent pattern: capabilities live as markdown artifacts under
`.claude/`, and every bit of feature extraction, training, and scoring is done by the
deterministic tools in `tools/` (standard library + NumPy, fully offline). You choose inputs
and interpret outputs — you never fit a model or compute an accuracy yourself.

## The pipeline (text → features → model → evaluation)

1. **Features.** Confirm the text vectorises sensibly:
   ```bash
   python -m tools.features "Earnings beat expectations and revenue surged."
   ```
2. **Train + predict.** Fit on the corpus and score one sentence:
   ```bash
   python -m tools.model "Earnings missed and the stock plunged on weak demand."
   ```
3. **Evaluate.** The headline number on a held-out split:
   ```bash
   python -m tools.evaluate --test-frac 0.3 --seed 42
   ```
4. **Report.** Save the accuracy, train/test sizes, confusion counts, and one example
   prediction to `reports/pipeline.md`, quoting every number exactly as printed.

## Rules

- Never state an accuracy or probability you did not get from a tool. No outside numbers.
- The vocabulary is fit on the training split only; `tools.evaluate` enforces this — don't
  evaluate on data the model was trained on.
- If `accuracy < 0.8`, report the failure plainly; do not round up or excuse it.
- For multi-step runs, delegate to the sub-agents in `.claude/agents/`
  (`feature-engineer`, `modeler`, `evaluator`).

## Data

`data/labeled/headlines.csv` is a fictional labelled set of short finance sentences
(`label,text`; 1 = up, 0 = down), built to be linearly separable so a simple classifier can
learn it. Everything runs offline; no network or API key is required.

Tests: `python -m pytest -q`.
