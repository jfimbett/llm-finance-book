---
name: valuation
description: Value a public company end-to-end from its CIK or ticker. Run `/valuation <cik|ticker>`. Orchestrates EDGAR fetch, three parallel valuation lanes (Monte-Carlo DCF, dual-source comparables, qualitative/risk), and reconciliation into a fair-value median + P10–P90, benchmarked against the real market price.
---

# /valuation — orchestrate a full business valuation

**Argument:** a ticker (e.g. `AAPL`) or a CIK (e.g. `320193`). Pick a run `SEED`
(default 0) and reuse it for reproducibility.

Announce: "Using the valuation skill to value <ARG>."

## Step 1 — Data (sequential; everything depends on it)
Dispatch the **edgar-analyst** agent with the ticker/CIK. It caches
`companyfacts.json` + `narrative.txt` and writes `financials.json`. Capture the
resolved `CIK` and `TICKER`. If it reports an error, stop and surface it.

## Step 2 — Three lanes IN PARALLEL
In a single message, dispatch these three agents concurrently (they are blind to
each other):
- **dcf-analyst** (CIK, SEED) → `dcf_result.json`
- **comps-analyst** (CIK, TICKER, SEED) → `comps_llm.json`, `comps_embedding.json`
- **qualitative-analyst** (CIK) → risk summary + `lane_weights`

If a lane fails, continue with the survivors and note the gap.

## Step 3 — Reconcile
Dispatch the **reconciliation-analyst** (CIK, TICKER, SEED) with the qualitative
lane's `lane_weights`. It runs `reconcile.py`, fetches the market benchmark, and
writes `reports/<TICKER>-<date>.md`.

## Step 4 — Headline
Print to the user:
`<TICKER> fair value ≈ $<median>/share (P10–P90: $<p10>–$<p90>); market $<price> (Δ <±k%>)`
followed by the report path.

## Rules
- All numbers come from the Python tools; never compute or guess a figure.
- Thread the same SEED through every stochastic tool call.
- Never feed the market price back into any valuation lane.
