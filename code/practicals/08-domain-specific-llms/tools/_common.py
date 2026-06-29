"""Shared helpers: tokenisation, dataset loading, lexicon scoring. Stdlib + NumPy only."""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SENTENCES_PATH = DATA_DIR / "sentences.jsonl"

LABELS = ("positive", "negative", "neutral")


def tokenize(text: str) -> list[str]:
    """Lowercase alphabetic tokens. Punctuation and casing are stripped so that
    a lexicon keyed on bare words ('beat', 'headwinds') matches regardless of context."""
    return re.findall(r"[a-z]+", text.lower())


def load_sentences(path: Path | str = SENTENCES_PATH) -> list[dict]:
    """Return the bundled labelled finance sentences as ``[{id, text, label}, ...]``."""
    path = Path(path)
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def load_lexicon(name: str) -> dict[str, int]:
    """Load a polarity lexicon by name ('general' or 'domain') as ``{word: score}``."""
    path = DATA_DIR / f"lexicon_{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def score_sentence(text: str, lexicon: dict[str, int]) -> int:
    """Sum the polarity of every token found in *lexicon*. Tokens absent from the
    lexicon contribute zero — that is exactly how a missing finance term is silently
    dropped by a model that never learned it."""
    return sum(lexicon.get(tok, 0) for tok in tokenize(text))


def classify(text: str, lexicon: dict[str, int]) -> str:
    """Map a sentence to a label by the sign of its summed polarity."""
    s = score_sentence(text, lexicon)
    if s > 0:
        return "positive"
    if s < 0:
        return "negative"
    return "neutral"


def accuracy(predictions: list[str], gold: list[str]) -> float:
    """Fraction of predictions that match the gold labels (NumPy)."""
    if not gold:
        return 0.0
    return float(np.mean(np.asarray(predictions) == np.asarray(gold)))
