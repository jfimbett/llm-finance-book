"""Grade a generated summary against the source filing (faithfulness & figure coverage).

Two reproducible numbers in [0, 1] that replace "eyeball whether the summary is honest":

* faithfulness — IDF-weighted share of the summary's content that is supported by the
  filing. A token's weight is its inverse document frequency over the filing's sentences,
  so ubiquitous words ("revenue", "margin") barely count while distinctive ones —
  especially numbers like "58" or an invented "73" — carry most of the weight. That is
  what makes a fabricated figure tank the score instead of hiding behind common words.
* figure_coverage — the blunt, literal check the chapter insists on: every numeric figure
  in the summary must appear verbatim in the source. ``5/5`` supported figures → 1.0; one
  invented number drags it down.

CLI:
    python -m tools.grade --summary "Revenue was $1.46 billion ..."
    python -m tools.grade --summary-file reports/_summary.txt
"""
from __future__ import annotations

import argparse
import json
import math
import re

from tools._common import load_filing_text, sentences, tokenize

FIGURE_RE = re.compile(r"\d+(?:\.\d+)?")


def _build_idf(source: str) -> tuple[dict[str, float], float]:
    """IDF over the filing's sentences; tokens never seen get the maximum weight."""
    docs = sentences(source)
    n = len(docs)
    df: dict[str, int] = {}
    for d in docs:
        for w in set(tokenize(d)):
            df[w] = df.get(w, 0) + 1
    idf = {w: math.log((1 + n) / (1 + d)) + 1.0 for w, d in df.items()}
    default = math.log(1 + n) + 1.0  # df = 0 → never in the filing → maximally distinctive
    return idf, default


def faithfulness(summary: str, source: str) -> float:
    """IDF-weighted share of the summary that is grounded in the source filing."""
    idf, default = _build_idf(source)
    summary_tokens = set(tokenize(summary))
    if not summary_tokens:
        return 0.0
    source_tokens = set(tokenize(source))
    num = sum(idf.get(w, default) for w in summary_tokens if w in source_tokens)
    den = sum(idf.get(w, default) for w in summary_tokens)
    return num / den if den else 0.0


def figures(text: str) -> set[str]:
    """Every numeric figure (e.g. '1.46', '58') appearing in *text*."""
    return set(FIGURE_RE.findall(text))


def figure_coverage(summary: str, source: str) -> float:
    """Fraction of the summary's figures that appear verbatim in the source."""
    summary_figs = figures(summary)
    if not summary_figs:
        return 1.0  # a summary with no numbers cannot invent one
    source_figs = figures(source)
    supported = sum(1 for f in summary_figs if f in source_figs)
    return supported / len(summary_figs)


def unsupported_figures(summary: str, source: str) -> list[str]:
    """Figures stated in the summary but absent from the source (sorted)."""
    return sorted(figures(summary) - figures(source), key=lambda x: (len(x), x))


def grade(summary: str, source: str | None = None) -> dict:
    if source is None:
        source = load_filing_text()
    f = round(faithfulness(summary, source), 3)
    fc = round(figure_coverage(summary, source), 3)
    return {
        "faithfulness": f,
        "figure_coverage": fc,
        "unsupported_figures": unsupported_figures(summary, source),
        "supported": f >= 0.7 and fc >= 1.0,
    }


def _main() -> None:
    ap = argparse.ArgumentParser(description="Grade a summary against the source filing.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--summary", help="the summary text to grade")
    src.add_argument("--summary-file", help="path to a file holding the summary text")
    ap.add_argument("--filing", help="filing text file (defaults to the bundled filing)")
    args = ap.parse_args()
    summary = args.summary or open(args.summary_file, encoding="utf-8").read()
    source = open(args.filing, encoding="utf-8").read() if args.filing else load_filing_text()
    print(json.dumps(grade(summary, source), indent=2))


if __name__ == "__main__":
    _main()
