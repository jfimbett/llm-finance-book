#!/usr/bin/env python3
"""Deterministic generator for the ch02 sinusoidal positional-encoding figure
(fig:ch02-illustration). Pure math, no network or data dependence.

PE[pos, 2i]   = sin(pos / 10000**(2i/d_model))
PE[pos, 2i+1] = cos(pos / 10000**(2i/d_model))

Run:  python3 gen_positional_encoding.py
Output: ../../book/chapters/02-llm-foundations/figures/fig_illustration.pdf
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless, deterministic
import matplotlib.pyplot as plt
import numpy as np

D_MODEL = 64
SEQ_LEN = 50

OUT = (Path(__file__).resolve().parents[3]
       / "book/chapters/02-llm-foundations/figures/fig_illustration.pdf")


def positional_encoding(seq_len, d_model):
    pos = np.arange(seq_len)[:, None]
    i = np.arange(d_model)[None, :]
    angle_rates = 1.0 / np.power(10000.0, (2 * (i // 2)) / d_model)
    angles = pos * angle_rates
    pe = np.zeros((seq_len, d_model))
    pe[:, 0::2] = np.sin(angles[:, 0::2])
    pe[:, 1::2] = np.cos(angles[:, 1::2])
    return pe


def cos_sim(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def main():
    pe = positional_encoding(SEQ_LEN, D_MODEL)

    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    im = ax.imshow(pe, cmap="RdBu", aspect="auto", origin="lower")
    ax.set_xlabel("Encoding dimension")
    ax.set_ylabel("Token position")
    ax.set_title(f"Sinusoidal positional encoding "
                 f"($d_{{\\mathrm{{model}}}}={D_MODEL}$, sequence length {SEQ_LEN})")
    fig.colorbar(im, ax=ax, label="value")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")

    # Worked numbers used in the chapter illustration: cosine similarity decays
    # with positional separation.
    s_5_10 = cos_sim(pe[5], pe[10])
    s_5_45 = cos_sim(pe[5], pe[45])
    print(f"wrote {OUT}")
    print(f"cos-sim(PE_5, PE_10) = {s_5_10:.3f}")
    print(f"cos-sim(PE_5, PE_45) = {s_5_45:.3f}")


if __name__ == "__main__":
    main()
