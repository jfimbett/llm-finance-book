"""Score candidate answers against a gold finance QA set (exact-match + token-F1).

Two reproducible numbers per item that replace "grade it by hand":

* exact_match — 1 if the normalised candidate equals the normalised gold answer.
* f1 — SQuAD-style token-level F1 between candidate and gold (partial credit).

An item counts as *correct* when it is an exact match. Accuracy is the share of
correct items; mean_f1 is the average token-F1. The agent never computes these —
it reads them.

CLI:
    python -m tools.score --gold data/gold.json --pred data/candidates_overconfident.json
    python -m tools.score --pred data/candidates_calibrated.json --out reports/_scored.json
"""
from __future__ import annotations

import argparse
import json
from collections import Counter

from tools._common import load_gold, load_predictions, normalize, tokens


def exact_match(candidate: str, gold: str) -> int:
    """1 if candidate and gold are equal after normalisation, else 0."""
    return int(normalize(candidate) == normalize(gold))


def token_f1(candidate: str, gold: str) -> float:
    """SQuAD-style token-level F1 in [0, 1].

    Returns 1.0 when both answers are empty, 0.0 when exactly one is empty.
    """
    cand_t, gold_t = tokens(candidate), tokens(gold)
    if not cand_t and not gold_t:
        return 1.0
    if not cand_t or not gold_t:
        return 0.0
    overlap = sum((Counter(cand_t) & Counter(gold_t)).values())
    if overlap == 0:
        return 0.0
    precision = overlap / len(cand_t)
    recall = overlap / len(gold_t)
    return 2 * precision * recall / (precision + recall)


def score_dataset(gold: dict[str, dict], preds: dict[str, dict]) -> dict:
    """Score every gold item against its prediction (missing prediction = empty answer)."""
    items = []
    for qid, g in gold.items():
        pred = preds.get(qid, {})
        candidate = pred.get("answer", "")
        em = exact_match(candidate, g["answer"])
        items.append({
            "id": qid,
            "question": g["question"],
            "gold": g["answer"],
            "candidate": candidate,
            "confidence": pred.get("confidence"),
            "exact_match": em,
            "f1": round(token_f1(candidate, g["answer"]), 4),
            "correct": bool(em),
        })
    n = len(items)
    accuracy = sum(i["exact_match"] for i in items) / n if n else 0.0
    mean_f1 = sum(i["f1"] for i in items) / n if n else 0.0
    return {
        "n": n,
        "n_correct": sum(i["exact_match"] for i in items),
        "accuracy": round(accuracy, 4),
        "mean_f1": round(mean_f1, 4),
        "items": items,
    }


def _main() -> None:
    ap = argparse.ArgumentParser(description="Score candidate answers against the gold QA set.")
    ap.add_argument("--gold", default=None, help="path to gold.json (default: data/gold.json)")
    ap.add_argument("--pred", required=True, help="path to a candidate predictions file")
    ap.add_argument("--out", default=None, help="also write the full scored JSON here")
    args = ap.parse_args()
    result = score_dataset(load_gold(args.gold), load_predictions(args.pred))
    text = json.dumps(result, indent=2)
    if args.out:
        from pathlib import Path
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    _main()
