# Practical 6 — Credit Risk (Claude Code / Cline)

**Large Language Models in Finance · Chapter 6**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive a credit-memo agent: it pulls a company's financial
figures, computes credit ratios, scores default risk, and drafts a grounded memo that
cites every number it states — the tool-using, file-based agent pattern applied to
Chapter 6's credit analysis.

The agent never does arithmetic or recalls a figure from memory: the deterministic tools
in `tools/` compute every ratio and the risk score, and the agent only chooses the company
and interprets the outputs.

## Setup

```bash
pip install -r requirements.txt   # numpy + pytest; the tools are otherwise standard-library
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts under
`.claude/`: three sub-agents (`analyst`, `ratio-checker`, `memo-writer`) and one command,
`/credit`.

## Run

```
/credit cobalt
```

The agent loads the company's figures, computes the ratios, scores default risk, writes a
cited memo, has the ratio-checker verify every number traces back to a tool, and saves the
memo to `reports/`. Everything is offline — the companies are bundled fictional fixtures in
`data/companies/`.

You can also run the steps by hand:

```bash
python -m tools.financials --list          # aurora, borealis, cobalt, delta
python -m tools.financials cobalt          # raw figures
python -m tools.ratios cobalt              # leverage, coverage, liquidity
python -m tools.score cobalt               # 0-100 risk score + LOW/MEDIUM/HIGH flag
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Load the company's raw figures | `analyst` | `tools/financials.py` |
| Compute credit ratios | `analyst` | `tools/ratios.py` (leverage, coverage, current ratio) |
| Score default risk | `analyst` | `tools/score.py` (transparent, rule-based, monotone) |
| Draft the grounded, cited memo | `memo-writer` | — (reads the tool outputs) |
| Verify every figure traces to a tool | `ratio-checker` | `tools/ratios.py`, `tools/score.py` |

The bundled companies span the risk spectrum: `aurora` (strong), `borealis` (mid-risk),
`cobalt` (distressed), and `delta` (debt-free, so interest coverage is undefined).

## Things to try

- Run `/credit aurora` and `/credit cobalt` back to back and compare the risk scores — the
  weaker balance sheet must score higher; the score is monotone in risk by construction
  (see `tools/score.py`).
- `/credit delta` — a debt-free firm. Interest coverage and cash-to-debt come back `null`;
  the memo must call them undefined rather than invent a number.
- Edit a figure in `data/companies/cobalt.json` (say, halve `interest_expense`) and re-run
  `python -m tools.score cobalt` to see the coverage sub-score and flag move.
- Add a fifth company under `data/companies/` and run `/credit <slug>` on it.
- Ask the agent to state a ratio the tools didn't print, then run the ratio-checker — watch
  it bounce the memo back.

## Tests

```bash
python -m pytest -q        # fully offline
```

Covers ratio math on a fixture, score monotonicity (a strictly-weaker company scores higher
risk), and edge handling (zero interest expense, zero current liabilities, no EBITDA).
