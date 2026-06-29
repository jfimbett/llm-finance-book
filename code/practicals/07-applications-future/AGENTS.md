# Finance Research-Brief Agent — agent instructions

Answer finance research questions about the bundled fictional company in `data/`, grounded
only in tool results. The deterministic tools in `tools/` do all routing, retrieval, and
figure lookup; you choose inputs and interpret outputs and never compute or recall numbers
yourself.

Loop for every question:

1. `python -m tools.route "<question>"` → read the `route`.
2. Gather evidence for that route into `reports/_evidence.json`:
   - `metrics`: `python -m tools.metrics "<metric name>" > reports/_evidence.json`
   - `filings` / `news`: `python -m tools.retrieve "<question>" --source <route> -k 3 > reports/_evidence.json`
3. Write a brief from `reports/_evidence.json`; cite a source for every claim (a metric's
   `source` field or a snippet id).
4. If a metric is `found: false`, or retrieval is off-topic, write "Not answerable from the
   available sources." A figure-plus-reason question needs both a metrics lookup and a
   filings retrieval.
5. Save the brief + evidence to `reports/<slug>.md`.

Cite a tool result for every claim; never invent a figure. Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline, Cursor,
generic `AGENTS.md` runners) — Chapter 7's point that an agent's capabilities are just
markdown artifacts.
