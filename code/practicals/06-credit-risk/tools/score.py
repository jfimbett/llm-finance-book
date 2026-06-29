"""Transparent rule-based default-risk score from a company's credit ratios.

The score is a weighted blend of three sub-scores, each in [0, 1] and each
*monotone in risk*: a more leveraged, less-covered, or less-liquid company always
scores at least as high. Because every sub-score moves the right way, a company
that is strictly weaker on every input is guaranteed a strictly higher score —
there is no black box and nothing the agent has to take on faith.

Sub-scores (0 = safe, 1 = maximal concern):
  leverage   net debt / EBITDA, 0x -> 0.0, >= 8x -> 1.0      (weight 0.40)
  coverage   EBITDA / interest, >= 8x -> 0.0, 0x -> 1.0      (weight 0.35)
  liquidity  current ratio,     >= 2.0 -> 0.0, 0 -> 1.0      (weight 0.25)

A company with no interest expense carries no coverage risk; one with no current
liabilities carries no liquidity risk; one with no EBITDA to service debt is pinned
to maximal leverage and coverage risk.

CLI:
    python -m tools.score aurora
"""
from __future__ import annotations

import argparse
import json

import numpy as np

from tools._common import load_financials
from tools.ratios import compute_ratios

# Thresholds at which a dimension is considered safe / maximally risky.
LEV_CAP = 8.0       # net debt / EBITDA at or above this is maximal leverage risk
COV_FLOOR = 8.0     # EBITDA / interest at or above this is fully covered
LIQ_TARGET = 2.0    # current ratio at or above this is comfortably liquid

WEIGHTS = {"leverage": 0.40, "coverage": 0.35, "liquidity": 0.25}

# Score bands -> default-risk flag.
BANDS = ((25.0, "LOW"), (55.0, "MEDIUM"), (float("inf"), "HIGH"))


def _clip01(x: float) -> float:
    return float(np.clip(x, 0.0, 1.0))


def risk_components(fin: dict) -> dict[str, float]:
    """The three monotone-in-risk sub-scores for a company."""
    r = compute_ratios(fin)
    ebitda = fin["ebitda"]
    interest = fin["interest_expense"]
    current_liabilities = fin["current_liabilities"]

    if ebitda <= 0:
        leverage_risk = 1.0            # no earnings to service debt
    else:
        leverage_risk = _clip01(r["net_leverage"] / LEV_CAP)

    if interest == 0:
        coverage_risk = 0.0            # no interest burden to cover
    elif ebitda <= 0:
        coverage_risk = 1.0            # negative coverage
    else:
        coverage_risk = _clip01((COV_FLOOR - r["interest_coverage"]) / COV_FLOOR)

    if current_liabilities == 0:
        liquidity_risk = 0.0           # no near-term obligations
    else:
        liquidity_risk = _clip01((LIQ_TARGET - r["current_ratio"]) / LIQ_TARGET)

    return {
        "leverage": round(leverage_risk, 4),
        "coverage": round(coverage_risk, 4),
        "liquidity": round(liquidity_risk, 4),
    }


def _flag(score: float) -> str:
    for cutoff, label in BANDS:
        if score < cutoff:
            return label
    return "HIGH"


def score_company(fin: dict) -> dict:
    """Combine the sub-scores into a 0-100 risk score and a default-risk flag."""
    comp = risk_components(fin)
    keys = list(WEIGHTS)
    blended = float(np.average([comp[k] for k in keys], weights=[WEIGHTS[k] for k in keys]))
    score = round(100.0 * blended, 1)
    flag = _flag(score)
    return {
        "company": fin.get("company"),
        "name": fin.get("name"),
        "risk_score": score,          # 0 (safest) .. 100 (most distressed)
        "risk_flag": flag,            # LOW | MEDIUM | HIGH
        "default_risk": flag == "HIGH",
        "components": comp,
        "weights": WEIGHTS,
    }


def score_for(company: str) -> dict:
    return score_company(load_financials(company))


def _main() -> None:
    ap = argparse.ArgumentParser(description="Score a company's default risk from its ratios.")
    ap.add_argument("company", help="company slug, e.g. aurora")
    args = ap.parse_args()
    print(json.dumps(score_for(args.company), indent=2))


if __name__ == "__main__":
    _main()
