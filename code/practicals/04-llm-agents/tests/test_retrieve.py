from tools.retrieve import build_default_retriever


def test_customer_concentration_retrieves_risk_factors():
    r = build_default_retriever()
    hits = r.search("What is NovaCorp's customer concentration risk?", k=3)
    top_doc = hits[0][0].doc
    assert top_doc == "novacorp_10k_risk.txt", top_doc
    assert hits[0][1] > 0.0


def test_gross_margin_question_finds_margin_passage():
    r = build_default_retriever()
    hits = r.search("How did gross margin change year over year?", k=3)
    joined = " ".join(c.text.lower() for c, _ in hits)
    assert "gross margin" in joined
    assert "64%" in joined


def test_scores_are_sorted_descending():
    r = build_default_retriever()
    hits = r.search("foreign currency revenue in euros and pounds", k=5)
    scores = [s for _, s in hits]
    assert scores == sorted(scores, reverse=True)
