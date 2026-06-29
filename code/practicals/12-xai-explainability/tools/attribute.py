"""Exact additive feature attributions for the bundled credit model (numpy, offline).

For a linear / logistic model the prediction in log-odds space is
``f(x) = intercept + sum_i w_i * x_i``. Each feature's contribution relative to a
fixed baseline is

    phi_i = w_i * (x_i - baseline_i)

This is the *exact* SHAP value for a linear model (Lundberg & Lee, 2017): no
sampling, no approximation. By construction the attributions satisfy the
efficiency / additivity property

    sum_i phi_i = f(x) - f(baseline)

so they account for the entire gap between this applicant and the reference
applicant. The language model never runs this arithmetic; it only reads the
result and turns it into a notice.

CLI:
    python -m tools.attribute alice
    python -m tools.attribute data/applicants/bob.json
"""
from __future__ import annotations

import argparse
import json

import numpy as np

from tools._common import (
    applicant_vector,
    feature_arrays,
    load_applicant,
    load_model,
    sigmoid,
)


def attribute(model: dict, x: np.ndarray) -> dict:
    """Compute exact additive attributions of ``x`` against the model baseline."""
    feats = model["features"]
    keys, weights, baselines = feature_arrays(model)
    intercept = float(model["intercept"])
    threshold = float(model.get("decision_threshold", 0.5))

    phi = weights * (x - baselines)                       # exact linear SHAP
    logit = intercept + float(weights @ x)
    baseline_logit = intercept + float(weights @ baselines)
    prob = sigmoid(logit)
    decision = "approve" if prob >= threshold else "deny"

    contributions = [
        {
            "key": f["key"],
            "label": f["label"],
            "value": float(x[i]),
            "baseline": float(baselines[i]),
            "weight": float(weights[i]),
            "phi": float(phi[i]),
            "adverse_action_reason": f["adverse_action_reason"],
        }
        for i, f in enumerate(feats)
    ]
    # Most negative (creditworthiness-reducing) contribution first.
    contributions.sort(key=lambda c: c["phi"])

    return {
        "model": model["name"],
        "task": model["task"],
        "baseline_logit": baseline_logit,
        "baseline_prob": sigmoid(baseline_logit),
        "logit": logit,
        "prob": prob,
        "threshold": threshold,
        "decision": decision,
        "sum_phi": float(phi.sum()),
        "contributions": contributions,
    }


def attribute_applicant(name: str) -> dict:
    """Convenience: load model + applicant by name and attribute."""
    model = load_model()
    applicant = load_applicant(name)
    result = attribute(model, applicant_vector(model, applicant))
    result["applicant_id"] = applicant.get("applicant_id", name)
    result["requested"] = applicant.get("requested")
    return result


def top_negative(result: dict, k: int = 4) -> list[dict]:
    """The ``k`` features that most reduced the applicant's odds (phi < 0)."""
    return [c for c in result["contributions"] if c["phi"] < 0][:k]


def _main() -> None:
    ap = argparse.ArgumentParser(description="Attribute a credit decision to its features.")
    ap.add_argument("applicant", help="applicant name (e.g. alice) or path to a JSON file")
    args = ap.parse_args()
    print(json.dumps(attribute_applicant(args.applicant), indent=2))


if __name__ == "__main__":
    _main()
