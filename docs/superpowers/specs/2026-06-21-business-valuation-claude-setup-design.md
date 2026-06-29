# Business Valuation Claude Code Setup — Design Spec

**Date:** 2026-06-21
**Location:** `exercises/business_valuation/`
**Author:** Juan F. Imbet (with Claude)
**Status:** Approved design — ready for implementation planning

---

## 1. Purpose

A self-contained **Claude Code project** that students open and drive with a single
command:

```
/valuation <cik|ticker>
```

A fleet of single-purpose agents coordinates — via a skill, parallel tasks, and a
reconciliation step — to produce a **fair-value point estimate plus an uncertainty
range** for a public company. The exercise teaches three things at once:

1. **Skill = workflow** — how a slash command orchestrates an agent fleet.
2. **Parallel agents** — fan-out → synthesize across independent valuation lanes.
3. **Tool delegation** — the LLM never does arithmetic; all math and data live behind
   Python CLI tools with strict JSON contracts.

This is a **complete, working reference setup** (not a gapped scaffold). It is used
live in class on different companies, and students may make small modifications
(swap the universe, change DCF priors, add a lane).

**Hard constraint (project convention):** the exercise must genuinely depend on
LLMs/agents/orchestration concepts — it is not a re-test of pure finance.

---

## 2. Architecture

```
exercises/business_valuation/
├── README.md                  # student-facing: install, run, "things to try in class"
├── requirements.txt
├── .claude/
│   ├── settings.json          # permissions for `python tools/*.py`; SEC_USER_AGENT env
│   ├── skills/
│   │   └── valuation/SKILL.md # the /valuation orchestrator (the "workflow")
│   └── agents/
│       ├── edgar-analyst.md          # fetch + sanity-check financial facts
│       ├── dcf-analyst.md            # choose assumption distributions, run MC-DCF
│       ├── comps-analyst.md          # propose peers, run multiples (two peer sources)
│       ├── qualitative-analyst.md    # read 10-K narrative → risk + prior adjustments
│       └── reconciliation-analyst.md # combine lanes → final number + range + report
├── tools/                     # ALL math & data lives here (LLM never computes)
│   ├── edgar_fetch.py         # ticker→CIK, company-facts JSON, 10-K narrative; caches
│   ├── financials.py          # normalize XBRL facts → clean DCF inputs
│   ├── montecarlo_dcf.py      # MC DCF → median + P10–P90 + samples
│   ├── embeddings.py          # embed narratives, build/query cached index → peer NN
│   ├── comps.py               # peer multiples (per source) → implied-value distribution
│   ├── market_price.py        # yfinance real price + market cap (benchmark only)
│   └── reconcile.py           # pool lane distributions w/ weights → final number+range
├── data/                      # cache (gitignored): data/<CIK>/...  + embedding index
├── reports/                   # output: reports/<TICKER>-<date>.md
└── tests/                     # pytest, runs fully offline against cached fixtures
```

### Agent fleet (5 single-purpose agents)

| Agent | Responsibility | Tools it calls |
|-------|----------------|----------------|
| `edgar-analyst` | Resolve ticker/CIK, fetch + cache facts & narrative, sanity-check | `edgar_fetch.py`, `financials.py` |
| `dcf-analyst` | Choose driver **distributions**, run Monte-Carlo DCF | `montecarlo_dcf.py` |
| `comps-analyst` | Propose LLM peers; get embedding peers; run multiples per source | `embeddings.py`, `comps.py` |
| `qualitative-analyst` | Read 10-K narrative → risk assessment + prior adjustments + lane weights | (reads `narrative.txt`) |
| `reconciliation-analyst` | Weight & pool lanes; benchmark vs market; write report | `reconcile.py`, `market_price.py` |

---

## 3. Methodology

Three valuation lanes run **in parallel, blind to each other**, then reconcile.

### Lane 1 — DCF (Monte Carlo)
`dcf-analyst` reads normalized financials and chooses **distributions** (not point
values) for the key drivers: revenue growth, operating margin, WACC, terminal growth.
`montecarlo_dcf.py` samples N paths → median equity value/share + P10–P90 band +
the raw sample array (so reconcile can pool distributions).

### Lane 2 — Comparables (dual source)
Peers come from **two independent sources**, run separately so the report can show
whether they converge:
- **Source A — LLM-proposed peers:** `comps-analyst` names 4–8 peers from domain
  knowledge; tool validates each exists on EDGAR.
- **Source B — embedding-similarity peers:** `embeddings.py` embeds the narrative
  text of a configurable **company universe** (`universe.txt`, shipped default
  ~100–150 large caps), builds a cached vector index, returns nearest neighbors —
  "similar" grounded in what companies *say about themselves*.

`comps.py` computes EV/EBITDA and P/E multiple **distributions** from each peer set
and applies them to the target → an implied value/share distribution per source.

### Lane 3 — Qualitative / Risk
`qualitative-analyst` reads `narrative.txt` (MD&A + risk factors) and emits concrete,
machine-usable adjustments: e.g. "widen WACC +1.5pp", "haircut terminal growth",
suggested **lane weights**, and caveats. This is the most LLM-native lane — text
understanding feeding the numeric model.

### Reconciliation
`reconciliation-analyst` decides lane weights **informed by** the qualitative output,
then `reconcile.py` pools the DCF and comps sample distributions under those weights
→ `final.json` (median + P10–P90). The agent writes the report.

### Market benchmark (post-hoc only)
`market_price.py` (yfinance) fetches the **real** current share price + market cap.
This is a **benchmark, never a valuation input** (to avoid anchoring the model to the
answer). The report shows fair value vs. market price, implied % over/undervaluation,
and where market price falls within the P10–P90 band.

---

## 4. Data flow (`/valuation AAPL`)

1. **Resolve & fetch** — `edgar-analyst` runs `edgar_fetch.py --ticker AAPL`
   (ticker→CIK via SEC `company_tickers.json`, company-facts JSON + latest 10-K
   narrative, cached to `data/<CIK>/`). `financials.py` normalizes XBRL →
   `data/<CIK>/financials.json`. Agent sanity-checks (latest fiscal year present, no
   negative revenue) and surfaces gaps.
2. **Parallel fan-out** — DCF, comps, and qualitative lanes run concurrently, each
   writing a structured JSON result.
3. **Reconcile** — `reconciliation-analyst` weights lanes (informed by qualitative),
   runs `reconcile.py` → `final.json`, fetches `market_price.py`, writes
   `reports/AAPL-<date>.md`.
4. **Headline** — skill prints: `AAPL fair value ≈ $X/share (P10–P90: $Y–$Z); market
   $M (Δ ±k%)` + report path.

---

## 5. Tool contracts (JSON in, JSON out; non-zero exit + `{"error": ...}` on failure)

| Tool | Key args | Emits |
|------|----------|-------|
| `edgar_fetch.py` | `--ticker/--cik`, `--no-cache` | `companyfacts.json`, `narrative.txt` |
| `financials.py` | `--cik` | `financials.json` (revenue, EBIT, D&A, capex, ΔNWC, debt, cash, shares) |
| `montecarlo_dcf.py` | `--financials --config --seed --n` | `dcf_result.json` (median, P10/P90, samples) |
| `embeddings.py` | `--cik --universe --top-k --rebuild` | `embed_peers.json` (neighbors + scores) |
| `comps.py` | `--cik --peers --source --seed` | `comps_<source>.json` (implied value dist per source) |
| `market_price.py` | `--ticker` | `market.json` (price, market cap, currency) |
| `reconcile.py` | `--dcf --comps --weights --seed` | `final.json` (median, P10/P90) |

---

## 6. Key design decisions (locked)

- **Tools via Bash CLI** (not MCP) — transparency + zero setup; "math behind a CLI
  contract" is the lesson.
- **Hybrid EDGAR source** — XBRL company-facts API for the numbers (robust), 10-K
  narrative for the qualitative + embedding lanes (real text).
- **Local caching** to `data/` — reproducible, works offline after first fetch.
- **Monte Carlo** for the range — median + P10–P90.
- **LLM-proposed peers + embedding peers** — two independent comparable sources.
- **Local `sentence-transformers` (`all-MiniLM-L6-v2`)** for embeddings — offline,
  free, no API key; ties to the book's privacy/local-models chapter.
- **Configurable embedding universe** (`universe.txt`, shipped default) — first index
  build is slow then cached.
- **Market price is benchmark-only**, never a valuation input.
- **Single `--seed`** threads all stochastic tools → deterministic class runs.

---

## 7. Error handling & reproducibility

- Tools fail loud (non-zero exit + JSON error) on: ticker/CIK not found, missing XBRL
  facts, network failure (fall back to cache if present, else error), too few valid
  peers, yfinance miss.
- Agents **surface tool errors verbatim; never invent a number.** If a lane fails, the
  skill proceeds with surviving lanes and the report notes the gap and its effect on
  confidence.
- SEC requires a descriptive `User-Agent` → `SEC_USER_AGENT` env via `settings.json`,
  documented in README.
- `--seed` makes same ticker + same seed + same cache → identical numbers.

---

## 8. Testing

- `pytest` per tool against **cached fixtures** (sample company-facts JSON, a tiny
  2-company universe) — suite runs **fully offline**.
- Fixed-seed smoke test: `montecarlo_dcf.py` reproduces a known median.
- One end-to-end test on cached data: the `/valuation` tool chain runs start→finish
  and produces a well-formed `final.json`.

---

## 9. Student-facing README

Covers: install (`pip install -r requirements.txt`), set `SEC_USER_AGENT`, run
`/valuation AAPL`, where outputs land, and **"things to try in class"** — different
companies, swap the universe, change DCF priors, compare LLM vs embedding peers, read
the market gap.

---

## 10. Out of scope (YAGNI)

- No MCP server, no hosted embedding API, no web UI.
- No gapped/starter version (working reference only; can be carved out later).
- Market price is not optimized into the valuation; no live trading data beyond a
  single price snapshot.
