# Practical 15 — Privacy and Local Models (Claude Code / Cline)

**Large Language Models in Finance · Chapter 15**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive a PII de-identification agent that detects and
redacts personal data in a document and reports the privacy/utility tradeoff — the
local-deployment, text-de-identification workflow from the chapter, built with the
file-based agents/skills pattern.

The agent never decides what counts as PII or grades a redaction from memory: the
deterministic tools in `tools/` do all detection, redaction, and scoring, and the
agent only chooses inputs and interprets outputs. Everything runs offline — no
network, no API key, no model download — which is the point of the chapter: sensitive
text can be processed on a local machine.

## Setup

```bash
pip install -r requirements.txt   # only pytest; the tools are standard-library
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts
under `.claude/`: three sub-agents (`detector`, `redactor`, `privacy-analyst`) and one
command, `/deidentify`.

## Run

```
/deidentify
```

The agent detects the personal data in the bundled document, replaces each identifier
with a typed placeholder, scores how much PII was removed (privacy) and how much
readable content survived (utility), and saves a report to `reports/`. The document is
a fictional **NovaCorp Financial** support ticket (`data/`) seeded with an email, a US
SSN, a phone number, person names, and an org/account number.

You can also run the steps by hand:

```bash
python -m tools.deidentify --json > reports/_scan.json   # detect + redact
python -m tools.metrics                                  # privacy / utility
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Detect personal data | `detector` | `tools/deidentify.py` (regex + name gazetteer) |
| Redact to typed placeholders | `redactor` | `tools/deidentify.py` |
| Score privacy & utility | `privacy-analyst` | `tools/metrics.py` |

## What the tools detect

| Type | Example | Rule |
|------|---------|------|
| `EMAIL` | `james.whitfield@example.com` | address regex |
| `SSN` | `123-45-6789` | US SSN pattern |
| `PHONE` | `415-555-0199` | US phone pattern |
| `ACCOUNT` | `NVC-88421003` | org code + digits |
| `PERSON` | `Maria Delgado`, `Dr. Alan Pierce` | titles + name gazetteer |

`data/seeded_pii.json` is the ground truth the **privacy** metric scores against, so
the score is an honest measure of what the detector actually caught — not a
self-graded number.

## Things to try

- Add a new email or phone number to `data/customer_support_ticket.txt`, re-run
  `/deidentify`, and watch the per-type counts change.
- Add a benign sentence full of capitalised words ("The Quarterly Review Board met").
  The detector should leave it alone and `utility` should stay at 1.0 — over-redaction
  is what drags utility down.
- Remove a name from the gazetteer in `tools/deidentify.py`, re-run the tests, and
  watch `privacy` fall below 1.0 as that identifier leaks through.
- Add a document the detector handles poorly (e.g. an international phone format) and
  see the privacy/utility numbers expose the gap.

## Tests

```bash
python -m pytest -q        # fully offline
```
