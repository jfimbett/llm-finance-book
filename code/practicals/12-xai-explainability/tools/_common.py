"""Shared helpers: load the bundled model and applicants. Standard library + numpy only."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MODEL_PATH = DATA_DIR / "model.json"
APPLICANTS_DIR = DATA_DIR / "applicants"

# Inputs a lawful credit explanation may NEVER cite, regardless of any data file.
PROTECTED_KEYS = frozenset({
    "race", "color", "religion", "national_origin", "sex", "gender",
    "marital_status", "age", "public_assistance", "protected",
})


def load_model(path: Path | str = MODEL_PATH) -> dict:
    """Return the bundled linear/logistic credit model as a dict."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def resolve_applicant(name: str) -> Path:
    """Accept either a path to an applicant JSON or a bare name like ``alice``."""
    p = Path(name)
    if p.exists():
        return p
    candidate = APPLICANTS_DIR / (name if name.endswith(".json") else f"{name}.json")
    if not candidate.exists():
        available = ", ".join(sorted(q.stem for q in APPLICANTS_DIR.glob("*.json")))
        raise FileNotFoundError(f"unknown applicant '{name}'. Available: {available}")
    return candidate


def load_applicant(name: str) -> dict:
    """Load an applicant record. Only the ``features`` block feeds the model."""
    return json.loads(resolve_applicant(name).read_text(encoding="utf-8"))


def feature_arrays(model: dict) -> tuple[list[str], np.ndarray, np.ndarray]:
    """Return ``(keys, weights, baselines)`` aligned to the model's feature order."""
    feats = model["features"]
    keys = [f["key"] for f in feats]
    weights = np.array([float(f["weight"]) for f in feats], dtype=float)
    baselines = np.array([float(f["baseline"]) for f in feats], dtype=float)
    return keys, weights, baselines


def applicant_vector(model: dict, applicant: dict) -> np.ndarray:
    """Pull the model's feature values out of an applicant, in model order.

    Any key not in the model's feature list is ignored — protected attributes in
    the applicant file never enter the computation.
    """
    keys, _, _ = feature_arrays(model)
    feats = applicant.get("features", {})
    missing = [k for k in keys if k not in feats]
    if missing:
        raise KeyError(f"applicant is missing model features: {missing}")
    return np.array([float(feats[k]) for k in keys], dtype=float)


def sigmoid(z: float) -> float:
    """Numerically stable logistic function."""
    if z >= 0:
        return 1.0 / (1.0 + np.exp(-z))
    ez = np.exp(z)
    return ez / (1.0 + ez)
