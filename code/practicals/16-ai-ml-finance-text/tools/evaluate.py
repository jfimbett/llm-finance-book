"""Train/test the text-to-signal pipeline and report out-of-sample accuracy.

This is the end-to-end step: split the labelled corpus with a fixed seed, learn
the vocabulary and IDF on the training half only, fit the logistic-regression
classifier, then score the held-out half. The split is deterministic, so the
reported accuracy and confusion counts are reproducible.

CLI:
    python -m tools.evaluate                 # default split, prints accuracy
    python -m tools.evaluate --test-frac 0.3 --seed 42
"""
from __future__ import annotations

import argparse
import json
import random

import numpy as np

from tools._common import load_dataset
from tools.features import TfidfVectorizer
from tools.model import LogisticRegressionGD


def train_test_split(n: int, *, test_frac: float, seed: int) -> tuple[list[int], list[int]]:
    """Deterministic index split. Same (n, test_frac, seed) → same partition."""
    idx = list(range(n))
    random.Random(seed).shuffle(idx)
    n_test = max(1, round(n * test_frac))
    return idx[n_test:], idx[:n_test]


def confusion_counts(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, int]:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return {
        "tp": int(np.sum((y_pred == 1) & (y_true == 1))),
        "tn": int(np.sum((y_pred == 0) & (y_true == 0))),
        "fp": int(np.sum((y_pred == 1) & (y_true == 0))),
        "fn": int(np.sum((y_pred == 0) & (y_true == 1))),
    }


def run_pipeline(*, test_frac: float = 0.3, seed: int = 42) -> dict:
    """Vectorise → train → predict → score on a held-out split."""
    texts, labels = load_dataset()
    labels = np.array(labels)
    train_idx, test_idx = train_test_split(len(texts), test_frac=test_frac, seed=seed)

    train_texts = [texts[i] for i in train_idx]
    test_texts = [texts[i] for i in test_idx]
    y_train, y_test = labels[train_idx], labels[test_idx]

    vec = TfidfVectorizer().fit(train_texts)
    X_train, X_test = vec.transform(train_texts), vec.transform(test_texts)

    model = LogisticRegressionGD().fit(X_train, y_train)
    y_pred = model.predict(X_test)

    counts = confusion_counts(y_test, y_pred)
    accuracy = float(np.mean(y_pred == y_test))
    return {
        "accuracy": round(accuracy, 4),
        "n_train": len(train_idx),
        "n_test": len(test_idx),
        "vocab_size": len(vec.vocabulary_),
        "confusion": counts,
    }


def _main() -> None:
    ap = argparse.ArgumentParser(description="Evaluate the text-to-signal pipeline out of sample.")
    ap.add_argument("--test-frac", type=float, default=0.3)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    report = run_pipeline(test_frac=args.test_frac, seed=args.seed)
    print(f"out-of-sample accuracy: {report['accuracy']:.3f} "
          f"({report['n_train']} train / {report['n_test']} test)")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    _main()
