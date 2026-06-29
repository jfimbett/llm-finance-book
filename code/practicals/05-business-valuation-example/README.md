# AAPL Equity Valuation Exercise

A complete multi-agent AI setup for computing Apple Inc.'s intrinsic equity value using
public SEC EDGAR data — demonstrating agents, skills, and workflows for financial analysis.

## What This Exercise Demonstrates

- How to retrieve structured financial data from the SEC EDGAR XBRL API (free, no auth)
- How to compute Free Cash Flow and historical growth rates from 10-K filings
- How to estimate WACC using CAPM with market-sourced inputs
- How to build a two-stage DCF model on a per-share basis (capturing buyback value)
- How to run comparable company analysis (P/E and EV/EBITDA multiples)
- How to orchestrate multi-agent workflows for iterative financial modeling

## Target Outcome

Estimate AAPL's share price (reference: $226.84 on Sep 27, 2024) within **10% accuracy**
using only freely available public data and justified assumptions.

## Prerequisites

- Claude Code, Cline, or Codex (any one will work)
- Internet access (for SEC EDGAR API calls and web searches)
- No paid data subscriptions required — everything uses free public sources

## Quick Start

**Claude Code:**
```bash
cd exercises/valuation_example
claude
# Then run: /workflows workflows/orchestrate-valuation.js
```

**Cline:**
Open this folder in VS Code with Cline installed. Ask Cline to:
"Follow .clinerules to run the AAPL equity valuation workflow."

**Codex:**
```bash
cd exercises/valuation_example
# Ask Codex to read AGENTS.md and follow the workflow
```

## Files

```
CLAUDE.md                    Main AI instructions (Claude Code)
AGENTS.md                    OpenAI Codex instructions
.clinerules                  Cline instructions

.claude/
  agents/
    edgar-fetcher.md         Fetch AAPL 10-K from EDGAR
    financial-analyst.md     Compute FCF and growth rates
    wacc-estimator.md        Estimate WACC via CAPM
    dcf-modeler.md           Two-stage DCF model
    comps-analyst.md         Peer comparables analysis
    assumption-auditor.md    Justify and validate assumptions
    accuracy-checker.md      Measure accuracy vs reference price
  skills/
    fetch-financials/        Skill: fetch EDGAR data
    compute-fcf/             Skill: compute FCF history
    estimate-wacc/           Skill: estimate WACC
    run-dcf/                 Skill: run DCF model
    run-comps/               Skill: run comparables
    validate-accuracy/       Skill: check vs reference price
    iterate-to-target/       Skill: refine until within 10%

workflows/
  orchestrate-valuation.js   Master workflow (Claude Code Workflow API)

assumptions/
  base-case.md               All assumptions documented with justification

data/                        EDGAR data saved here by agents (auto-populated)
results/                     Valuation outputs saved here (auto-populated)
```

## Methodology

**DCF (50% weight):**
Two-stage model. Stage 1 (5 years): growth rate derived from historical 5-year FCF/share CAGR
(~15-17%), supported by Apple Services growth (~14% YoY), Apple Intelligence monetization, and
India/emerging market expansion. Stage 2 (terminal): 3% perpetual growth (long-run nominal GDP).
WACC computed via CAPM using Fed funds adjusted risk-free rate, Damodaran ERP, and AAPL beta.

**Comparables (50% weight):**
Tech mega-cap peers (MSFT, GOOGL, META). P/E applied to FY2024 diluted EPS ($6.11).
EV/EBITDA applied to FY2024 EBITDA ($134.7B). AAPL trades at a 5% premium to peer median
due to its brand moat, ecosystem lock-in, and lower earnings volatility.

**Data Sources (all free):**
- Financial statements: SEC EDGAR XBRL API
- WACC inputs: Damodaran's website (ERP), FRED (risk-free rate), publicly cited beta
- Peer multiples: web search / publicly reported analyst estimates
- Reference price: Yahoo Finance / Google Finance historical data

## Expected Results

With calibrated assumptions, the model produces ~$215-235/share, within the 10% target band.
The iterating workflow adjusts growth rate assumptions if the initial estimate falls outside
the acceptable range ($204-$249).

## Learning Objectives

After completing this exercise, you will understand:
1. How AI agents can automate the full equity valuation pipeline end-to-end
2. How EDGAR XBRL data enables programmatic financial statement analysis
3. How multi-stage DCF models capture growth stage transitions
4. How per-share FCF adjusts for buyback-driven value creation
5. How to orchestrate iterative refinement loops for model calibration
6. How to justify valuation assumptions with verifiable public data
