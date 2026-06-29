"""Credit ratios from a company's raw figures (deterministic, offline).

Every number a credit memo cites comes from here, not from the language model.
Ratios that divide by zero (no interest expense, no current liabilities, no debt)
return ``null`` rather than a bogus or infinite figure; ``score.py`` and the memo
treat ``null`` as "no burden on that dimension".

CLI:
    python -m tools.ratios aurora
"""
from __future__ import annotations

import argparse
import json

from tools._common import load_financials


def _ratio(numerator: float, denominator: float) -> float | None:
    """Divide, or return ``None`` when the denominator is zero (undefined ratio)."""
    if denominator == 0:
        return None
    return numerator / denominator


def compute_ratios(fin: dict) -> dict:
    """Standard credit ratios. Net debt = total debt minus cash."""
    ebitda = fin["ebitda"]
    debt = fin["total_debt"]
    cash = fin["cash"]
    net_debt = debt - cash

    leverage = _ratio(debt, ebitda)                       # gross debt / EBITDA  (lower is safer)
    net_leverage = _ratio(net_debt, ebitda)               # net debt / EBITDA    (lower is safer)
    interest_coverage = _ratio(ebitda, fin["interest_expense"])  # EBITDA / interest (higher is safer)
    current_ratio = _ratio(fin["current_assets"], fin["current_liabilities"])  # (higher is safer)
    cash_to_debt = _ratio(cash, debt)                     # cash / total debt    (higher is safer)

    def _round(x: float | None) -> float | None:
        return None if x is None else round(x, 3)

    return {
        "company": fin.get("company"),
        "name": fin.get("name"),
        "net_debt": net_debt,
        "leverage": _round(leverage),
        "net_leverage": _round(net_leverage),
        "interest_coverage": _round(interest_coverage),
        "current_ratio": _round(current_ratio),
        "cash_to_debt": _round(cash_to_debt),
    }


def ratios_for(company: str) -> dict:
    return compute_ratios(load_financials(company))


def _main() -> None:
    ap = argparse.ArgumentParser(description="Compute credit ratios for a bundled company.")
    ap.add_argument("company", help="company slug, e.g. aurora")
    args = ap.parse_args()
    print(json.dumps(ratios_for(args.company), indent=2))


if __name__ == "__main__":
    _main()
