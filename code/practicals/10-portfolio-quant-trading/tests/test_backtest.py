import numpy as np

from tools._common import load_market
from tools.backtest import backtest


def test_equal_weight_backtest_reproduces_on_fixture():
    market = load_market()
    w = np.full(len(market["assets"]), 1.0 / len(market["assets"]))
    result = backtest(w, market["returns"], market["periods_per_year"])
    assert result["periods"] == 24
    # Deterministic values pinned to the bundled return series.
    assert np.isclose(result["cumulative_return"], -0.062101, atol=1e-6)
    assert np.isclose(result["sharpe"], -0.272849, atol=1e-6)


def test_backtest_matches_manual_computation():
    market = load_market()
    R = market["returns"]
    w = np.array([0.3, 0.1, 0.1, 0.3, 0.2])
    result = backtest(w, R, 12)

    port = R @ w
    expected_cum = float(np.prod(1.0 + port) - 1.0)
    expected_sharpe = float(port.mean() / port.std(ddof=1) * np.sqrt(12))
    assert np.isclose(result["cumulative_return"], expected_cum)
    assert np.isclose(result["sharpe"], expected_sharpe)


def test_single_asset_cumulative_return_is_compounded_series():
    market = load_market()
    R = market["returns"]
    w = np.array([1.0, 0.0, 0.0, 0.0, 0.0])   # hold only the first asset
    result = backtest(w, R, 12)
    expected = float(np.prod(1.0 + R[:, 0]) - 1.0)
    assert np.isclose(result["cumulative_return"], expected)
