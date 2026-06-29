"""Closed-form mean-variance portfolio weights (NumPy linear algebra, deterministic).

Two fully-invested objectives, both with weights that sum to 1:

* min-variance  — the global minimum-variance portfolio
      w = Sigma^{-1} 1 / (1' Sigma^{-1} 1)
  Uses only the covariance matrix; expected returns are ignored.

* max-sharpe    — the tangency portfolio for a given risk-free rate rf
      w = Sigma^{-1} (mu - rf 1) / (1' Sigma^{-1} (mu - rf 1))
  Tilts toward assets with higher expected return per unit of risk.

These are the analytical optima; no solver, no randomness. The LLM picks the
objective and reads the weights — it never does the algebra.

CLI:
    python -m tools.optimize --objective min-variance
    python -m tools.optimize --objective max-sharpe --rf 0.02   # uses the text views for mu
"""
from __future__ import annotations

import argparse
import json

import numpy as np

from tools._common import load_market
from tools.views import build_views


def min_variance_weights(Sigma: np.ndarray) -> np.ndarray:
    """Global minimum-variance weights for covariance matrix ``Sigma`` (sum to 1)."""
    Sigma = np.asarray(Sigma, dtype=float)
    ones = np.ones(Sigma.shape[0])
    z = np.linalg.solve(Sigma, ones)
    return z / z.sum()


def max_sharpe_weights(mu: np.ndarray, Sigma: np.ndarray, rf: float = 0.0) -> np.ndarray:
    """Tangency (max-Sharpe) weights for excess returns ``mu - rf`` (sum to 1)."""
    mu = np.asarray(mu, dtype=float)
    Sigma = np.asarray(Sigma, dtype=float)
    excess = mu - rf
    z = np.linalg.solve(Sigma, excess)
    s = z.sum()
    if abs(s) < 1e-12:
        raise ValueError("degenerate tangency portfolio: excess-return weights sum to ~0")
    return z / s


def portfolio_stats(w: np.ndarray, mu: np.ndarray, Sigma: np.ndarray, rf: float = 0.0) -> dict:
    """Expected return, volatility and Sharpe of weights ``w`` under (mu, Sigma)."""
    w = np.asarray(w, dtype=float)
    ret = float(w @ mu)
    var = float(w @ Sigma @ w)
    vol = var ** 0.5
    sharpe = (ret - rf) / vol if vol > 0 else 0.0
    return {"expected_return": ret, "volatility": vol, "sharpe": sharpe}


def optimize(objective: str, market: dict | None = None, rf: float = 0.0):
    """Return ``(weights, mu, Sigma)`` for the chosen objective using the bundled data."""
    market = market or load_market()
    Sigma = market["covariance"]
    mu, _ = build_views(market)
    if objective == "min-variance":
        w = min_variance_weights(Sigma)
    elif objective == "max-sharpe":
        w = max_sharpe_weights(mu, Sigma, rf=rf)
    else:
        raise ValueError(f"unknown objective: {objective!r} (use 'min-variance' or 'max-sharpe')")
    return w, mu, Sigma


def _main() -> None:
    ap = argparse.ArgumentParser(description="Mean-variance optimal weights for the bundled assets.")
    ap.add_argument("--objective", choices=["min-variance", "max-sharpe"], default="max-sharpe")
    ap.add_argument("--rf", type=float, default=0.0, help="annual risk-free rate (max-sharpe only)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args()

    market = load_market()
    w, mu, Sigma = optimize(args.objective, market, rf=args.rf)
    stats = portfolio_stats(w, mu, Sigma, rf=args.rf)
    payload = {
        "objective": args.objective,
        "rf": args.rf,
        "assets": market["assets"],
        "weights": [round(float(x), 6) for x in w],
        "weights_sum": round(float(w.sum()), 6),
        "expected_return": round(stats["expected_return"], 6),
        "volatility": round(stats["volatility"], 6),
        "sharpe": round(stats["sharpe"], 6),
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(f"Objective: {args.objective}  (rf={args.rf})")
    for a, wi in zip(payload["assets"], payload["weights"]):
        print(f"  {a:<9} {wi:+.4f}")
    print(f"  {'sum':<9} {payload['weights_sum']:+.4f}")
    print(f"E[r]={payload['expected_return']:.4f}  vol={payload['volatility']:.4f}  Sharpe={payload['sharpe']:.4f}")


if __name__ == "__main__":
    _main()
