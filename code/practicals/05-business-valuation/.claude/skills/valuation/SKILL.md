---
name: valuation
description: Value a public company end-to-end from its CIK or ticker. Run `/valuation <cik|ticker>`. Orchestrates EDGAR fetch, three parallel valuation lanes (Monte-Carlo DCF, dual-source comparables, qualitative/risk), and reconciliation into a fair-value median + P10–P90, benchmarked against the real market price.
---

# /valuation — orchestrate a full business valuation

**Argument:** a ticker (e.g. `AAPL`) or a CIK (e.g. `320193`). Pick a run `SEED`
(default 0) and reuse it for reproducibility.

Announce: "Using the valuation skill to value <ARG>."

For a clean agent timeline in the final HTML report, start each run from a fresh
trace: empty `data/trace.jsonl` (the PreToolUse/PostToolUse hooks append every
tool and sub-agent call to it as the run proceeds).

## Step 1 — Data (sequential; everything depends on it)
Dispatch the **edgar-analyst** agent with the ticker/CIK. It caches
`companyfacts.json` + `narrative.txt` and writes `financials.json`. Capture the
resolved `CIK` and `TICKER`. If it reports an error, stop and surface it.

## Step 2 — Three lanes IN PARALLEL
In a single message, dispatch these three agents concurrently (they are blind to
each other):
- **dcf-analyst** (CIK, SEED) → `dcf_result.json` + `sensitivity.json`
- **comps-analyst** (CIK, TICKER, SEED) → `comps_llm.json`, `comps_embedding.json`
- **qualitative-analyst** (CIK) → `risk_summary`, `non_recurring_notes`, `lane_weights`

If a lane fails, continue with the survivors and note the gap.

## Step 3 — Reconcile + report
Dispatch the **reconciliation-analyst** (CIK, TICKER, SEED) with the qualitative
lane's `lane_weights`, `risk_summary`, and `non_recurring_notes`. It runs
`reconcile.py` (which returns a `review_required` governance flag), fetches the
market benchmark, writes `report_meta.json` + `reports/<TICKER>-<date>.md`, and
then runs `build_trace_site.py` to produce the interactive
`reports/<TICKER>-<date>.html` (valuation + WACC×g sensitivity heatmap + the
agent timeline captured in `data/trace.jsonl`).

## Step 4 — Headline
Print to the user:
`<TICKER> fair value ≈ $<median>/share (P10–P90: $<p10>–$<p90>); market $<price> (Δ <±k%>)`
Add `⚠ human review required` if the reconcile flag is set, followed by both the
`.md` and `.html` report paths.

## Rules
- All numbers come from the Python tools; never compute or guess a figure.
- Thread the same SEED through every stochastic tool call.
- Never feed the market price back into any valuation lane.
