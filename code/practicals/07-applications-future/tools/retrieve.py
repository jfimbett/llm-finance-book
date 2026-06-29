"""TF-IDF cosine retrieval over the bundled snippets (stdlib + NumPy, deterministic, offline).

Each snippet file (a filing or news excerpt) is one retrievable document, identified by its
file name so a brief can cite it. Restrict the search to one source with ``--source`` once the
router has decided where the evidence should come from.

CLI:
    python -m tools.retrieve "autonomous warehouse partnership" --source news -k 2
"""
from __future__ import annotations

import argparse
import json

import numpy as np

from tools._common import load_snippets, tokenize


class Retriever:
    """A tiny TF-IDF retriever: fit on snippets, then rank them against a query."""

    def __init__(self, snippets: dict[str, str]):
        self.ids = list(snippets.keys())
        self.texts = list(snippets.values())
        self._tokens = [tokenize(t) for t in self.texts]
        self._vocab = sorted({w for toks in self._tokens for w in toks})
        self._index = {w: j for j, w in enumerate(self._vocab)}

        n = len(self.texts)
        v = len(self._vocab)
        df = np.zeros(v)
        for toks in self._tokens:
            for w in set(toks):
                df[self._index[w]] += 1
        self._idf = np.log((1 + n) / (1 + df)) + 1.0
        self._matrix = np.vstack([self._vectorize(toks) for toks in self._tokens]) if n else np.zeros((0, v))

    def _vectorize(self, toks: list[str]) -> np.ndarray:
        vec = np.zeros(len(self._vocab))
        if not toks:
            return vec
        for w in toks:
            j = self._index.get(w)
            if j is not None:
                vec[j] += 1.0
        vec = (vec / len(toks)) * self._idf
        norm = np.linalg.norm(vec)
        return vec / norm if norm else vec

    def search(self, query: str, k: int = 3) -> list[tuple[str, str, float]]:
        """Return up to *k* ``(snippet_id, text, score)`` tuples, best first."""
        if not self.ids:
            return []
        q = self._vectorize(tokenize(query))
        scores = self._matrix @ q
        order = np.argsort(-scores, kind="stable")[:k]
        return [(self.ids[i], self.texts[i], float(scores[i])) for i in order]


def build_retriever(source: str = "all") -> Retriever:
    return Retriever(load_snippets(source))


def _main() -> None:
    ap = argparse.ArgumentParser(description="Retrieve the top snippets for a question.")
    ap.add_argument("question")
    ap.add_argument("--source", default="all", choices=["all", "filings", "news"])
    ap.add_argument("-k", type=int, default=3)
    args = ap.parse_args()
    hits = build_retriever(args.source).search(args.question, k=args.k)
    print(json.dumps(
        [{"id": sid, "score": round(s, 4), "text": text} for sid, text, s in hits],
        indent=2,
    ))


if __name__ == "__main__":
    _main()
