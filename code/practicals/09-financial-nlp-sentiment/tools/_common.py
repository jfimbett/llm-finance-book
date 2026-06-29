"""Shared helpers: tokenisation, lexicon and headline loading. Standard library only."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
LEXICON_PATH = DATA_DIR / "lexicon.json"
HEADLINES_PATH = DATA_DIR / "headlines.csv"


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens, in order, with NO stop-word removal.

    Sentiment scoring depends on function words: negators ("not", "no") flip a
    polarity word and intensifiers ("strong", "sharp") amplify it, so dropping
    them — as a retrieval tokenizer would — silently breaks the signal.
    """
    return re.findall(r"[a-z]+", text.lower())


def load_lexicon(path: Path | str = LEXICON_PATH) -> dict:
    """Load the bundled finance polarity lexicon.

    Positive/negative/negator word lists become sets for O(1) lookup; the
    intensifier map (word -> multiplier) is kept as-is.
    """
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return {
        "positive": set(raw["positive"]),
        "negative": set(raw["negative"]),
        "negators": set(raw["negators"]),
        "intensifiers": {k: float(v) for k, v in raw["intensifiers"].items()},
    }


def load_headlines(path: Path | str = HEADLINES_PATH) -> list[dict]:
    """Return ``[{date, id, text}]`` for every row in the bundled headlines CSV."""
    rows: list[dict] = []
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            rows.append({"date": row["date"], "id": row["id"], "text": row["headline"]})
    return rows
