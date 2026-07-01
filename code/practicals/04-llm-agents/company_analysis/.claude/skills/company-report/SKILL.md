---
name: company-report
description: Generate a professional 2-page report on a publicly-traded company as a self-contained HTML website. Given a company name, orchestrates five subagents in order (Generalist, Data Retriever, Data Scientist, Financial Analyst, Report Writer) — pulling the latest 10-K from SEC EDGAR, cleaning the financials, analyzing them, and writing the report. Use when the user asks for a company report, equity write-up, or 10-K-based analysis. Triggers include "write a report on <company>", "company report for <X>", "/company-report".
---

# Company Report

Produce a professional ~2-page corporate report on a publicly-traded company for
a portfolio manager, delivered as a single self-contained `report.html`. The work
runs as a five-stage pipeline of subagents that pass data through files in a
per-run working directory.

## Input

A company name or ticker (e.g. "Apple", "AAPL", "Coca Cola"). If the user did not
name a company, ask for one before starting.

## Setup

1. Pick a working ticker/slug for the run (use the obvious ticker if the user
   gave one; otherwise a short uppercase slug — the Data Retriever will confirm
   the real ticker).
2. Create the working directory `output/<TICKER>/` (and `output/<TICKER>/raw/`).
3. This directory path is passed to every stage; agents read prior stages'
   outputs from it and write their own outputs into it.

## Pipeline — run these subagents IN THIS ORDER

Dispatch each as a subagent (Agent tool) with the company name and the working
directory path. **Each stage depends on the previous one — run them
sequentially, not in parallel.** Stop and report to the user if a stage fails.

1. **Generalist** → writes `00_key_variables.md` (key financial variables to
   focus on for this company).
2. **Data Retriever** → runs `tools/edgar_fetch.py` to fetch CIK + latest 10-K +
   `companyfacts.json` into `raw/`, and writes `raw/meta.json`. If the company
   can't be resolved, stop and ask the user to disambiguate (use the candidate
   list the tool prints).
3. **Data Scientist** → writes `02_financials.json` (cleaned metrics, ratios,
   growth) from `raw/companyfacts.json`.
4. **Financial Analyst** → writes `03_analysis.md` (rigorous analysis grounded in
   the cleaned data + 10-K).
5. **Report Writer** → writes `report.html` (the final ~2-page self-contained
   website).

Use the matching subagent type for each stage: `generalist`, `data-retriever`,
`data-scientist`, `financial-analyst`, `report-writer`.

## Output

The deliverable is `output/<TICKER>/report.html`. Report its path to the user and
offer to open it in a browser (e.g. `open output/<TICKER>/report.html` on macOS).

## Notes

- All data is grounded in the company's latest 10-K and XBRL facts from SEC
  EDGAR. There is no live market-price feed; valuation is framed qualitatively or
  via per-share metrics.
- The EDGAR tool uses only the Python standard library — no `pip install` needed.
  SEC requires a descriptive User-Agent; the default is set in the tool and can
  be overridden via the `EDGAR_UA` environment variable.
- Never fabricate financial figures. If data is missing, the report says so.
