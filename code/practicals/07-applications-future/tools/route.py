"""Route a research question to the right evidence source by keyword rules.

Three destinations, each backed by a different deterministic tool:

* ``metrics``  — a specific figure from the bundled metrics table (``tools.metrics``).
* ``filings``  — discussion/disclosure text from the 10-K snippets (``tools.retrieve``).
* ``news``     — recent events from the news snippets (``tools.retrieve``).

The rules are plain substring matches over a small finance vocabulary, so the choice is
reproducible and inspectable — no model judgement is involved.

CLI:
    python -m tools.route "What was Meridian's gross margin in fiscal 2025?"
"""
from __future__ import annotations

import argparse
import json

# A figure that lives in the metrics table. A question naming one of these AND asking
# for a value (see VALUE_CUES) is a lookup, not a reading task.
METRIC_TERMS = (
    "revenue", "sales", "gross margin", "operating margin", "margin", "net income",
    "earnings per share", "eps", "free cash flow", "fcf", "cash", "total debt", "debt",
    "research and development", "r&d", "headcount", "employees", "growth",
)
VALUE_CUES = (
    "what was", "what is", "what's", "what were", "how much", "how many",
    "how large", "how big", "value of", "figure for", "number for",
)

# Words that signal a recent event rather than a steady-state disclosure.
NEWS_TERMS = (
    "announce", "announced", "announcement", "partnership", "partner", "recall",
    "lawsuit", "litigation", "acquire", "acquisition", "launch", "press release",
    "hire", "appoint", "investigation", "news", "recently", "this week", "latest news",
)

# Words tied to formal disclosure / steady-state risk and outlook language.
FILING_TERMS = (
    "risk", "risks", "risk factor", "10-k", "10k", "10-q", "filing", "disclose",
    "disclosure", "disclosed", "guidance", "outlook", "segment", "concentration",
    "supply chain", "regulation", "regulatory", "going concern", "liquidity",
    "md&a", "annual report",
)

ROUTES = ("metrics", "filings", "news")
# Tie-break order when scores are equal: prefer the most specific destination.
_PRIORITY = {"metrics": 3, "filings": 2, "news": 1}


def _hits(question: str, terms) -> list[str]:
    q = question.lower()
    return [t for t in terms if t in q]


def classify(question: str) -> dict:
    """Return ``{"route", "scores", "matched", "value_seeking"}`` for *question*."""
    metric_hits = _hits(question, METRIC_TERMS)
    news_hits = _hits(question, NEWS_TERMS)
    filing_hits = _hits(question, FILING_TERMS)
    value_seeking = any(cue in question.lower() for cue in VALUE_CUES)

    scores = {
        "metrics": len(metric_hits),
        "filings": len(filing_hits),
        "news": len(news_hits),
    }
    # Naming a metric and asking for its value is the strongest signal for a lookup.
    if metric_hits and value_seeking:
        scores["metrics"] += 2

    if not any(scores.values()):
        route = "filings"  # default: read the filings rather than guess
    else:
        route = max(ROUTES, key=lambda r: (scores[r], _PRIORITY[r]))

    return {
        "route": route,
        "scores": scores,
        "value_seeking": value_seeking,
        "matched": {"metrics": metric_hits, "filings": filing_hits, "news": news_hits},
    }


def _main() -> None:
    ap = argparse.ArgumentParser(description="Route a research question to an evidence source.")
    ap.add_argument("question")
    args = ap.parse_args()
    print(json.dumps(classify(args.question), indent=2))


if __name__ == "__main__":
    _main()
