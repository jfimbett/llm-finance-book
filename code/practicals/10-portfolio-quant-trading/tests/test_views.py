import numpy as np

from tools._common import load_market
from tools.views import build_views, _tilt_for_view, TILT


def test_bullish_view_raises_and_bearish_lowers():
    market = load_market()
    base = market["expected_returns"]
    mu, breakdown = build_views(market)
    assets = market["assets"]

    # DELPHI carries a bullish note -> its expected return must rise above the base.
    j_delphi = assets.index("DELPHI")
    assert mu[j_delphi] > base[j_delphi]

    # BOREALIS carries a bearish note -> its expected return must fall below the base.
    j_borealis = assets.index("BOREALIS")
    assert mu[j_borealis] < base[j_borealis]


def test_neutral_and_uncovered_assets_keep_base_return():
    market = load_market()
    base = market["expected_returns"]
    mu, _ = build_views(market)
    assets = market["assets"]

    # EQUINOX has a neutral note; CYGNUS has no note at all -> both unchanged.
    assert np.isclose(mu[assets.index("EQUINOX")], base[assets.index("EQUINOX")])
    assert np.isclose(mu[assets.index("CYGNUS")], base[assets.index("CYGNUS")])


def test_tilt_counts_sentiment_keywords():
    assert np.isclose(_tilt_for_view("bullish, strong upside"), 3 * TILT)
    assert np.isclose(_tilt_for_view("bearish with downside risk"), -2 * TILT)
    assert np.isclose(_tilt_for_view("a neutral hold"), 0.0)
