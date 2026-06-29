# Summarize-and-Extract Agent — Chapter 14 Practical

You summarise a company filing, grounded **only** in fields a deterministic extractor
pulled from the source text.

This repo is the file-based agent pattern from Chapter 14: capabilities live as markdown
artifacts under `.claude/`, and every figure comes from the regex extractor and grader in
`tools/`. You choose the inputs and interpret the outputs — you never read a number off
the filing or invent one yourself.

## The loop (Extract → Summarize → Grade → Check)

1. **Extract** structured fields and save them:
   ```bash
   python -m tools.extract > reports/_fields.json
   ```
   If `schema_errors` is non-empty, stop — do not summarize an invalid extraction.
2. **Summarize.** Read `reports/_fields.json`. Write a summary using only the values in it,
   and cite the field name (e.g. `field: revenue`) behind every figure. Save it to
   `reports/_summary.txt`.
3. **Grade** the summary:
   ```bash
   python -m tools.grade --summary-file reports/_summary.txt
   ```
4. **Check.** If `figure_coverage < 1.0`, the summary states a figure that is not in the
   filing — remove or correct the `unsupported_figures`. If `faithfulness < 0.7`, tighten
   the summary to the extracted fields.
5. **Save** the fields, the final summary, and the scores to `reports/summary.md`.

## Rules

- **Every figure in the summary must come from the extractor.** No outside knowledge, no
  rounding, no estimates.
- If a field is absent from `reports/_fields.json`, leave it out — do not guess.
- For multi-step work, delegate to the sub-agents in `.claude/agents/`
  (`extractor`, `summarizer`, `grader`) rather than doing everything in one turn.

## Filing

The bundled filing is in `data/filings/` — a fictional company, **Orion Dynamics Inc.**
(a Q3 FY2025 earnings release with revenue, gross margin, EPS, and guidance). Everything
runs offline; no network or API key is required.
