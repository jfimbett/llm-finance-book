"""Quantify the privacy/utility tradeoff of a redaction (deterministic, offline).

Two reproducible numbers in [0, 1] that replace "eyeball whether it's redacted enough":

* privacy — fraction of the seeded PII that no longer appears in the redacted text.
            1.0 means every known identifier is gone.
* utility — fraction of the *non-PII* tokens that survive redaction. 1.0 means the
            redaction removed identifiers without collateral damage to the readable
            content; lower values mean over-redaction ate into useful text.

Privacy is measured against ground truth (``data/seeded_pii.json``), not against the
detector's own output, so the metric is an honest evaluation of how much the detector
actually caught.

CLI:
    python -m tools.metrics                      # score redaction of the bundled document
    python -m tools.metrics path/to/file.txt     # score redaction of another file
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from tools._common import DEFAULT_DOC, load_doc, seeded_pii_values, tokenize
from tools.deidentify import deidentify


def privacy(redacted: str, seeded_pii: list[str]) -> float:
    """Fraction of seeded PII strings that no longer occur in *redacted*."""
    if not seeded_pii:
        return 1.0
    removed = sum(1 for value in seeded_pii if value not in redacted)
    return removed / len(seeded_pii)


def utility(original: str, redacted: str, seeded_pii: list[str]) -> float:
    """Fraction of the original's non-PII tokens that are retained after redaction."""
    pii_tokens: set[str] = set()
    for value in seeded_pii:
        pii_tokens.update(tokenize(value))
    non_pii = [t for t in tokenize(original) if t not in pii_tokens]
    if not non_pii:
        return 1.0
    available = Counter(tokenize(redacted))
    retained = 0
    for t in non_pii:
        if available[t] > 0:
            available[t] -= 1
            retained += 1
    return retained / len(non_pii)


def tradeoff(original: str, redacted: str, seeded_pii: list[str]) -> dict[str, float]:
    """Return both metrics, rounded, as ``{"privacy", "utility"}``."""
    return {
        "privacy": round(privacy(redacted, seeded_pii), 3),
        "utility": round(utility(original, redacted, seeded_pii), 3),
    }


def _main() -> None:
    ap = argparse.ArgumentParser(description="Score the privacy/utility tradeoff of a redaction.")
    ap.add_argument("path", nargs="?", default=str(DEFAULT_DOC),
                    help="document to score (defaults to the bundled ticket)")
    args = ap.parse_args()
    original = load_doc(Path(args.path)) if args.path != str(DEFAULT_DOC) else load_doc()
    result = deidentify(original)
    scores = tradeoff(original, result["redacted"], seeded_pii_values())
    print(json.dumps({"counts": result["counts"], **scores}, indent=2))


if __name__ == "__main__":
    _main()
