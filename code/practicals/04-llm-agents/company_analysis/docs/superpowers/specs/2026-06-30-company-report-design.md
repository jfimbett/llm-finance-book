# Company Report — Design Spec

**Date:** 2026-06-30
**Status:** Approved

## Goal

Given a publicly-traded company name, produce a professional ~2-page corporate
report (as a self-contained HTML website) for a portfolio manager. The work is
done by a pipeline of five Claude Code subagents, orchestrated by one skill.

## Form factor (decided)

- **Claude Code subagents + skill** — `.claude/agents/*.md` definitions plus a
  `.claude/skills/company-report/SKILL.md` orchestrator. Not a standalone app.
- **EDGAR retrieval** — a Python script (`tools/edgar_fetch.py`) using the free
  SEC EDGAR REST APIs, stdlib only (no `pip install`), with a descriptive
  `User-Agent` header as SEC requires.
- **Final output** — a single self-contained `report.html` (inline CSS),
  openable directly in a browser.

## Directory layout

```
/company_analysis
├── .claude/
│   ├── agents/
│   │   ├── generalist.md
│   │   ├── data-retriever.md
│   │   ├── data-scientist.md
│   │   ├── financial-analyst.md
│   │   └── report-writer.md
│   └── skills/company-report/
│       └── SKILL.md
├── tools/
│   └── edgar_fetch.py
└── output/<TICKER>/          # created per run
    ├── 00_key_variables.md   # Generalist
    ├── raw/                  # Data Retriever: 10-K doc + companyfacts.json + meta.json
    ├── 02_financials.json    # Data Scientist: cleaned metrics + ratios
    ├── 03_analysis.md        # Financial Analyst
    └── report.html           # Report Writer: final deliverable
```

## Data flow

Subagents do not share memory, so each stage communicates by reading/writing
files in `output/<TICKER>/`. The skill creates the directory and passes its path
to every agent.

## The EDGAR tool — `tools/edgar_fetch.py`

Pure Python stdlib (`urllib.request`, `json`, `argparse`, `difflib`).

CLI: `python tools/edgar_fetch.py "<company name or ticker>" --out output/<TICKER>/raw`

Steps:
1. **Name → CIK.** Download `https://www.sec.gov/files/company_tickers.json`
   (maps ticker → CIK → title). Match the input against ticker (exact, case-
   insensitive) first, then fuzzy-match against title via `difflib`. Print the
   resolved ticker / CIK / title; exit non-zero with candidates if ambiguous.
2. **CIK → latest 10-K.** GET `https://data.sec.gov/submissions/CIK##########.json`
   (10-digit zero-padded). Filter `recent.form == "10-K"`, take the most recent
   by `filingDate`, build the primary document URL from `accessionNumber` +
   `primaryDocument`, download it to `raw/`.
3. **Structured financials.** GET
   `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` and save to
   `raw/companyfacts.json` — XBRL numeric facts the Data Scientist will tidy.
4. Write `raw/meta.json` with ticker, CIK, company title, filing date,
   accession number, and the source URLs.

Requirements: a descriptive `User-Agent` (e.g. `company-analysis/1.0
(jfimbett@gmail.com)`); basic retry/backoff on HTTP errors; clear errors when a
company can't be resolved or has no 10-K.

## The agents

Each is a focused subagent matching the task's role descriptions.

- **generalist** — expert macroeconomist. Reads the company name, outputs
  `00_key_variables.md`: the key financial variables/metrics a financial analyst
  should focus on for this company's report (and why).
- **data-retriever** — runs `edgar_fetch.py` to resolve CIK + download the latest
  10-K + companyfacts into `raw/`. Reports the resolved ticker/CIK/filing date.
- **data-scientist** — cleans the raw XBRL into `02_financials.json`: the last
  several fiscal years of the key metrics (revenue, net income, assets,
  liabilities, equity, cash flow, EPS, shares), plus computed ratios and
  growth rates. Notes any gaps.
- **financial-analyst** — expert graduate financial analyst. Reads
  `00_key_variables.md` + `02_financials.json` (+ skims the 10-K for qualitative
  context), writes `03_analysis.md`: profitability, leverage, liquidity, growth,
  valuation, risks, and an outlook.
- **report-writer** — turns `03_analysis.md` into a polished, ~2-page
  self-contained `report.html` (inline CSS, professional corporate styling) for
  the portfolio manager.

## The skill — `company-report`

Triggered with a company name. It:
1. Resolves a working ticker/slug and creates `output/<TICKER>/`.
2. Invokes the five subagents **in the order the task specifies**:
   Generalist → Data Retriever → Data Scientist → Financial Analyst →
   Report Writer — passing the working-dir path to each.
3. Stops and reports if a stage fails (e.g. company not found, no 10-K).
4. Final deliverable: `output/<TICKER>/report.html`, with the path surfaced to
   the user.

## Non-goals (YAGNI)

- No real-time market/price data; the report is grounded in the latest 10-K +
  XBRL facts.
- No multi-file site, server, or build step.
- No third-party Python packages.
