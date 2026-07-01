#!/usr/bin/env python3
"""Retrieve a company's latest 10-K and structured financials from SEC EDGAR.

Given a company name or ticker, this resolves the CIK, downloads the most recent
10-K filing document, and downloads the company's XBRL "company facts" JSON.

Pure standard library only (no pip installs). SEC requires a descriptive
User-Agent on every request; set EDGAR_UA to override the default.

Usage:
    python tools/edgar_fetch.py "Apple" --out output/AAPL/raw
    python tools/edgar_fetch.py AAPL --out output/AAPL/raw
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from difflib import SequenceMatcher

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik10}.json"
COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json"
ARCHIVES_BASE = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc_nodash}/{doc}"

DEFAULT_UA = os.environ.get(
    "EDGAR_UA", "company-analysis/1.0 (jfimbett@gmail.com)"
)


def _get(url: str, *, retries: int = 4, backoff: float = 1.5) -> bytes:
    """HTTP GET with the required User-Agent and simple retry/backoff."""
    last_err: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": DEFAULT_UA,
                "Accept-Encoding": "gzip, deflate",
                "Accept": "application/json, text/html, */*",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                if resp.headers.get("Content-Encoding") == "gzip":
                    import gzip

                    data = gzip.decompress(data)
                elif resp.headers.get("Content-Encoding") == "deflate":
                    import zlib

                    data = zlib.decompress(data)
                return data
        except urllib.error.HTTPError as e:
            last_err = e
            # 403/429 -> back off and retry; 404 -> no point retrying.
            if e.code == 404:
                raise
            time.sleep(backoff ** attempt)
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            time.sleep(backoff ** attempt)
    raise RuntimeError(f"GET failed after {retries} attempts: {url}\n{last_err}")


def _get_json(url: str) -> object:
    return json.loads(_get(url).decode("utf-8"))


def resolve_cik(query: str) -> dict:
    """Resolve a company name or ticker to {cik, ticker, title}.

    Exact ticker match wins; otherwise fuzzy-match against the company title.
    Raises ValueError with candidates when the match is too weak.
    """
    raw = _get_json(TICKERS_URL)
    # company_tickers.json is a dict keyed by index: {"0": {cik_str, ticker, title}, ...}
    rows = list(raw.values()) if isinstance(raw, dict) else raw
    q = query.strip()
    ql = q.lower()

    # 1) exact ticker match
    for row in rows:
        if str(row.get("ticker", "")).lower() == ql:
            return {
                "cik": int(row["cik_str"]),
                "ticker": row["ticker"],
                "title": row["title"],
            }

    # 2) exact title match
    for row in rows:
        if str(row.get("title", "")).lower() == ql:
            return {
                "cik": int(row["cik_str"]),
                "ticker": row["ticker"],
                "title": row["title"],
            }

    # 3) fuzzy match against title
    scored = []
    for row in rows:
        title = str(row.get("title", ""))
        score = SequenceMatcher(None, ql, title.lower()).ratio()
        # boost if query is a substring of the title (or vice versa)
        if ql in title.lower() or title.lower() in ql:
            score = max(score, 0.85)
        scored.append((score, row))
    scored.sort(key=lambda x: x[0], reverse=True)
    best_score, best = scored[0]

    if best_score < 0.7:
        cands = ", ".join(
            f"{r['ticker']} ({r['title']})" for _, r in scored[:5]
        )
        raise ValueError(
            f"Could not confidently resolve '{query}'. Closest: {cands}"
        )

    return {
        "cik": int(best["cik_str"]),
        "ticker": best["ticker"],
        "title": best["title"],
    }


def latest_10k(cik: int) -> dict:
    """Return metadata for the most recent 10-K filing for a CIK."""
    cik10 = f"{cik:010d}"
    sub = _get_json(SUBMISSIONS_URL.format(cik10=cik10))
    recent = sub["filings"]["recent"]
    forms = recent["form"]
    best_idx = None
    for i, form in enumerate(forms):
        if form == "10-K":
            if best_idx is None or recent["filingDate"][i] > recent["filingDate"][best_idx]:
                best_idx = i
    if best_idx is None:
        raise ValueError(f"No 10-K filing found for CIK {cik10}")

    acc = recent["accessionNumber"][best_idx]
    acc_nodash = acc.replace("-", "")
    doc = recent["primaryDocument"][best_idx]
    doc_url = ARCHIVES_BASE.format(cik=cik, acc_nodash=acc_nodash, doc=doc)
    return {
        "accessionNumber": acc,
        "filingDate": recent["filingDate"][best_idx],
        "reportDate": recent.get("reportDate", [None] * len(forms))[best_idx],
        "primaryDocument": doc,
        "primaryDocUrl": doc_url,
        "companyName": sub.get("name"),
    }


def fetch(query: str, out_dir: str) -> dict:
    os.makedirs(out_dir, exist_ok=True)

    ident = resolve_cik(query)
    cik = ident["cik"]
    cik10 = f"{cik:010d}"
    print(f"Resolved '{query}' -> {ident['ticker']} (CIK {cik10}) {ident['title']}")

    filing = latest_10k(cik)
    print(f"Latest 10-K: {filing['filingDate']} (accession {filing['accessionNumber']})")

    # download the 10-K primary document
    tenk_bytes = _get(filing["primaryDocUrl"])
    tenk_path = os.path.join(out_dir, filing["primaryDocument"])
    with open(tenk_path, "wb") as f:
        f.write(tenk_bytes)
    print(f"Saved 10-K document -> {tenk_path} ({len(tenk_bytes):,} bytes)")

    # download companyfacts XBRL
    facts_path = os.path.join(out_dir, "companyfacts.json")
    try:
        facts = _get(COMPANYFACTS_URL.format(cik10=cik10))
        with open(facts_path, "wb") as f:
            f.write(facts)
        print(f"Saved company facts -> {facts_path} ({len(facts):,} bytes)")
        facts_ok = True
    except Exception as e:  # noqa: BLE001
        print(f"WARNING: could not fetch companyfacts: {e}", file=sys.stderr)
        facts_ok = False

    meta = {
        "query": query,
        "ticker": ident["ticker"],
        "cik": cik10,
        "title": ident["title"],
        "companyName": filing["companyName"],
        "filingDate": filing["filingDate"],
        "reportDate": filing["reportDate"],
        "accessionNumber": filing["accessionNumber"],
        "primaryDocument": filing["primaryDocument"],
        "tenkPath": tenk_path,
        "companyFactsPath": facts_path if facts_ok else None,
        "sources": {
            "tickers": TICKERS_URL,
            "submissions": SUBMISSIONS_URL.format(cik10=cik10),
            "companyfacts": COMPANYFACTS_URL.format(cik10=cik10),
            "tenk": filing["primaryDocUrl"],
        },
    }
    meta_path = os.path.join(out_dir, "meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"Saved metadata -> {meta_path}")
    return meta


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Fetch latest 10-K + XBRL from SEC EDGAR.")
    p.add_argument("company", help="Company name or ticker (e.g. 'Apple' or AAPL)")
    p.add_argument(
        "--out",
        required=True,
        help="Output directory for the raw filing + facts (e.g. output/AAPL/raw)",
    )
    args = p.parse_args(argv)
    try:
        fetch(args.company, args.out)
    except (ValueError, RuntimeError, urllib.error.HTTPError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
