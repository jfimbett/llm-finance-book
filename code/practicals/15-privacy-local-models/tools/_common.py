"""Shared helpers: tokenisation and document/PII loading. Standard library only."""
from __future__ import annotations

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_DOC = DATA_DIR / "customer_support_ticket.txt"
SEEDED_PII = DATA_DIR / "seeded_pii.json"


def tokenize(text: str) -> list[str]:
    """Lowercase content tokens (words AND numbers).

    Numbers are kept deliberately: an SSN fragment like '6789' or an account
    suffix is exactly the kind of token whose disappearance the utility metric
    must account for.
    """
    return re.findall(r"[a-z0-9]+", text.lower())


def load_doc(path: Path | str = DEFAULT_DOC) -> str:
    """Return the bundled fictional document as text."""
    return Path(path).read_text(encoding="utf-8")


def load_seeded_pii(path: Path | str = SEEDED_PII) -> dict[str, list[str]]:
    """Return the ground-truth PII seeded into the document, grouped by type."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def seeded_pii_values(path: Path | str = SEEDED_PII) -> list[str]:
    """Flatten the seeded PII into a single list of exact strings."""
    grouped = load_seeded_pii(path)
    return [v for values in grouped.values() for v in values]
