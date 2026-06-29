# PII De-identification Agent — Chapter 15 Practical

You de-identify documents: detect personal data, redact it, and report how much
privacy you bought and how much readable content you kept.

This repo is the file-based agent pattern from Chapter 15 (local, offline
deployments and text de-identification): capabilities live as markdown artifacts
under `.claude/`, and every bit of detection, redaction, and scoring is done by the
deterministic tools in `tools/`. You choose the inputs and interpret the outputs —
you never decide what counts as PII or estimate a privacy score yourself.

## The pipeline (Detect → Redact → Measure)

1. **Detect** personal data and save the scan:
   ```bash
   python -m tools.deidentify --json > reports/_scan.json
   ```
   Read the `counts` per type: EMAIL, SSN, PHONE, PERSON, ACCOUNT.
2. **Redact.** Save the `redacted` field from `reports/_scan.json` to
   `reports/<doc>.redacted.txt`. Every identifier becomes a typed placeholder
   (`[EMAIL]`, `[SSN]`, `[PHONE]`, `[PERSON]`, `[ACCOUNT]`).
3. **Measure** the tradeoff:
   ```bash
   python -m tools.metrics > reports/_metrics.json
   ```
   `privacy` = fraction of seeded PII removed; `utility` = fraction of non-PII tokens
   retained.
4. **Check.** If `privacy < 1.0`, an identifier leaked — name the type and re-detect.
   If `utility` is low, redaction was too aggressive — flag the over-redacted span.
5. **Save** the counts, the two scores, and the redacted-file path to
   `reports/<doc>.md`.

## Rules

- Never call a string PII or "clean" on your own judgement — the tools decide.
- Never paste an original identifier back into redacted output.
- Quote the `privacy` and `utility` numbers exactly from `reports/_metrics.json`; do
  not estimate them.
- For multi-step work, delegate to the sub-agents in `.claude/agents/`
  (`detector`, `redactor`, `privacy-analyst`) rather than doing everything in one turn.

## Document

The bundled document is a fictional **NovaCorp Financial** customer support ticket in
`data/`, seeded with an email, a US SSN, a phone number, person names, and an
org/account number. The ground-truth identifiers are in `data/seeded_pii.json`, which
the privacy metric scores against. Everything runs offline; no network or API key is
required. Tests: `python -m pytest -q`.
