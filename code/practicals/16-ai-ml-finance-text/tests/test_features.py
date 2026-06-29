import numpy as np

from tools._common import load_dataset
from tools.features import TfidfVectorizer


def test_matrix_shape_matches_texts_and_vocab():
    texts, _ = load_dataset()
    vec = TfidfVectorizer().fit(texts)
    X = vec.transform(texts)
    assert X.shape == (len(texts), len(vec.vocabulary_))
    assert len(vec.vocabulary_) > 0


def test_rows_are_l2_normalised():
    texts, _ = load_dataset()
    X = TfidfVectorizer().fit_transform(texts)
    norms = np.linalg.norm(X, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-9)


def test_transform_only_uses_fitted_vocabulary():
    vec = TfidfVectorizer().fit(["earnings surged and profit rose"])
    # an out-of-vocabulary sentence yields an all-zero row, never an error
    row = vec.transform(["zzz totally unseen tokens here"])
    assert row.shape == (1, len(vec.vocabulary_))
    assert np.count_nonzero(row) == 0
