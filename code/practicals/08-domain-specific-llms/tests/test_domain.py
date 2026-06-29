from tools import domain, general
from tools._common import accuracy, load_sentences


def test_domain_classifier_runs_on_every_sentence():
    rows = load_sentences()
    preds = domain.predict_all(rows)
    assert len(preds) == len(rows)
    assert all(p in ("positive", "negative", "neutral") for p in preds)


def test_domain_reads_finance_terms_correctly():
    assert domain.classify_sentence("The company beat consensus estimates this quarter.") == "positive"
    assert domain.classify_sentence("Liability for deferred taxes remained unchanged.") == "neutral"
    assert domain.classify_sentence("The auditor flagged a goodwill impairment charge.") == "negative"


def test_term_general_misses_is_handled_by_domain():
    # 'headwinds' is absent from the general lexicon (scores neutral) but is correctly
    # negative in the domain lexicon — the core domain-adaptation payoff.
    s = "Management cited mounting headwinds across the European segment."
    assert "headwinds" not in general.LEXICON
    assert "headwinds" in domain.LEXICON
    assert general.classify_sentence(s) != "negative"
    assert domain.classify_sentence(s) == "negative"


def test_domain_accuracy_at_least_as_high_overall():
    rows = load_sentences()
    gold = [r["label"] for r in rows]
    assert accuracy(domain.predict_all(rows), gold) >= accuracy(general.predict_all(rows), gold)
