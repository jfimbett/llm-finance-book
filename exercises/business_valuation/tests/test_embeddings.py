import numpy as np

import embeddings


def fake_embed(texts):
    # deterministic 2-D vectors keyed by first character, L2-normalized
    out = []
    for t in texts:
        v = np.array([1.0, 0.0]) if t.startswith("a") else np.array([0.0, 1.0])
        out.append(v / np.linalg.norm(v))
    return np.array(out)


def test_build_index_shape():
    items = [{"ticker": "A", "cik": 1, "text": "apple alpha"},
             {"ticker": "B", "cik": 2, "text": "banana beta"}]
    vecs, kept = embeddings.build_index(items, embed=fake_embed)
    assert vecs.shape == (2, 2)
    assert kept[0]["ticker"] == "A"


def test_nearest_ranks_by_cosine_and_excludes_self():
    items = [{"ticker": "A", "cik": 1, "text": "apple"},
             {"ticker": "A2", "cik": 2, "text": "almond"},
             {"ticker": "B", "cik": 3, "text": "banana"}]
    vecs, kept = embeddings.build_index(items, embed=fake_embed)
    target = fake_embed(["apricot"])[0]   # also "a*" -> [1,0]
    out = embeddings.nearest(target, vecs, kept, k=2, exclude_cik=1)
    tickers = [o["ticker"] for o in out]
    assert "A" not in tickers          # excluded self
    assert tickers[0] == "A2"          # nearest remaining "a*" beats "b*"
