"""Shared helpers: normalisation, data loading, figure extraction. Standard library only."""
from __future__ import annotations

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SOURCE_PATH = DATA_DIR / "source.txt"
TARGET_PATH = DATA_DIR / "target.json"

# A numeric figure: an integer/decimal, optionally trailing '%'. Commas are stripped first.
_FIGURE_RE = re.compile(r"\d+(?:\.\d+)?%?")


def normalize(text: str) -> str:
    """Lowercase and collapse all runs of whitespace to a single space.

    Substring matching of a required phrase (``"2.4 billion"``) is then stable
    regardless of line breaks or double spaces in the candidate draft.
    """
    return re.sub(r"\s+", " ", text.lower()).strip()


def figures(text: str) -> set[str]:
    """Every numeric token in *text* (``'22%'``, ``'2.4'``, ``'310'``), commas removed."""
    return set(_FIGURE_RE.findall(text.replace(",", "")))


def load_source(path: Path | str = SOURCE_PATH) -> str:
    return Path(path).read_text(encoding="utf-8")


def load_target(path: Path | str = TARGET_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_candidate(arg: str) -> str:
    """Resolve a candidate: if *arg* is an existing file path, read it; else treat it as text."""
    p = Path(arg)
    if p.exists() and p.is_file():
        return p.read_text(encoding="utf-8")
    return arg
