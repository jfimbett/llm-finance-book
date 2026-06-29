# PII De-identification Agent — agent instructions

De-identify documents in `data/`: detect personal data, redact it, and score the
privacy/utility tradeoff. The deterministic tools in `tools/` do all detection,
redaction, and scoring; you choose inputs and interpret outputs and never decide what
counts as PII or estimate a score yourself.

Pipeline for every document:

1. `python -m tools.deidentify --json > reports/_scan.json` — note `counts` per type
   (EMAIL, SSN, PHONE, PERSON, ACCOUNT).
2. Save the `redacted` field to `reports/<doc>.redacted.txt`; confirm placeholders.
3. `python -m tools.metrics > reports/_metrics.json` — read `privacy` and `utility`.
4. If `privacy < 1.0`, an identifier leaked — name the type and re-detect; if
   `utility` is low, redaction was too aggressive — flag the span.
5. Save counts + both scores + the redacted-file path to `reports/<doc>.md`.

Never paste an original identifier back into redacted text and never estimate a
metric. Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline,
Cursor, generic `AGENTS.md` runners) — Chapter 15's point that an agent's
capabilities are just markdown artifacts, runnable on a local, offline machine.
