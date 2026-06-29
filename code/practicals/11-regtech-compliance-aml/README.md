# Practical 11 — RegTech, Compliance & AML (Claude Code / Cline)

**Large Language Models in Finance · Chapter 11**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive an anti-money-laundering (AML) screening
agent: it runs transparent rule tools over a set of transactions, flags the
suspicious ones, and drafts a SAR-style narrative (Suspicious Activity Report)
that cites the specific flags behind every claim.

The agent never decides what is suspicious: the deterministic rules in `tools/`
do all detection — structuring, round amounts, high-risk jurisdictions, velocity
— and the agent only chooses which rules to run and writes up what they returned.

## Setup

```bash
pip install -r requirements.txt   # numpy + pytest; the rules are otherwise stdlib
```

Open the folder in Claude Code (or Cline). The capabilities are markdown
artifacts under `.claude/`: three sub-agents (`screener`, `sar-writer`,
`reviewer`) and one command, `/screen`.

## Run

```
/screen
```

The agent screens every transaction, groups the flags by account, drafts a
grounded SAR narrative, checks each claim against a flag, and saves a report to
`reports/`. Everything is offline — the data is a bundled fictional
`data/transactions.csv` and a `data/high_risk.json` jurisdiction list.

You can also run the screen by hand:

```bash
python -m tools.screen                       # readable table of all flags
python -m tools.screen --rule structuring    # one rule only (repeatable)
python -m tools.screen --json > reports/_flags.json
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Run the AML rules, list the flags | `screener` | `tools/screen.py` |
| Draft a SAR narrative from the flags | `sar-writer` | — (reads `reports/_flags.json`) |
| Verify each claim is backed by a flag | `reviewer` | — (reads `reports/_flags.json`) |

The rules and their thresholds (all in `tools/screen.py`):

| Rule | Fires when |
|------|-----------|
| `structuring` | ≥ 3 deposits in `[9,000, 10,000)` on one account within 7 days |
| `round_number` | amount is an exact multiple of 1,000 and ≥ 5,000 |
| `high_risk_jurisdiction` | origin or destination is on `data/high_risk.json` |
| `velocity` | ≥ 4 transactions on one account within 24 hours |

## Things to try

- Run `/screen` and confirm each rule fires: structuring on `ACC201`,
  round-number on `ACC202`, high-risk on `ACC203`, velocity on `ACC204`. The
  benign accounts (`ACC100`, `ACC105`) should produce no flags.
- Lower `STRUCTURING_BAND_LOW` in `tools/screen.py` to `8,000` and re-run the
  tests — watch which clean rows start tripping and a test turn red.
- Add a country to `data/high_risk.json` that one benign transaction routes
  through, re-screen, and see a new flag appear.
- Ask the agent to assert a transaction the tool did **not** flag. The reviewer
  step should reject it as unsupported.
- Add a fifth account to `data/transactions.csv` that trips two rules at once and
  check the narrative cites both.

## Tests

```bash
python -m pytest -q        # fully offline; each rule fires on a positive fixture
                           # and stays silent on a clean one
```
