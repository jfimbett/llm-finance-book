"""Finance-domain sentiment classifier (domain-adapted polarity lexicon).

This stands in for a model adapted to financial text (FinBERT-style). It scores 'beat'
as positive (beat estimates), knows 'headwinds', 'impairment', and 'writedown' are
negative, knows 'tailwinds' and 'accretive' are positive, and treats balance-sheet terms
like 'liability', 'liabilities', and 'covenant' as neutral rather than emotionally loaded.

CLI:
    python -m tools.domain             # classify every bundled sentence, print accuracy
    python -m tools.domain "Revenue beat guidance."    # classify one sentence
"""
from __future__ import annotations

import argparse
import json
import sys

from tools._common import accuracy, classify, load_lexicon, load_sentences

NAME = "domain"
LEXICON = load_lexicon(NAME)


def classify_sentence(text: str) -> str:
    return classify(text, LEXICON)


def predict_all(rows: list[dict] | None = None) -> list[str]:
    rows = rows if rows is not None else load_sentences()
    return [classify_sentence(r["text"]) for r in rows]


def _main() -> None:
    ap = argparse.ArgumentParser(description="Finance-domain sentiment classifier.")
    ap.add_argument("text", nargs="?", help="a single sentence to classify")
    args = ap.parse_args()
    if args.text is not None:
        print(json.dumps({"classifier": NAME, "text": args.text,
                          "label": classify_sentence(args.text)}, indent=2))
        return
    rows = load_sentences()
    preds = predict_all(rows)
    gold = [r["label"] for r in rows]
    acc = accuracy(preds, gold)
    print(json.dumps({
        "classifier": NAME,
        "accuracy": round(acc, 4),
        "predictions": [
            {"id": r["id"], "gold": r["label"], "pred": p, "ok": r["label"] == p}
            for r, p in zip(rows, preds)
        ],
    }, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    _main()
