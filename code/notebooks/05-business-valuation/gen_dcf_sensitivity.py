#!/usr/bin/env python3
"""Deterministic generator for the ch05 DCF sensitivity heatmap (fig:ch05-illustration).

The figure is a Gordon-Growth terminal-value sensitivity grid,
    EV = FCF * (1 + g) / (WACC - g),
evaluated over a WACC x g grid for a *fixed, documented* base free cash flow.
It depends on NO live data: the base FCF is Apple Inc.'s FY2024 free cash flow of
USD 108.8B, sourced from the company's FY2024 10-K (operating cash flow minus capex),
the same figure used by the companion exercise in exercises/valuation_example/.
This makes the figure fully reproducible and deterministic.

Run:  python3 gen_dcf_sensitivity.py
Output: ../../book/chapters/05-business-valuation/figures/fig_illustration.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt
import numpy as np

# --- Fixed, documented inputs (no network) ---
FCF_BASE_USD_B = 108.8          # AAPL FY2024 free cash flow, USD billions (10-K: OCF - capex)
WACC_GRID = np.round(np.arange(0.06, 0.1401, 0.01), 4)   # 6% .. 14%
G_GRID = np.round(np.arange(0.01, 0.0401, 0.005), 4)     # 1% .. 4%

OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/05-business-valuation/figures/fig_illustration.pdf")


def enterprise_value(fcf_b, wacc, g):
    """Gordon-Growth terminal value in USD billions; NaN where g >= WACC."""
    if g >= wacc:
        return np.nan
    return fcf_b * (1.0 + g) / (wacc - g)


def main():
    ev = np.array([[enterprise_value(FCF_BASE_USD_B, w, g) for g in G_GRID]
                   for w in WACC_GRID])

    fig, ax = plt.subplots(figsize=(8.0, 5.2))
    im = ax.imshow(ev, cmap="RdYlGn", aspect="auto", origin="lower")

    ax.set_xticks(range(len(G_GRID)))
    ax.set_xticklabels([f"{g*100:.1f}%" for g in G_GRID])
    ax.set_yticks(range(len(WACC_GRID)))
    ax.set_yticklabels([f"{w*100:.0f}%" for w in WACC_GRID])
    ax.set_xlabel("Terminal growth rate $g$")
    ax.set_ylabel("WACC")
    ax.set_title(f"AAPL DCF terminal-value sensitivity "
                 f"(base FCF = \\${FCF_BASE_USD_B:.1f}B, FY2024)")

    for i in range(len(WACC_GRID)):
        for j in range(len(G_GRID)):
            v = ev[i, j]
            if np.isfinite(v):
                ax.text(j, i, f"{v:,.0f}", ha="center", va="center",
                        fontsize=7, color="black")

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Implied enterprise value (\\$B)")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT} ({ev[np.isfinite(ev)].min():,.0f}--{ev[np.isfinite(ev)].max():,.0f} $B range)")


if __name__ == "__main__":
    main()
