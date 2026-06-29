"""Shared helpers: tokenisation and labelled-dataset loading. Standard library only."""
from __future__ import annotations

import csv
import re
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "labeled" / "headlines.csv"

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "to", "is", "are", "was", "were",
    "for", "on", "at", "by", "as", "with", "this", "that", "from", "it", "its",
    "be", "been", "has", "have", "had", "will", "we", "our", "their", "which",
    "not", "but", "also", "more", "than", "such", "may", "can", "any", "all",
    "up", "out", "per", "no", "us", "after", "amid", "again", "every", "above",
    "below", "year", "full", "new",
}


def tokenize(text: str, *, min_len: int = 2) -> list[str]:
    """Lowercase content tokens of length >= min_len, stop-words removed.

    Sentiment-bearing words ("surged", "plunged") are exactly the features the
    classifier leans on, so the stop-word list strips only function words.
    """
    return [
        w for w in re.findall(r"[a-z0-9]+", text.lower())
        if len(w) >= min_len and w not in STOPWORDS
    ]


def load_dataset(path: Path | str = DATA_PATH) -> tuple[list[str], list[int]]:
    """Return ``(texts, labels)`` from a two-column ``label,text`` CSV."""
    path = Path(path)
    texts: list[str] = []
    labels: list[int] = []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            texts.append(row["text"])
            labels.append(int(row["label"]))
    return texts, labels
