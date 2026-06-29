"""A logistic-regression classifier trained by gradient descent (NumPy, deterministic).

No scikit-learn, no randomness: weights start at zero and full-batch gradient
descent drives them to a separating direction. On linearly separable text
features this converges to (near-)perfect training accuracy, and the learned
weight on each word is the signed strength of that word as an up/down signal.

CLI:
    python -m tools.model "Profit rose sharply and the board approved a buyback."
"""
from __future__ import annotations

import argparse

import numpy as np


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60.0, 60.0)))


class LogisticRegressionGD:
    """Binary logistic regression fit by full-batch gradient descent."""

    def __init__(self, *, lr: float = 0.5, n_iter: int = 3000, l2: float = 1e-4):
        self.lr = lr
        self.n_iter = n_iter
        self.l2 = l2
        self.weights_: np.ndarray = np.zeros(0)
        self.bias_: float = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LogisticRegressionGD":
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        n, d = X.shape
        self.weights_ = np.zeros(d)
        self.bias_ = 0.0
        for _ in range(self.n_iter):
            preds = _sigmoid(X @ self.weights_ + self.bias_)
            error = preds - y
            grad_w = (X.T @ error) / n + self.l2 * self.weights_
            grad_b = float(error.mean())
            self.weights_ -= self.lr * grad_w
            self.bias_ -= self.lr * grad_b
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        X = np.asarray(X, dtype=float)
        if self.weights_.size == 0:
            raise ValueError("call fit() before predict_proba()")
        return _sigmoid(X @ self.weights_ + self.bias_)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return (self.predict_proba(X) >= 0.5).astype(int)


def train_full() -> tuple["LogisticRegressionGD", object]:
    """Fit a vectoriser + classifier on the whole bundled dataset.

    Returns ``(model, vectorizer)`` for ad-hoc single-sentence prediction.
    """
    from tools._common import load_dataset
    from tools.features import TfidfVectorizer

    texts, labels = load_dataset()
    vec = TfidfVectorizer().fit(texts)
    X = vec.transform(texts)
    model = LogisticRegressionGD().fit(X, np.array(labels))
    return model, vec


def classify_text(text: str, model: "LogisticRegressionGD", vectorizer) -> tuple[int, float]:
    """Return ``(label, probability_of_up)`` for one sentence."""
    x = vectorizer.transform([text])
    prob = float(model.predict_proba(x)[0])
    return int(prob >= 0.5), prob


def _main() -> None:
    ap = argparse.ArgumentParser(description="Classify one sentence as an up (1) or down (0) signal.")
    ap.add_argument("text", help="a sentence to score")
    args = ap.parse_args()

    model, vec = train_full()
    label, prob = classify_text(args.text, model, vec)
    direction = "UP (1)" if label == 1 else "DOWN (0)"
    print(f"prediction: {direction}")
    print(f"P(up) = {prob:.3f}")


if __name__ == "__main__":
    _main()
