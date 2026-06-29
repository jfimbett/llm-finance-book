"""Shared helpers: tokenisation and snippet loading. Standard library only."""
from __future__ import annotations

import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SOURCES = ("filings", "news")

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "to", "is", "are", "was", "were",
    "for", "on", "at", "by", "as", "with", "this", "that", "from", "it", "its",
    "be", "been", "has", "have", "had", "will", "we", "our", "their", "which",
    "not", "but", "also", "more", "than", "such", "may", "can", "any", "all",
    "up", "out", "per", "no", "us", "about",
    # question / auxiliary words — function words that shouldn't drive relevance
    "how", "what", "when", "where", "why", "who", "did", "do", "does", "the",
}


def tokenize(text: str, *, min_len: int = 2) -> list[str]:
    """Lowercase content tokens (words AND numbers) of length >= min_len, stop-words removed.

    Numbers are kept deliberately — for financial text, matching '58' or '2025' is exactly
    how a brief is checked against the snippet it claims to be quoting.
    """
    return [
        w for w in re.findall(r"[a-z0-9]+", text.lower())
        if len(w) >= min_len and w not in STOPWORDS
    ]


def load_snippets(source: str = "all", data_dir: Path | str = DATA_DIR) -> dict[str, str]:
    """Return ``{snippet_id: text}`` for the requested source.

    ``source`` is one of ``"filings"``, ``"news"``, or ``"all"``. The snippet id is the
    file name (e.g. ``meridian_10k_risk.txt``) so a brief can cite the exact document.
    """
    data_dir = Path(data_dir)
    if source == "all":
        folders = SOURCES
    elif source in SOURCES:
        folders = (source,)
    else:
        raise ValueError(f"source must be one of {('all', *SOURCES)}, got {source!r}")
    out: dict[str, str] = {}
    for folder in folders:
        for p in sorted((data_dir / folder).glob("*.txt")):
            out[p.name] = p.read_text(encoding="utf-8")
    return out
