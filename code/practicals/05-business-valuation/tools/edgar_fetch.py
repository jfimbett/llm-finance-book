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
