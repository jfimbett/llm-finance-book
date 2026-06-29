"""Grade a generated answer against its retrieved context (faithfulness & relevance).

Two reproducible numbers in [0, 1] that replace "grade it by hand":

* faithfulness — how much of the answer is supported by the retrieved chunks.
* relevance — how well the retrieved chunks cover the question.

Both use **IDF-weighted** token coverage: a token's weight is its inverse document
frequency over the bundled corpus, so ubiquitous words ("gross", "margin") barely
count while distinctive ones — especially numbers like "64" or an invented "30" — carry
most of the weight. That's what makes a fabricated figure tank the faithfulness score
instead of hiding behind a couple of matching common words.

CLI:
    python -m tools.grade --question "..." --answer "..." --context reports/_context.json
"""
from __future__ import annotations

import argparse
import json
import math

from tools._common import load_corpus, tokenize
from tools.chunk import chunk_corpus


def _build_idf() -> tuple[dict[str, float], float]:
    """IDF over the bundled corpus chunks; unknown tokens get the maximum weight."""
    chunks = chunk_corpus(load_corpus())
    n = len(chunks)
    df: dict[str, int] = {}
    for c in chunks:
        for w in set(tokenize(c.text)):
            df[w] = df.get(w, 0) + 1
    idf = {w: math.log((1 + n) / (1 + d)) + 1.0 for w, d in df.items()}
    default = math.log(1 + n) + 1.0  # df = 0  → never in the corpus → maximally distinctive
    return idf, default


_IDF, _IDF_DEFAULT = _build_idf()


def _weighted_coverage(target: str, context: str) -> float:
    target_tokens = set(tokenize(target))
    if not target_tokens:
        return 0.0
    context_tokens = set(tokenize(context))
    num = sum(_IDF.get(w, _IDF_DEFAULT) for w in target_tokens if w in context_tokens)
    den = sum(_IDF.get(w, _IDF_DEFAULT) for w in target_tokens)
    return num / den if den else 0.0


def faithfulness(answer: str, chunks: list[str]) -> float:
    """IDF-weighted share of the answer that is grounded in the retrieved chunks."""
    return _weighted_coverage(answer, " ".join(chunks))


def relevance(question: str, chunks: list[str]) -> float:
    """IDF-weighted share of the question covered by the retrieved chunks."""
    return _weighted_coverage(question, " ".join(chunks))


def grade(question: str, answer: str, chunks: list[str]) -> dict[str, float]:
    return {
        "faithfulness": round(faithfulness(answer, chunks), 3),
        "relevance": round(relevance(question, chunks), 3),
    }


def _main() -> None:
    ap = argparse.ArgumentParser(description="Grade an answer against its retrieved context.")
    ap.add_argument("--question", required=True)
    ap.add_argument("--answer", required=True)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--context", help="path to the JSON emitted by `tools.retrieve` (list of {text})")
    src.add_argument("--chunks", nargs="+", help="paths to text files, each holding one retrieved chunk")
    args = ap.parse_args()
    if args.context:
        chunks = [item["text"] for item in json.load(open(args.context, encoding="utf-8"))]
    else:
        chunks = [open(p, encoding="utf-8").read() for p in args.chunks]
    print(json.dumps(grade(args.question, args.answer, chunks), indent=2))


if __name__ == "__main__":
    _main()
