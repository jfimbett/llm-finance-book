# Credit-Decision Explanation Agent — agent instructions

Explain a credit decision for an applicant in `data/applicants/`, grounded only in the
attribution tool's output. The deterministic tools in `tools/` compute every attribution;
you choose the applicant and interpret the result and never compute one yourself.

Loop for every applicant:

1. `python -m tools.attribute "<applicant>" > reports/_attribution.json`
2. `python -m tools.check --attribution reports/_attribution.json` — if `ok` is false, stop
   and re-run; a non-additive attribution is not faithful.
3. If the decision is `deny`, write an adverse-action notice citing the features with the
   most negative `phi` — at most four, each by its `adverse_action_reason`. If `approve`,
   write a short approval note.
4. Save the notice and the additivity gap to `reports/<applicant>.md`.

Every factor cited must come from the attribution tool. Never cite a protected attribute
(race, color, religion, national origin, sex, marital status, age, public assistance); they
are not model inputs. Tests: `python -m pytest -q`.

This file mirrors `CLAUDE.md` so the practical works in any agentic IDE (Cline, Cursor,
generic `AGENTS.md` runners) — an agent's capabilities are just markdown artifacts.
