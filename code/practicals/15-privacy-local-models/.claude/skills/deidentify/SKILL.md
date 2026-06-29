---
name: deidentify
description: Detect and redact PII in the bundled document, then report the privacy/utility tradeoff. Usage /deidentify [path]
---

# /deidentify [path]

Run the full Detect → Redact → Measure pipeline on a document (defaults to the
bundled `data/customer_support_ticket.txt`) and save a grounded report.

1. **Detect** (detector agent):
   `python -m tools.deidentify --json > reports/_scan.json`
   Read it; note the entity `counts` per type (EMAIL, SSN, PHONE, PERSON, ACCOUNT).
2. **Redact** (redactor agent): save the `redacted` field from `reports/_scan.json`
   to `reports/<doc>.redacted.txt`. Confirm each placeholder appears.
3. **Measure** (privacy-analyst agent):
   `python -m tools.metrics > reports/_metrics.json`
   Read the `privacy` and `utility` numbers.
4. **Gate**: if `privacy < 1.0`, an identifier leaked — name the type and re-run
   detection before reporting. If `utility` is low, redaction was too aggressive —
   flag the over-redacted span. Loop at most 3 times.
5. **Save** to `reports/<doc>.md`:
   - the per-type entity counts,
   - the privacy and utility numbers (quote them exactly from `reports/_metrics.json`),
   - one sentence on the tradeoff (what was removed vs. what readable content remains),
   - the path to the redacted file.

Cite only the tool outputs — entity counts and the two metrics. Do not claim PII was
removed without the `privacy` number, and never estimate a score by hand.

Try these to start:
- `/deidentify`  ← the bundled support ticket.
- Add a new identifier to `data/customer_support_ticket.txt` and re-run; watch the
  counts change.
- Add a benign sentence with capitalised words and confirm `utility` stays at 1.0 —
  the detector should not redact it.
