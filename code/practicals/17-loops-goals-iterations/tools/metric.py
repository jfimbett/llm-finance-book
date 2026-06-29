"""Score a candidate summary against the source text and the target fact list.

This is the deterministic target metric for the iterate-to-target loop. The agent
never computes it: it drafts text, this tool returns a number and the exact list of
required facts still missing, and the agent revises. Two reproducible quantities:

* coverage  — fraction of the required facts in ``data/target.json`` whose anchor
              phrases all appear in the candidate. This is the headline score the
              loop drives toward the threshold.
* faithful  — True iff every numeric figure in the candidate also occurs in
              ``data/source.txt``. A fabricated number (a figure not in the source)
              makes this False, so the agent cannot reach the target by inventing
              facts — it must pull them from the source.

CLI:
    python -m tools.metric --candidate reports/draft.md
    python -m tools.metric --candidate-text "Revenue rose 22% to 2.4 billion ..."
"""
from __future__ import annotations

import argparse
import json

from tools._common import (
    figures,
    load_source,
    load_target,
    normalize,
    read_candidate,
)


def missing_facts(candidate: str, facts: list[dict]) -> list[dict]:
    """Required facts whose anchor phrases are not all present in the candidate."""
    norm = normalize(candidate)
    missing = []
    for fact in facts:
        if not all(normalize(term) in norm for term in fact["must_include"]):
            missing.append(fact)
    return missing


def coverage(candidate: str, facts: list[dict]) -> float:
    """Fraction of required facts fully covered by the candidate, in [0, 1]."""
    if not facts:
        return 0.0
    return (len(facts) - len(missing_facts(candidate, facts))) / len(facts)


def unsupported_figures(candidate: str, source: str) -> list[str]:
    """Numeric tokens in the candidate that do not appear anywhere in the source."""
    src = figures(source)
    return sorted(f for f in figures(candidate) if f not in src)


def score(candidate: str, source: str, target: dict) -> dict:
    """Full metric report for one candidate."""
    facts = target["facts"]
    missing = missing_facts(candidate, facts)
    unsupported = unsupported_figures(candidate, source)
    return {
        "coverage": round(coverage(candidate, facts), 3),
        "covered": len(facts) - len(missing),
        "total": len(facts),
        "missing": [{"id": f["id"], "label": f["label"]} for f in missing],
        "faithful": not unsupported,
        "unsupported_figures": unsupported,
        "threshold": target["threshold"],
    }


def _main() -> None:
    ap = argparse.ArgumentParser(description="Score a candidate summary against the source and target.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--candidate", help="path to a draft file (e.g. reports/draft.md)")
    src.add_argument("--candidate-text", help="the draft text itself")
    args = ap.parse_args()

    candidate = read_candidate(args.candidate) if args.candidate else args.candidate_text
    report = score(candidate, load_source(), load_target())
    print(json.dumps(report, indent=2))
    if report["missing"]:
        print("\nStill missing (add these, citing the source):")
        for f in report["missing"]:
            print(f"  - [{f['id']}] {f['label']}")
    if report["unsupported_figures"]:
        print("\nFigures not found in the source (remove or correct):")
        print("  " + ", ".join(report["unsupported_figures"]))


if __name__ == "__main__":
    _main()
