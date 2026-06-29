---
name: evaluate
description: Score a bundled model's answers against the gold finance QA set and report honest metrics + calibration. Usage /evaluate [predictions.json]
---

# /evaluate [predictions.json]

Run the full evaluation and write a grounded report. Default predictions file:
`data/candidates_overconfident.json`. The tools own every number; you only run them,
read them back, and explain them.

1. **Score** (scorer agent):
   ```bash
   python -m tools.score --gold data/gold.json --pred <predictions.json> --out reports/_scored.json
   ```
   Record `accuracy`, `mean_f1`, `n`, `n_correct`.

2. **Calibrate** (calibration-analyst agent):
   ```bash
   python -m tools.calibration --scored reports/_scored.json
   ```
   Record `ece`, `mean_confidence`, the `confident_wrong` list, and the reliability `bins`.

3. **Report** (reviewer agent): write `reports/<model>.md` with, every figure cited from
   the tools above:
   - headline metrics: accuracy, mean F1, ECE, mean confidence;
   - the honesty gap (mean confidence minus accuracy);
   - a table of the confident-but-wrong cases (id, question, model answer, gold, confidence) — **first, not buried**;
   - the bins where accuracy fell below confidence;
   - a verdict on whether the model's confidence can be trusted.

**Rules:** report the numbers honestly; never round away a failure. Do not call an
overconfident model "well calibrated" because its accuracy looks acceptable. If the
`confident_wrong` list is non-empty, it leads the report.

Try these to start:
- `/evaluate`  → evaluates `data/candidates_overconfident.json`; expect ~0.5 accuracy, high ECE, five confident-wrong cases.
- `/evaluate data/candidates_calibrated.json`  → a model whose confidence tracks its accuracy; expect low ECE and no confident-wrong cases.
- Compare the two reports: same harness, very different trustworthiness.
