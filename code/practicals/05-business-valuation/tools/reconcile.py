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
