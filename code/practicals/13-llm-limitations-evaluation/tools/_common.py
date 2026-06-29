"""Shared helpers: answer normalisation, tokenisation, and data loading.

Standard library + numpy only. No network, no external services.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Keep letters, digits, '%' and '.' (so "64%" and "1.14" survive); drop the rest.
_KEEP = re.compile(r"[^a-z0-9%. ]+")
_WS = re.compile(r"\s+")


def normalize(text: str) -> str:
    """Lowercase, strip punctuation (except % and decimal points), collapse whitespace.

    Exact-match scoring compares two answers after this normalisation, so
    "US dollars", "us dollars" and "  US Dollars " all collapse to the same string,
    while "1.4 billion" and "1.14 billion" stay distinct.
    """
    text = _KEEP.sub(" ", text.lower())
    text = _WS.sub(" ", text).strip()
    # strip stray leading/trailing dots left on a token (e.g. "21%." -> "21%")
    return " ".join(t.strip(".") for t in text.split())


def tokens(text: str) -> list[str]:
    """Normalised whitespace tokens, used for token-level F1."""
    norm = normalize(text)
    return norm.split() if norm else []


def load_json(path: Path | str) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_gold(path: Path | str | None = None) -> dict[str, dict]:
    """Return ``{id: {id, question, answer}}`` for the gold QA set."""
    path = Path(path) if path else DATA_DIR / "gold.json"
    return {item["id"]: item for item in load_json(path)}


def load_predictions(path: Path | str) -> dict[str, dict]:
    """Return ``{id: {id, answer, confidence}}`` for a candidate model file.

    Accepts either a bare list of predictions or an object with a ``predictions`` key.
    """
    obj = load_json(path)
    preds = obj["predictions"] if isinstance(obj, dict) else obj
    return {item["id"]: item for item in preds}
