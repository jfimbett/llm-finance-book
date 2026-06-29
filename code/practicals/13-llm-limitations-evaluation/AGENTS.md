# Evaluation-Harness Agent — agent instructions

Evaluate a model's answers against the bundled gold finance QA set in `data/` and report
honest metrics. The deterministic tools in `tools/` compute every metric; you choose the
eval set and interpret outputs and never score an answer or compute a metric yourself.

Loop:

1. `python -m tools.score --gold data/gold.json --pred <predictions.json> --out reports/_scored.json`
2. `python -m tools.calibration --scored reports/_scored.json`
3. Write `reports/<model>.md`: accuracy, mean F1, ECE, mean confidence; the gap between
   confidence and accuracy; a table of the confident-but-wrong items (first, not buried);
   the bins where accuracy fell below confidence; and a verdict on whether the confidence
   can be trusted.

Report the numbers honestly; never round away a failure. A decent accuracy does not make
an overconfident model trustworthy. Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline, Cursor,
generic `AGENTS.md` runners) — Chapter 13's point that an agent's capabilities are just
markdown artifacts.
