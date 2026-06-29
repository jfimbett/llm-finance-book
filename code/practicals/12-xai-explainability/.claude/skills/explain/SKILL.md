---
name: explain
description: Explain a credit decision for an applicant and draft a grounded adverse-action notice. Usage /explain <applicant>
---

# /explain <applicant>

Run the attribute → check → write loop and save a report.

1. **Attribute** (attributor agent):
   `python -m tools.attribute "<applicant>" > reports/_attribution.json`
   Read it; note the decision, probability, and the most negative features.
2. **Check** (checker agent):
   `python -m tools.check --attribution reports/_attribution.json`
   If `ok` is false, stop and re-run step 1 — a non-additive attribution is not faithful
   and may not be used.
3. **Decide the format:**
   - If `decision == "approve"`, write a short approval note; no adverse-action reasons.
   - If `decision == "deny"`, write an **adverse-action notice** (adverse-action-writer
     agent): the principal reasons are the features with the most negative `phi`, at most
     **four**, each cited by its `adverse_action_reason`. Never cite a protected attribute.
4. **Save** to `reports/<applicant>.md`:
   - the decision and predicted probability (from the tool),
   - the principal reasons, each tied to its feature key and `phi`,
   - the additivity gap from step 2,
   - a one-line statement that every reason came from the attribution tool.

Every factor in the notice must come from `reports/_attribution.json`. No outside reasons,
no protected attributes, no numbers the tool did not produce.

Try these to start:
- `/explain alice`  ← denied; recent delinquencies dominate.
- `/explain carol`  ← denied; high credit utilization dominates.
- `/explain bob`    ← approved; no adverse-action reasons.
