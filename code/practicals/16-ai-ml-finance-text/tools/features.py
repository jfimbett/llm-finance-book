"""Turn financial text into a numeric feature matrix (TF-IDF, NumPy, offline).

The vocabulary and IDF weights are learned from the *training* texts only and
then reused to transform held-out texts, so the test set never leaks into the
features. Each row is L2-normalised, which is what lets a linear classifier read
a TF-IDF vector as a direction in word space.

CLI:
    python -m tools.features "Earnings beat expectations and revenue surged."
"""
from __future__ import annotations

import argparse
import math

import numpy as np

from tools._common import tokenize


class TfidfVectorizer:
    """A tiny fit/transform TF-IDF vectoriser over a fixed vocabulary."""

    def __init__(self, *, min_df: int = 1):
        self.min_df = min_df
        self.vocabulary_: list[str] = []
        self._index: dict[str, int] = {}
        self._idf: np.ndarray = np.zeros(0)

    def fit(self, texts: list[str]) -> "TfidfVectorizer":
        tokenized = [tokenize(t) for t in texts]
        df: dict[str, int] = {}
        for toks in tokenized:
            for w in set(toks):
                df[w] = df.get(w, 0) + 1
        self.vocabulary_ = sorted(w for w, d in df.items() if d >= self.min_df)
        self._index = {w: j for j, w in enumerate(self.vocabulary_)}
        n = len(texts)
        self._idf = np.array(
            [math.log((1 + n) / (1 + df[w])) + 1.0 for w in self.vocabulary_],
            dtype=float,
        )
        return self

    def transform(self, texts: list[str]) -> np.ndarray:
        if not self.vocabulary_:
            raise ValueError("call fit() before transform()")
        rows = np.zeros((len(texts), len(self.vocabulary_)), dtype=float)
        for i, t in enumerate(texts):
            for w in tokenize(t):
                j = self._index.get(w)
                if j is not None:
                    rows[i, j] += 1.0
        rows *= self._idf  # broadcast IDF across columns
        norms = np.linalg.norm(rows, axis=1, keepdims=True)
        norms[norms == 0.0] = 1.0
        return rows / norms

    def fit_transform(self, texts: list[str]) -> np.ndarray:
        return self.fit(texts).transform(texts)


def _main() -> None:
    from tools._common import load_dataset

    ap = argparse.ArgumentParser(description="Vectorise text against the bundled corpus vocabulary.")
    ap.add_argument("text", help="a sentence to turn into a TF-IDF feature vector")
    args = ap.parse_args()

    texts, _ = load_dataset()
    vec = TfidfVectorizer().fit(texts)
    row = vec.transform([args.text])[0]
    active = sorted(
        ((vec.vocabulary_[j], round(float(row[j]), 4)) for j in np.nonzero(row)[0]),
        key=lambda t: t[1],
        reverse=True,
    )
    print(f"vocabulary size: {len(vec.vocabulary_)}")
    print(f"non-zero features for the input: {len(active)}")
    for word, weight in active:
        print(f"  {word:<14} {weight}")


if __name__ == "__main__":
    _main()
