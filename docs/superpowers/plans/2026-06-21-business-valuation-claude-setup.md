# Business Valuation Claude Code Setup — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a self-contained Claude Code project under `exercises/business_valuation/` where students run `/valuation <cik|ticker>` and a fleet of agents coordinates three parallel valuation lanes (Monte-Carlo DCF, dual-source comparables, qualitative/risk) to produce a median + P10–P90 fair value, benchmarked against the real market price.

**Architecture:** Seven Python CLI tools own ALL data + math behind strict JSON contracts; five single-purpose agents and one orchestrating skill own the reasoning. Tools are invoked via Bash. Each tool exposes pure functions (unit-tested offline against fixtures) plus a thin `__main__` CLI. Numbers never come from the LLM.

**Tech Stack:** Python 3.10+, `requests` (EDGAR), `numpy` (Monte Carlo), `sentence-transformers` (local embeddings, `all-MiniLM-L6-v2`), `yfinance` (market price), `pytest` (offline tests). Claude Code skill + agent markdown.

## Global Constraints

- All tool paths are relative to the project root `exercises/business_valuation/`; tools live in `tools/` and import siblings by module name (the script's dir is on `sys.path`).
- Every tool: prints its result JSON to stdout; on failure prints `{"error": "..."}` to stdout and exits non-zero (via `die()`).
- All stochastic tools accept `--seed` (default `0`); same ticker + same seed + same cache → identical numbers.
- CIK is always zero-padded to 10 digits via `cik_pad()`.
- Cache root is `data/` (gitignored); embedding index and `company_tickers.json` cache live directly under `data/`.
- SEC network calls require `SEC_USER_AGENT` env var; tools `die()` with a clear message if unset.
- Market price is a BENCHMARK only — never an input to any valuation lane.
- Embedding model is local `all-MiniLM-L6-v2` (offline, no API key).
- Tests run FULLY OFFLINE against fixtures in `tests/fixtures/`; no test makes a network call.
- Commit after every task with `feat(valuation): <summary>`.

---

## File Structure

```
exercises/business_valuation/
├── README.md                       # Task 11
├── requirements.txt                # Task 1
├── .gitignore                      # Task 1
├── universe.txt                    # Task 1 (default embedding universe)
├── .claude/
│   ├── settings.json               # Task 1
│   ├── agents/                     # Task 9
│   │   ├── edgar-analyst.md
│   │   ├── dcf-analyst.md
│   │   ├── comps-analyst.md
│   │   ├── qualitative-analyst.md
│   │   └── reconciliation-analyst.md
│   └── skills/valuation/SKILL.md   # Task 10
├── tools/
│   ├── _common.py                      # Task 1  shared cache/JSON/error helpers
│   ├── edgar_fetch.py              # Task 2
│   ├── financials.py               # Task 3
│   ├── montecarlo_dcf.py           # Task 4
│   ├── market_price.py             # Task 5
│   ├── comps.py                    # Task 6
│   ├── embeddings.py               # Task 7
│   └── reconcile.py                # Task 8
├── data/                           # cache (gitignored)
├── reports/                        # output reports (gitignored except .gitkeep)
└── tests/
    ├── fixtures/
    │   ├── company_tickers.json    # Task 1
    │   └── companyfacts_TEST.json  # Task 3
    ├── test_common.py                  # Task 1
    ├── test_edgar_fetch.py         # Task 2
    ├── test_financials.py          # Task 3
    ├── test_montecarlo_dcf.py      # Task 4
    ├── test_market_price.py        # Task 5
    ├── test_comps.py               # Task 6
    ├── test_embeddings.py          # Task 7
    ├── test_reconcile.py           # Task 8
    └── test_e2e.py                 # Task 11
```

All `pytest` commands run from `exercises/business_valuation/`. Add `tests/conftest.py` (Task 1) so `tools/` is importable in tests.

---

### Task 1: Scaffold — directories, deps, shared I/O helpers

**Files:**
- Create: `exercises/business_valuation/requirements.txt`
- Create: `exercises/business_valuation/.gitignore`
- Create: `exercises/business_valuation/universe.txt`
- Create: `exercises/business_valuation/.claude/settings.json`
- Create: `exercises/business_valuation/tools/_common.py`
- Create: `exercises/business_valuation/tests/conftest.py`
- Create: `exercises/business_valuation/tests/fixtures/company_tickers.json`
- Create: `exercises/business_valuation/reports/.gitkeep`
- Test: `exercises/business_valuation/tests/test_common.py`

**Interfaces:**
- Produces:
  - `cik_pad(cik) -> str` — digits only, left-padded to 10.
  - `data_dir(cik) -> pathlib.Path` — `data/<cik10>/`, created.
  - `write_json(path, obj) -> path`, `read_json(path) -> obj`
  - `emit(obj) -> None` — `print(json.dumps(obj, indent=2))`
  - `die(msg) -> NoReturn` — prints `{"error": msg}`, `sys.exit(1)`
  - `sec_headers() -> dict` — `{"User-Agent": $SEC_USER_AGENT, ...}`, `die()` if env unset.
  - Module constants `PROJECT_ROOT`, `DATA_ROOT`.

- [ ] **Step 1: Create `requirements.txt`**

```
requests>=2.31
numpy>=1.24
sentence-transformers>=2.2
yfinance>=0.2.40
pytest>=7.4
```

- [ ] **Step 2: Create `.gitignore`**

```
data/
reports/*
!reports/.gitkeep
__pycache__/
*.pyc
.pytest_cache/
```

- [ ] **Step 3: Create `universe.txt`** (default embedding universe; instructor may expand to ~100–150)

```
AAPL
MSFT
GOOGL
AMZN
META
NVDA
TSLA
ORCL
CRM
ADBE
INTC
AMD
CSCO
IBM
QCOM
TXN
AVGO
NFLX
DIS
KO
PEP
PG
WMT
COST
HD
NKE
MCD
JPM
BAC
V
MA
```

- [ ] **Step 4: Create `.claude/settings.json`** (permissions for tools; SEC env placeholder)

```json
{
  "permissions": {
    "allow": [
      "Bash(python tools/edgar_fetch.py:*)",
      "Bash(python tools/financials.py:*)",
      "Bash(python tools/montecarlo_dcf.py:*)",
      "Bash(python tools/market_price.py:*)",
      "Bash(python tools/comps.py:*)",
      "Bash(python tools/embeddings.py:*)",
      "Bash(python tools/reconcile.py:*)",
      "Bash(pip install:*)"
    ]
  },
  "env": {
    "SEC_USER_AGENT": "REPLACE WITH: Your Name your-email@example.com"
  }
}
```

- [ ] **Step 5: Create `tests/conftest.py`** (make `tools/` importable)

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
```

- [ ] **Step 6: Create `tests/fixtures/company_tickers.json`** (SEC format: index -> {cik_str, ticker, title})

```json
{
  "0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."},
  "1": {"cik_str": 789019, "ticker": "MSFT", "title": "Microsoft Corp"},
  "2": {"cik_str": 1318605, "ticker": "TSLA", "title": "Tesla Inc"}
}
```

- [ ] **Step 7: Create `reports/.gitkeep`** (empty file).

- [ ] **Step 8: Write the failing test** — `tests/test_common.py`

```python
import json
import pytest
import _common


def test_cik_pad_from_int():
    assert _common.cik_pad(320193) == "0000320193"


def test_cik_pad_from_padded_string():
    assert _common.cik_pad("CIK0000320193") == "0000320193"


def test_write_then_read_roundtrip(tmp_path):
    p = tmp_path / "x.json"
    _common.write_json(p, {"a": 1})
    assert _common.read_json(p) == {"a": 1}


def test_die_exits_nonzero_with_error_json(capsys):
    with pytest.raises(SystemExit) as e:
        _common.die("boom")
    assert e.value.code == 1
    out = json.loads(capsys.readouterr().out)
    assert out == {"error": "boom"}


def test_sec_headers_requires_env(monkeypatch):
    monkeypatch.delenv("SEC_USER_AGENT", raising=False)
    with pytest.raises(SystemExit):
        _common.sec_headers()


def test_sec_headers_uses_env(monkeypatch):
    monkeypatch.setenv("SEC_USER_AGENT", "Tester t@example.com")
    assert _common.sec_headers()["User-Agent"] == "Tester t@example.com"
```

- [ ] **Step 9: Run test to verify it fails**

Run: `cd exercises/business_valuation && python -m pytest tests/test_common.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named '_common'` / attribute errors.

- [ ] **Step 10: Create `tools/_common.py`**

```python
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = PROJECT_ROOT / "data"


def cik_pad(cik):
    digits = "".join(ch for ch in str(cik) if ch.isdigit())
    if not digits:
        die(f"invalid CIK: {cik!r}")
    return digits.rjust(10, "0")


def data_dir(cik):
    d = DATA_ROOT / cik_pad(cik)
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2))
    return path


def read_json(path):
    return json.loads(Path(path).read_text())


def emit(obj):
    print(json.dumps(obj, indent=2))


def die(msg):
    print(json.dumps({"error": str(msg)}))
    sys.exit(1)


def sec_headers():
    ua = os.environ.get("SEC_USER_AGENT")
    if not ua or ua.startswith("REPLACE"):
        die("SEC_USER_AGENT env var not set. Set it to e.g. 'Your Name you@example.com'")
    return {"User-Agent": ua, "Accept-Encoding": "gzip, deflate"}
```

- [ ] **Step 11: Run test to verify it passes**

Run: `cd exercises/business_valuation && python -m pytest tests/test_common.py -v`
Expected: PASS (6 passed).

- [ ] **Step 12: Commit**

```bash
git add exercises/business_valuation
git commit -m "feat(valuation): scaffold project, deps, and shared I/O helpers"
```

---

### Task 2: `edgar_fetch.py` — resolve CIK, fetch + cache facts & narrative

**Files:**
- Create: `exercises/business_valuation/tools/edgar_fetch.py`
- Test: `exercises/business_valuation/tests/test_edgar_fetch.py`

**Interfaces:**
- Consumes: `_common.cik_pad`, `_common.sec_headers`, `_common.read_json`, `_common.write_json`, `_common.data_dir`, `_common.emit`, `_common.die`, `_common.DATA_ROOT`.
- Produces:
  - `resolve_cik(ticker, tickers_map) -> str` (10-digit; `die()` if not found)
  - `strip_html(html) -> str` (tags/entities/whitespace removed)
  - `fetch_company_facts(cik, no_cache=False) -> dict` (network; cache-first)
  - `fetch_narrative(cik, no_cache=False) -> str` (network; cache-first; writes `narrative.txt`)
  - CLI writes/uses `data/<cik>/companyfacts.json` and `data/<cik>/narrative.txt`.

- [ ] **Step 1: Write the failing test** — `tests/test_edgar_fetch.py` (pure functions only; no network)

```python
import pytest
import edgar_fetch


def test_resolve_cik_found():
    m = {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}}
    assert edgar_fetch.resolve_cik("aapl", m) == "0000320193"


def test_resolve_cik_missing_dies():
    with pytest.raises(SystemExit):
        edgar_fetch.resolve_cik("ZZZZ", {"0": {"cik_str": 1, "ticker": "AAPL"}})


def test_strip_html_removes_tags_and_collapses_space():
    html = "<html><body><p>Risk&nbsp;Factors:   competition</p></body></html>"
    assert edgar_fetch.strip_html(html) == "Risk Factors: competition"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd exercises/business_valuation && python -m pytest tests/test_edgar_fetch.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'edgar_fetch'`.

- [ ] **Step 3: Create `tools/edgar_fetch.py`**

```python
import argparse
import re

import requests

from _common import (DATA_ROOT, cik_pad, data_dir, die, emit, read_json,
                 sec_headers, write_json)

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"


def load_tickers_map(no_cache=False):
    cache = DATA_ROOT / "company_tickers.json"
    if cache.exists() and not no_cache:
        return read_json(cache)
    r = requests.get(TICKERS_URL, headers=sec_headers(), timeout=30)
    r.raise_for_status()
    data = r.json()
    write_json(cache, data)
    return data


def resolve_cik(ticker, tickers_map):
    t = ticker.upper()
    for row in tickers_map.values():
        if str(row["ticker"]).upper() == t:
            return cik_pad(row["cik_str"])
    die(f"ticker {ticker} not found in SEC company_tickers")


def ticker_for_cik(cik, tickers_map):
    c = cik_pad(cik)
    for row in tickers_map.values():
        if cik_pad(row["cik_str"]) == c:
            return str(row["ticker"]).upper()
    return None


def strip_html(html):
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&#?\w+;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def fetch_company_facts(cik, no_cache=False):
    path = data_dir(cik) / "companyfacts.json"
    if path.exists() and not no_cache:
        return read_json(path)
    r = requests.get(FACTS_URL.format(cik=cik_pad(cik)), headers=sec_headers(), timeout=30)
    if r.status_code != 200:
        if path.exists():
            return read_json(path)
        die(f"company facts unavailable for CIK {cik} (HTTP {r.status_code})")
    data = r.json()
    write_json(path, data)
    return data


def fetch_narrative(cik, no_cache=False):
    path = data_dir(cik) / "narrative.txt"
    if path.exists() and not no_cache:
        return path.read_text()
    sub = requests.get(SUBMISSIONS_URL.format(cik=cik_pad(cik)), headers=sec_headers(), timeout=30)
    if sub.status_code != 200:
        if path.exists():
            return path.read_text()
        die(f"submissions unavailable for CIK {cik} (HTTP {sub.status_code})")
    recent = sub.json()["filings"]["recent"]
    idx = next((i for i, f in enumerate(recent["form"]) if f == "10-K"), None)
    if idx is None:
        die(f"no 10-K filing found for CIK {cik}")
    accession = recent["accessionNumber"][idx].replace("-", "")
    primary = recent["primaryDocument"][idx]
    doc_url = (f"https://www.sec.gov/Archives/edgar/data/"
               f"{int(cik_pad(cik))}/{accession}/{primary}")
    doc = requests.get(doc_url, headers=sec_headers(), timeout=60)
    if doc.status_code != 200:
        die(f"10-K document fetch failed for CIK {cik} (HTTP {doc.status_code})")
    text = strip_html(doc.text)
    path.write_text(text)
    return text


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--ticker")
    g.add_argument("--cik")
    ap.add_argument("--no-cache", action="store_true")
    a = ap.parse_args()
    tickers = load_tickers_map(a.no_cache)
    if a.ticker:
        cik = resolve_cik(a.ticker, tickers)
        ticker = a.ticker.upper()
    else:
        cik = cik_pad(a.cik)
        ticker = ticker_for_cik(cik, tickers)
    facts = fetch_company_facts(cik, a.no_cache)
    fetch_narrative(cik, a.no_cache)
    emit({
        "cik": cik,
        "ticker": ticker,
        "entity": facts.get("entityName"),
        "companyfacts": str(data_dir(cik) / "companyfacts.json"),
        "narrative": str(data_dir(cik) / "narrative.txt"),
    })


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd exercises/business_valuation && python -m pytest tests/test_edgar_fetch.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add exercises/business_valuation/tools/edgar_fetch.py exercises/business_valuation/tests/test_edgar_fetch.py
git commit -m "feat(valuation): EDGAR fetch tool (CIK resolve, facts, narrative) with caching"
```

---

### Task 3: `financials.py` — normalize XBRL company facts into DCF inputs

**Files:**
- Create: `exercises/business_valuation/tools/financials.py`
- Create: `exercises/business_valuation/tests/fixtures/companyfacts_TEST.json`
- Test: `exercises/business_valuation/tests/test_financials.py`

**Interfaces:**
- Consumes: `_common.read_json`, `_common.write_json`, `_common.data_dir`, `_common.cik_pad`, `_common.emit`, `_common.die`; `edgar_fetch` (CLI path only).
- Produces:
  - `latest_annual(facts, tags, unit="USD") -> float | None`
  - `delta_nwc(facts) -> float`
  - `normalize(facts, ticker=None) -> dict` with keys: `cik, ticker, entity, fiscal_year, revenue, ebit, da, capex, delta_nwc, total_debt, cash, shares, net_income, ebitda, tax_rate`.
  - CLI writes `data/<cik>/financials.json`.

- [ ] **Step 1: Create the fixture** — `tests/fixtures/companyfacts_TEST.json` (minimal, two annual years where needed)

```json
{
  "cik": 320193,
  "entityName": "TEST CO",
  "facts": {
    "us-gaap": {
      "Revenues": {"units": {"USD": [
        {"form": "10-K", "fy": 2023, "fp": "FY", "end": "2023-12-31", "val": 1000},
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 1100}
      ]}},
      "OperatingIncomeLoss": {"units": {"USD": [
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 300}
      ]}},
      "DepreciationDepletionAndAmortization": {"units": {"USD": [
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 90}
      ]}},
      "PaymentsToAcquirePropertyPlantAndEquipment": {"units": {"USD": [
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 70}
      ]}},
      "AssetsCurrent": {"units": {"USD": [
        {"form": "10-K", "fy": 2023, "fp": "FY", "end": "2023-12-31", "val": 500},
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 560}
      ]}},
      "LiabilitiesCurrent": {"units": {"USD": [
        {"form": "10-K", "fy": 2023, "fp": "FY", "end": "2023-12-31", "val": 300},
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 320}
      ]}},
      "LongTermDebtNoncurrent": {"units": {"USD": [
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 400}
      ]}},
      "CashAndCashEquivalentsAtCarryingValue": {"units": {"USD": [
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 200}
      ]}},
      "NetIncomeLoss": {"units": {"USD": [
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 240}
      ]}},
      "IncomeTaxExpenseBenefit": {"units": {"USD": [
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 60}
      ]}},
      "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest": {"units": {"USD": [
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 300}
      ]}},
      "CommonStockSharesOutstanding": {"units": {"shares": [
        {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-12-31", "val": 100}
      ]}}
    }
  }
}
```

- [ ] **Step 2: Write the failing test** — `tests/test_financials.py`

```python
import json
from pathlib import Path

import financials

FIX = Path(__file__).parent / "fixtures" / "companyfacts_TEST.json"


def load():
    return json.loads(FIX.read_text())


def test_normalize_picks_latest_revenue():
    out = financials.normalize(load(), ticker="TEST")
    assert out["revenue"] == 1100
    assert out["fiscal_year"] == 2024


def test_normalize_computes_ebitda_and_delta_nwc():
    out = financials.normalize(load(), ticker="TEST")
    # ebitda = ebit + da = 300 + 90
    assert out["ebitda"] == 390
    # delta_nwc = (560-320) - (500-300) = 240 - 200 = 40
    assert out["delta_nwc"] == 40


def test_normalize_tax_rate_from_expense_over_pretax():
    out = financials.normalize(load(), ticker="TEST")
    # 60 / 300 = 0.2
    assert abs(out["tax_rate"] - 0.20) < 1e-9


def test_normalize_total_debt_and_shares():
    out = financials.normalize(load(), ticker="TEST")
    assert out["total_debt"] == 400
    assert out["shares"] == 100
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd exercises/business_valuation && python -m pytest tests/test_financials.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'financials'`.

- [ ] **Step 4: Create `tools/financials.py`**

```python
import argparse

from _common import cik_pad, data_dir, die, emit, read_json, write_json

TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax",
                "Revenues", "SalesRevenueNet"],
    "ebit": ["OperatingIncomeLoss"],
    "da": ["DepreciationDepletionAndAmortization",
           "DepreciationAmortizationAndAccretionNet",
           "DepreciationAndAmortization"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment",
              "PaymentsToAcquireProductiveAssets"],
    "current_assets": ["AssetsCurrent"],
    "current_liabilities": ["LiabilitiesCurrent"],
    "long_term_debt": ["LongTermDebtNoncurrent", "LongTermDebt"],
    "debt_current": ["LongTermDebtCurrent", "DebtCurrent"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue",
             "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"],
    "net_income": ["NetIncomeLoss"],
    "pretax_income": [
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
    "tax_expense": ["IncomeTaxExpenseBenefit"],
    "shares": ["CommonStockSharesOutstanding",
               "WeightedAverageNumberOfDilutedSharesOutstanding",
               "EntityCommonStockSharesOutstanding"],
}


def _annual_rows(facts, tag):
    gaap = facts.get("facts", {}).get("us-gaap", {})
    node = gaap.get(tag)
    if not node:
        return []
    units = node["units"]
    unit = "USD" if "USD" in units else ("shares" if "shares" in units else next(iter(units)))
    rows = [u for u in units[unit] if str(u.get("form", "")).startswith("10-K")]
    rows.sort(key=lambda u: u.get("end", ""))
    return rows


def latest_annual(facts, tags, unit="USD"):
    for tag in tags:
        rows = _annual_rows(facts, tag)
        if rows:
            return rows[-1]["val"]
    return None


def _two_latest(facts, tags):
    for tag in tags:
        rows = _annual_rows(facts, tag)
        if len(rows) >= 2:
            return rows[-1]["val"], rows[-2]["val"]
        if len(rows) == 1:
            return rows[-1]["val"], None
    return None, None


def delta_nwc(facts):
    ca1, ca0 = _two_latest(facts, TAGS["current_assets"])
    cl1, cl0 = _two_latest(facts, TAGS["current_liabilities"])
    if None in (ca1, ca0, cl1, cl0):
        return 0.0
    return (ca1 - cl1) - (ca0 - cl0)


def _fiscal_year(facts):
    for tag in TAGS["revenue"]:
        rows = _annual_rows(facts, tag)
        if rows:
            return rows[-1].get("fy")
    return None


def _num(facts, tags, default=0.0):
    val = latest_annual(facts, tags)
    return float(val) if val is not None else default


def normalize(facts, ticker=None):
    rev = latest_annual(facts, TAGS["revenue"])
    if rev is None or rev <= 0:
        die("could not find positive annual revenue in company facts")
    ebit = _num(facts, TAGS["ebit"])
    da = _num(facts, TAGS["da"])
    capex = _num(facts, TAGS["capex"])
    ltd = _num(facts, TAGS["long_term_debt"])
    dc = _num(facts, TAGS["debt_current"])
    cash = _num(facts, TAGS["cash"])
    ni = _num(facts, TAGS["net_income"])
    shares = latest_annual(facts, TAGS["shares"])
    if not shares or shares <= 0:
        die("could not find shares outstanding in company facts")
    pretax = latest_annual(facts, TAGS["pretax_income"])
    tax_exp = latest_annual(facts, TAGS["tax_expense"])
    if pretax and pretax > 0 and tax_exp is not None:
        tax_rate = max(0.0, min(0.45, tax_exp / pretax))
    else:
        tax_rate = 0.21
    return {
        "cik": cik_pad(facts.get("cik", 0)),
        "ticker": ticker,
        "entity": facts.get("entityName"),
        "fiscal_year": _fiscal_year(facts),
        "revenue": float(rev),
        "ebit": float(ebit),
        "da": float(da),
        "capex": float(capex),
        "delta_nwc": float(delta_nwc(facts)),
        "total_debt": float(ltd + dc),
        "cash": float(cash),
        "shares": float(shares),
        "net_income": float(ni),
        "ebitda": float(ebit + da),
        "tax_rate": float(tax_rate),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cik", required=True)
    ap.add_argument("--ticker")
    a = ap.parse_args()
    facts_path = data_dir(a.cik) / "companyfacts.json"
    if not facts_path.exists():
        die(f"{facts_path} not found — run edgar_fetch.py first")
    out = normalize(read_json(facts_path), ticker=a.ticker)
    write_json(data_dir(a.cik) / "financials.json", out)
    emit(out)


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd exercises/business_valuation && python -m pytest tests/test_financials.py -v`
Expected: PASS (4 passed).

- [ ] **Step 6: Commit**

```bash
git add exercises/business_valuation/tools/financials.py exercises/business_valuation/tests/test_financials.py exercises/business_valuation/tests/fixtures/companyfacts_TEST.json
git commit -m "feat(valuation): normalize XBRL company facts into DCF inputs"
```

---

### Task 4: `montecarlo_dcf.py` — Monte-Carlo DCF lane

**Files:**
- Create: `exercises/business_valuation/tools/montecarlo_dcf.py`
- Test: `exercises/business_valuation/tests/test_montecarlo_dcf.py`

**Interfaces:**
- Consumes: `_common.read_json`, `_common.write_json`, `_common.data_dir`, `_common.emit`, `_common.die`; financials dict from Task 3.
- Produces:
  - `run_dcf(fin: dict, cfg: dict, seed=0, n=10000) -> dict` with keys `lane="dcf", median, p10, p90, n, samples`.
  - Config schema: `{years, revenue_growth, operating_margin, wacc, terminal_growth, tax_rate?}` where each driver is `{"dist": "normal"|"lognormal"|"uniform"|"fixed", ...}`.
  - CLI writes `data/<cik>/dcf_result.json`.

- [ ] **Step 1: Write the failing test** — `tests/test_montecarlo_dcf.py`

```python
import montecarlo_dcf as mc

FIN = {"revenue": 1000.0, "da": 100.0, "capex": 50.0, "delta_nwc": 0.0,
       "total_debt": 0.0, "cash": 0.0, "shares": 100.0, "tax_rate": 0.0}

FIXED_CFG = {
    "years": 5,
    "revenue_growth": {"dist": "fixed", "value": 0.05},
    "operating_margin": {"dist": "fixed", "value": 0.20},
    "wacc": {"dist": "fixed", "value": 0.10},
    "terminal_growth": {"dist": "fixed", "value": 0.02},
    "tax_rate": 0.0,
}


def test_fixed_config_is_deterministic():
    out = mc.run_dcf(FIN, FIXED_CFG, seed=0, n=2000)
    # all draws identical -> band collapses to the point estimate
    assert abs(out["p10"] - out["p90"]) < 1e-6
    assert out["median"] > 0
    assert out["lane"] == "dcf"


def test_seed_reproducible():
    cfg = dict(FIXED_CFG, revenue_growth={"dist": "normal", "mean": 0.05, "sd": 0.02})
    a = mc.run_dcf(FIN, cfg, seed=42, n=3000)
    b = mc.run_dcf(FIN, cfg, seed=42, n=3000)
    assert a["median"] == b["median"]


def test_wacc_le_terminal_growth_is_guarded():
    cfg = dict(FIXED_CFG,
               wacc={"dist": "fixed", "value": 0.02},
               terminal_growth={"dist": "fixed", "value": 0.05})
    out = mc.run_dcf(FIN, cfg, seed=0, n=500)
    # guard prevents division blow-up -> finite, positive
    assert out["median"] > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd exercises/business_valuation && python -m pytest tests/test_montecarlo_dcf.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'montecarlo_dcf'`.

- [ ] **Step 3: Create `tools/montecarlo_dcf.py`**

```python
import argparse

import numpy as np

from _common import data_dir, die, emit, read_json, write_json


def _draw(rng, spec, n):
    d = spec.get("dist", "normal")
    if d == "fixed":
        return np.full(n, float(spec["value"]))
    if d == "normal":
        return rng.normal(spec["mean"], spec.get("sd", 0.0), n)
    if d == "lognormal":
        return rng.lognormal(spec["mean"], spec.get("sd", 0.0), n)
    if d == "uniform":
        return rng.uniform(spec["low"], spec["high"], n)
    die(f"unknown distribution: {d}")


def run_dcf(fin, cfg, seed=0, n=10000):
    rng = np.random.default_rng(seed)
    years = int(cfg.get("years", 5))
    g = _draw(rng, cfg["revenue_growth"], n)
    margin = _draw(rng, cfg["operating_margin"], n)
    wacc = _draw(rng, cfg["wacc"], n)
    tg = _draw(rng, cfg["terminal_growth"], n)
    tax = float(cfg.get("tax_rate", fin.get("tax_rate", 0.21)))

    rev0 = float(fin["revenue"])
    da_pct = float(fin["da"]) / rev0
    capex_pct = float(fin["capex"]) / rev0
    nwc_pct = float(fin.get("delta_nwc", 0.0)) / rev0

    # guard: terminal model requires wacc strictly above terminal growth
    wacc = np.where(wacc > tg + 0.005, wacc, tg + 0.01)
    fcff_margin = margin * (1.0 - tax) + da_pct - capex_pct - nwc_pct

    ev = np.zeros(n)
    rev = np.full(n, rev0)
    for y in range(1, years + 1):
        rev = rev * (1.0 + g)
        fcff = rev * fcff_margin
        ev += fcff / (1.0 + wacc) ** y
    fcff_final = rev * fcff_margin
    tv = fcff_final * (1.0 + tg) / (wacc - tg)
    ev += tv / (1.0 + wacc) ** years

    equity = ev - float(fin.get("total_debt", 0.0)) + float(fin.get("cash", 0.0))
    per_share = equity / float(fin["shares"])
    per_share = per_share[np.isfinite(per_share)]
    if per_share.size == 0:
        die("DCF produced no finite samples")
    return {
        "lane": "dcf",
        "median": float(np.median(per_share)),
        "p10": float(np.percentile(per_share, 10)),
        "p90": float(np.percentile(per_share, 90)),
        "n": int(per_share.size),
        "samples": per_share.tolist(),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--financials", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--cik", required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n", type=int, default=10000)
    a = ap.parse_args()
    out = run_dcf(read_json(a.financials), read_json(a.config), a.seed, a.n)
    write_json(data_dir(a.cik) / "dcf_result.json", out)
    emit({k: v for k, v in out.items() if k != "samples"})


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd exercises/business_valuation && python -m pytest tests/test_montecarlo_dcf.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add exercises/business_valuation/tools/montecarlo_dcf.py exercises/business_valuation/tests/test_montecarlo_dcf.py
git commit -m "feat(valuation): Monte-Carlo DCF lane with seedable drivers"
```

---

### Task 5: `market_price.py` — real share price benchmark (yfinance)

**Files:**
- Create: `exercises/business_valuation/tools/market_price.py`
- Test: `exercises/business_valuation/tests/test_market_price.py`

**Interfaces:**
- Consumes: `_common.emit`, `_common.die`, `_common.data_dir`, `_common.write_json`.
- Produces:
  - `get_price(ticker, fetcher=None) -> dict` with keys `ticker, price, market_cap, currency`. `fetcher` is injectable `(ticker) -> dict` for offline testing; default uses yfinance.

- [ ] **Step 1: Write the failing test** — `tests/test_market_price.py`

```python
import market_price


def fake_fetcher(ticker):
    return {"ticker": ticker.upper(), "price": 123.45,
            "market_cap": 2.0e12, "currency": "USD"}


def test_get_price_uses_injected_fetcher():
    out = market_price.get_price("aapl", fetcher=fake_fetcher)
    assert out["ticker"] == "AAPL"
    assert out["price"] == 123.45
    assert out["currency"] == "USD"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd exercises/business_valuation && python -m pytest tests/test_market_price.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'market_price'`.

- [ ] **Step 3: Create `tools/market_price.py`**

```python
import argparse

from _common import data_dir, die, emit, write_json


def _yfinance_fetch(ticker):
    import yfinance as yf
    t = yf.Ticker(ticker)
    fast = {}
    try:
        fast = dict(t.fast_info)
    except Exception:
        fast = {}
    price = fast.get("last_price") or fast.get("lastPrice")
    if price is None:
        hist = t.history(period="1d")
        if hist.empty:
            die(f"no market price available for {ticker}")
        price = float(hist["Close"].iloc[-1])
    return {
        "ticker": ticker.upper(),
        "price": float(price),
        "market_cap": float(fast["market_cap"]) if fast.get("market_cap") else None,
        "currency": fast.get("currency", "USD"),
    }


def get_price(ticker, fetcher=None):
    fetcher = fetcher or _yfinance_fetch
    return fetcher(ticker)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--cik")
    a = ap.parse_args()
    out = get_price(a.ticker)
    if a.cik:
        write_json(data_dir(a.cik) / "market.json", out)
    emit(out)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd exercises/business_valuation && python -m pytest tests/test_market_price.py -v`
Expected: PASS (1 passed).

- [ ] **Step 5: Commit**

```bash
git add exercises/business_valuation/tools/market_price.py exercises/business_valuation/tests/test_market_price.py
git commit -m "feat(valuation): market price benchmark tool (yfinance, injectable fetcher)"
```

---

### Task 6: `comps.py` — comparables lane (peer multiples → implied value)

**Files:**
- Create: `exercises/business_valuation/tools/comps.py`
- Test: `exercises/business_valuation/tests/test_comps.py`

**Interfaces:**
- Consumes: `_common.emit`, `_common.die`, `_common.read_json`, `_common.write_json`, `_common.data_dir`, `_common.cik_pad`; `financials.normalize`, `edgar_fetch.{load_tickers_map,resolve_cik,fetch_company_facts}`, `market_price.get_price`.
- Produces:
  - `peer_metrics(fin: dict, price: float) -> dict` with keys `ev_ebitda, pe` (either may be `None`).
  - `implied_values(target: dict, multiples: list[dict], seed=0, n=10000) -> dict` with keys `median, p10, p90, n, samples`.
  - CLI writes `data/<cik>/comps_<source>.json` tagged with `source` and `peers`.

- [ ] **Step 1: Write the failing test** — `tests/test_comps.py`

```python
import comps

TARGET = {"ebit": 300.0, "da": 90.0, "ebitda": 390.0, "net_income": 240.0,
          "shares": 100.0, "total_debt": 400.0, "cash": 200.0}


def test_peer_metrics_basic():
    fin = {"shares": 50.0, "total_debt": 100.0, "cash": 50.0,
           "ebitda": 200.0, "net_income": 120.0, "ebit": 150.0, "da": 50.0}
    m = comps.peer_metrics(fin, price=20.0)
    # market_cap = 20*50 = 1000 ; ev = 1000 + 100 - 50 = 1050
    assert abs(m["ev_ebitda"] - 1050 / 200) < 1e-9
    # pe = 1000 / 120
    assert abs(m["pe"] - 1000 / 120) < 1e-9


def test_implied_values_within_peer_range():
    multiples = [{"ev_ebitda": 5.0, "pe": 4.0}, {"ev_ebitda": 7.0, "pe": 6.0}]
    out = comps.implied_values(TARGET, multiples, seed=1, n=4000)
    assert out["p10"] <= out["median"] <= out["p90"]
    assert out["median"] > 0


def test_implied_values_no_valid_multiples_dies():
    import pytest
    with pytest.raises(SystemExit):
        comps.implied_values(TARGET, [{"ev_ebitda": None, "pe": None}], seed=0, n=10)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd exercises/business_valuation && python -m pytest tests/test_comps.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'comps'`.

- [ ] **Step 3: Create `tools/comps.py`**

```python
import argparse

import numpy as np

from _common import data_dir, die, emit, read_json, write_json


def peer_metrics(fin, price):
    shares = float(fin["shares"])
    market_cap = price * shares
    ev = market_cap + float(fin.get("total_debt", 0.0)) - float(fin.get("cash", 0.0))
    ebitda = float(fin.get("ebitda") or (fin["ebit"] + fin["da"]))
    ni = float(fin.get("net_income", 0.0))
    return {
        "ev_ebitda": ev / ebitda if ebitda > 0 else None,
        "pe": market_cap / ni if ni > 0 else None,
    }


def implied_values(target, multiples, seed=0, n=10000):
    rng = np.random.default_rng(seed)
    evb = np.array([m["ev_ebitda"] for m in multiples if m.get("ev_ebitda") is not None], dtype=float)
    pe = np.array([m["pe"] for m in multiples if m.get("pe") is not None], dtype=float)
    if evb.size == 0 and pe.size == 0:
        die("no valid peer multiples to build comparables")
    shares = float(target["shares"])
    target_ebitda = float(target.get("ebitda") or (target["ebit"] + target["da"]))
    target_ni = float(target.get("net_income", 0.0))
    debt = float(target.get("total_debt", 0.0))
    cash = float(target.get("cash", 0.0))

    samples = np.empty(n)
    for i in range(n):
        vals = []
        if evb.size:
            ev = target_ebitda * rng.choice(evb)
            vals.append((ev - debt + cash) / shares)
        if pe.size and target_ni > 0:
            vals.append(rng.choice(pe) * target_ni / shares)
        samples[i] = np.mean(vals)
    samples = samples[np.isfinite(samples)]
    return {
        "median": float(np.median(samples)),
        "p10": float(np.percentile(samples, 10)),
        "p90": float(np.percentile(samples, 90)),
        "n": int(samples.size),
        "samples": samples.tolist(),
    }


def _peer_financials_and_price(ticker, tickers_map):
    import edgar_fetch
    import financials as fin_mod
    import market_price
    cik = edgar_fetch.resolve_cik(ticker, tickers_map)
    facts = edgar_fetch.fetch_company_facts(cik)
    fin = fin_mod.normalize(facts, ticker=ticker)
    price = market_price.get_price(ticker)["price"]
    return fin, price


def main():
    import edgar_fetch
    ap = argparse.ArgumentParser()
    ap.add_argument("--cik", required=True)
    ap.add_argument("--peers", required=True, help="comma-separated peer tickers")
    ap.add_argument("--source", default="llm", help="peer-source label (llm|embedding)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n", type=int, default=10000)
    a = ap.parse_args()

    target = read_json(data_dir(a.cik) / "financials.json")
    tickers_map = edgar_fetch.load_tickers_map()
    multiples, used = [], []
    for tk in [p.strip().upper() for p in a.peers.split(",") if p.strip()]:
        try:
            fin, price = _peer_financials_and_price(tk, tickers_map)
            multiples.append(peer_metrics(fin, price))
            used.append(tk)
        except SystemExit:
            continue
    if not multiples:
        die("no peer multiples could be computed (check peer tickers / network)")
    out = implied_values(target, multiples, a.seed, a.n)
    out["source"] = a.source
    out["peers"] = used
    write_json(data_dir(a.cik) / f"comps_{a.source}.json", out)
    emit({k: v for k, v in out.items() if k != "samples"})


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd exercises/business_valuation && python -m pytest tests/test_comps.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add exercises/business_valuation/tools/comps.py exercises/business_valuation/tests/test_comps.py
git commit -m "feat(valuation): comparables lane (peer multiples -> implied value distribution)"
```

---

### Task 7: `embeddings.py` — embedding-similarity peers

**Files:**
- Create: `exercises/business_valuation/tools/embeddings.py`
- Test: `exercises/business_valuation/tests/test_embeddings.py`

**Interfaces:**
- Consumes: `_common.read_json`, `_common.write_json`, `_common.data_dir`, `_common.cik_pad`, `_common.emit`, `_common.die`, `_common.DATA_ROOT`; `edgar_fetch.{load_tickers_map,resolve_cik,fetch_narrative}`.
- Produces:
  - `build_index(items, embed=...) -> (np.ndarray, list)` where `items` is `list[{"ticker","cik","text"}]`; `embed(texts) -> np.ndarray` is injectable (rows L2-normalized).
  - `nearest(target_vec, vecs, items, k=8, exclude_cik=None) -> list[{"ticker","cik","score"}]`.
  - CLI writes `data/<cik>/embed_peers.json`; caches the universe index at `data/embed_index.npz`.

- [ ] **Step 1: Write the failing test** — `tests/test_embeddings.py`

```python
import numpy as np

import embeddings


def fake_embed(texts):
    # deterministic 2-D vectors keyed by first character, L2-normalized
    out = []
    for t in texts:
        v = np.array([1.0, 0.0]) if t.startswith("a") else np.array([0.0, 1.0])
        out.append(v / np.linalg.norm(v))
    return np.array(out)


def test_build_index_shape():
    items = [{"ticker": "A", "cik": 1, "text": "apple alpha"},
             {"ticker": "B", "cik": 2, "text": "banana beta"}]
    vecs, kept = embeddings.build_index(items, embed=fake_embed)
    assert vecs.shape == (2, 2)
    assert kept[0]["ticker"] == "A"


def test_nearest_ranks_by_cosine_and_excludes_self():
    items = [{"ticker": "A", "cik": 1, "text": "apple"},
             {"ticker": "A2", "cik": 2, "text": "almond"},
             {"ticker": "B", "cik": 3, "text": "banana"}]
    vecs, kept = embeddings.build_index(items, embed=fake_embed)
    target = fake_embed(["apricot"])[0]   # also "a*" -> [1,0]
    out = embeddings.nearest(target, vecs, kept, k=2, exclude_cik=1)
    tickers = [o["ticker"] for o in out]
    assert "A" not in tickers          # excluded self
    assert tickers[0] == "A2"          # nearest remaining "a*" beats "b*"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd exercises/business_valuation && python -m pytest tests/test_embeddings.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'embeddings'`.

- [ ] **Step 3: Create `tools/embeddings.py`**

```python
import argparse

import numpy as np

import edgar_fetch
from _common import DATA_ROOT, cik_pad, data_dir, die, emit, write_json

_MODEL = None


def _default_embed(texts):
    global _MODEL
    from sentence_transformers import SentenceTransformer
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return np.asarray(_MODEL.encode(list(texts), normalize_embeddings=True))


def build_index(items, embed=_default_embed):
    texts = [it["text"] for it in items]
    vecs = np.asarray(embed(texts))
    return vecs, items


def nearest(target_vec, vecs, items, k=8, exclude_cik=None):
    sims = vecs @ np.asarray(target_vec)
    out = []
    for i in np.argsort(-sims):
        if exclude_cik is not None and cik_pad(items[i]["cik"]) == cik_pad(exclude_cik):
            continue
        out.append({"ticker": items[i]["ticker"],
                    "cik": cik_pad(items[i]["cik"]),
                    "score": float(sims[i])})
        if len(out) >= k:
            break
    return out


def _load_universe(path):
    with open(path) as fh:
        return [ln.strip().upper() for ln in fh if ln.strip()]


def _build_universe_index(universe_tickers, tickers_map, rebuild=False):
    cache = DATA_ROOT / "embed_index.npz"
    if cache.exists() and not rebuild:
        z = np.load(cache, allow_pickle=True)
        return z["vecs"], [dict(d) for d in z["items"]]
    items = []
    for tk in universe_tickers:
        try:
            cik = edgar_fetch.resolve_cik(tk, tickers_map)
            text = edgar_fetch.fetch_narrative(cik)
        except SystemExit:
            continue
        items.append({"ticker": tk, "cik": cik, "text": text[:20000]})
    if not items:
        die("could not build embedding universe (no narratives fetched)")
    vecs, items = build_index(items)
    np.savez(cache, vecs=vecs, items=np.array(items, dtype=object))
    return vecs, items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cik", required=True)
    ap.add_argument("--universe", default="universe.txt")
    ap.add_argument("--top-k", type=int, default=8)
    ap.add_argument("--rebuild", action="store_true")
    a = ap.parse_args()

    tickers_map = edgar_fetch.load_tickers_map()
    universe = _load_universe(a.universe)
    vecs, items = _build_universe_index(universe, tickers_map, a.rebuild)

    narrative_path = data_dir(a.cik) / "narrative.txt"
    if not narrative_path.exists():
        die(f"{narrative_path} not found — run edgar_fetch.py first")
    target_vec = build_index([{"ticker": "TARGET", "cik": a.cik,
                               "text": narrative_path.read_text()[:20000]}])[0][0]
    peers = nearest(target_vec, vecs, items, k=a.top_k, exclude_cik=a.cik)
    out = {"cik": cik_pad(a.cik), "source": "embedding", "peers": peers}
    write_json(data_dir(a.cik) / "embed_peers.json", out)
    emit(out)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd exercises/business_valuation && python -m pytest tests/test_embeddings.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add exercises/business_valuation/tools/embeddings.py exercises/business_valuation/tests/test_embeddings.py
git commit -m "feat(valuation): embedding-similarity peer discovery (local sentence-transformers)"
```

---

### Task 8: `reconcile.py` — pool lane distributions into final number + range

**Files:**
- Create: `exercises/business_valuation/tools/reconcile.py`
- Test: `exercises/business_valuation/tests/test_reconcile.py`

**Interfaces:**
- Consumes: `_common.read_json`, `_common.write_json`, `_common.data_dir`, `_common.emit`, `_common.die`.
- Produces:
  - `pool(dcf: dict, comps_list: list[dict], weights: dict, seed=0, n=10000) -> dict` with keys `median, p10, p90, n, weights`. Each input result carries a `samples` list; comps results carry a `source` label; DCF lane name is `"dcf"`.
  - CLI reads `--dcf`, repeated `--comps`, `--weights` (JSON string), writes `data/<cik>/final.json`.

- [ ] **Step 1: Write the failing test** — `tests/test_reconcile.py`

```python
import reconcile


def test_pool_blends_two_lanes():
    dcf = {"lane": "dcf", "samples": [10.0] * 100}
    comps = {"source": "llm", "samples": [20.0] * 100}
    out = reconcile.pool(dcf, [comps], weights={"dcf": 0.5, "llm": 0.5}, seed=0, n=1000)
    # 50/50 blend of point masses at 10 and 20 -> median in [10, 20]
    assert 10.0 <= out["median"] <= 20.0
    assert out["p10"] == 10.0 and out["p90"] == 20.0


def test_pool_weight_skews_median():
    dcf = {"lane": "dcf", "samples": [10.0] * 100}
    comps = {"source": "llm", "samples": [20.0] * 100}
    heavy_dcf = reconcile.pool(dcf, [comps], {"dcf": 0.9, "llm": 0.1}, seed=0, n=1000)
    assert heavy_dcf["median"] == 10.0


def test_pool_normalizes_weights_and_reports_them():
    dcf = {"lane": "dcf", "samples": [10.0] * 50}
    comps = {"source": "llm", "samples": [20.0] * 50}
    out = reconcile.pool(dcf, [comps], {"dcf": 2.0, "llm": 2.0}, seed=0, n=400)
    assert abs(sum(out["weights"].values()) - 1.0) < 1e-9
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd exercises/business_valuation && python -m pytest tests/test_reconcile.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'reconcile'`.

- [ ] **Step 3: Create `tools/reconcile.py`**

```python
import argparse
import json

import numpy as np

from _common import data_dir, die, emit, read_json, write_json


def pool(dcf, comps_list, weights, seed=0, n=10000):
    rng = np.random.default_rng(seed)
    lanes = [("dcf", dcf)]
    for i, c in enumerate(comps_list):
        lanes.append((c.get("source", f"comps{i}"), c))

    w = np.array([float(weights.get(name, 1.0)) for name, _ in lanes])
    if w.sum() <= 0:
        die("lane weights sum to zero")
    w = w / w.sum()

    draws = []
    for (name, res), wi in zip(lanes, w):
        samples = np.asarray(res.get("samples", []), dtype=float)
        if samples.size == 0:
            continue
        cnt = max(1, int(round(wi * n)))
        draws.append(rng.choice(samples, cnt))
    if not draws:
        die("no lane samples available to reconcile")
    pooled = np.concatenate(draws)
    return {
        "median": float(np.median(pooled)),
        "p10": float(np.percentile(pooled, 10)),
        "p90": float(np.percentile(pooled, 90)),
        "n": int(pooled.size),
        "weights": {name: float(wi) for (name, _), wi in zip(lanes, w)},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dcf", required=True)
    ap.add_argument("--comps", action="append", default=[],
                    help="path to a comps_*.json (repeatable)")
    ap.add_argument("--weights", default="{}", help="JSON object of lane->weight")
    ap.add_argument("--cik", required=True)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n", type=int, default=10000)
    a = ap.parse_args()
    dcf = read_json(a.dcf)
    comps_list = [read_json(p) for p in a.comps]
    out = pool(dcf, comps_list, json.loads(a.weights), a.seed, a.n)
    write_json(data_dir(a.cik) / "final.json", out)
    emit(out)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd exercises/business_valuation && python -m pytest tests/test_reconcile.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add exercises/business_valuation/tools/reconcile.py exercises/business_valuation/tests/test_reconcile.py
git commit -m "feat(valuation): reconcile lane distributions into final number + range"
```

---

### Task 9: Agent fleet — five single-purpose agent definitions

**Files:**
- Create: `exercises/business_valuation/.claude/agents/edgar-analyst.md`
- Create: `exercises/business_valuation/.claude/agents/dcf-analyst.md`
- Create: `exercises/business_valuation/.claude/agents/comps-analyst.md`
- Create: `exercises/business_valuation/.claude/agents/qualitative-analyst.md`
- Create: `exercises/business_valuation/.claude/agents/reconciliation-analyst.md`

**Interfaces:**
- Consumes: the tool CLIs from Tasks 2–8 (each agent calls them via Bash).
- Produces: structured JSON files under `data/<cik>/` that the skill (Task 10) wires together. Every agent is instructed to surface tool errors verbatim and NEVER invent a number.

- [ ] **Step 1: Create `edgar-analyst.md`**

```markdown
---
name: edgar-analyst
description: Fetches and sanity-checks a company's EDGAR financial facts and 10-K narrative. Use first in the valuation pipeline.
tools: Bash, Read
---

You retrieve and validate the raw data every other lane depends on. You never
compute valuations and never invent numbers.

Steps:
1. Run `python tools/edgar_fetch.py --ticker <TICKER>` (or `--cik <CIK>`). This
   resolves the CIK and caches `companyfacts.json` and `narrative.txt`.
2. Run `python tools/financials.py --cik <CIK> --ticker <TICKER>` to produce
   `data/<CIK>/financials.json`.
3. Sanity-check the normalized financials: revenue > 0, shares > 0, a recent
   `fiscal_year` is present, debt/cash are non-negative. If any tool prints
   `{"error": ...}`, STOP and report the error verbatim — do not proceed.

Return (as your final message) a compact JSON object: the resolved `cik`,
`ticker`, `fiscal_year`, and a one-line data-quality note. Nothing else.
```

- [ ] **Step 2: Create `dcf-analyst.md`**

```markdown
---
name: dcf-analyst
description: Builds Monte-Carlo DCF assumption distributions from normalized financials and runs the DCF lane.
tools: Bash, Read, Write
---

You own the DCF lane. You choose DISTRIBUTIONS for the drivers; the Python tool
does all arithmetic. Never compute a valuation yourself.

Steps:
1. Read `data/<CIK>/financials.json`.
2. Choose plausible distributions for `revenue_growth`, `operating_margin`,
   `wacc`, and `terminal_growth`, justified by the company's recent figures and
   sector. Use `normal` dists with sensible means/sds (e.g. WACC mean 0.08–0.11;
   terminal_growth mean 0.02–0.03 and below WACC). Set `years` (default 5) and
   `tax_rate` (use the financials' `tax_rate`).
3. Write the config to `data/<CIK>/dcf_config.json`.
4. Run: `python tools/montecarlo_dcf.py --financials data/<CIK>/financials.json
   --config data/<CIK>/dcf_config.json --cik <CIK> --seed <SEED>`.
5. Report the resulting median, p10, p90 and a one-sentence rationale for your
   assumptions. If the tool errors, report it verbatim and stop.
```

- [ ] **Step 3: Create `comps-analyst.md`**

```markdown
---
name: comps-analyst
description: Builds comparables from two independent peer sources (LLM-proposed and embedding-similarity) and runs multiples.
tools: Bash, Read
---

You own the comparables lane. Peers come from TWO independent sources so we can
see whether they agree. You never compute multiples by hand.

Steps:
1. LLM peers: propose 4–8 peer tickers from your domain knowledge for the target
   company. Run:
   `python tools/comps.py --cik <CIK> --peers TICK1,TICK2,... --source llm --seed <SEED>`.
2. Embedding peers: run
   `python tools/embeddings.py --cik <CIK> --universe universe.txt --top-k 8`.
   This writes `data/<CIK>/embed_peers.json`. Read that file, take the `ticker`
   field from each entry in its `peers` list (ignore the `cik` and `score`
   fields), and join those tickers comma-separated. Pass that comma-separated
   string to:
   `python tools/comps.py --cik <CIK> --peers TICK1,TICK2,... --source embedding --seed <SEED>`.
3. Report both implied-value ranges (median, p10, p90) per source, the peer
   lists used, and whether the two sources converge or diverge. Surface any tool
   errors verbatim; if one source fails, continue with the other and say so.
```

- [ ] **Step 4: Create `qualitative-analyst.md`**

```markdown
---
name: qualitative-analyst
description: Reads the 10-K narrative (MD&A, risk factors) and emits machine-usable risk adjustments and lane weights.
tools: Read
---

You own the qualitative/risk lane. You read text and translate it into concrete,
numeric guidance for reconciliation. You never produce a valuation. Never invent a
number — every weight and adjustment you emit must derive from the text you actually read.

Steps:
1. Read `data/<CIK>/narrative.txt`.
2. Identify the most material risks and tailwinds (competition, leverage,
   concentration, regulation, secular demand).
3. Emit a JSON object with: `risk_summary` (3–5 bullet strings), suggested
   `assumption_adjustments` (e.g. "widen wacc sd", "haircut terminal_growth"),
   and suggested `lane_weights` — a mapping over `dcf`, `llm`, `embedding` that
   sums to ~1 and reflects which lanes you trust most for THIS company.
   Justify each weight in one short clause.

Return only that JSON object as your final message.
```

- [ ] **Step 5: Create `reconciliation-analyst.md`**

```markdown
---
name: reconciliation-analyst
description: Combines the DCF, comparables, and qualitative lanes into a final number + range, benchmarks vs market, and writes the report.
tools: Bash, Read, Write
---

You synthesize all lanes into one answer. Weighting is yours to decide, informed
by the qualitative lane. The Python tool does the pooling math.

Steps:
1. Read `data/<CIK>/dcf_result.json`, every `data/<CIK>/comps_*.json`, and the
   qualitative analyst's `lane_weights`.
2. Run: `python tools/reconcile.py --dcf data/<CIK>/dcf_result.json
   --comps data/<CIK>/comps_llm.json --comps data/<CIK>/comps_embedding.json
   --weights '{"dcf":W1,"llm":W2,"embedding":W3}' --cik <CIK> --seed <SEED>`.
3. Run `python tools/market_price.py --ticker <TICKER> --cik <CIK>` for the real
   price benchmark. Market price is NEVER fed back into the valuation.
4. Write `reports/<TICKER>-<YYYY-MM-DD>.md` containing: headline median + P10–P90,
   per-lane breakdown, chosen weights with rationale, the qualitative risk
   summary, and the market comparison (price, % over/under-valued, where price
   falls in the P10–P90 band). If a lane is missing, note it and its effect on
   confidence.
5. Return the headline line and the report path.

If any tool (`reconcile.py`, `market_price.py`) exits with an error, report it
verbatim and stop before writing the report; never fill in a number the tools did
not produce.
```

- [ ] **Step 6: Verify the agents reference real tool commands**

Run: `cd exercises/business_valuation && for t in edgar_fetch financials montecarlo_dcf comps embeddings reconcile market_price; do grep -rq "tools/$t.py" .claude/agents/ && echo "ok $t" || echo "MISSING $t"; done`
Expected: every line prints `ok <tool>`.

- [ ] **Step 7: Commit**

```bash
git add exercises/business_valuation/.claude/agents
git commit -m "feat(valuation): five single-purpose valuation agents"
```

---

### Task 10: `/valuation` skill — the orchestrator

**Files:**
- Create: `exercises/business_valuation/.claude/skills/valuation/SKILL.md`

**Interfaces:**
- Consumes: the five agents (Task 9) and all tool CLIs.
- Produces: the end-to-end `/valuation <cik|ticker>` workflow (fan-out → reconcile → headline).

- [ ] **Step 1: Create `SKILL.md`**

```markdown
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
```

- [ ] **Step 2: Verify the skill frontmatter parses and references the agents**

Run: `cd exercises/business_valuation && head -3 .claude/skills/valuation/SKILL.md && grep -c -E "edgar-analyst|dcf-analyst|comps-analyst|qualitative-analyst|reconciliation-analyst" .claude/skills/valuation/SKILL.md`
Expected: frontmatter shows `name: valuation`; grep count ≥ 5.

- [ ] **Step 3: Commit**

```bash
git add exercises/business_valuation/.claude/skills/valuation/SKILL.md
git commit -m "feat(valuation): /valuation orchestrator skill"
```

---

### Task 11: README + offline end-to-end test + final commit

**Files:**
- Create: `exercises/business_valuation/README.md`
- Test: `exercises/business_valuation/tests/test_e2e.py`

**Interfaces:**
- Consumes: `financials.normalize`, `montecarlo_dcf.run_dcf`, `comps.{peer_metrics,implied_values}`, `reconcile.pool` — exercised together, fully offline, against fixtures.

- [ ] **Step 1: Write the failing end-to-end test** — `tests/test_e2e.py`

```python
import json
from pathlib import Path

import comps
import financials
import montecarlo_dcf as mc
import reconcile

FIX = Path(__file__).parent / "fixtures" / "companyfacts_TEST.json"


def test_full_chain_offline_produces_final_range():
    facts = json.loads(FIX.read_text())
    fin = financials.normalize(facts, ticker="TEST")

    cfg = {
        "years": 5,
        "revenue_growth": {"dist": "normal", "mean": 0.05, "sd": 0.02},
        "operating_margin": {"dist": "normal", "mean": 0.27, "sd": 0.03},
        "wacc": {"dist": "normal", "mean": 0.09, "sd": 0.01},
        "terminal_growth": {"dist": "normal", "mean": 0.025, "sd": 0.004},
        "tax_rate": fin["tax_rate"],
    }
    dcf = mc.run_dcf(fin, cfg, seed=7, n=3000)

    peer = dict(fin)  # one synthetic peer derived from the target
    multiples = [comps.peer_metrics(peer, price=12.0)]
    comps_res = comps.implied_values(fin, multiples, seed=7, n=3000)
    comps_res["source"] = "llm"

    final = reconcile.pool(dcf, [comps_res],
                           weights={"dcf": 0.6, "llm": 0.4}, seed=7, n=3000)

    assert final["median"] > 0
    assert final["p10"] <= final["median"] <= final["p90"]
    assert abs(sum(final["weights"].values()) - 1.0) < 1e-9
```

- [ ] **Step 2: Run test to verify it fails (or check it is wired)**

Run: `cd exercises/business_valuation && python -m pytest tests/test_e2e.py -v`
Expected: PASS once all prior tasks are complete (this test only imports already-built modules). If any import fails, the corresponding task is incomplete — fix that task first.

- [ ] **Step 3: Run the FULL offline suite**

Run: `cd exercises/business_valuation && python -m pytest -q`
Expected: all tests pass, zero network calls.

- [ ] **Step 4: Create `README.md`**

```markdown
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
```

- [ ] **Step 5: Commit**

```bash
git add exercises/business_valuation/README.md exercises/business_valuation/tests/test_e2e.py
git commit -m "feat(valuation): README and offline end-to-end test"
```

---

## Self-Review

**Spec coverage check (spec §→task):**
- §2 Architecture / directory → Task 1 (scaffold) + all tasks create their files. ✓
- §2 Agent fleet (5 agents) → Task 9. ✓
- §3 DCF Monte Carlo → Task 4. ✓
- §3 Comparables dual-source (LLM + embedding) → Task 6 (multiples) + Task 7 (embedding peers) + Task 9 comps-analyst (drives both). ✓
- §3 Qualitative lane → Task 9 qualitative-analyst. ✓
- §3 Reconciliation (qual-informed weights) → Task 8 + Task 9 reconciliation-analyst. ✓
- §3 Market benchmark, benchmark-only → Task 5 + reconciliation-analyst step 3; "never an input" stated in Global Constraints, skill rules, and agent. ✓
- §4 Data flow / parallel fan-out → Task 10 skill. ✓
- §5 Tool contracts (7 tools, JSON, non-zero exit) → Tasks 2–8; `die()` enforces error contract. ✓
- §6 Locked decisions (Bash CLI, hybrid EDGAR, cache, MC, dual peers, local embeddings, configurable universe, benchmark-only, single seed) → Global Constraints + respective tasks. ✓
- §7 Error handling / reproducibility → `die()` everywhere; `--seed` threaded; SEC UA in Task 1. ✓
- §8 Testing (offline fixtures, fixed-seed smoke, e2e) → per-task tests + Task 11 e2e; `conftest.py` Task 1. ✓
- §9 README → Task 11. ✓

**Placeholder scan:** No "TBD/TODO/handle edge cases" — every code and test step shows complete content. ✓

**Type/name consistency:** Result dicts use consistent keys across tasks — DCF result `{lane,median,p10,p90,n,samples}`; comps result adds `{source,peers}`; `reconcile.pool` consumes `samples` + (`lane`/`source`) and emits `{median,p10,p90,n,weights}`. `cik_pad`, `data_dir`, `die`, `emit`, `read_json`, `write_json`, `sec_headers` are defined once in Task 1 and referenced identically thereafter. Peer-source labels `llm`/`embedding` match between `comps.py` CLI, `reconcile` weights, agents, and skill. ✓
