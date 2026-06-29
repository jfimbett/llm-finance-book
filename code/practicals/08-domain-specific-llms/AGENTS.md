# General-vs-Domain Comparison Agent — agent instructions

Compare a general-purpose classifier against a finance-domain classifier on the bundled
labelled finance sentences in `data/`, grounded only in what the tools print. The
deterministic tools in `tools/` do all classification and scoring; you choose inputs and
interpret outputs and never compute or recall numbers yourself.

Comparison loop:

1. `python -m tools.general`   — general-purpose accuracy and its misses.
2. `python -m tools.domain`    — finance-domain accuracy and its flips.
3. `python -m tools.compare --json`  — source of truth: both accuracies, `winner`,
   `margin`, and `domain_wins` with their `deciding_terms`.
4. Write a verdict that cites the two accuracies and the deciding finance terms
   (`beat`, `headwinds`, `liability`, `impairment`).
5. Save the verdict to `reports/compare.md`.

Never state an accuracy or label the tools did not print. Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline, Cursor,
generic `AGENTS.md` runners) — Chapter 8's point that an agent's capabilities are just
markdown artifacts.
