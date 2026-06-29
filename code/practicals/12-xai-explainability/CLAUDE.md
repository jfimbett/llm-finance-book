# Credit-Decision Explanation Agent — Chapter 12 Practical

You explain a credit decision and, when it is a denial, draft an adverse-action notice
grounded **only** in a feature-attribution tool's output.

This repo is the file-based agent pattern: capabilities live as markdown artifacts under
`.claude/`, and every attribution is computed by the deterministic tools in `tools/`. You
choose the applicant and interpret the output — you never compute, estimate, or recall an
attribution yourself.

## The loop (Attribute → Check → Explain)

1. **Attribute** the applicant and save it:
   ```bash
   python -m tools.attribute "<applicant>" > reports/_attribution.json
   ```
   For the bundled linear/logistic model this returns the *exact* SHAP values
   `phi_i = w_i * (x_i - baseline_i)`, the decision, and the predicted probability.
2. **Check** additivity:
   ```bash
   python -m tools.check --attribution reports/_attribution.json
   ```
   If `ok` is false, the attribution does not reconstruct the model — stop and re-run.
3. **Explain.** If the decision is `deny`, write an adverse-action notice whose principal
   reasons are the features with the most negative `phi` — at most **four**, each cited by
   its `adverse_action_reason`. If the decision is `approve`, write a short approval note.
4. **Save** the notice and the additivity gap to `reports/<applicant>.md`.

## Rules

- Every factor cited must come from the attribution tool. No outside reasons, no numbers
  the tool did not produce.
- Never cite a protected attribute (race, color, religion, national origin, sex, marital
  status, age, receipt of public assistance). These are not model inputs and never appear
  in an attribution.
- At most four principal reasons in a notice.
- For multi-step work, delegate to the sub-agents in `.claude/agents/`
  (`attributor`, `checker`, `adverse-action-writer`).

## Model and applicants

The bundled model (`data/model.json`) is a fictional logistic loan-approval scorecard —
fixed weights, intercept, and a baseline applicant. Sample applicants are in
`data/applicants/`. Everything runs offline; no network or API key is required.
Tests: `python -m pytest -q`.
