# AAPL Equity Valuation — Codex/OpenAI Agents

## Project Goal
Compute Apple Inc. (AAPL) intrinsic equity value per share from FY2024 SEC EDGAR filings.
Target: within 10% of $226.84 (AAPL close, September 27 2024).

## How to Run

Run the orchestrating workflow script:
```
node workflows/orchestrate-valuation.js
```
Or follow skills manually in this order:
1. fetch-financials (agents/edgar-fetcher)
2. compute-fcf (agents/financial-analyst)
3. estimate-wacc (agents/wacc-estimator)
4. run-dcf (agents/dcf-modeler)
5. run-comps (agents/comps-analyst)
6. validate-accuracy (agents/accuracy-checker)

If error > 10%, run iterate-to-target.

## Key Facts

- AAPL CIK: 0000320193
- Fiscal year end: 2024-09-28
- Reference price: $226.84
- Data source: SEC EDGAR free APIs (no API key needed)
- XBRL endpoint: https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json

## Agent Files

All agent personas are in `.claude/agents/`. Each file contains:
- Role description
- Required inputs
- Step-by-step instructions
- Output format

## Skill Files

All skills are in `.claude/skills/*/SKILL.md`. Each file contains:
- Preconditions
- Ordered steps
- Expected outputs
- Error handling

## Compatibility

This project structure is compatible with:
- **Claude Code**: runs `.claude/agents/*.md` and `.claude/skills/*/SKILL.md`
- **Cline**: reads `.clinerules` which references the same agents
- **Codex (this file)**: reads `AGENTS.md` and follows `.claude/agents/*.md`

All three tools can execute the same workflow with identical results.

## Verified FY2024 Fallback Values (Apple press release, Oct 31, 2024)

If EDGAR fetch fails, use:
- Revenue: $391,035M
- Net income: $93,736M
- Operating CF: $118,254M
- CapEx: $9,447M
- FCF: $108,807M
- Total debt: $101,304M
- Cash + ST investments: $65,171M
- Net debt: $36,133M
- EPS diluted: $6.11
- Diluted shares: 15,343M
- D&A: $11,445M
- EBITDA: $134,661M
