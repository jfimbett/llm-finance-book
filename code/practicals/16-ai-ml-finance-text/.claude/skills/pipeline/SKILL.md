---
name: pipeline
description: Run the end-to-end text-to-signal ML pipeline and save a grounded report. Usage /pipeline
---

# /pipeline

Turn the labelled financial text in `data/labeled/headlines.csv` into features, train the
classifier, score it out of sample, and save a report citing the measured accuracy.

1. **Features** (feature-engineer agent): confirm the text vectorises sensibly.
   `python -m tools.features "Earnings beat expectations and revenue surged."`
2. **Train + predict** (modeler agent): fit on the corpus and sanity-check a sentence.
   `python -m tools.model "Earnings missed and the stock plunged on weak demand."`
3. **Evaluate** (evaluator agent): the headline number.
   `python -m tools.evaluate --test-frac 0.3 --seed 42`
4. **Report** — write `reports/pipeline.md` containing only facts from the tool output:
   - the out-of-sample **accuracy** and the train/test split sizes,
   - the confusion counts (`tp`, `tn`, `fp`, `fn`),
   - the vocabulary size,
   - one example prediction with its `P(up)`.
   Quote every number exactly as the tools printed it. State no accuracy you did not run.

If `accuracy < 0.8`, say the pipeline did not clear the floor — do not round up or excuse it.

Try these:
- `/pipeline` ← full run on the default split.
- Change `--seed` and re-run to see how the held-out estimate moves.
- Add rows to `data/labeled/headlines.csv` and re-run `python -m pytest -q`.
