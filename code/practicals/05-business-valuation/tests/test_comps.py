import comps

TARGET = {"ebit": 300.0, "da": 90.0, "ebitda": 390.0, "net_income": 240.0,
          "shares": 100.0, "total_debt": 400.0, "cash": 200.0}


def test_peer_metrics_basic():
    fin = {"shares": 50.0, "total_debt": 100.0, "cash": 50.0,
           "ebitda": 200.0, "net_income": 120.0, "ebit": 150.0, "da": 50.0}
    m = comps.peer_metrics(fin, price=20.0)
    # market_cap = 20*50 = 1000 ; ev = 1000 + 100 - 50 = 1050
    assert abs(m["ev_ebitda"] - 1050 / 200) < 1e-9
    # pe = 1000 / 120
    assert abs(m["pe"] - 1000 / 120) < 1e-9


def test_implied_values_within_peer_range():
    multiples = [{"ev_ebitda": 5.0, "pe": 4.0}, {"ev_ebitda": 7.0, "pe": 6.0}]
    out = comps.implied_values(TARGET, multiples, seed=1, n=4000)
    assert out["p10"] <= out["median"] <= out["p90"]
    assert out["median"] > 0


def test_implied_values_no_valid_multiples_dies():
    import pytest
    with pytest.raises(SystemExit):
        comps.implied_values(TARGET, [{"ev_ebitda": None, "pe": None}], seed=0, n=10)


def test_implied_values_skips_pe_for_loss_making_target():
    target = dict(TARGET, net_income=-50.0)
    multiples = [{"ev_ebitda": 6.0, "pe": 5.0}]
    out = comps.implied_values(target, multiples, seed=1, n=2000)
    # P/E arm skipped (net_income <= 0); only EV/EBITDA arm:
    # implied_ev = ebitda*6 = 390*6 = 2340; equity/share = (2340 - 400 + 200)/100 = 21.4
    assert abs(out["median"] - 21.4) < 1e-6
