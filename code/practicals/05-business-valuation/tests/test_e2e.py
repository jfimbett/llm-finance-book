import json
from pathlib import Path

import comps
import financials
import montecarlo_dcf as mc
import reconcile

FIX = Path(__file__).parent / "fixtures" / "companyfacts_TEST.json"


def test_full_chain_offline_produces_final_range():
    facts = json.loads(FIX.read_text())
    fin = financials.normalize(facts, ticker="TEST")

    cfg = {
        "years": 5,
        "revenue_growth": {"dist": "normal", "mean": 0.05, "sd": 0.02},
        "operating_margin": {"dist": "normal", "mean": 0.27, "sd": 0.03},
        "wacc": {"dist": "normal", "mean": 0.09, "sd": 0.01},
        "terminal_growth": {"dist": "normal", "mean": 0.025, "sd": 0.004},
        "tax_rate": fin["tax_rate"],
    }
    dcf = mc.run_dcf(fin, cfg, seed=7, n=3000)

    peer = dict(fin)  # one synthetic peer derived from the target
    multiples = [comps.peer_metrics(peer, price=12.0)]
    comps_res = comps.implied_values(fin, multiples, seed=7, n=3000)
    comps_res["source"] = "llm"

    final = reconcile.pool(dcf, [comps_res],
                           weights={"dcf": 0.6, "llm": 0.4}, seed=7, n=3000)

    assert final["median"] > 0
    assert final["p10"] <= final["median"] <= final["p90"]
    assert abs(sum(final["weights"].values()) - 1.0) < 1e-9
