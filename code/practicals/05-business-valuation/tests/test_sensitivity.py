import sensitivity


FIN = {
    "revenue": 1000.0, "da": 50.0, "capex": 40.0, "delta_nwc": 10.0,
    "total_debt": 100.0, "cash": 80.0, "shares": 100.0, "tax_rate": 0.21,
}
CFG = {
    "revenue_growth": {"dist": "fixed", "value": 0.05},
    "operating_margin": {"dist": "fixed", "value": 0.25},
    "wacc": {"dist": "normal", "mean": 0.09, "sd": 0.015},
    "terminal_growth": {"dist": "normal", "mean": 0.025, "sd": 0.01},
    "years": 5,
}


def test_central_extracts_point_of_each_dist():
    assert sensitivity.central({"dist": "fixed", "value": 0.07}) == 0.07
    assert sensitivity.central({"dist": "normal", "mean": 0.09}) == 0.09
    assert sensitivity.central({"dist": "uniform", "low": 0.02, "high": 0.04}) == 0.03


def test_grid_shape_matches_axes():
    out = sensitivity.grid(FIN, CFG, wacc_steps=7, tg_steps=5)
    assert len(out["wacc_axis"]) == 7 and len(out["tg_axis"]) == 5
    assert len(out["grid"]) == 7 and all(len(r) == 5 for r in out["grid"])


def test_cells_where_growth_exceeds_wacc_are_null():
    # force axes that include a g >= WACC cell
    out = sensitivity.grid(FIN, CFG,
                           wacc_axis=[0.03, 0.10], tg_axis=[0.02, 0.05])
    # wacc=0.03, tg=0.05 -> tg >= wacc -> None
    assert out["grid"][0][1] is None
    # wacc=0.10, tg=0.02 -> valid, positive
    assert out["grid"][1][0] is not None and out["grid"][1][0] > 0


def test_value_falls_as_wacc_rises():
    out = sensitivity.grid(FIN, CFG,
                           wacc_axis=[0.08, 0.12], tg_axis=[0.025])
    assert out["grid"][0][0] > out["grid"][1][0]


def test_base_per_share_reported_and_positive():
    out = sensitivity.grid(FIN, CFG)
    assert out["base"]["per_share"] > 0
    assert out["base"]["wacc"] == 0.09 and out["base"]["terminal_growth"] == 0.025
