import argparse

import numpy as np

from _common import data_dir, die, emit, read_json, write_json
from montecarlo_dcf import project_per_share


def central(spec):
    """The point value of a driver distribution — the axis anchor for the grid."""
    d = spec.get("dist", "normal")
    if d == "fixed":
        return float(spec["value"])
    if d == "normal":
        return float(spec["mean"])
    if d == "lognormal":
        return float(np.exp(spec["mean"]))
    if d == "uniform":
        return 0.5 * (float(spec["low"]) + float(spec["high"]))
    die(f"unknown distribution: {d}")


def _axis(center, half_width, steps, floor=None):
    lo = center - half_width
    if floor is not None:
        lo = max(floor, lo)
    return [round(float(v), 4) for v in np.linspace(lo, center + half_width, steps)]


def grid(fin, cfg, wacc_axis=None, tg_axis=None, wacc_steps=7, tg_steps=5):
    """EV/share over a WACC x terminal-growth mesh, holding the other drivers at
    their central values. Cells where g >= WACC (Gordon model undefined) are
    left as None so the heatmap shows the blow-up region explicitly."""
    tax = float(cfg.get("tax_rate", fin.get("tax_rate", 0.21)))
    years = int(cfg.get("years", 5))
    g0 = central(cfg["revenue_growth"])
    margin0 = central(cfg["operating_margin"])
    wacc0 = central(cfg["wacc"])
    tg0 = central(cfg["terminal_growth"])

    if wacc_axis is None:
        wacc_axis = _axis(wacc0, 0.03, wacc_steps, floor=0.01)
    if tg_axis is None:
        tg_axis = _axis(tg0, 0.02, tg_steps, floor=0.0)

    rows = []
    for w in wacc_axis:
        row = []
        for tg in tg_axis:
            if tg >= w - 0.005:  # matches the DCF lane's own terminal-value guard
                row.append(None)
                continue
            v = float(project_per_share(fin, g0, margin0, w, tg, tax, years))
            row.append(v if np.isfinite(v) else None)
        rows.append(row)

    base = float(project_per_share(fin, g0, margin0, wacc0, tg0, tax, years))
    return {
        "lane": "dcf",
        "wacc_axis": wacc_axis,
        "tg_axis": tg_axis,
        "grid": rows,
        "base": {
            "wacc": round(wacc0, 4),
            "terminal_growth": round(tg0, 4),
            "revenue_growth": round(g0, 4),
            "operating_margin": round(margin0, 4),
            "per_share": base if np.isfinite(base) else None,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--financials", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--cik", required=True)
    ap.add_argument("--wacc-steps", type=int, default=7)
    ap.add_argument("--tg-steps", type=int, default=5)
    a = ap.parse_args()
    out = grid(read_json(a.financials), read_json(a.config),
               wacc_steps=a.wacc_steps, tg_steps=a.tg_steps)
    write_json(data_dir(a.cik) / "sensitivity.json", out)
    emit(out)


if __name__ == "__main__":
    main()
