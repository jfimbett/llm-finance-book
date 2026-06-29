from tools.compare import compare


def test_both_classifiers_run_and_are_scored():
    r = compare()
    assert isinstance(r["general_accuracy"], float)
    assert isinstance(r["domain_accuracy"], float)
    assert 0.0 <= r["general_accuracy"] <= 1.0
    assert 0.0 <= r["domain_accuracy"] <= 1.0


def test_domain_beats_general_on_finance_text():
    r = compare()
    assert r["domain_accuracy"] > r["general_accuracy"]
    assert r["winner"] == "domain"
    assert r["margin"] > 0.0


def test_domain_wins_are_explained_by_finance_terms():
    r = compare()
    assert r["domain_wins"], "domain should win at least one sentence the general one missed"
    # every flipped sentence must carry at least one deciding term the lexicons disagree on
    for w in r["domain_wins"]:
        assert w["deciding_terms"]
        assert w["domain_pred"] == w["gold"]
        assert w["general_pred"] != w["gold"]
