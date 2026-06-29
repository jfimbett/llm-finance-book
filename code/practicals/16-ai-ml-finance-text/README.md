# Practical 16 — Text-to-Signal ML Pipeline (Claude Code / Cline)

**Large Language Models in Finance · Chapter 16 — Artificial Intelligence, Machine Learning, and Text in Finance**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive an agent that runs the chapter's text-as-data
workflow end to end: labelled financial sentences become features, a classifier learns the
up/down signal, and the agent reports the **out-of-sample accuracy**.

The agent never fits a model or computes a score: the deterministic tools in `tools/`
(standard library + NumPy) do all feature extraction, training, and evaluation, and the
agent only chooses inputs and interprets outputs.

## Setup

```bash
pip install -r requirements.txt   # NumPy for the tools, pytest for the suite
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts under
`.claude/`: three sub-agents (`feature-engineer`, `modeler`, `evaluator`) and one command,
`/pipeline`.

## Run

```
/pipeline
```

The agent vectorises the corpus, trains the classifier, scores it on a held-out split,
sanity-checks a couple of example predictions, and saves a report citing the accuracy to
`reports/`. Everything is offline — the data is a bundled fictional labelled set
(`data/labeled/headlines.csv`).

You can also run the steps by hand:

```bash
python -m tools.features "Earnings beat expectations and revenue surged."
python -m tools.model "Earnings missed and the stock plunged on weak demand."
python -m tools.evaluate --test-frac 0.3 --seed 42
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Text → TF-IDF feature matrix | `feature-engineer` | `tools/features.py` (NumPy) |
| Train classifier, predict     | `modeler`          | `tools/model.py` (logistic regression by gradient descent) |
| Held-out accuracy + confusion | `evaluator`        | `tools/evaluate.py` (deterministic split, CLI prints accuracy) |

## Things to try

- Re-run `python -m tools.evaluate --seed 7` (and other seeds) and watch the held-out
  estimate move — that variance is why one split is never the whole story.
- Score a deliberately neutral sentence with `python -m tools.model` and see `P(up)` sit
  near 0.5 — little text signal, low confidence.
- Add new labelled rows to `data/labeled/headlines.csv` and re-run the tests; see whether the
  vocabulary still separates the two classes.
- Inspect `python -m tools.features "<sentence>"` to see which words carry the most weight —
  the sentiment terms ("surged", "plunged") should dominate.

## Tests

```bash
python -m pytest -q        # fully offline
```
