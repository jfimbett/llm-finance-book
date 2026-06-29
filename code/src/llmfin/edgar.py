"""A tiny, rate-limited SEC EDGAR REST client used by the student practicals.

No API key is required — the SEC only asks for a descriptive ``User-Agent``.
Set ``EDGAR_USER_AGENT`` in your environment (``"Name your-email@example.com"``)
before fetching; the default below is a placeholder you should replace.

All calls sleep ~110 ms to stay under the SEC's 10 requests/second limit.
"""
from __future__ import annotations

import os
import re
import time

import requests

EDGAR_USER_AGENT = os.environ.get(
    "EDGAR_USER_AGENT", "LLM-Finance-Course your-email@example.com"
)
_HEADERS = {"User-Agent": EDGAR_USER_AGENT}
_RATE_DELAY = 0.11  # seconds between requests (<= 10 req/s)


def _get_json(url: str) -> dict:
    time.sleep(_RATE_DELAY)
    r = requests.get(url, headers=_HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()


def _get_text(url: str, timeout: int = 30) -> str:
    time.sleep(_RATE_DELAY)
    r = requests.get(url, headers=_HEADERS, timeout=timeout)
    r.raise_for_status()
    return r.text


def get_cik(ticker: str) -> str:
    """Zero-padded 10-digit CIK for a ticker symbol."""
    data = _get_json("https://www.sec.gov/files/company_tickers.json")
    for v in data.values():
        if v["ticker"].upper() == ticker.upper():
            return str(v["cik_str"]).zfill(10)
    raise ValueError(f"Ticker {ticker!r} not found in EDGAR ticker map")


def get_submissions(cik: str) -> dict:
    """Full submission history JSON for a CIK."""
    return _get_json(f"https://data.sec.gov/submissions/CIK{cik}.json")


def get_concept(cik: str, concept: str, taxonomy: str = "us-gaap") -> dict:
    """XBRL company-concept JSON (e.g. concept='Revenues')."""
    return _get_json(
        f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/{taxonomy}/{concept}.json"
    )


def latest_10k(submissions: dict) -> tuple[int, dict]:
    """Return ``(index, recent_filings_dict)`` for the most recent 10-K."""
    f = submissions["filings"]["recent"]
    idx = next(i for i, form in enumerate(f["form"]) if form == "10-K")
    return idx, f


def fetch_10k_html(ticker: str) -> str:
    """Download the primary HTML document of *ticker*'s most recent 10-K."""
    cik = get_cik(ticker)
    idx, f = latest_10k(get_submissions(cik))
    accession = f["accessionNumber"][idx].replace("-", "")
    url = (
        f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}"
        f"/{accession}/{f['primaryDocument'][idx]}"
    )
    return _get_text(url)


_MDA_RE = re.compile(
    r"Item\s+7[.\s]+Management.{0,80}Discussion.*?(?=Item\s+7A|Item\s+8)",
    re.IGNORECASE | re.DOTALL,
)


def extract_mda(html: str) -> str:
    """Strip HTML tags and return the Management's Discussion & Analysis text.

    Falls back to the first 30k characters if the Item 7 anchor isn't found.
    """
    text = re.sub(r"<[^>]+>", " ", html)
    m = _MDA_RE.search(text)
    raw = m.group(0) if m else text[:30000]
    return re.sub(r"\s+", " ", raw).strip()
