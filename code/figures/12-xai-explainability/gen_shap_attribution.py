#!/usr/bin/env python3
"""Deterministic generator for the ch12 SHAP attribution figure (fig:ch12-shap).

Renders the token-level SHAP values from Example "SHAP Attribution for a Credit
Decision" (ex:shap-credit) as a horizontal bar chart. The values are the fixed,
documented attributions stated in the chapter text — this figure depends on NO
external data or model and is fully deterministic.

Run:  python3 gen_shap_attribution.py
Output: ../../book/chapters/12-xai-explainability/figures/fig_shap_attribution.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt

# Fixed values from ex:shap-credit (chapter.tex). Baseline P(creditworthy)=0.50,
# model output 0.14; tokens push the prediction down by 0.36 in total.
TOKENS = [
    ("struggled", -0.089),
    ("declining", -0.073),
    ("down 30%", -0.061),
    ("competitive", -0.047),
    ("restaurant", -0.038),
    ("pandemic", -0.029),
    ("operates", +0.012),
]

OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/12-xai-explainability/figures/fig_shap_attribution.pdf")


def main():
    # Sort most-negative at the bottom for a waterfall-like read.
    items = sorted(TOKENS, key=lambda t: t[1])
    labels = [t[0] for t in items]
    values = [t[1] for t in items]
    colors = ["#d62728" if v < 0 else "#2ca02c" for v in values]

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.barh(range(len(values)), values, color=colors, edgecolor="black", linewidth=0.4)
    ax.set_yticks(range(len(values)))
    ax.set_yticklabels(labels)
    ax.axvline(0.0, color="black", linewidth=0.8)
    ax.set_xlabel("SHAP value (contribution to $P(\\mathrm{creditworthy})$)")
    ax.set_title("Token attributions for a credit-decision classifier\n"
                 "(baseline 0.50 $\\rightarrow$ model output 0.14)")
    for i, v in enumerate(values):
        ax.text(v + (0.002 if v >= 0 else -0.002), i, f"{v:+.3f}",
                va="center", ha="left" if v >= 0 else "right", fontsize=8)
    ax.margins(x=0.18)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    print(f"wrote {OUT} (sum of shown tokens = {sum(values):+.3f})")


if __name__ == "__main__":
    main()
