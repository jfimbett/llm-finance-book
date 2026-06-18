# AAPL Equity Valuation — AI Agent Project

## Goal
Compute the intrinsic equity value per share of Apple Inc. (AAPL) using:
- FY2024 10-K financial statements retrieved from SEC EDGAR (free, no authentication)
- Two-stage DCF model on per-share free cash flow (accounts for buyback-driven share reduction)
- Comparable company analysis (P/E and EV/EBITDA multiples)

**Target accuracy**: final estimate within 10% of AAPL's market price at fiscal year-end.
**Reference price**: $226.84/share — AAPL closing price on September 27, 2024 (last trading
  day before fiscal year-end on September 28, 2024; verify via web search if needed).
**Acceptable range**: $204.16 – $249.52

## Quick Start

Run the master workflow from this directory using Claude Code:
```
# Inside Claude Code session (cd to this directory first):
/workflows workflows/orchestrate-valuation.js
```

Or run individual skills (must be in this directory):
- `/fetch-financials` — download AAPL FY2024 10-K from SEC EDGAR
- `/compute-fcf`       — compute 5-year historical FCF and CAGR
- `/estimate-wacc`     — estimate WACC via CAPM
- `/run-dcf`           — run the two-stage DCF model
- `/run-comps`         — run comparable company analysis
- `/validate-accuracy` — compare estimate to $226.84 reference
- `/iterate-to-target` — adjust assumptions until within 10%

## Key Reference Data

| Item | Value |
|------|-------|
| Ticker | AAPL |
| SEC CIK | 0000320193 |
| Fiscal year end | September 28, 2024 |
| Reference price | $226.84/share |
| FY2024 FCF (verified) | $108,807M |
| Diluted shares (FY2024) | 15,343M |

## EDGAR APIs Used (all free, no auth required)

- XBRL company facts: `https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json`
- Submissions index:  `https://data.sec.gov/submissions/CIK0000320193.json`

## Directory Structure

```
.claude/agents/    Role-based AI personas — read before acting
.claude/skills/    Step-by-step skill workflows
workflows/         Executable workflow scripts
assumptions/       All assumptions documented with justification
data/              EDGAR raw data (populated by agents)
results/           Valuation outputs (populated by agents)
```

## Agents

| Agent | Purpose |
|-------|---------|
| edgar-fetcher | Retrieve AAPL 10-K financials via EDGAR XBRL API |
| financial-analyst | Compute FCF, historical growth rates, per-share metrics |
| wacc-estimator | Estimate WACC via CAPM with data-backed inputs |
| dcf-modeler | Build and run two-stage per-share DCF model |
| comps-analyst | Gather tech peer multiples; run P/E and EV/EBITDA comps |
| assumption-auditor | Validate every assumption against external data |
| accuracy-checker | Compare intrinsic estimate to reference price; report error |

## Valuation Methodology

1. **DCF (50% weight)**: Two-stage model — 5yr high-growth phase driven by historical
   FCF/share CAGR + AI tailwinds, then perpetuity at 3% terminal growth.
2. **Comparables (50% weight)**: Average of P/E and EV/EBITDA methods using MSFT/GOOGL/META
   as tech mega-cap peers.

## Success Criterion

```
|estimated_price - 226.84| / 226.84 ≤ 0.10
```
