# Business Valuation — Agentic Exercise

Run `/valuation <ticker|cik>` inside this folder and a fleet of Claude Code agents
values a public company: a Monte-Carlo DCF lane, a dual-source comparables lane
(LLM-proposed peers + 10-K-embedding-similarity peers), and a qualitative/risk
lane, reconciled into a fair-value **median + P10–P90** and benchmarked against
the real market price. All math and data live in `tools/*.py` — the LLM chooses
inputs and interprets outputs, but never does arithmetic.

Every run also produces an interactive **HTML report** that fuses the valuation,
a **WACC × terminal-growth sensitivity heatmap**, and a **timeline of every agent
and tool call** — so a student can see not just the answer but how the fleet got
there.

## Setup

```bash
pip install -r requirements.txt
```

Set your **own** SEC User-Agent (EDGAR requires a real name + email, and each
person must identify themselves). Copy the template to your personal, git-ignored
local settings file and edit it:

```bash
cp .claude/settings.local.json.example .claude/settings.local.json
# then edit .claude/settings.local.json → "Your Name your-email@example.com"
```

Claude Code merges `settings.local.json` over the shared `settings.json`, so your
identity stays on your machine and is never committed. (Prefer a shell env var,
or using Cline/Codex instead? `export SEC_USER_AGENT="Your Name you@example.com"`
works too — the tools read the env var either way.)

## Run

```
/valuation AAPL
```

Outputs land in `data/<CIK>/` (cached facts, narrative, per-lane JSON) plus two
reports in `reports/`: a `<TICKER>-<date>.md` summary and an interactive
`<TICKER>-<date>.html` (valuation + sensitivity heatmap + agent timeline). Open
the `.html` in any browser. The first run fetches from EDGAR; later runs reuse the
cache. Use the same seed for reproducible numbers.

## The pipeline

| Stage | Agent | Tools |
|-------|-------|-------|
| Fetch + normalize | edgar-analyst | `edgar_fetch.py`, `financials.py` |
| DCF + sensitivity | dcf-analyst | `montecarlo_dcf.py`, `sensitivity.py` |
| Comparables (2 sources) | comps-analyst | `embeddings.py`, `comps.py` |
| Qualitative / risk / non-recurring | qualitative-analyst | (reads `narrative.txt`) |
| Reconcile + report | reconciliation-analyst | `reconcile.py`, `market_price.py`, `build_trace_site.py` |

The **P90/P10 governance gate**: `reconcile.py` flags `review_required` when the
fair-value spread exceeds 2× (or the downside is non-positive), mirroring the
"human review before publication" rule from the lecture.

The **agent timeline** comes from PreToolUse/PostToolUse hooks (`.claude/settings.json`)
that append each tool/sub-agent call to `data/trace.jsonl`; `build_trace_site.py`
turns that log into the timeline. Delete `data/trace.jsonl` between runs for a
clean slate.

## Things to try in class

- Run several companies and compare the market gap (over/under-valued).
- Swap `universe.txt` for a sector list and re-run with `--rebuild` to see how
  embedding peers change.
- Edit a DCF prior (e.g. WACC mean) and watch the range move.
- Read the sensitivity heatmap: how fast does value explode as terminal growth
  `g` approaches WACC? (This is the terminal-value dominance from the lecture.)
- Compare LLM-proposed peers vs embedding peers — do they agree?
- Make a lane fail (bad ticker) and see how reconciliation degrades gracefully.
- Widen a prior until the P90/P10 gate trips `review_required` — what spread is
  "too fragile to publish"?
- Open the HTML report and walk the agent timeline: which lane took longest, and
  which tool call produced each number?

## Tests

```bash
python -m pytest -q   # fully offline, uses tests/fixtures/
```
