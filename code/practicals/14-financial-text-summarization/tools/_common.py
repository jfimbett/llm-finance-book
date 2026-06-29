"""Shared helpers: tokenisation, whitespace normalisation, filing loading.

Standard library only.
"""
from __future__ import annotations

import re
from pathlib import Path

FILINGS_DIR = Path(__file__).resolve().parents[1] / "data" / "filings"

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "to", "is", "are", "was", "were",
    "for", "on", "at", "by", "as", "with", "this", "that", "from", "it", "its",
    "be", "been", "has", "have", "had", "will", "we", "our", "their", "which",
    "not", "but", "also", "more", "than", "such", "may", "can", "any", "all",
    "up", "out", "per", "no", "us", "now", "year", "quarter",
}


def normalize(text: str) -> str:
    """Collapse runs of whitespace to single spaces so patterns match across line wraps."""
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str, *, min_len: int = 1) -> list[str]:
    """Lowercase content tokens (words AND numbers) of length >= min_len, stop-words removed.

    Numbers are kept deliberately — for an earnings summary, matching '58' or '1.27' is
    exactly how the grader catches a summary that invents figures not in the filing.
    """
    return [
        w for w in re.findall(r"[a-z0-9]+", text.lower())
        if len(w) >= min_len and w not in STOPWORDS
    ]


def sentences(text: str) -> list[str]:
    """Split filing text into sentence-like units (used as the IDF document set)."""
    parts = re.split(r"(?<=[.!?])\s+|\n+", normalize(text))
    return [p.strip() for p in parts if p.strip()]


def load_filings(filings_dir: Path | str = FILINGS_DIR) -> dict[str, str]:
    """Return ``{filename: text}`` for every .txt filing in the data directory."""
    filings_dir = Path(filings_dir)
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(filings_dir.glob("*.txt"))}


def load_filing_text(filings_dir: Path | str = FILINGS_DIR) -> str:
    """Return the concatenated text of all bundled filings."""
    return "\n".join(load_filings(filings_dir).values())
