import reconcile


def test_pool_blends_two_lanes():
    dcf = {"lane": "dcf", "samples": [10.0] * 100}
    comps = {"source": "llm", "samples": [20.0] * 100}
    out = reconcile.pool(dcf, [comps], weights={"dcf": 0.5, "llm": 0.5}, seed=0, n=1000)
    # 50/50 blend of point masses at 10 and 20 -> median in [10, 20]
    assert 10.0 <= out["median"] <= 20.0
    assert out["p10"] == 10.0 and out["p90"] == 20.0


def test_pool_weight_skews_median():
    dcf = {"lane": "dcf", "samples": [10.0] * 100}
    comps = {"source": "llm", "samples": [20.0] * 100}
    heavy_dcf = reconcile.pool(dcf, [comps], {"dcf": 0.9, "llm": 0.1}, seed=0, n=1000)
    assert heavy_dcf["median"] == 10.0


def test_pool_normalizes_weights_and_reports_them():
    dcf = {"lane": "dcf", "samples": [10.0] * 50}
    comps = {"source": "llm", "samples": [20.0] * 50}
    out = reconcile.pool(dcf, [comps], {"dcf": 2.0, "llm": 2.0}, seed=0, n=400)
    assert abs(sum(out["weights"].values()) - 1.0) < 1e-9
