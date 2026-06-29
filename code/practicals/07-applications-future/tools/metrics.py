"""Look up a single figure from the bundled metrics table (stdlib only, offline).

The table (``data/metrics.csv``) holds one row per figure for the fictional company,
each with a value, a unit, the period, and the source document the figure comes from.
The agent never recites a number from memory; it calls this and quotes what comes back,
including the ``source`` so the brief stays grounded.

CLI:
    python -m tools.metrics "gross margin"
    python -m tools.metrics --list
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from tools._common import DATA_DIR

METRICS_CSV = DATA_DIR / "metrics.csv"

# Map the words a question is likely to use onto the canonical metric key in the table.
# Longer phrases are listed first so "gross margin" wins before bare "margin".
ALIASES: list[tuple[str, str]] = [
    ("revenue growth", "revenue_growth"),
    ("sales growth", "revenue_growth"),
    ("gross margin", "gross_margin"),
    ("operating margin", "operating_margin"),
    ("net income", "net_income"),
    ("earnings per share", "eps"),
    ("free cash flow", "free_cash_flow"),
    ("cash and equivalents", "cash_and_equivalents"),
    ("total debt", "total_debt"),
    ("research and development", "rd_expense"),
    ("revenue", "revenue"),
    ("sales", "revenue"),
    ("margin", "gross_margin"),
    ("earnings", "net_income"),
    ("profit", "net_income"),
    ("eps", "eps"),
    ("fcf", "free_cash_flow"),
    ("cash", "cash_and_equivalents"),
    ("debt", "total_debt"),
    ("r&d", "rd_expense"),
    ("headcount", "headcount"),
    ("employees", "headcount"),
    ("growth", "revenue_growth"),
]


def load_table(path: Path | str = METRICS_CSV) -> dict[str, dict]:
    """Return ``{metric_key: row}`` from the CSV."""
    with open(path, encoding="utf-8", newline="") as fh:
        return {row["metric"]: row for row in csv.DictReader(fh)}


def resolve_key(query: str) -> str | None:
    """Map a free-text metric name to a canonical key, or ``None`` if nothing matches."""
    q = query.lower().strip()
    table = load_table()
    if q in table:
        return q
    for phrase, key in ALIASES:
        if phrase in q:
            return key
    return None


def lookup(query: str, path: Path | str = METRICS_CSV) -> dict:
    """Look up *query* in the metrics table.

    Returns ``{"found": True, "metric", "value", "unit", "period", "source"}`` on a hit,
    or ``{"found": False, "query": ...}`` when no metric matches.
    """
    key = resolve_key(query)
    table = load_table(path)
    if key is None or key not in table:
        return {"found": False, "query": query}
    row = table[key]
    return {"found": True, **row}


def _main() -> None:
    ap = argparse.ArgumentParser(description="Look up a figure from the metrics table.")
    ap.add_argument("metric", nargs="?", help="metric name, e.g. 'gross margin'")
    ap.add_argument("--list", action="store_true", help="list every metric key in the table")
    args = ap.parse_args()
    if args.list or not args.metric:
        print(json.dumps(sorted(load_table()), indent=2))
        return
    print(json.dumps(lookup(args.metric), indent=2))


if __name__ == "__main__":
    _main()
