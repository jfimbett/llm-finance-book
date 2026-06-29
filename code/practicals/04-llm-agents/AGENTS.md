# Filing Q&A Agent — agent instructions

Answer questions about the bundled SEC filings in `data/corpus/`, grounded only in
retrieved text. The deterministic tools in `tools/` do all retrieval and scoring; you
choose inputs and interpret outputs and never compute or recall numbers yourself.

Loop for every question:

1. `python -m tools.retrieve "<question>" -k 4 > reports/_context.json`
2. Write an answer using only facts in `reports/_context.json`; cite chunk ids.
3. `python -m tools.grade --question "<q>" --answer "<a>" --context reports/_context.json`
4. If `faithfulness < 0.7`, revise or answer "Not answerable from the available filings";
   if `relevance < 0.5`, re-retrieve with a better query.
5. Save the answer + scores to `reports/<slug>.md`.

Never state a figure that is not in a retrieved chunk. Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline, Cursor,
generic `AGENTS.md` runners) — Chapter 4's point that an agent's capabilities are just
markdown artifacts.
