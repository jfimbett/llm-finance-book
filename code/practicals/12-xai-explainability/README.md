# Practical 12 — Explainability and Interpretability (Claude Code / Cline)

**Large Language Models in Finance · Chapter 12**

This practical is an **agentic project**, not a notebook. You open this folder in
**Claude Code** or **Cline** and drive an *explanation* agent for a credit decision. You
run `/explain <applicant>`; the agent runs a deterministic feature-attribution tool on a
bundled logistic credit model, verifies the attribution is faithful, and — when the
decision is a denial — drafts a grounded adverse-action notice citing the top negative
features.

The agent never computes an attribution or recalls a number from memory: the deterministic
tools in `tools/` do all the math, and the agent only chooses the applicant and interprets
the output. That separation is the whole point of the chapter — the explanation is anchored
to an *exact* additive decomposition of the model, not to the language model's intuition.

## Setup

```bash
pip install -r requirements.txt   # numpy + pytest; the tools are otherwise standard-library
```

Open the folder in Claude Code (or Cline). The capabilities are markdown artifacts under
`.claude/`: three sub-agents (`attributor`, `checker`, `adverse-action-writer`) and one
command, `/explain`.

## Run

```
/explain alice
```

The agent attributes the decision, checks additivity, writes a notice grounded in the top
negative features, and saves a report to `reports/`. Everything is offline — the model and
applicants are bundled fictional data (`data/`).

You can also run the steps by hand:

```bash
python -m tools.attribute alice > reports/_attribution.json
python -m tools.check --attribution reports/_attribution.json
```

## The pipeline

| Step | Agent | Tool |
|------|-------|------|
| Attribute the decision to features | `attributor` | `tools/attribute.py` (exact linear SHAP) |
| Verify the attribution is additive | `checker` | `tools/check.py` |
| Draft the adverse-action notice | `adverse-action-writer` | — (reads `reports/_attribution.json`) |

For a linear / logistic model the contribution of feature *i* is exactly
`phi_i = w_i * (x_i - baseline_i)`, and these contributions satisfy
`sum_i phi_i = f(x) - f(baseline)` — they account for the entire gap between this applicant
and the reference applicant. `check.py` confirms that identity before any notice is written.

## Things to try

- `/explain bob` — a clean applicant who is **approved**. The agent must write an approval
  note, not invent reasons for a denial that did not happen.
- `/explain carol` — denied, but for a *different* dominant reason than Alice (high credit
  utilization vs. recent delinquencies). Compare which factor leads each notice.
- Open `data/applicants/alice.json`: it carries a `protected` block (age, sex, ...). Confirm
  it never appears in the attribution or the notice — those fields are not model inputs.
- Edit a weight in `data/model.json` and re-run `python -m tools.check alice`; the gap stays
  ~0 because additivity is a property of *linear* models, not of the specific numbers.
- Add a new applicant JSON to `data/applicants/` and explain it.

## Tests

```bash
python -m pytest -q        # fully offline; checks additivity, sign, and top-factor selection
```
