"""TF-IDF cosine retrieval over filing chunks (NumPy only, deterministic, offline).

CLI:
    python -m tools.retrieve "What is NovaCorp's customer concentration?" -k 3
"""
from __future__ import annotations

import argparse
import json
import math

from tools._common import load_corpus, tokenize
from tools.chunk import Chunk, chunk_corpus


class Retriever:
    """A tiny TF-IDF retriever: fit on chunks, then rank them against a query."""

    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self._tokens = [tokenize(c.text) for c in chunks]
        self._vocab = sorted({w for toks in self._tokens for w in toks})
        self._index = {w: j for j, w in enumerate(self._vocab)}
        n = len(chunks)
        df = [0] * len(self._vocab)
        for toks in self._tokens:
            for w in set(toks):
                df[self._index[w]] += 1
        self._idf = [math.log((1 + n) / (1 + df[j])) + 1.0 for j in range(len(self._vocab))]
        self._matrix = [self._vectorize(toks) for toks in self._tokens]

    def _vectorize(self, toks: list[str]) -> dict[int, float]:
        if not toks:
            return {}
        vec: dict[int, float] = {}
        for w in toks:
            j = self._index.get(w)
            if j is not None:
                vec[j] = vec.get(j, 0.0) + 1.0
        for j in vec:
            vec[j] = (vec[j] / len(toks)) * self._idf[j]
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {j: v / norm for j, v in vec.items()}

    @staticmethod
    def _cosine(a: dict[int, float], b: dict[int, float]) -> float:
        if len(a) > len(b):
            a, b = b, a
        return sum(v * b.get(j, 0.0) for j, v in a.items())

    def search(self, query: str, k: int = 3) -> list[tuple[Chunk, float]]:
        q = self._vectorize(tokenize(query))
        scored = [(c, self._cosine(q, vec)) for c, vec in zip(self.chunks, self._matrix)]
        scored.sort(key=lambda t: t[1], reverse=True)
        return scored[:k]


def build_default_retriever(*, size: int = 60, overlap: int = 15) -> Retriever:
    return Retriever(chunk_corpus(load_corpus(), size=size, overlap=overlap))


def _main() -> None:
    ap = argparse.ArgumentParser(description="Retrieve the top filing chunks for a question.")
    ap.add_argument("question")
    ap.add_argument("-k", type=int, default=3)
    args = ap.parse_args()
    hits = build_default_retriever().search(args.question, k=args.k)
    print(json.dumps(
        [{"id": c.id, "score": round(s, 4), "text": c.text} for c, s in hits],
        indent=2,
    ))


if __name__ == "__main__":
    _main()
