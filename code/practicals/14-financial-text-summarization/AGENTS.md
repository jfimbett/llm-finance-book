# Summarize-and-Extract Agent — agent instructions

Summarise the bundled filing in `data/filings/`, grounded only in fields extracted from
it. The deterministic tools in `tools/` do all extraction and scoring; you choose inputs
and interpret outputs and never read or invent a number yourself.

Loop for every summary:

1. `python -m tools.extract > reports/_fields.json` (stop if `schema_errors` is non-empty).
2. Write a summary using only the values in `reports/_fields.json`; cite the field name
   behind every figure. Save it to `reports/_summary.txt`.
3. `python -m tools.grade --summary-file reports/_summary.txt`
4. If `figure_coverage < 1.0`, remove or correct the `unsupported_figures`; if
   `faithfulness < 0.7`, tighten the summary to the extracted fields.
5. Save the fields, summary, and scores to `reports/summary.md`.

Every figure in the summary must come from the extractor. Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline, Cursor,
generic `AGENTS.md` runners) — Chapter 14's point that an agent's capabilities are just
markdown artifacts.
