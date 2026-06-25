import argparse

import numpy as np

from _common import data_dir, die, emit, read_json, write_json


def peer_metrics(fin, price):
    shares = float(fin["shares"])
    market_cap = price * shares
    ev = market_cap + float(fin.get("total_debt", 0.0)) - float(fin.get("cash", 0.0))
    ebitda = float(fin.get("ebitda") or (fin["ebit"] + fin["da"]))
    ni = float(fin.get("net_income", 0.0))
    return {
        "ev_ebitda": ev / ebitda if ebitda > 0 else None,
        "pe": market_cap / ni if ni > 0 else None,
    }


def implied_values(target, multiples, seed=0, n=10000):
    rng = np.random.default_rng(seed)
    evb = np.array([m["ev_ebitda"] for m in multiples if m.get("ev_ebitda") is not None], dtype=float)
    pe = np.array([m["pe"] for m in multiples if m.get("pe") is not None], dtype=float)
    if evb.size == 0 and pe.size == 0:
        die("no valid peer multiples to build comparables")
    shares = float(target["shares"])
    target_ebitda = float(target.get("ebitda") or (target["ebit"] + target["da"]))
    target_ni = float(target.get("net_income", 0.0))
    debt = float(target.get("total_debt", 0.0))
    cash = float(target.get("cash", 0.0))

    samples = np.empty(n)
    for i in range(n):
        vals = []
        if evb.size:
            ev = target_ebitda * rng.choice(evb)
            vals.append((ev - debt + cash) / shares)
        if pe.size and target_ni > 0:
            vals.append(rng.choice(pe) * target_ni / shares)
        samples[i] = np.mean(vals)
    samples = samples[np.isfinite(samples)]
    return {
        "median": float(np.median(samples)),
        "p10": float(np.percentile(samples, 10)),
        "p90": float(np.percentile(samples, 90)),
        "n": int(samples.size),
        "samples": samples.tolist(),
    }


def _peer_financials_and_price(ticker, tickers_map):
    import edgar_fetch
    import financials as fin_mod
    import market_price
    cik = edgar_fetch.resolve_cik(ticker, tickers_map)
    facts = edgar_fetch.fetch_company_facts(cik)
    fin = fin_mod.normalize(facts, ticker=ticker)
    price = market_price.get_price(ticker)["price"]
    return fin, price


def main():
    import edgar_fetch
    ap = argparse.ArgumentParser()
    ap.add_argument("--cik", required=True)
    ap.add_argument("--peers", required=True, help="comma-separated peer tickers")
    ap.add_argument("--source", default="llm", help="peer-source label (llm|embedding)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n", type=int, default=10000)
    a = ap.parse_args()

    target = read_json(data_dir(a.cik) / "financials.json")
    tickers_map = edgar_fetch.load_tickers_map()
    multiples, used = [], []
    for tk in [p.strip().upper() for p in a.peers.split(",") if p.strip()]:
        try:
            fin, price = _peer_financials_and_price(tk, tickers_map)
            multiples.append(peer_metrics(fin, price))
            used.append(tk)
        except SystemExit:
            continue
    if not multiples:
        die("no peer multiples could be computed (check peer tickers / network)")
    out = implied_values(target, multiples, a.seed, a.n)
    out["source"] = a.source
    out["peers"] = used
    write_json(data_dir(a.cik) / f"comps_{a.source}.json", out)
    emit({k: v for k, v in out.items() if k != "samples"})


if __name__ == "__main__":
    main()
