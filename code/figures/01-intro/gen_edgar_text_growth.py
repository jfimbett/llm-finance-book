#!/usr/bin/env python3
"""
Generate fig_edgar_text_growth.pdf for ch01 of LLM Finance book.

Measures mean alphabetic-character count per 10-K filing by year (1993-2023)
using the SEC EDGAR full-text index.  Results cached to avoid re-downloading.
"""

import json
import os
import random
import re
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import requests

print("Script started", flush=True)

# ── Config ────────────────────────────────────────────────────────────────────
YEARS       = list(range(1993, 2024))
N_SAMPLE    = 25
CHUNK_BYTES = 2_000_000  # first 2 MB — enough to get past HTML headers into body text
DELAY       = 0.12

SCRIPT_DIR  = Path(__file__).resolve().parent
REPO_ROOT   = SCRIPT_DIR.parents[2]          # .../book-course-template
FIGURES_DIR = REPO_ROOT / "book" / "chapters" / "01-intro" / "figures"
CACHE_FILE  = SCRIPT_DIR / "edgar_text_stats_cache.json"
OUT_PDF     = FIGURES_DIR / "fig_edgar_text_growth.pdf"
OUT_PNG     = FIGURES_DIR / "fig_edgar_text_growth.png"

print(f"Figures dir: {FIGURES_DIR}", flush=True)
print(f"Cache file:  {CACHE_FILE}", flush=True)

# SEC EDGAR requires a User-Agent with contact info. Set EDGAR_USER_AGENT in your
# environment; the default is a placeholder you must replace before fetching.
HEADERS      = {"User-Agent": os.environ.get("EDGAR_USER_AGENT", "Finance Research your-email@example.com")}
BASE         = "https://www.sec.gov/Archives/"
TARGET_FORMS = {"10-K", "10-K405"}

# Regexes for robust index parsing
_FORM_RE = re.compile(r'\b(10-K405|10-K)\b')
_FILE_RE = re.compile(r'edgar/\S+\.txt')


# ── EDGAR helpers ─────────────────────────────────────────────────────────────

def edgar_get(url: str, max_bytes: int | None = None) -> str:
    time.sleep(DELAY)
    try:
        r = requests.get(url, headers=HEADERS, timeout=30,
                         stream=(max_bytes is not None))
        r.raise_for_status()
        if max_bytes:
            chunks, total = [], 0
            for chunk in r.iter_content(chunk_size=16_384):
                chunks.append(chunk)
                total += len(chunk)
                if total >= max_bytes:
                    break
            return b"".join(chunks).decode("utf-8", errors="ignore")
        return r.text
    except Exception as exc:
        print(f"    [WARN] {url[:80]} — {exc}", flush=True)
        return ""


def parse_idx(text: str) -> list[dict]:
    """Extract 10-K filing records from EDGAR company.idx using regex."""
    rows = []
    for line in text.splitlines():
        mf = _FORM_RE.search(line)
        mp = _FILE_RE.search(line)
        if mf and mp:
            rows.append({"form": mf.group(1), "filename": mp.group(0).rstrip()})
    return rows


def get_10k_index(year: int) -> list[dict]:
    rows = []
    for q in (1, 2):
        url = f"https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{q}/company.idx"
        print(f"  index {year}/Q{q} ... ", end="", flush=True)
        text = edgar_get(url)
        new  = parse_idx(text)
        rows.extend(new)
        print(f"{len(new)} 10-K entries", flush=True)
        if len(rows) >= N_SAMPLE * 4:
            break
    return rows


# ── Text measurement ──────────────────────────────────────────────────────────

_TAG_RE    = re.compile(r"<[^>]{0,1000}>", re.DOTALL | re.IGNORECASE)
_ENTITY_RE = re.compile(r"&[a-zA-Z0-9#]{1,10};")

def alpha_char_count(raw: str) -> int:
    text = _TAG_RE.sub(" ", raw)
    text = _ENTITY_RE.sub(" ", text)
    return sum(1 for c in text if c.isalpha())


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    random.seed(42)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    cache: dict[str, list[int]] = {}
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            cache = json.load(f)
        print(f"Cache loaded: {len(cache)} years already done", flush=True)

    yearly_stats: list[dict] = []

    for year in YEARS:
        key = str(year)
        if key in cache and len(cache[key]) >= 8:
            counts = cache[key]
            print(f"{year}: [cached] n={len(counts)} mean={np.mean(counts)/1e3:.0f}k alpha", flush=True)
            yearly_stats.append({"year": year, "counts": counts})
            continue

        print(f"\n{year}:", flush=True)
        filings = get_10k_index(year)

        if not filings:
            print(f"  no filings found, skipping {year}", flush=True)
            continue

        sample = random.sample(filings, min(N_SAMPLE, len(filings)))
        counts: list[int] = []

        for i, f in enumerate(sample):
            url = BASE + f["filename"]   # filename already starts with "edgar/"
            raw = edgar_get(url, max_bytes=CHUNK_BYTES)
            n   = alpha_char_count(raw)
            if n > 500:
                counts.append(n)
            if i < 2:
                print(f"    [{i}] alpha={n:,}  url=.../{f['filename'][-50:]}", flush=True)
            if (i + 1) % 10 == 0:
                print(f"  {i+1}/{len(sample)} done, valid={len(counts)}", flush=True)

        if counts:
            print(f"  -> n={len(counts)}, mean={np.mean(counts)/1e3:.0f}k alpha chars", flush=True)
            cache[key] = counts
            with open(CACHE_FILE, "w") as fp:
                json.dump(cache, fp)
            yearly_stats.append({"year": year, "counts": counts})
        else:
            print(f"  -> no valid downloads for {year}", flush=True)

    if not yearly_stats:
        print("ERROR: no data collected", flush=True)
        sys.exit(1)

    # ── Build summary DataFrame ───────────────────────────────────────────────
    rows = [{"year": r["year"], "alpha": c}
            for r in yearly_stats for c in r["counts"]]
    df  = pd.DataFrame(rows)
    print(f"\nTotal observations: {len(df)}, years: {df['year'].nunique()}", flush=True)

    agg = (df.groupby("year")["alpha"]
             .agg(mean="mean", std="std", n="count")
             .reset_index())
    agg["se"] = agg["std"] / np.sqrt(agg["n"])

    # ── Plot ──────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(7.2, 3.8))

    ax.fill_between(
        agg["year"],
        (agg["mean"] - agg["se"]) / 1e3,
        (agg["mean"] + agg["se"]) / 1e3,
        alpha=0.20, color="#2166ac", zorder=2
    )
    ax.plot(agg["year"], agg["mean"] / 1e3,
            color="#2166ac", lw=2.2, marker="o", ms=4.5,
            label="Mean (±1 SE shaded)", zorder=3)

    ax.axvline(2002, color="#b2182b", lw=1.2, ls="--", alpha=0.75,
               label="Sarbanes-Oxley (2002)")
    ax.axvline(2005, color="#d6604d", lw=1.2, ls=":", alpha=0.75,
               label="SEC Rel. 33-8591 (2005)")

    ax.set_xlabel("Year of 10-K filing", fontsize=11)
    ax.set_ylabel("Mean alphabetic characters\nper 10-K (thousands)", fontsize=10)
    ax.set_title("Growth of Narrative Text in SEC 10-K Annual Filings, 1993–2023",
                 fontsize=11, pad=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}k"))
    ax.set_xlim(1992.3, 2023.7)
    ax.legend(framealpha=0.9, fontsize=9, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", ls="--", alpha=0.3, zorder=1)

    plt.tight_layout(pad=0.6)
    plt.savefig(OUT_PDF, bbox_inches="tight")
    plt.savefig(OUT_PNG, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nSaved:\n  {OUT_PDF}\n  {OUT_PNG}", flush=True)


if __name__ == "__main__":
    main()
