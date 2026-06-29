"""Verify that an attribution actually reconstructs the model — the additivity gate.

A feature attribution is only trustworthy if it satisfies the efficiency property

    sum_i phi_i + f(baseline) == f(x)

If that identity fails, the explanation does not faithfully decompose the model and
must not be turned into an adverse-action notice. This tool reduces "is the
explanation faithful?" to a single reproducible number — the residual gap.

CLI:
    python -m tools.check alice
    python -m tools.check --attribution reports/_attribution.json
"""
from __future__ import annotations

import argparse
import json

from tools.attribute import attribute_applicant

TOL = 1e-9


def check_additivity(result: dict, tol: float = TOL) -> dict:
    """Compare ``sum(phi) + baseline_logit`` against the model's own ``f(x)``."""
    reconstructed = result["sum_phi"] + result["baseline_logit"]
    gap = abs(reconstructed - result["logit"])
    return {
        "sum_phi": result["sum_phi"],
        "baseline_logit": result["baseline_logit"],
        "reconstructed_logit": reconstructed,
        "model_logit": result["logit"],
        "gap": gap,
        "tolerance": tol,
        "ok": gap <= tol,
    }


def _main() -> None:
    ap = argparse.ArgumentParser(description="Check additivity of an attribution.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("applicant", nargs="?", help="applicant name or path to a JSON file")
    src.add_argument("--attribution", help="path to JSON emitted by tools.attribute")
    args = ap.parse_args()
    if args.attribution:
        result = json.load(open(args.attribution, encoding="utf-8"))
    else:
        result = attribute_applicant(args.applicant)
    print(json.dumps(check_additivity(result), indent=2))


if __name__ == "__main__":
    _main()
