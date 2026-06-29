"""Shared helpers: locate and load the bundled company fixtures. Stdlib only."""
from __future__ import annotations

import json
from pathlib import Path

COMPANIES_DIR = Path(__file__).resolve().parents[1] / "data" / "companies"

# Fields every fixture must provide, all in the same currency unit (USD millions).
REQUIRED_FIELDS = (
    "revenue",
    "ebitda",
    "total_debt",
    "interest_expense",
    "current_assets",
    "current_liabilities",
    "cash",
)


def list_companies(companies_dir: Path | str = COMPANIES_DIR) -> list[str]:
    """Return the available company slugs (the .json file stems), sorted."""
    companies_dir = Path(companies_dir)
    return sorted(p.stem for p in companies_dir.glob("*.json"))


def load_financials(company: str, companies_dir: Path | str = COMPANIES_DIR) -> dict:
    """Load one company's raw figures from ``data/companies/<company>.json``.

    Raises ``FileNotFoundError`` (listing the known companies) for an unknown slug
    and ``ValueError`` if a required figure is missing, so a typo fails loudly
    instead of silently producing a bogus ratio.
    """
    companies_dir = Path(companies_dir)
    path = companies_dir / f"{company.lower()}.json"
    if not path.exists():
        known = ", ".join(list_companies(companies_dir)) or "(none)"
        raise FileNotFoundError(f"unknown company '{company}'. Available: {known}")
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        raise ValueError(f"{path.name} is missing required fields: {', '.join(missing)}")
    return data
