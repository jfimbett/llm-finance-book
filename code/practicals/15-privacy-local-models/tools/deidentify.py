"""Rule-based PII detection and redaction (standard library only, deterministic, offline).

Detects five categories of personal data with explicit regular expressions and a
small name gazetteer — no model, no network, no training:

* EMAIL    — addresses
* SSN      — US Social Security numbers (ddd-dd-dddd)
* PHONE    — US phone numbers
* ACCOUNT  — org/account numbers of the form LETTERS-DIGITS (e.g. NVC-88421003)
* PERSON   — titled names (Dr. Alan Pierce) and gazetteer first names + surnames

Each detected span is replaced by a typed placeholder (``[EMAIL]``, ``[SSN]`` …)
so the redacted text stays readable while every seeded identifier is removed.

CLI:
    python -m tools.deidentify                       # redact the bundled document
    python -m tools.deidentify path/to/file.txt      # redact another file
    python -m tools.deidentify --json                # emit entities + redacted text as JSON
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from tools._common import DEFAULT_DOC, load_doc

# A deliberately small, explicit gazetteer. Detection stays conservative: a name is
# only redacted when it is title-prefixed or its first name is on this list, so a
# benign capitalised word at the start of a sentence is never mistaken for a person.
FIRST_NAMES = sorted({
    "James", "Maria", "Alan", "Robert", "Linda", "Michael", "Susan",
    "David", "Karen", "John", "Patricia", "William", "Elizabeth",
})
_TITLES = r"(?:Mr|Mrs|Ms|Miss|Dr|Prof)\.?"
# Name continuation uses horizontal whitespace only, so a match never runs across a
# line break and swallows the next field label (e.g. an "Email:" line below a name).
_PERSON = re.compile(
    r"\b(?:"
    + _TITLES + r"[ \t]+[A-Z][a-z]+(?:[ \t]+[A-Z][a-z]+){0,2}"          # title + capitalised name(s)
    + r"|(?:" + "|".join(FIRST_NAMES) + r")(?:[ \t]+[A-Z][a-z]+){0,2}"  # gazetteer first + surname(s)
    + r")\b"
)

# Order matters: more specific digit patterns (SSN) are listed before PHONE so that,
# on the rare overlap, the specific type wins during span resolution.
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("EMAIL", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("PHONE", re.compile(r"\b(?:\+?1[ \-.])?\(?\d{3}\)?[ \-.]\d{3}[ \-.]\d{4}\b")),
    ("ACCOUNT", re.compile(r"\b[A-Z]{2,5}-\d{5,}\b")),
    ("PERSON", _PERSON),
]


def detect(text: str) -> list[dict]:
    """Return non-overlapping detected entities, ordered by position in *text*.

    Each entity is ``{"type", "value", "start", "end"}``.
    """
    spans = []
    for typ, pat in PATTERNS:
        for m in pat.finditer(text):
            spans.append((m.start(), m.end(), typ, m.group()))
    # Earliest start first; on a tie, the longer (more complete) span wins.
    spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
    kept: list[dict] = []
    last_end = -1
    for start, end, typ, val in spans:
        if start >= last_end:
            kept.append({"type": typ, "value": val, "start": start, "end": end})
            last_end = end
    return kept


def redact(text: str, entities: list[dict] | None = None) -> str:
    """Replace every detected entity in *text* with its typed placeholder."""
    if entities is None:
        entities = detect(text)
    out: list[str] = []
    cursor = 0
    for e in sorted(entities, key=lambda e: e["start"]):
        out.append(text[cursor:e["start"]])
        out.append(f"[{e['type']}]")
        cursor = e["end"]
    out.append(text[cursor:])
    return "".join(out)


def deidentify(text: str) -> dict:
    """Detect and redact in one call.

    Returns ``{"redacted": str, "entities": [...], "counts": {type: n}}``.
    """
    entities = detect(text)
    counts: dict[str, int] = {}
    for e in entities:
        counts[e["type"]] = counts.get(e["type"], 0) + 1
    return {"redacted": redact(text, entities), "entities": entities, "counts": counts}


def _main() -> None:
    ap = argparse.ArgumentParser(description="Detect and redact PII in a document.")
    ap.add_argument("path", nargs="?", default=str(DEFAULT_DOC),
                    help="document to de-identify (defaults to the bundled ticket)")
    ap.add_argument("--json", action="store_true",
                    help="emit detected entities and redacted text as JSON")
    args = ap.parse_args()
    text = load_doc(Path(args.path)) if args.path != str(DEFAULT_DOC) else load_doc()
    result = deidentify(text)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["redacted"])


if __name__ == "__main__":
    _main()
