from tools.retrieve import build_retriever


def test_partnership_question_retrieves_partnership_news():
    r = build_retriever("news")
    hits = r.search("autonomous warehouse partnership with a logistics operator", k=2)
    assert hits[0][0] == "meridian_partnership.txt", hits[0][0]
    assert hits[0][2] > 0.0


def test_risk_question_retrieves_risk_factors_filing():
    r = build_retriever("filings")
    hits = r.search("customer concentration and supply chain risk", k=2)
    assert hits[0][0] == "meridian_10k_risk.txt", hits[0][0]


def test_source_filter_excludes_other_sources():
    ids = {sid for sid, _, _ in build_retriever("news").search("revenue", k=10)}
    assert all(i in {"meridian_partnership.txt", "meridian_recall.txt"} for i in ids)


def test_scores_are_sorted_descending():
    hits = build_retriever("all").search("gross margin and revenue growth", k=4)
    scores = [s for _, _, s in hits]
    assert scores == sorted(scores, reverse=True)
