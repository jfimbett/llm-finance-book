import argparse

import numpy as np

import edgar_fetch
from _common import DATA_ROOT, cik_pad, data_dir, die, emit, write_json

_MODEL = None


def _default_embed(texts):
    global _MODEL
    from sentence_transformers import SentenceTransformer
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return np.asarray(_MODEL.encode(list(texts), normalize_embeddings=True))


def build_index(items, embed=_default_embed):
    texts = [it["text"] for it in items]
    vecs = np.asarray(embed(texts))
    return vecs, items


def nearest(target_vec, vecs, items, k=8, exclude_cik=None):
    sims = vecs @ np.asarray(target_vec)
    out = []
    for i in np.argsort(-sims):
        if exclude_cik is not None and cik_pad(items[i]["cik"]) == cik_pad(exclude_cik):
            continue
        out.append({"ticker": items[i]["ticker"],
                    "cik": cik_pad(items[i]["cik"]),
                    "score": float(sims[i])})
        if len(out) >= k:
            break
    return out


def _load_universe(path):
    with open(path) as fh:
        return [ln.strip().upper() for ln in fh if ln.strip()]


def _build_universe_index(universe_tickers, tickers_map, rebuild=False):
    cache = DATA_ROOT / "embed_index.npz"
    if cache.exists() and not rebuild:
        z = np.load(cache, allow_pickle=True)
        return z["vecs"], [dict(d) for d in z["items"]]
    items = []
    for tk in universe_tickers:
        try:
            cik = edgar_fetch.resolve_cik(tk, tickers_map)
            text = edgar_fetch.fetch_narrative(cik)
        except SystemExit:
            continue
        items.append({"ticker": tk, "cik": cik, "text": text[:20000]})
    if not items:
        die("could not build embedding universe (no narratives fetched)")
    vecs, items = build_index(items)
    np.savez(cache, vecs=vecs, items=np.array(items, dtype=object))
    return vecs, items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cik", required=True)
    ap.add_argument("--universe", default="universe.txt")
    ap.add_argument("--top-k", type=int, default=8)
    ap.add_argument("--rebuild", action="store_true")
    a = ap.parse_args()

    tickers_map = edgar_fetch.load_tickers_map()
    universe = _load_universe(a.universe)
    vecs, items = _build_universe_index(universe, tickers_map, a.rebuild)

    narrative_path = data_dir(a.cik) / "narrative.txt"
    if not narrative_path.exists():
        die(f"{narrative_path} not found — run edgar_fetch.py first")
    target_vec = build_index([{"ticker": "TARGET", "cik": a.cik,
                               "text": narrative_path.read_text()[:20000]}])[0][0]
    peers = nearest(target_vec, vecs, items, k=a.top_k, exclude_cik=a.cik)
    out = {"cik": cik_pad(a.cik), "source": "embedding", "peers": peers}
    write_json(data_dir(a.cik) / "embed_peers.json", out)
    emit(out)


if __name__ == "__main__":
    main()
