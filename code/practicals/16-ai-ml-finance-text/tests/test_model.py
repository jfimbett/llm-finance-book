import numpy as np

from tools.features import TfidfVectorizer
from tools.model import LogisticRegressionGD, classify_text, train_full


def test_probabilities_stay_in_unit_interval():
    X = np.array([[0.0, 1.0], [1.0, 0.0], [0.5, 0.5]])
    y = np.array([1, 0, 1])
    model = LogisticRegressionGD(n_iter=200).fit(X, y)
    p = model.predict_proba(X)
    assert np.all(p >= 0.0) and np.all(p <= 1.0)


def test_learns_a_linearly_separable_toy_set():
    texts = [
        "gains gains gains", "profit profit", "growth gains profit",
        "loss loss loss", "decline decline", "loss decline weak",
    ]
    y = np.array([1, 1, 1, 0, 0, 0])
    vec = TfidfVectorizer().fit(texts)
    model = LogisticRegressionGD().fit(vec.transform(texts), y)
    preds = model.predict(vec.transform(texts))
    assert np.array_equal(preds, y)


def test_clearly_positive_sentence_predicts_up():
    model, vec = train_full()
    label, prob = classify_text(
        "Earnings beat expectations and revenue surged to a record high.", model, vec
    )
    assert label == 1
    assert prob > 0.5
