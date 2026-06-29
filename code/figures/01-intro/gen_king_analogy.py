#!/usr/bin/env python3
"""Word-analogy figure for ch01 — and a sandbox for playing with word vectors.

====================================================================
WHAT IS THIS SCRIPT ABOUT?  (read this first)
====================================================================
A *word embedding* turns every word into a vector — a long list of
numbers (here, 300 of them). Words that are used in similar contexts
end up with similar vectors. The surprising part is that *directions*
in this space carry meaning, so you can do arithmetic with words:

        king  -  man  +  woman   ≈   queen

Read it as: "take 'king', remove the 'man' direction, add the 'woman'
direction, and you land almost exactly on 'queen'." The model learned
this purely from reading text — nobody told it about royalty or gender.

This script:
  1. loads REAL pre-trained GloVe vectors (300 numbers per word,
     trained on Wikipedia + Gigaword news);
  2. computes the analogy arithmetic you ask for;
  3. asks the model for the nearest real words to the result;
  4. squashes the 300-d vectors down to 2-d with PCA *only so we can
     draw them* (see the caveat below) and saves a labelled figure.

The default run reproduces the exact figure printed in the book
(king - man + woman ≈ queen). You are encouraged to change the words!

--------------------------------------------------------------------
CAVEAT about the picture: the math happens in the full 300 dimensions.
PCA flattens that to 2-d so it fits on a page, the same way a photo
flattens a 3-d scene. Distances/angles in the picture are only an
approximation — trust the printed cosine numbers, not your eyeballs.
--------------------------------------------------------------------

====================================================================
HOW TO PLAY WITH IT  (two ways — pick whichever you like)
====================================================================
The arithmetic is just two lists of words:

        result = (sum of POSITIVE words) - (sum of NEGATIVE words)

(A) EDIT THIS FILE: scroll to the "EDIT HERE" block below, change the
    word lists, save, and re-run:

        conda run -n llmfin python gen_king_analogy.py

(B) USE THE COMMAND LINE (no editing needed): pass the words as flags.
    Anything you pass overrides the EDIT-HERE defaults.

        # capital-of analogy:  paris - france + italy ≈ rome
        python gen_king_analogy.py --positive paris italy --negative france --expected rome

        # plurals:  cars - car + apple ≈ apples
        python gen_king_analogy.py --positive cars apple --negative car --expected apples

        # a finance flavour:  ceo - company + bank ≈ ?
        python gen_king_analogy.py --positive ceo bank --negative company

Tips:
  * Use lowercase, single words that are common in news/Wikipedia.
  * If a word isn't in the model's vocabulary you'll get a clear error
    listing the offending word — just pick another.
  * --expected is optional: it's a word you *think* the answer should be,
    drawn on the plot so you can see how close you got.

Custom experiments are saved into a 'playground/' folder next to this
script, so your tinkering never overwrites the official book figure.

Run inside the project env:
    conda run -n llmfin python gen_king_analogy.py
"""

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless backend: render to file, no GUI window needed
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

# ---------------------------------------------------------------------------
# ╔═══════════════════════════════════════════════════════════════════════╗
# ║  EDIT HERE  — change these to run your own analogy, then re-run.       ║
# ╚═══════════════════════════════════════════════════════════════════════╝
#
# The arithmetic is:  result = (sum of POSITIVE) - (sum of NEGATIVE)
# The classic example below reads as:  king - man + woman ≈ queen
POSITIVE_WORDS = ["king", "woman"]   # words to ADD      (the "+" side)
NEGATIVE_WORDS = ["man"]             # words to SUBTRACT (the "-" side)

# A word you EXPECT the result to be near, drawn on the plot for comparison.
# Set to None if you have no guess.
EXPECTED_WORD = "queen"

# How many nearest real words to look up and print for the result.
TOP_N = 3
# ---------------------------------------------------------------------------

# Which pre-trained embeddings to use. "300" = 300 numbers per word.
# gensim downloads this once (~376 MB) and caches it for next time.
MODEL_NAME = "glove-wiki-gigaword-300"

# Where the official book figure lives (only written by the DEFAULT analogy).
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
FIGURES_DIR = REPO_ROOT / "book" / "chapters" / "01-intro" / "figures"
# Your custom experiments go here instead, so the book figure stays safe.
PLAYGROUND_DIR = SCRIPT_DIR / "playground"

# The one canonical analogy that produces the figure used in the book.
# If you run exactly this, we overwrite the book figure; anything else is
# treated as an experiment and routed to playground/.
DEFAULT_POSITIVE = ["king", "woman"]
DEFAULT_NEGATIVE = ["man"]


def unit(v):
    """Return v scaled to length 1 (a 'unit vector').

    We compare words by *direction*, not magnitude, so we put every vector
    on the unit sphere first. The tiny +1e-12 just avoids dividing by zero.
    """
    return v / (np.linalg.norm(v) + 1e-12)


def cos(a, b):
    """Cosine similarity: how aligned two vectors are, from -1 to +1.

    +1 = same direction (synonyms-ish), 0 = unrelated, -1 = opposite.
    Because both inputs are unit vectors, this is just their dot product.
    This number is the *honest* measure of closeness — trust it over the
    flattened 2-d plot.
    """
    return float(np.dot(unit(a), unit(b)))


def check_vocab(kv, words):
    """Fail early with a friendly message if a word isn't in the model."""
    missing = [w for w in words if w not in kv]
    if missing:
        sys.exit(
            f"\nThese words are not in the {MODEL_NAME} vocabulary: {missing}\n"
            "Try common, lowercase, single words (e.g. 'king', 'paris', 'bank').\n"
        )


def expression_string(positive, negative):
    """Build a human-readable label like 'king + woman - man'."""
    expr = " + ".join(positive)
    if negative:
        expr += " - " + " - ".join(negative)
    return expr


def parse_args():
    """Read command-line flags; defaults come from the EDIT-HERE block above."""
    p = argparse.ArgumentParser(
        description="Play with word-vector analogies (king - man + woman ≈ queen).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--positive", nargs="+", default=POSITIVE_WORDS,
                   help="Words to ADD together (the '+' side of the analogy).")
    p.add_argument("--negative", nargs="*", default=NEGATIVE_WORDS,
                   help="Words to SUBTRACT (the '-' side). Can be empty.")
    p.add_argument("--expected", default=EXPECTED_WORD,
                   help="A word you think the answer should be (drawn for "
                        "comparison). Pass 'none' to omit.")
    p.add_argument("--topn", type=int, default=TOP_N,
                   help="How many nearest words to find for the result.")
    p.add_argument("--model", default=MODEL_NAME,
                   help="Which gensim-downloadable embedding model to load.")
    p.add_argument("--out", default=None,
                   help="Output path WITHOUT extension. Default: the book "
                        "figure for the classic analogy, else playground/.")
    return p.parse_args()


def choose_output(args):
    """Decide where to save, protecting the official book figure.

    Only the exact classic analogy (king - man + woman) is allowed to write
    the book's fig_king_analogy. Any customised run is saved under
    playground/ with a name built from the words, so students can keep and
    compare several experiments without clobbering anything.
    """
    if args.out:
        return Path(args.out)

    is_default = (args.positive == DEFAULT_POSITIVE
                  and args.negative == DEFAULT_NEGATIVE)
    if is_default:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        return FIGURES_DIR / "fig_king_analogy"

    PLAYGROUND_DIR.mkdir(parents=True, exist_ok=True)
    name = "analogy_" + "_".join(args.positive)
    if args.negative:
        name += "__minus__" + "_".join(args.negative)
    return PLAYGROUND_DIR / name


def main():
    args = parse_args()
    positive, negative = args.positive, args.negative
    expected = None if str(args.expected).lower() == "none" else args.expected

    # gensim is imported here (not at the top) so that `--help` is instant and
    # doesn't trigger the big model download just to read the usage text.
    import gensim.downloader as api

    print(f"Loading {args.model} (downloads & caches on first run)…", flush=True)
    kv = api.load(args.model)  # kv = a KeyedVectors table: word -> 300 numbers

    # 1) Make sure every word the user asked for actually exists in the model.
    words_to_check = positive + negative + ([expected] if expected else [])
    check_vocab(kv, words_to_check)

    # 2) Do the arithmetic. Each word is put on the unit sphere first, then we
    #    add the positives and subtract the negatives. This is the vector that
    #    "king - man + woman" literally evaluates to.
    result = np.zeros(kv.vector_size, dtype=float)
    for w in positive:
        result += unit(kv[w])
    for w in negative:
        result -= unit(kv[w])

    # 3) Ask the model: which REAL words sit closest to that result vector?
    #    (gensim automatically excludes the input words from the answer.)
    nearest = kv.most_similar(positive=positive, negative=negative, topn=args.topn)
    expr = expression_string(positive, negative)
    print(f"{expr} ≈ {nearest}", flush=True)
    if expected:
        print(f"cosine(result, {expected!r}) = {cos(result, kv[expected]):.3f}",
              flush=True)

    # ----------------------------------------------------------------------
    # 4) Build the picture. Gather every point we want to draw, remember what
    #    "role" each plays (so we can colour it), then PCA everything together
    #    down to 2-d. PCA must see all points at once so they share one frame.
    # ----------------------------------------------------------------------
    points = []  # list of (label, 300-d vector, role)
    for w in positive:
        points.append((w, unit(kv[w]), "positive"))
    for w in negative:
        points.append((w, unit(kv[w]), "negative"))
    if expected:
        points.append((expected, unit(kv[expected]), "expected"))
    # Also show the model's top answer word, if it isn't already on the plot.
    top_word = nearest[0][0]
    already = {lab for lab, _, _ in points}
    if top_word not in already:
        points.append((top_word, unit(kv[top_word]), "nearest"))
    points.append((expr, result, "result"))  # the computed vector itself

    vectors = np.vstack([v for _, v, _ in points])
    xy = PCA(n_components=2, random_state=0).fit_transform(vectors)

    # One colour/marker per role. (colour, marker, size)
    role_style = {
        "positive": ("#2ca02c", "s", 130),   # green squares  — words we ADD
        "negative": ("#d62728", "X", 150),   # red X          — words we SUBTRACT
        "expected": ("#1f77b4", "o", 150),   # blue circle    — your guess
        "nearest":  ("#9467bd", "D", 120),   # purple diamond — model's answer
        "result":   ("#ff7f0e", "*", 440),   # orange star    — the arithmetic result
    }

    fig, ax = plt.subplots(figsize=(7.0, 5.8))
    res_xy = None
    first_pos_xy = None
    for (x, y), (label, _, role) in zip(xy, points):
        c, m, s = role_style[role]
        ax.scatter(x, y, c=c, marker=m, s=s, zorder=4,
                   edgecolors="black", linewidths=0.7)
        # A short, readable label next to each marker.
        shown = "result" if role == "result" else label
        ax.annotate(shown, (x, y), textcoords="offset points", xytext=(9, 6),
                    fontsize=11,
                    fontweight="bold" if role == "result" else "normal")
        if role == "result":
            res_xy = (x, y)
        if role == "positive" and first_pos_xy is None:
            first_pos_xy = (x, y)

    # Arrow from the first "+" word to the result: shows the displacement that
    # the subtraction/addition produced.
    if first_pos_xy is not None and res_xy is not None:
        ax.annotate("", xy=res_xy, xytext=first_pos_xy,
                    arrowprops=dict(arrowstyle="-|>", color="#ff7f0e", lw=2.2),
                    zorder=3)
    # Dotted line from the result to your expected word: short line = good hit.
    if expected and res_xy is not None:
        exp_xy = xy[[lab for lab, _, _ in points].index(expected)]
        ax.plot([res_xy[0], exp_xy[0]], [res_xy[1], exp_xy[1]], ":",
                color="black", lw=1.6, zorder=3)

    # Info box: the model's nearest words and their similarity scores.
    box = ("nearest words to\n" + expr + ":\n"
           + "\n".join(f"  {w:<10}{s:.2f}" for w, s in nearest))
    ax.text(0.02, 0.02, box, transform=ax.transAxes, fontsize=9,
            va="bottom", ha="left", family="monospace",
            bbox=dict(boxstyle="round,pad=0.4", fc="#f7f7f7", ec="grey", lw=0.7))

    ax.axhline(0, color="lightgrey", lw=0.6, zorder=0)
    ax.axvline(0, color="lightgrey", lw=0.6, zorder=0)
    ax.set_xlabel("PC 1  (PCA-flattened from 300d)", fontsize=11)
    ax.set_ylabel("PC 2", fontsize=11)
    title = f"Word analogy in GloVe (300d):  {expr}"
    if expected:
        title += f"  $\\approx$  {expected}"
    ax.set_title(title, fontsize=12)
    ax.margins(0.22)
    fig.tight_layout()

    # 5) Save. Default analogy -> book figure; anything else -> playground/.
    out = choose_output(args)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)
    cos_str = f"  (cos to {expected} = {cos(result, kv[expected]):.3f})" if expected else ""
    print(f"Wrote {out.with_suffix('.pdf')}{cos_str}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
