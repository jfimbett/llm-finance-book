from tools import general
from tools._common import load_sentences


def test_general_classifier_runs_on_every_sentence():
    rows = load_sentences()
    preds = general.predict_all(rows)
    assert len(preds) == len(rows)
    assert all(p in ("positive", "negative", "neutral") for p in preds)


def test_general_inverts_finance_polarity_on_beat():
    # 'beat' = beat estimates (positive) in finance, but the general lexicon scores it
    # negative, so it must get this gold-positive sentence wrong.
    s = "The company beat consensus estimates this quarter."
    assert general.classify_sentence(s) != "positive"


def test_general_misreads_liability_as_negative():
    # A balance-sheet 'liability' is neutral, but general English treats it as a burden.
    s = "Liability for deferred taxes remained unchanged."
    assert general.classify_sentence(s) == "negative"
