#!/usr/bin/env python3
"""
Test the call-option / put-option analogy across several embedding backends and
compare them to plain GloVe.  Backends:

  st:<model>   local sentence-transformers model (default: a finance-tuned one)
  openai       commercial OpenAI text-embedding-3-large   (needs OPENAI_API_KEY)
  voyage       commercial Voyage voyage-finance-2          (needs VOYAGE_API_KEY)

Reads API keys from <repo>/.env if present.  Reports, for each backend:
  * cos(call option, put option)                      -- raw similarity
  * analogy = call - upside + downside : nearest finance term + parallelogram cos
  * the classic king - man + woman analogy as a sanity control

Usage:
  conda run -n llm-finance python analogy_backends.py st:FinLang/finance-embeddings-investopedia
  conda run -n llm-finance python analogy_backends.py openai
  conda run -n llm-finance python analogy_backends.py voyage
"""

import os
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]


def load_dotenv():
    env = REPO_ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def unit(v):
    v = np.asarray(v, dtype=float)
    return v / (np.linalg.norm(v) + 1e-12)


def cos(a, b):
    return float(np.dot(unit(a), unit(b)))


# ── Embedding backends: each returns a function  texts -> np.ndarray[n, d] ─────
def get_embedder(backend):
    if backend.startswith("st:") or backend == "st":
        from sentence_transformers import SentenceTransformer

        name = backend.split(":", 1)[1] if ":" in backend else \
            "FinLang/finance-embeddings-investopedia"
        print(f"[st] loading {name} …", flush=True)
        model = SentenceTransformer(name)
        return lambda texts: np.asarray(model.encode(texts, normalize_embeddings=False)), name

    if backend == "openai":
        from openai import OpenAI

        name = os.environ.get("OPENAI_EMBED_MODEL", "text-embedding-3-large")
        client = OpenAI()
        print(f"[openai] using {name}", flush=True)

        def embed(texts):
            resp = client.embeddings.create(model=name, input=list(texts))
            return np.asarray([d.embedding for d in resp.data])

        return embed, name

    if backend == "voyage":
        import voyageai

        name = os.environ.get("VOYAGE_EMBED_MODEL", "voyage-finance-2")
        client = voyageai.Client()
        print(f"[voyage] using {name}", flush=True)

        def embed(texts):
            r = client.embed(list(texts), model=name, input_type="document")
            return np.asarray(r.embeddings)

        return embed, name

    raise SystemExit(f"unknown backend {backend!r}")


def main():
    load_dotenv()
    backend = sys.argv[1] if len(sys.argv) > 1 else \
        "st:FinLang/finance-embeddings-investopedia"
    embed, name = get_embedder(backend)

    # One batched call keeps commercial cost/latency low.
    vocab = [
        "call option", "put option", "upside", "downside",          # 0-3 analogy
        "king", "man", "woman", "queen",                            # 4-7 control
        "warrant", "futures", "forward", "swap", "hedge",           # finance shortlist
        "derivative", "premium", "strike", "volatility", "bond",
    ]
    E = embed(vocab)
    V = {w: E[i] for i, w in enumerate(vocab)}

    print(f"\n=== backend: {backend}  ({name})  dim={E.shape[1]} ===")

    # Raw similarity that better embeddings should get right.
    print(f"cos(call option, put option) = {cos(V['call option'], V['put option']):.3f}")
    print(f"cos(upside, downside)        = {cos(V['upside'], V['downside']):.3f}")

    # Control analogy.
    rk = unit(V["king"]) - unit(V["man"]) + unit(V["woman"])
    print(f"\n[control] king-man+woman: cos(result, queen) = {cos(rk, V['queen']):.3f}"
          f"  parallelogram cos(king-queen, man-woman) = "
          f"{cos(V['king'] - V['queen'], V['man'] - V['woman']):+.3f}")

    # Finance analogy (unit-normalised arithmetic, as for GloVe).
    r = unit(V["call option"]) - unit(V["upside"]) + unit(V["downside"])
    shortlist = ["put option", "warrant", "futures", "forward", "swap", "hedge",
                 "derivative", "premium", "strike", "volatility", "bond"]
    ranked = sorted(((w, cos(r, V[w])) for w in shortlist), key=lambda x: -x[1])
    para = cos(V["call option"] - V["put option"], V["upside"] - V["downside"])
    print(f"\n[finance] call option - upside + downside ≈ ?")
    for w, s in ranked[:6]:
        tag = "  <-- target" if w == "put option" else ""
        print(f"    {w:<12} {s:.3f}{tag}")
    print(f"  cos(result, put option)  = {cos(r, V['put option']):.3f}")
    print(f"  cos(result, call option) = {cos(r, V['call option']):.3f}  (source bleed)")
    print(f"  parallelogram cos(call-put, upside-downside) = {para:+.3f}")
    rank = next((i + 1 for i, (w, _) in enumerate(ranked) if w == "put option"), None)
    print(f"  'put option' rank in finance shortlist: {rank}/{len(shortlist)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
