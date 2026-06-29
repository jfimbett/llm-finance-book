"""Transparent AML screening rules over a transaction set (NumPy + stdlib, offline).

Every rule is a pure function of the data with thresholds stated as named
constants below — no model judgement, no hidden state. Each rule returns a
``{transaction_id: reason}`` map, and the reason string names the exact figure,
date window, or country that tripped it, so a downstream SAR narrative can cite
the flag instead of inventing one.

Rules
-----
* structuring            — several deposits just under the reporting threshold,
                           same account, inside a short window (smurfing).
* round_number           — a large, suspiciously round amount.
* high_risk_jurisdiction — origin or destination on the bundled high-risk list.
* velocity               — many transactions on one account in a short window.

CLI:
    python -m tools.screen                 # screen the bundled dataset
    python -m tools.screen --rule velocity # only one rule
    python -m tools.screen --json          # machine-readable output
"""
from __future__ import annotations

import argparse
import json
from datetime import timedelta

import numpy as np

from tools._common import Transaction, load_high_risk, load_transactions

# --- Rule thresholds (transparent and adjustable) --------------------------
REPORTING_THRESHOLD = 10_000.0      # the figure deposits are kept "just under"
STRUCTURING_BAND_LOW = 9_000.0      # amounts in [9000, 10000) look like structuring
STRUCTURING_MIN_COUNT = 3           # how many such deposits make a pattern
STRUCTURING_WINDOW_DAYS = 7         # ... within this many days, same account

ROUND_MULTIPLE = 1_000.0            # "round" == an exact multiple of this
ROUND_MIN_AMOUNT = 5_000.0          # ... and at least this large to be worth a flag

VELOCITY_MIN_COUNT = 4              # this many transactions ...
VELOCITY_WINDOW_HOURS = 24          # ... on one account within this many hours


def _by_account(txns: list[Transaction]) -> dict[str, list[Transaction]]:
    groups: dict[str, list[Transaction]] = {}
    for t in txns:
        groups.setdefault(t.account, []).append(t)
    for g in groups.values():
        g.sort(key=lambda t: t.dt)
    return groups


def rule_structuring(txns: list[Transaction]) -> dict[str, str]:
    """Flag sub-threshold deposit clusters (amounts just under the reporting limit)."""
    flagged: dict[str, str] = {}
    for account, group in _by_account(txns).items():
        band = [t for t in group if STRUCTURING_BAND_LOW <= t.amount < REPORTING_THRESHOLD]
        window = timedelta(days=STRUCTURING_WINDOW_DAYS)
        for t in band:
            cluster = [o for o in band if abs(o.dt - t.dt) <= window]
            if len(cluster) >= STRUCTURING_MIN_COUNT:
                flagged[t.id] = (
                    f"amount {t.amount:,.2f} sits in the structuring band "
                    f"[{STRUCTURING_BAND_LOW:,.0f}, {REPORTING_THRESHOLD:,.0f}); "
                    f"account {account} made {len(cluster)} such deposits within "
                    f"{STRUCTURING_WINDOW_DAYS} days"
                )
    return flagged


def rule_round_number(txns: list[Transaction]) -> dict[str, str]:
    """Flag large amounts that are exact multiples of ROUND_MULTIPLE."""
    flagged: dict[str, str] = {}
    for t in txns:
        is_round = np.isclose(t.amount % ROUND_MULTIPLE, 0.0)
        if is_round and t.amount >= ROUND_MIN_AMOUNT:
            flagged[t.id] = (
                f"amount {t.amount:,.2f} is an exact multiple of "
                f"{ROUND_MULTIPLE:,.0f} and at or above {ROUND_MIN_AMOUNT:,.0f}"
            )
    return flagged


def rule_high_risk_jurisdiction(
    txns: list[Transaction], high_risk: set[str] | None = None
) -> dict[str, str]:
    """Flag transactions whose origin or destination is on the high-risk list."""
    if high_risk is None:
        high_risk = load_high_risk()
    flagged: dict[str, str] = {}
    for t in txns:
        hits = [c for c in (t.origin_country, t.dest_country) if c in high_risk]
        if hits:
            where = " and ".join(sorted(set(hits)))
            flagged[t.id] = (
                f"counterparty jurisdiction {where} is on the high-risk list "
                f"(origin {t.origin_country} -> dest {t.dest_country})"
            )
    return flagged


def rule_velocity(txns: list[Transaction]) -> dict[str, str]:
    """Flag bursts: many transactions on one account inside a short window."""
    flagged: dict[str, str] = {}
    window = timedelta(hours=VELOCITY_WINDOW_HOURS)
    for account, group in _by_account(txns).items():
        times = np.array([t.dt.timestamp() for t in group])
        for i, t in enumerate(group):
            # forward window starting at this transaction
            members = times[(times >= t.dt.timestamp()) & (times <= (t.dt + window).timestamp())]
            if members.size >= VELOCITY_MIN_COUNT:
                for o in group:
                    if t.dt <= o.dt <= t.dt + window:
                        flagged.setdefault(
                            o.id,
                            f"account {account} ran {members.size} transactions within "
                            f"{VELOCITY_WINDOW_HOURS} hours starting {t.dt:%Y-%m-%d %H:%M}",
                        )
    return flagged


RULES = {
    "structuring": rule_structuring,
    "round_number": rule_round_number,
    "high_risk_jurisdiction": rule_high_risk_jurisdiction,
    "velocity": rule_velocity,
}


def screen(
    txns: list[Transaction] | None = None,
    rules: list[str] | None = None,
    high_risk: set[str] | None = None,
) -> dict[str, dict]:
    """Run the requested rules and return ``{transaction_id: {flags: {...}}}``.

    Each flag is ``{rule_name: reason}``; a transaction can trip more than one rule.
    """
    if txns is None:
        txns = load_transactions()
    if high_risk is None:
        high_risk = load_high_risk()
    names = rules or list(RULES)
    index = {t.id: t for t in txns}
    out: dict[str, dict] = {}
    for name in names:
        fn = RULES[name]
        fired = fn(txns, high_risk) if name == "high_risk_jurisdiction" else fn(txns)
        for tid, reason in fired.items():
            entry = out.setdefault(
                tid,
                {
                    "account": index[tid].account,
                    "date": f"{index[tid].dt:%Y-%m-%d %H:%M}",
                    "amount": index[tid].amount,
                    "flags": {},
                },
            )
            entry["flags"][name] = reason
    # stable order: by date, then id
    return dict(sorted(out.items(), key=lambda kv: (kv[1]["date"], kv[0])))


def _main() -> None:
    ap = argparse.ArgumentParser(description="Screen transactions for AML red flags.")
    ap.add_argument("--rule", choices=list(RULES), action="append",
                    help="limit to one rule (repeatable); default runs all")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = ap.parse_args()

    flags = screen(rules=args.rule)
    if args.json:
        print(json.dumps(flags, indent=2))
        return

    if not flags:
        print("No transactions flagged.")
        return
    print(f"{len(flags)} transaction(s) flagged:\n")
    for tid, info in flags.items():
        rules_fired = ", ".join(info["flags"])
        print(f"{tid}  {info['date']}  {info['amount']:>12,.2f}  "
              f"account {info['account']}  ->  {rules_fired}")
        for rule, reason in info["flags"].items():
            print(f"    [{rule}] {reason}")
        print()


if __name__ == "__main__":
    _main()
