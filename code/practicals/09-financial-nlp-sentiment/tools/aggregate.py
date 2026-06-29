"""Aggregate per-headline polarities into a daily sentiment signal (NumPy, offline).

Scores every headline with ``tools.lexicon`` and groups the results by date. The
daily signal is the mean polarity of that date's headlines, labelled against a
symmetric threshold:

    mean >  threshold  -> bullish
    mean < -threshold  -> bearish
    otherwise          -> neutral

CLI:
    python -m tools.aggregate                       # all bundled dates
    python -m tools.aggregate --date 2024-02-13     # one date
"""
from __future__ import annotations

import argparse
import json

import numpy as np

from tools._common import load_headlines
from tools.lexicon import score

DEFAULT_THRESHOLD = 0.15


def score_records(records: list[dict], lex: dict | None = None) -> list[dict]:
    """Score a list of ``{date, id, text}`` rows into ``{date, id, text, polarity, ...}``."""
    scored = []
    for r in records:
        s = score(r["text"], lex)
        scored.append({
            "id": r.get("id"),
            "date": r["date"],
            "text": r["text"],
            "polarity": s["polarity"],
            "positive": s["positive"],
            "negative": s["negative"],
        })
    return scored


def label(mean: float, threshold: float = DEFAULT_THRESHOLD) -> str:
    if mean > threshold:
        return "bullish"
    if mean < -threshold:
        return "bearish"
    return "neutral"


def daily_signal(scored: list[dict], threshold: float = DEFAULT_THRESHOLD) -> dict:
    """Mean polarity, count, label and item ids for each date present in *scored*."""
    out: dict[str, dict] = {}
    for d in sorted({s["date"] for s in scored}):
        day = [s for s in scored if s["date"] == d]
        mean = round(float(np.mean([s["polarity"] for s in day])), 4)
        out[d] = {
            "mean": mean,
            "count": len(day),
            "label": label(mean, threshold),
            "item_ids": [s["id"] for s in day],
        }
    return out


def build_signal(headlines_path=None, lex=None, threshold: float = DEFAULT_THRESHOLD) -> dict:
    """Load the bundled headlines, score them, and return signal + per-headline detail."""
    records = load_headlines(headlines_path) if headlines_path else load_headlines()
    scored = score_records(records, lex)
    return {"by_date": daily_signal(scored, threshold), "headlines": scored}


def _main() -> None:
    ap = argparse.ArgumentParser(description="Aggregate headline polarities into a daily signal.")
    ap.add_argument("--headlines", help="path to a headlines CSV (default: bundled data)")
    ap.add_argument("--date", help="keep only this date, e.g. 2024-02-13")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help="abs(mean) above which a day is bullish/bearish (default 0.15)")
    args = ap.parse_args()

    out = build_signal(args.headlines, threshold=args.threshold)
    if args.date:
        out = {
            "by_date": {k: v for k, v in out["by_date"].items() if k == args.date},
            "headlines": [h for h in out["headlines"] if h["date"] == args.date],
        }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    _main()
