"""Backtest a fixed weight vector against the bundled return series (deterministic).

Applies buy-and-hold weights to every period of ``data/market.json['returns']``:

    portfolio return  p_t   = R_t . w
    cumulative return       = prod(1 + p_t) - 1
    Sharpe (annualised)     = mean(p_t) / std(p_t) * sqrt(periods_per_year)

No rebalancing, no costs, no randomness — same weights and fixture give the same
numbers every time. The LLM reads these numbers; it never computes them.

CLI:
    python -m tools.backtest --objective max-sharpe        # optimise, then backtest
    python -m tools.backtest --weights 0.2 0.2 0.2 0.2 0.2 # backtest given weights
"""
from __future__ import annotations

import argparse
import json

import numpy as np

from tools._common import load_market
from tools.optimize import optimize


def backtest(weights: np.ndarray, returns: np.ndarray, periods_per_year: int = 12) -> dict:
    """Buy-and-hold backtest of ``weights`` over the ``returns`` matrix (T periods x N assets)."""
    w = np.asarray(weights, dtype=float)
    R = np.asarray(returns, dtype=float)
    port = R @ w
    cumulative = float(np.prod(1.0 + port) - 1.0)
    mean = float(port.mean())
    std = float(port.std(ddof=1))
    sharpe = float(mean / std * np.sqrt(periods_per_year)) if std > 0 else 0.0
    return {
        "periods": int(R.shape[0]),
        "cumulative_return": cumulative,
        "mean_period_return": mean,
        "volatility": std,
        "sharpe": sharpe,
    }


def _main() -> None:
    ap = argparse.ArgumentParser(description="Backtest portfolio weights on the bundled return series.")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--objective", choices=["min-variance", "max-sharpe"],
                     help="optimise weights first, then backtest them")
    src.add_argument("--weights", nargs="+", type=float, help="explicit weights (must sum to ~1)")
    ap.add_argument("--rf", type=float, default=0.0, help="annual risk-free rate (max-sharpe only)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args()

    market = load_market()
    assets = market["assets"]
    if args.weights is not None:
        if len(args.weights) != len(assets):
            ap.error(f"expected {len(assets)} weights, got {len(args.weights)}")
        w = np.asarray(args.weights, dtype=float)
    else:
        objective = args.objective or "max-sharpe"
        w, _, _ = optimize(objective, market, rf=args.rf)

    result = backtest(w, market["returns"], market["periods_per_year"])
    payload = {
        "assets": assets,
        "weights": [round(float(x), 6) for x in w],
        "periods": result["periods"],
        "cumulative_return": round(result["cumulative_return"], 6),
        "mean_period_return": round(result["mean_period_return"], 6),
        "volatility": round(result["volatility"], 6),
        "sharpe": round(result["sharpe"], 6),
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print("Weights:")
    for a, wi in zip(assets, payload["weights"]):
        print(f"  {a:<9} {wi:+.4f}")
    print(f"Backtest over {payload['periods']} periods:")
    print(f"  cumulative return = {payload['cumulative_return']:+.4f}")
    print(f"  Sharpe (annual)   = {payload['sharpe']:+.4f}")


if __name__ == "__main__":
    _main()
