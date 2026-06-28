# Business Valuation — Agentic Exercise

Run `/valuation <ticker|cik>` inside this folder and a fleet of Claude Code agents
values a public company: a Monte-Carlo DCF lane, a dual-source comparables lane
(LLM-proposed peers + 10-K-embedding-similarity peers), and a qualitative/risk
lane, reconciled into a fair-value **median + P10–P90** and benchmarked against
the real market price. All math and data live in `tools/*.py` — the LLM chooses
inputs and interprets outputs, but never does arithmetic.

## Setup

```bash
pip install -r requirements.txt
```

Set your SEC User-Agent (EDGAR requires it) — edit `.claude/settings.json` and
replace the `SEC_USER_AGENT` value with `Your Name your-email@example.com`, or:

```bash
export SEC_USER_AGENT="Your Name your-email@example.com"
```

## Run

```
/valuation AAPL
```

Outputs land in `data/<CIK>/` (cached facts, narrative, per-lane JSON) and a
report in `reports/<TICKER>-<date>.md`. The first run fetches from EDGAR; later
runs reuse the cache. Use the same seed for reproducible numbers.

## The pipeline

| Stage | Agent | Tools |
|-------|-------|-------|
| Fetch + normalize | edgar-analyst | `edgar_fetch.py`, `financials.py` |
| DCF (Monte Carlo) | dcf-analyst | `montecarlo_dcf.py` |
| Comparables (2 sources) | comps-analyst | `embeddings.py`, `comps.py` |
| Qualitative / risk | qualitative-analyst | (reads `narrative.txt`) |
| Reconcile + report | reconciliation-analyst | `reconcile.py`, `market_price.py` |

## Things to try in class

- Run several companies and compare the market gap (over/under-valued).
- Swap `universe.txt` for a sector list and re-run with `--rebuild` to see how
  embedding peers change.
- Edit a DCF prior (e.g. WACC mean) and watch the range move.
- Compare LLM-proposed peers vs embedding peers — do they agree?
- Make a lane fail (bad ticker) and see how reconciliation degrades gracefully.

## Tests

```bash
python -m pytest -q   # fully offline, uses tests/fixtures/
```
