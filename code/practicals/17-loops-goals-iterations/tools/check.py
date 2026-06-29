"""Pass/fail gate for the iterate-to-target loop.

The target is met only when BOTH hold:
  * coverage >= threshold (from data/target.json), and
  * faithful is True (no figure invented beyond the source).

This is the single authority that ends the loop. The agent keeps iterating until this
tool exits 0; it does not get to decide for itself that the draft is "good enough".

Exit code: 0 if the target is met, 1 otherwise — so it works as a shell/CI gate too.

CLI:
    python -m tools.check --candidate reports/draft.md
    python -m tools.check --candidate-text "Revenue rose 22% ..."
"""
from __future__ import annotations

import argparse
import json
import sys

from tools._common import load_source, load_target, read_candidate
from tools.metric import score


def passes(report: dict) -> bool:
    return report["coverage"] >= report["threshold"] and report["faithful"]


def _main() -> None:
    ap = argparse.ArgumentParser(description="Gate a candidate against the target threshold.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--candidate", help="path to a draft file (e.g. reports/draft.md)")
    src.add_argument("--candidate-text", help="the draft text itself")
    args = ap.parse_args()

    candidate = read_candidate(args.candidate) if args.candidate else args.candidate_text
    report = score(candidate, load_source(), load_target())
    ok = passes(report)
    print(json.dumps({**report, "pass": ok}, indent=2))
    print(
        f"\nTARGET MET — coverage {report['coverage']:.0%} >= {report['threshold']:.0%}, faithful."
        if ok
        else f"\nTARGET NOT MET — coverage {report['coverage']:.0%} "
        f"(need {report['threshold']:.0%}); faithful={report['faithful']}. Keep iterating."
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    _main()
