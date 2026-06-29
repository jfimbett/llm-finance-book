"""Load a bundled company's raw financial figures (offline, deterministic).

CLI:
    python -m tools.financials aurora      # one company's figures as JSON
    python -m tools.financials --list      # available company slugs
"""
from __future__ import annotations

import argparse
import json

from tools._common import list_companies, load_financials


def _main() -> None:
    ap = argparse.ArgumentParser(description="Load a company's bundled financial figures.")
    ap.add_argument("company", nargs="?", help="company slug, e.g. aurora")
    ap.add_argument("--list", action="store_true", help="list available companies and exit")
    args = ap.parse_args()

    if args.list or not args.company:
        print(json.dumps({"companies": list_companies()}, indent=2))
        return

    print(json.dumps(load_financials(args.company), indent=2))


if __name__ == "__main__":
    _main()
