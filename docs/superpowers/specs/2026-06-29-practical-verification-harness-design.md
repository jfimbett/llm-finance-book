# Practical Verification Harness — Design

**Date:** 2026-06-29
**Status:** Approved (design); pending implementation plan
**Scope:** A single local command that verifies every practical in `code/practicals/`
works before a teaching session or course release.

---

## Problem

`code/practicals/` contains two species of exercise:

1. **Notebook practicals** (`01-intro`, `02-llm-foundations`, `03-llm-training-finetuning`)
   — a single `practical.ipynb`, standard Python, straightforward to test.
2. **Agentic practicals** (`04`–`17`) — each is a folder the student opens in **Claude
   Code**: a `.claude/` directory (settings, sub-agents, one headline skill such as
   `/ask`, `/valuation`, `/sentiment`), a `CLAUDE.md`, deterministic `tools/`, `tests/`,
   and bundled `data/`. Plus one oddball, `05-business-valuation-example/`, which has 7
   skills but no `tools/tests/requirements`.

Standard Python is easy to test. The hard question is the agentic practicals: how do we
confirm they "work properly" — both the deterministic backbone *and* the agent behavior a
student experiences when they run the headline skill?

## Goals

- One local command that gives a confident pass/fail across all practicals.
- Catch the real first-run failures a student hits (missing deps, broken `.claude`
  config, dangling file references, commands that don't run).
- Optionally validate live agent behavior on critical-path skills.
- Never dirty the tracked working tree while doing so.

## Non-Goals (YAGNI)

- No CI / GitHub Actions. This is a local pre-session/pre-release tool.
- No LLM-judge scoring of agent answers in v1 — deterministic assertions only.
- No testing of Cline or other harnesses — Claude Code headless only.

---

## Approach: a layered verification pyramid (decision: option C)

Two layers, run from one script:

- **Layer A — deterministic, no API key.** Runs always. Broad, cheap coverage.
- **Layer B — live Claude, opt-in (`--live`).** Runs occasionally (before a release) on
  critical-path skills only.

Coverage is **hybrid** (decision: option A): the harness auto-discovers the cheap checks
with zero config, and a tiny per-practical `verify.yaml` declares only what can't be
inferred (the live skill call and its assertions, plus any deterministic "by hand"
smoke commands).

---

## Components

### 1. Runner / CLI — `code/practicals/verify.py`

- **Discovery:** immediate subdirs matching `NN-*`.
- **Classification:** *notebook* (`*.ipynb` present, no `.claude`) vs *agentic*
  (`.claude/` present).
- **Flags:**
  - `--live` — also run Layer B.
  - `--only 04,09` — restrict to listed practicals.
  - `--fast` / `--shared-env` — reuse one shared venv instead of a fresh venv per
    practical (faster iteration; less faithful).
  - `--layer a|b` — run only one layer.
- **Output:** a pass/fail table (row per practical, column per check); a machine-readable
  `code/practicals/.verify-report.json` (gitignored). Exit non-zero if any check fails.

### 2. Repo-safety wrapper (applies to every practical)

Before any execution, the practical is **copied to a temp directory**. All venvs,
generated `reports/`, `_context.json`, `__pycache__`, and `.pytest_cache` are created in
the copy. The tracked tree is never modified by the verifier.

Rationale: `auto_commit` is on in this project and there is a standing caution about
working-tree integrity. The verifier must be incapable of dirtying or deleting tracked
files.

### 3. Layer A — deterministic checks (per agentic practical)

Run in the temp copy, inside a fresh venv (unless `--fast`):

1. **Environment:** create a throwaway virtualenv, `pip install -r requirements.txt`
   (skip if absent). This is the honest "student starting fresh" test — it catches
   missing or under-pinned dependencies that a shared environment would mask
   (decision: option A, fresh isolated venv per practical).
2. **Config lint:** `.claude/settings.json` parses as valid JSON; every
   `.claude/skills/*/SKILL.md` and `.claude/agents/*.md` has parseable YAML frontmatter
   with `name` and `description`.
3. **Reference integrity:** tool modules referenced as `tools.<x>`, `data/` files, and
   sub-agent names mentioned in `CLAUDE.md` / `SKILL.md` actually exist on disk.
4. **pytest:** `python -m pytest -q` if `tests/` exists.
5. **Smoke commands:** the deterministic commands declared in `verify.yaml` (the "run by
   hand" commands from the README) run with exit code 0.

### 4. Layer B — live Claude checks (per agentic practical, `--live` only)

- Headless invocation in the temp copy: `claude -p '<skill call>'` with permissions
  pre-accepted and a turn cap.
- **Deterministic assertions** declared in `verify.yaml`:
  - `expect_file` — a glob (e.g. `reports/*.md`) that must exist after the run.
  - `expect_contains` / `expect_not_contains` — substrings the produced output/report
    must include or omit (e.g. the unanswerable probe must yield `Not answerable`).
- **Implementation risk to validate first:** confirm `claude -p` invokes project
  slash-commands / skills as expected in headless mode. This is smoke-tested on
  `04-llm-agents` before any manifests are authored.

### 5. Per-practical manifest — `code/practicals/NN-*/verify.yaml`

About 10 lines. Example (`04-llm-agents`):

```yaml
smoke:                      # Layer A — deterministic, must exit 0
  - python -m tools.retrieve "How did gross margin change?" -k 4 > reports/_context.json
  - python -m tools.grade --question "How did gross margin change?" --answer "..." --context reports/_context.json
live:                       # Layer B — only with --live
  - prompt: '/ask "What is NovaCorp customer concentration risk?"'
    expect_file: 'reports/*.md'
    expect_contains: ['concentration']
  - prompt: '/ask "What was NovaCorp net income?"'
    expect_contains: ['Not answerable']
```

A practical with no `verify.yaml` still gets all auto-discovered Layer A checks; the
manifest only adds smoke commands and live checks.

### 6. Notebook practicals (01–03)

Executed via `pytest --nbmake` in a shared base environment; assert no cell errors. These
have no `requirements.txt` today — flagged as a minor gap to either add or document.

### 7. The oddball — `05-business-valuation-example/`

Has 7 skills, no `tools/tests/requirements`. Gets a manifest with **config-lint plus one
representative live flow only** — no pytest, no smoke commands.

---

## Rollout

1. Build `verify.py` + the harness (discovery, repo-safe temp copy, Layer A, table
   output).
2. Prove it end-to-end on **one** practical (`04-llm-agents`), including `--live`, to
   retire the `claude -p` headless risk.
3. Author the ~15 `verify.yaml` manifests.
4. Verify notebook practicals and the `05-*-example` oddball.

## Open items folded into implementation

- Exact `claude -p` permission/turn-cap flags (validated in step 2).
- Whether to add `requirements.txt` to notebook practicals or pin them to the repo base
  env.
```
