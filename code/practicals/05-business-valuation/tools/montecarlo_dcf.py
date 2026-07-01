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


def project_per_share(fin, g, margin, wacc, tg, tax, years):
    """Per-share equity value for one or many DCF paths. Inputs broadcast, so
    this drives both the Monte-Carlo lane (drawn arrays) and the sensitivity
    grid (scalar sweeps) from one source of truth."""
    g, margin, wacc, tg = np.broadcast_arrays(
        np.asarray(g, dtype=float), np.asarray(margin, dtype=float),
        np.asarray(wacc, dtype=float), np.asarray(tg, dtype=float))

    rev0 = float(fin["revenue"])
    da_pct = float(fin["da"]) / rev0
    capex_pct = float(fin["capex"]) / rev0
    nwc_pct = float(fin.get("delta_nwc", 0.0)) / rev0

    # guard: terminal model requires wacc strictly above terminal growth
    wacc = np.where(wacc > tg + 0.005, wacc, tg + 0.01)
    fcff_margin = margin * (1.0 - tax) + da_pct - capex_pct - nwc_pct

    ev = np.zeros(g.shape)
    rev = np.full(g.shape, rev0)
    for y in range(1, int(years) + 1):
        rev = rev * (1.0 + g)
        ev = ev + rev * fcff_margin / (1.0 + wacc) ** y
    fcff_final = rev * fcff_margin
    tv = fcff_final * (1.0 + tg) / (wacc - tg)
    ev = ev + tv / (1.0 + wacc) ** int(years)

    equity = ev - float(fin.get("total_debt", 0.0)) + float(fin.get("cash", 0.0))
    return equity / float(fin["shares"])


def run_dcf(fin, cfg, seed=0, n=10000):
    rng = np.random.default_rng(seed)
    years = int(cfg.get("years", 5))
    g = _draw(rng, cfg["revenue_growth"], n)
    margin = _draw(rng, cfg["operating_margin"], n)
    wacc = _draw(rng, cfg["wacc"], n)
    tg = _draw(rng, cfg["terminal_growth"], n)
    tax = float(cfg.get("tax_rate", fin.get("tax_rate", 0.21)))

    per_share = project_per_share(fin, g, margin, wacc, tg, tax, years)
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
