# General-vs-Domain Comparison Agent — Chapter 8 Practical

You compare a general-purpose classifier against a finance-domain classifier on labelled
finance text, and report which one wins and why.

This repo is the file-based agent pattern from Chapter 8: capabilities live as markdown
artifacts under `.claude/`, and every bit of classification and scoring is done by the
deterministic tools in `tools/`. You choose the inputs and interpret the outputs — you
never classify, score, or recall a number yourself.

## The comparison

1. **Baseline.** Run the general-purpose classifier:
   ```bash
   python -m tools.general
   ```
2. **Domain.** Run the finance-domain classifier:
   ```bash
   python -m tools.domain
   ```
3. **Adjudicate.** Score both against the gold labels and name the winner:
   ```bash
   python -m tools.compare --json
   ```
4. **Explain.** Read `domain_wins` from step 3. Each entry lists the `deciding_terms` —
   the words the general lexicon scored wrongly or never saw (`beat`, `headwinds`,
   `liability`, `impairment`). The verdict must cite those terms and the two accuracies.
5. **Save** the verdict to `reports/compare.md`.

## Rules

- Never state an accuracy or a label that the tools did not print. No outside knowledge.
- Quote the `deciding_terms` from the tool output verbatim; do not invent why a word flips.
- For a multi-part comparison, delegate to the sub-agents in `.claude/agents/`
  (`generalist`, `specialist`, `adjudicator`) rather than doing everything in one turn.

## Data

`data/sentences.jsonl` is a fictional labelled finance-sentence dataset. `data/lexicon_general.json`
is a naive English polarity lexicon; `data/lexicon_domain.json` is the finance-adapted one
where finance terms are scored correctly. Everything runs offline; no network or API key
is required. Tests: `python -m pytest -q`.
