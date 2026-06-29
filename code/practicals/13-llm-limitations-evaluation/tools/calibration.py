"""Calibration analysis: Expected Calibration Error, reliability bins, confident-wrong cases.

A model can be accurate *and* badly calibrated: if it says "95% sure" on answers it
gets wrong half the time, its confidence is a lie even when the accuracy looks fine.
This tool measures that gap.

* reliability_bins — group predictions by stated confidence; for each bin report the
  mean confidence and the actual accuracy. A well-calibrated model has accuracy ~= confidence.
* expected_calibration_error (ECE) — the N-weighted average gap |accuracy - confidence|
  across bins. Lower is better; 0 means confidence matches reality everywhere.
* confident_wrong — the items the model got wrong while claiming high confidence. These
  are the dangerous failures: the model is not just wrong, it is sure.

Numbers only; numpy + standard library. Feed it the JSON that ``tools.score`` produced,
or point it straight at a gold/prediction pair.

CLI:
    python -m tools.score --pred data/candidates_overconfident.json --out reports/_scored.json
    python -m tools.calibration --scored reports/_scored.json
    python -m tools.calibration --pred data/candidates_overconfident.json   # scores internally
"""
from __future__ import annotations

import argparse
import json

import numpy as np


def _arrays(items: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    """Confidence and correctness arrays for items that actually stated a confidence."""
    conf, correct = [], []
    for it in items:
        c = it.get("confidence")
        if c is None:
            continue
        conf.append(float(c))
        correct.append(1.0 if it.get("correct") else 0.0)
    return np.asarray(conf, dtype=float), np.asarray(correct, dtype=float)


def reliability_bins(items: list[dict], n_bins: int = 10) -> list[dict]:
    """Equal-width confidence bins over [0, 1] with per-bin accuracy and mean confidence."""
    conf, correct = _arrays(items)
    bins = []
    for b in range(n_bins):
        lo, hi = b / n_bins, (b + 1) / n_bins
        # last bin is closed on the right so confidence == 1.0 lands somewhere
        if b == n_bins - 1:
            mask = (conf >= lo) & (conf <= hi)
        else:
            mask = (conf >= lo) & (conf < hi)
        count = int(mask.sum())
        bins.append({
            "lo": round(lo, 3),
            "hi": round(hi, 3),
            "count": count,
            "confidence": round(float(conf[mask].mean()), 4) if count else None,
            "accuracy": round(float(correct[mask].mean()), 4) if count else None,
            "gap": round(abs(float(conf[mask].mean() - correct[mask].mean())), 4) if count else None,
        })
    return bins


def expected_calibration_error(items: list[dict], n_bins: int = 10) -> float:
    """ECE = sum_b (n_b / N) * |accuracy_b - confidence_b|."""
    conf, correct = _arrays(items)
    n = conf.size
    if n == 0:
        return 0.0
    ece = 0.0
    for b in range(n_bins):
        lo, hi = b / n_bins, (b + 1) / n_bins
        mask = (conf >= lo) & (conf <= hi) if b == n_bins - 1 else (conf >= lo) & (conf < hi)
        count = int(mask.sum())
        if count == 0:
            continue
        ece += (count / n) * abs(conf[mask].mean() - correct[mask].mean())
    return float(ece)


def confident_wrong(items: list[dict], threshold: float = 0.8) -> list[dict]:
    """Items the model got wrong while stating confidence >= threshold (sorted, most sure first)."""
    flagged = [
        {
            "id": it["id"],
            "question": it.get("question"),
            "gold": it.get("gold"),
            "candidate": it.get("candidate"),
            "confidence": it.get("confidence"),
        }
        for it in items
        if it.get("confidence") is not None
        and float(it["confidence"]) >= threshold
        and not it.get("correct")
    ]
    flagged.sort(key=lambda it: it["confidence"], reverse=True)
    return flagged


def analyze(items: list[dict], n_bins: int = 10, threshold: float = 0.8) -> dict:
    conf, correct = _arrays(items)
    return {
        "n": int(conf.size),
        "accuracy": round(float(correct.mean()), 4) if conf.size else 0.0,
        "mean_confidence": round(float(conf.mean()), 4) if conf.size else 0.0,
        "ece": round(expected_calibration_error(items, n_bins), 4),
        "n_bins": n_bins,
        "confident_wrong_threshold": threshold,
        "confident_wrong": confident_wrong(items, threshold),
        "bins": reliability_bins(items, n_bins),
    }


def _load_items(args) -> list[dict]:
    if args.scored:
        return json.loads(open(args.scored, encoding="utf-8").read())["items"]
    # score internally from a gold/prediction pair
    from tools.score import score_dataset
    from tools._common import load_gold, load_predictions
    return score_dataset(load_gold(args.gold), load_predictions(args.pred))["items"]


def _main() -> None:
    ap = argparse.ArgumentParser(description="Calibration analysis of a scored eval run.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--scored", help="path to the JSON emitted by `tools.score` (has an 'items' list)")
    src.add_argument("--pred", help="path to a candidate predictions file (scored internally)")
    ap.add_argument("--gold", default=None, help="gold.json, when using --pred (default: data/gold.json)")
    ap.add_argument("--bins", type=int, default=10)
    ap.add_argument("--confident-threshold", type=float, default=0.8)
    args = ap.parse_args()
    items = _load_items(args)
    print(json.dumps(analyze(items, args.bins, args.confident_threshold), indent=2))


if __name__ == "__main__":
    _main()
