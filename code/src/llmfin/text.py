"""Lightweight, dependency-free text helpers for the practicals.

Pure NumPy/standard-library so a student notebook runs without scikit-learn.
"""
from __future__ import annotations

import re
from math import log

import numpy as np

DEFAULT_STOP = {
    "the", "a", "an", "and", "or", "of", "in", "to", "is", "are", "was", "were",
    "for", "on", "at", "by", "as", "with", "this", "that", "from", "it", "its",
    "be", "been", "has", "have", "had", "will", "we", "our", "their", "which",
    "not", "but", "also", "more", "than", "such", "may", "can", "any", "all",
    "one", "year", "million", "billion",
}


def tokenize(text: str, *, min_len: int = 3, stop: set[str] | None = None) -> list[str]:
    """Lowercase alphabetic tokens of length >= ``min_len``, stop-words removed."""
    stop = DEFAULT_STOP if stop is None else stop
    return [w for w in re.findall(rf"[a-z]{{{min_len},}}", text.lower()) if w not in stop]


def tfidf(docs: list[str], *, min_len: int = 3,
          stop: set[str] | None = None) -> tuple[list[str], np.ndarray]:
    """Compute a (terms, matrix) TF-IDF representation of a list of documents.

    ``matrix[i, j]`` is the TF-IDF weight of term ``terms[j]`` in ``docs[i]``,
    using ``tf = count/len`` and ``idf = log(N / df)``. No external NLP deps.
    """
    tokenized = [tokenize(d, min_len=min_len, stop=stop) for d in docs]
    vocab = sorted({w for toks in tokenized for w in toks})
    index = {w: j for j, w in enumerate(vocab)}
    n = len(docs)

    df = np.zeros(len(vocab))
    for toks in tokenized:
        for w in set(toks):
            df[index[w]] += 1
    idf = np.log(n / np.maximum(df, 1))

    mat = np.zeros((n, len(vocab)))
    for i, toks in enumerate(tokenized):
        if not toks:
            continue
        for w in toks:
            mat[i, index[w]] += 1
        mat[i] = mat[i] / len(toks) * idf
    return vocab, mat


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two 1-D vectors."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(a @ b / denom) if denom else 0.0
