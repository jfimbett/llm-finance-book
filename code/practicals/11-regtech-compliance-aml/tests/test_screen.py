"""Each rule must fire on a crafted positive fixture and stay silent on a clean one,
and the bundled dataset must produce the flags the practical promises with no
false positives on the benign accounts. Fully offline and deterministic.
"""
from datetime import datetime

from tools._common import Transaction, load_transactions
from tools.screen import (
    rule_high_risk_jurisdiction,
    rule_round_number,
    rule_structuring,
    rule_velocity,
    screen,
)

HIGH_RISK = {"IR", "KP", "SY", "MM", "AF"}


def tx(tid, date, amount, origin="US", dest="US", account="A1"):
    return Transaction(tid, datetime.strptime(date, "%Y-%m-%d %H:%M"),
                       float(amount), origin, dest, account)


# --- structuring -----------------------------------------------------------
def test_structuring_fires_on_subthreshold_cluster():
    txns = [
        tx("s1", "2024-03-01 09:00", 9600, account="ACC"),
        tx("s2", "2024-03-02 11:00", 9450, account="ACC"),
        tx("s3", "2024-03-04 16:00", 9800, account="ACC"),
    ]
    flagged = rule_structuring(txns)
    assert set(flagged) == {"s1", "s2", "s3"}


def test_structuring_silent_on_clean_rows():
    # below the band, and well-spaced amounts that never form a sub-threshold cluster
    clean = [
        tx("c1", "2024-03-01 09:00", 250, account="OK"),
        tx("c2", "2024-03-10 09:00", 1875, account="OK"),
        tx("c3", "2024-03-20 09:00", 642, account="OK"),
    ]
    assert rule_structuring(clean) == {}


def test_structuring_silent_when_spread_beyond_window():
    spread = [
        tx("d1", "2024-01-01 09:00", 9600, account="SLOW"),
        tx("d2", "2024-02-01 09:00", 9450, account="SLOW"),
        tx("d3", "2024-03-01 09:00", 9800, account="SLOW"),
    ]
    assert rule_structuring(spread) == {}


# --- round number ----------------------------------------------------------
def test_round_number_fires_on_large_round_amount():
    flagged = rule_round_number([tx("r1", "2024-04-05 12:00", 50000)])
    assert set(flagged) == {"r1"}


def test_round_number_silent_on_non_round_and_small():
    clean = [
        tx("n1", "2024-04-05 12:00", 9600),   # round-ish but not a multiple of 1000
        tx("n2", "2024-04-05 12:00", 3000),   # round but below the size floor
        tx("n3", "2024-04-05 12:00", 4380.40),
    ]
    assert rule_round_number(clean) == {}


# --- high-risk jurisdiction ------------------------------------------------
def test_high_risk_fires_on_listed_country():
    txns = [
        tx("h1", "2024-05-01 10:00", 3200, dest="IR"),
        tx("h2", "2024-05-15 13:00", 1500, origin="KP"),
    ]
    flagged = rule_high_risk_jurisdiction(txns, HIGH_RISK)
    assert set(flagged) == {"h1", "h2"}


def test_high_risk_silent_on_safe_countries():
    clean = [
        tx("g1", "2024-05-01 10:00", 3200, dest="CA"),
        tx("g2", "2024-05-15 13:00", 1500, origin="GB"),
    ]
    assert rule_high_risk_jurisdiction(clean, HIGH_RISK) == {}


# --- velocity --------------------------------------------------------------
def test_velocity_fires_on_burst():
    burst = [
        tx("v1", "2024-07-01 08:00", 1200, account="FAST"),
        tx("v2", "2024-07-01 10:30", 800, account="FAST"),
        tx("v3", "2024-07-01 13:15", 1500, account="FAST"),
        tx("v4", "2024-07-01 18:45", 2100, account="FAST"),
    ]
    flagged = rule_velocity(burst)
    assert set(flagged) == {"v1", "v2", "v3", "v4"}


def test_velocity_silent_when_spread_out():
    spread = [
        tx("w1", "2024-07-01 08:00", 1200, account="CALM"),
        tx("w2", "2024-07-05 10:30", 800, account="CALM"),
        tx("w3", "2024-07-12 13:15", 1500, account="CALM"),
    ]
    assert rule_velocity(spread) == {}


# --- whole bundled dataset -------------------------------------------------
def test_bundled_dataset_each_rule_fires_at_least_once():
    flags = screen()
    fired = {rule for info in flags.values() for rule in info["flags"]}
    assert fired == {
        "structuring",
        "round_number",
        "high_risk_jurisdiction",
        "velocity",
    }


def test_bundled_dataset_flags_expected_ids():
    flags = screen()
    by_rule: dict[str, set[str]] = {}
    for tid, info in flags.items():
        for rule in info["flags"]:
            by_rule.setdefault(rule, set()).add(tid)
    assert by_rule["structuring"] == {"T010", "T011", "T012"}
    assert by_rule["round_number"] == {"T020", "T021"}
    assert by_rule["high_risk_jurisdiction"] == {"T030", "T031"}
    assert by_rule["velocity"] == {"T040", "T041", "T042", "T043"}


def test_benign_accounts_have_no_false_positives():
    flags = screen()
    benign_ids = {t.id for t in load_transactions() if t.account in {"ACC100", "ACC105"}}
    assert benign_ids.isdisjoint(flags), benign_ids & set(flags)
