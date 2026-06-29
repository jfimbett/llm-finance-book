# Sentiment-Signal Agent — agent instructions

Turn the bundled headlines in `data/headlines.csv` into a daily sentiment signal,
grounded only in what the tools score. The deterministic tools in `tools/` do all polarity
scoring and aggregation; you choose inputs and interpret the signal and never compute or
recall numbers yourself.

Pipeline:

1. `python -m tools.aggregate > reports/_signal.json` (add `--date YYYY-MM-DD` for one day).
2. Read `reports/_signal.json`: per-date `mean`, `label`, `count`, `item_ids`, plus each
   scored headline in `headlines`.
3. Spot-check a headline with `python -m tools.lexicon "<headline>"`.
4. Write a summary that states each day's `mean` and `label` verbatim and cites the
   headlines that drove it by `id`.
5. Save the summary to `reports/<date>.md`.

Never state a polarity or mean that is not in `reports/_signal.json`, and never relabel a
day the tool already labelled. Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline, Cursor,
generic `AGENTS.md` runners) — Chapter 9's point that an agent's capabilities are just
markdown artifacts.
