"""Shared helpers: the transaction record, CSV loading, and the jurisdiction list.

Standard library plus NumPy only — no network, no external services.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TRANSACTIONS_CSV = DATA_DIR / "transactions.csv"
HIGH_RISK_JSON = DATA_DIR / "high_risk.json"

_DATE_FORMATS = ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d")


def _parse_date(raw: str) -> datetime:
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(raw.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"unrecognised date: {raw!r}")


@dataclass(frozen=True)
class Transaction:
    id: str
    dt: datetime
    amount: float
    origin_country: str
    dest_country: str
    account: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "Transaction":
        return cls(
            id=row["id"].strip(),
            dt=_parse_date(row["date"]),
            amount=float(row["amount"]),
            origin_country=row["origin_country"].strip().upper(),
            dest_country=row["dest_country"].strip().upper(),
            account=row["account"].strip(),
        )


def load_transactions(path: Path | str = TRANSACTIONS_CSV) -> list[Transaction]:
    """Read the bundled transactions CSV into a list of ``Transaction`` records."""
    with open(path, encoding="utf-8", newline="") as fh:
        return [Transaction.from_row(row) for row in csv.DictReader(fh)]


def load_high_risk(path: Path | str = HIGH_RISK_JSON) -> set[str]:
    """Return the set of high-risk jurisdiction codes from the bundled list."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {c.strip().upper() for c in data["codes"]}
