"""Shared helpers: tokenisation and corpus loading. Standard library only."""
from __future__ import annotations

import re
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parents[1] / "data" / "corpus"

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "to", "is", "are", "was", "were",
    "for", "on", "at", "by", "as", "with", "this", "that", "from", "it", "its",
    "be", "been", "has", "have", "had", "will", "we", "our", "their", "which",
    "not", "but", "also", "more", "than", "such", "may", "can", "any", "all",
    "up", "out", "per", "no", "us",
    # question / auxiliary words — function words that shouldn't drive relevance
    "how", "what", "when", "where", "why", "who", "did", "do", "does",
}


def tokenize(text: str, *, min_len: int = 2) -> list[str]:
    """Lowercase content tokens (words AND numbers) of length >= min_len, stop-words removed.

    Numbers are kept deliberately — for financial text, matching '64' or '2024' is
    exactly how the grader catches an answer that invents figures not in the source.
    """
    return [
        w for w in re.findall(r"[a-z0-9]+", text.lower())
        if len(w) >= min_len and w not in STOPWORDS
    ]


def load_corpus(corpus_dir: Path | str = CORPUS_DIR) -> dict[str, str]:
    """Return ``{filename: text}`` for every .txt file in the corpus directory."""
    corpus_dir = Path(corpus_dir)
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(corpus_dir.glob("*.txt"))}
