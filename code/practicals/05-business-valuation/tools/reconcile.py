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
    median = float(np.median(pooled))
    p10 = float(np.percentile(pooled, 10))
    p90 = float(np.percentile(pooled, 90))

    # Governance gate: a P90/P10 spread wider than 2x, or a negative downside,
    # means the valuation is too fragile to publish without human review.
    ratio = float(p90 / p10) if p10 > 0 else None
    if p10 <= 0:
        review_required, reason = True, "downside (P10) is non-positive"
    elif ratio > 2.0:
        review_required, reason = True, f"P90/P10 spread {ratio:.1f}x exceeds 2x"
    else:
        review_required, reason = False, f"P90/P10 spread {ratio:.1f}x within 2x"

    return {
        "median": median,
        "p10": p10,
        "p90": p90,
        "n": int(pooled.size),
        "weights": {name: float(wi) for (name, _), wi in zip(lanes, w)},
        "p90_p10_ratio": ratio,
        "review_required": review_required,
        "review_reason": reason,
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
