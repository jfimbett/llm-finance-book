"""Turn the bundled text views into an expected-returns vector (mu).

The agent does not invent numbers from prose; this tool does. It starts from the
equilibrium expected returns in ``data/market.json`` and tilts each asset by a fixed
step for every sentiment keyword found in a view that names that asset:

    bullish / overweight / positive / constructive / upside / strong / buy   -> +TILT
    bearish / underweight / negative / downside / weak / sell / trim         -> -TILT
    neutral / hold                                                           ->  0

So a note that calls an asset "bullish ... strong upside ... overweight" lifts its
expected return by 3 x TILT; a "neutral" note leaves it at the equilibrium value.
The mapping is deliberately simple and deterministic — same views in, same vector out.

CLI:
    python -m tools.views            # print the tilted mu vector and the per-view tilts
"""
from __future__ import annotations

import argparse
import json
import re

import numpy as np

from tools._common import load_market, load_views

TILT = 0.02  # expected-return step applied per sentiment keyword

POSITIVE = {"bullish", "overweight", "positive", "constructive", "upside", "strong", "buy"}
NEGATIVE = {"bearish", "underweight", "negative", "downside", "weak", "sell", "trim"}


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def _tilt_for_view(text: str) -> float:
    words = _words(text)
    pos = sum(1 for w in words if w in POSITIVE)
    neg = sum(1 for w in words if w in NEGATIVE)
    return TILT * (pos - neg)


def _asset_in_view(assets: list[str], text: str) -> str | None:
    """Return the first bundled asset whose name appears in the view text, else None."""
    lowered = text.lower()
    for a in assets:
        if re.search(rf"\b{re.escape(a.lower())}\b", lowered):
            return a
    return None


def build_views(market: dict | None = None, views: dict[str, str] | None = None):
    """Return ``(mu, breakdown)``: the tilted expected-returns vector and per-view detail.

    ``mu`` starts at ``market['expected_returns']`` and each view shifts the asset it
    names by ``_tilt_for_view``. Assets with no view keep their equilibrium return.
    """
    market = market or load_market()
    views = load_views() if views is None else views
    assets = market["assets"]
    base = market["expected_returns"].astype(float)
    mu = base.copy()
    breakdown = []
    for name, text in views.items():
        asset = _asset_in_view(assets, text)
        if asset is None:
            continue
        tilt = _tilt_for_view(text)
        j = assets.index(asset)
        mu[j] += tilt
        breakdown.append({"view": name, "asset": asset, "tilt": round(tilt, 4)})
    return mu, breakdown


def _main() -> None:
    ap = argparse.ArgumentParser(description="Build the expected-returns vector from the text views.")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args()
    market = load_market()
    mu, breakdown = build_views(market)
    payload = {
        "assets": market["assets"],
        "base_expected_returns": [round(float(x), 4) for x in market["expected_returns"]],
        "view_expected_returns": [round(float(x), 4) for x in mu],
        "tilts": breakdown,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print("View-adjusted expected returns (annual):")
    for a, b, m in zip(payload["assets"], payload["base_expected_returns"], payload["view_expected_returns"]):
        print(f"  {a:<9} base {b:+.4f}  ->  view {m:+.4f}")
    if breakdown:
        print("Applied tilts:")
        for row in breakdown:
            print(f"  {row['asset']:<9} {row['tilt']:+.4f}  ({row['view']})")


if __name__ == "__main__":
    _main()
