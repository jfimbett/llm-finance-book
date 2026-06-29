"""Shared helpers: load the bundled market data and the text views. NumPy + stdlib only."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MARKET_FILE = DATA_DIR / "market.json"
VIEWS_DIR = DATA_DIR / "views"


def load_market(market_file: Path | str = MARKET_FILE) -> dict:
    """Return the bundled market block: assets, expected_returns, covariance, returns.

    Arrays are converted to NumPy; the raw JSON scalars (frequency, periods_per_year)
    are passed through unchanged.
    """
    raw = json.loads(Path(market_file).read_text(encoding="utf-8"))
    return {
        "assets": list(raw["assets"]),
        "frequency": raw.get("frequency", "monthly"),
        "periods_per_year": int(raw.get("periods_per_year", 12)),
        "expected_returns": np.asarray(raw["expected_returns"], dtype=float),
        "covariance": np.asarray(raw["covariance"], dtype=float),
        "returns": np.asarray(raw["returns"], dtype=float),
    }


def load_views(views_dir: Path | str = VIEWS_DIR) -> dict[str, str]:
    """Return ``{filename: text}`` for every .txt view in the views directory."""
    views_dir = Path(views_dir)
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(views_dir.glob("*.txt"))}
