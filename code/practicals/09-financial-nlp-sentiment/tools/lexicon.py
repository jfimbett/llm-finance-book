"""Score one text's net polarity with the bundled finance lexicon (deterministic, offline).

Each polarity word contributes +1 (positive) or -1 (negative). Two local modifiers,
both Loughran-McDonald in spirit, adjust that base before it is summed:

* negation — a negator ("not", "no", "fails") in the three tokens before a polarity
  word flips its sign, so "did not beat" scores negative, not positive.
* intensity — an intensifier ("strong", "sharp", "significant") in the two tokens
  before a polarity word multiplies its magnitude (e.g. x1.5).

The net polarity is the signed sum divided by the number of sentiment-bearing words,
so it lands in roughly [-1.5, 1.5]: > 0 bullish, < 0 bearish, 0 neutral. Text with no
lexicon words scores exactly 0.

CLI:
    python -m tools.lexicon "NovaCorp beats estimates on strong cloud growth"
"""
from __future__ import annotations

import argparse
import json

from tools._common import load_lexicon, tokenize

_NEG_WINDOW = 3   # how many preceding tokens to scan for a negator
_INT_WINDOW = 2   # how many preceding tokens to scan for an intensifier

_LEXICON: dict | None = None


def _lexicon(lex: dict | None) -> dict:
    global _LEXICON
    if lex is not None:
        return lex
    if _LEXICON is None:
        _LEXICON = load_lexicon()
    return _LEXICON


def score(text: str, lex: dict | None = None) -> dict:
    """Return the net polarity of *text* and the words that drove it."""
    lex = _lexicon(lex)
    pos, neg = lex["positive"], lex["negative"]
    negators, intensifiers = lex["negators"], lex["intensifiers"]

    tokens = tokenize(text)
    signed: list[float] = []
    matched_pos: list[str] = []
    matched_neg: list[str] = []

    for i, tok in enumerate(tokens):
        base = 1.0 if tok in pos else -1.0 if tok in neg else 0.0
        if base == 0.0:
            continue

        weight = 1.0
        for j in range(max(0, i - _INT_WINDOW), i):
            if tokens[j] in intensifiers:
                weight = max(weight, intensifiers[tokens[j]])

        negated = any(tokens[j] in negators for j in range(max(0, i - _NEG_WINDOW), i))
        value = base * weight * (-1.0 if negated else 1.0)

        signed.append(value)
        (matched_pos if value > 0 else matched_neg).append(tok)

    n = len(signed)
    raw = float(sum(signed))
    polarity = raw / n if n else 0.0

    return {
        "text": text,
        "polarity": round(polarity, 4),
        "raw": round(raw, 4),
        "n_sentiment": n,
        "n_tokens": len(tokens),
        "positive": matched_pos,
        "negative": matched_neg,
    }


def _main() -> None:
    ap = argparse.ArgumentParser(description="Score one text's net finance-sentiment polarity.")
    ap.add_argument("text", help="the headline or sentence to score")
    args = ap.parse_args()
    print(json.dumps(score(args.text), indent=2))


if __name__ == "__main__":
    _main()
