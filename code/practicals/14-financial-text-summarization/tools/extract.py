"""Pattern-extract named numeric fields from a filing, validated against a small schema.

The agent never reads a number off the page. This tool finds each field with an explicit
regex, records the exact source span it came from, casts it to a typed value, and checks
the result against a JSON-schema-style contract. Anything that does not match a pattern is
simply absent from the record — there is no guessing.

CLI:
    python -m tools.extract                 # extract from the bundled filing
    python -m tools.extract path/to.txt     # extract from a specific file
"""
from __future__ import annotations

import argparse
import json
import re
import sys

from tools._common import load_filing_text, normalize


class SchemaError(ValueError):
    """Raised when an extraction record does not satisfy the field schema."""


# field name -> (capture regex, caster). The first capture group is the field value.
PATTERNS: dict[str, tuple[str, type]] = {
    "revenue": (r"[Tt]otal revenue was (\$\d[\d.]* (?:billion|million))", str),
    "gross_margin": (r"[Gg]ross margin was (\d+(?:\.\d+)?)\s*%", float),
    "eps": (r"[Dd]iluted earnings per share were \$(\d+(?:\.\d+)?)", float),
    "guidance": (
        r"revenue guidance to a range of (\$\d[\d.]* billion to \$\d[\d.]* billion)",
        str,
    ),
}

# A small JSON-schema-style contract for the extracted *values*.
SCHEMA: dict[str, dict] = {
    "revenue": {"type": "string", "pattern": r"^\$\d.*\b(billion|million)$"},
    "gross_margin": {"type": "number", "min": 0, "max": 100},
    "eps": {"type": "number", "min": 0},
    "guidance": {"type": "string", "pattern": r"to"},
}

REQUIRED = ["revenue", "gross_margin", "guidance", "eps"]


def extract(text: str) -> dict[str, dict]:
    """Extract every defined field from *text*.

    Returns ``{field: {"value": <typed>, "span": [start, end], "source": <matched text>}}``.
    Spans index into the whitespace-normalised source so they survive line wraps.
    """
    norm = normalize(text)
    record: dict[str, dict] = {}
    for name, (pattern, cast) in PATTERNS.items():
        m = re.search(pattern, norm)
        if m is None:
            continue
        record[name] = {
            "value": cast(m.group(1)),
            "span": [m.start(1), m.end(1)],
            "source": m.group(0),
        }
    return record


def validate(record: dict[str, dict], schema: dict = SCHEMA, required=REQUIRED) -> list[str]:
    """Return a list of human-readable errors; empty list means the record is valid."""
    errors: list[str] = []
    for field in required:
        if field not in record:
            errors.append(f"missing required field: {field}")
            continue
        entry = record[field]
        if not isinstance(entry, dict) or "value" not in entry:
            errors.append(f"{field}: entry must be an object containing a 'value'")
            continue
        value = entry["value"]
        spec = schema[field]
        if spec["type"] == "number":
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                errors.append(f"{field}: expected number, got {type(value).__name__}")
                continue
            if "min" in spec and value < spec["min"]:
                errors.append(f"{field}: {value} is below the minimum {spec['min']}")
            if "max" in spec and value > spec["max"]:
                errors.append(f"{field}: {value} is above the maximum {spec['max']}")
        elif spec["type"] == "string":
            if not isinstance(value, str):
                errors.append(f"{field}: expected string, got {type(value).__name__}")
                continue
            if "pattern" in spec and not re.search(spec["pattern"], value):
                errors.append(f"{field}: '{value}' does not match required pattern")
    return errors


def validate_or_raise(record: dict[str, dict]) -> dict[str, dict]:
    """Return the record unchanged if valid, otherwise raise ``SchemaError``."""
    errors = validate(record)
    if errors:
        raise SchemaError("; ".join(errors))
    return record


def _main() -> None:
    ap = argparse.ArgumentParser(description="Extract named numeric fields from a filing.")
    ap.add_argument("path", nargs="?", help="filing text file (defaults to the bundled filing)")
    args = ap.parse_args()
    text = open(args.path, encoding="utf-8").read() if args.path else load_filing_text()
    record = extract(text)
    errors = validate(record)
    print(json.dumps({"fields": record, "schema_errors": errors}, indent=2))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    _main()
