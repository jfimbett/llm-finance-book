import numpy as np

from tools._common import load_market
from tools.optimize import min_variance_weights, max_sharpe_weights, optimize


def test_weights_sum_to_one():
    market = load_market()
    for objective in ("min-variance", "max-sharpe"):
        w, _, _ = optimize(objective, market)
        assert np.isclose(w.sum(), 1.0), (objective, w.sum())


def test_min_variance_matches_closed_form_two_assets():
    # Known 2-asset global minimum-variance portfolio:
    #   w1 = (s2^2 - cov) / (s1^2 + s2^2 - 2 cov)
    s1, s2, cov = 0.04, 0.09, 0.01   # variances and covariance
    Sigma = np.array([[s1, cov], [cov, s2]])
    w = min_variance_weights(Sigma)
    w1 = (s2 - cov) / (s1 + s2 - 2 * cov)
    assert np.allclose(w, [w1, 1 - w1])
    assert np.isclose(w.sum(), 1.0)


def test_higher_expected_return_tilts_weight_toward_that_asset():
    # Raising one asset's expected return must raise its max-Sharpe weight.
    market = load_market()
    Sigma = market["covariance"]
    mu = market["expected_returns"].astype(float)
    base_w = max_sharpe_weights(mu, Sigma)

    bumped = mu.copy()
    bumped[3] += 0.05            # bullish view on asset index 3 (DELPHI)
    tilted_w = max_sharpe_weights(bumped, Sigma)

    assert tilted_w[3] > base_w[3]


def test_min_variance_ignores_expected_returns():
    # Min-variance depends only on Sigma, so changing mu must not move the weights.
    market = load_market()
    Sigma = market["covariance"]
    w_a = min_variance_weights(Sigma)
    market["expected_returns"] = market["expected_returns"] * 3.0
    w_b, _, _ = optimize("min-variance", market)
    assert np.allclose(w_a, w_b)
