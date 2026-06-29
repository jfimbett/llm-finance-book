import montecarlo_dcf as mc

FIN = {"revenue": 1000.0, "da": 100.0, "capex": 50.0, "delta_nwc": 0.0,
       "total_debt": 0.0, "cash": 0.0, "shares": 100.0, "tax_rate": 0.0}

FIXED_CFG = {
    "years": 5,
    "revenue_growth": {"dist": "fixed", "value": 0.05},
    "operating_margin": {"dist": "fixed", "value": 0.20},
    "wacc": {"dist": "fixed", "value": 0.10},
    "terminal_growth": {"dist": "fixed", "value": 0.02},
    "tax_rate": 0.0,
}


def test_fixed_config_is_deterministic():
    out = mc.run_dcf(FIN, FIXED_CFG, seed=0, n=2000)
    # all draws identical -> band collapses to the point estimate
    assert abs(out["p10"] - out["p90"]) < 1e-6
    assert out["median"] > 0
    assert out["lane"] == "dcf"


def test_seed_reproducible():
    cfg = dict(FIXED_CFG, revenue_growth={"dist": "normal", "mean": 0.05, "sd": 0.02})
    a = mc.run_dcf(FIN, cfg, seed=42, n=3000)
    b = mc.run_dcf(FIN, cfg, seed=42, n=3000)
    assert a["median"] == b["median"]


def test_wacc_le_terminal_growth_is_guarded():
    cfg = dict(FIXED_CFG,
               wacc={"dist": "fixed", "value": 0.02},
               terminal_growth={"dist": "fixed", "value": 0.05})
    out = mc.run_dcf(FIN, cfg, seed=0, n=500)
    # guard prevents division blow-up -> finite, positive
    assert out["median"] > 0
