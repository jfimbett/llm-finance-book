# Text-to-Signal Pipeline — agent instructions

Run the text-as-data ML pipeline over the labelled finance sentences in
`data/labeled/headlines.csv`. The deterministic tools in `tools/` (standard library + NumPy,
offline) do all feature extraction, training, and scoring; you choose inputs and interpret
outputs and never fit a model or compute an accuracy yourself.

Pipeline:

1. `python -m tools.features "<sentence>"` — check the text becomes sensible features.
2. `python -m tools.model "<sentence>"` — train on the corpus, predict UP (1) / DOWN (0).
3. `python -m tools.evaluate --test-frac 0.3 --seed 42` — out-of-sample accuracy + confusion.
4. Save accuracy, split sizes, confusion counts, and one example prediction to
   `reports/pipeline.md`, quoting every number exactly.

The vocabulary is fit on the training split only (`tools.evaluate` enforces this). Never
state an accuracy you did not run; if `accuracy < 0.8`, report it as a failure. Tests:
`python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline, Cursor,
generic `AGENTS.md` runners) — Chapter 16's point that the modelling stays in the tools and
the agent only orchestrates them.
