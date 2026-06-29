# BOOK_AUDIT_PROJECT_CONTEXT.md

> Factual diagnostic of the **"Large Language Models in Finance"** book repository, produced to let another AI assistant design a rigorous multi-agent review/editing workflow. This report is **diagnostic only** — no chapters, agents, skills, or workflows were created or modified (only this file and the prior scan task were added). Generated 2026-06-20 against branch `master` at commit `bd39f8c`.

---

# 1. Repository overview

* **Project root:** `/Users/juan/Documents/llm-finance-book`
* **Git status:** Clean working tree except two untracked files: `tasks/00_generate_book_audit_context.md` (the instruction file for this task) and this report. Branch `master`, ahead of nothing tracked. `auto_commit: true` is set in `TOPIC.md` — content writes are auto-committed by a hook (see §2).
* **Toolchain / format:** This is a **LaTeX book** (`book` document class, `pdflatex` + `biber`/biblatex), *not* Quarto / Jupyter Book / plain Markdown. The companion course is Markdown + Beamer; companion code is Jupyter notebooks + a (stub) Python package.
* **Build command (book):** `cd book && pdflatex main.tex && biber main && pdflatex main.tex && pdflatex main.tex` (wrapped by `scripts/build-book.sh` and the `/build-book` skill). A compiled `book/main.pdf` (2.5 MB) is present and current.
* **Main book source dir:** `book/` — entry point `book/main.tex`, shared config `book/preamble.tex`, chapters under `book/chapters/NN-slug/chapter.tex`, appendices under `book/appendices/X-slug/chapter.tex`.
* **Output/build artifacts:** `book/main.pdf` plus LaTeX aux files (`.aux/.bbl/.bcf/.log/.toc/.lof/.out`) and `book/_minted/` cache (gitignored). Generated figures live in each chapter's `figures/` subdir and are checked in (see §6).
* **Main config files:** `TOPIC.md` (project config — title, author, audience, `quality_threshold: 8`, `max_refine_iterations: 5`, `auto_commit: true`, git remote), `.claude/CLAUDE.md` (master AI instructions), `.claude/settings.json` (hook wiring + permissions), `book/preamble.tex` (LaTeX packages, `\addbibresource{bibliography.bib}`, custom environments), `code/requirements.txt`.

### Compact tree (heavy/aux folders excluded)

```
llm-finance-book/
├── TOPIC.md                      # project config (read first)
├── README.md
├── .claude/
│   ├── CLAUDE.md                 # master AI instructions
│   ├── settings.json             # hook wiring + permissions
│   ├── agents/   (26 *.md)       # role personas
│   ├── skills/   (29 skill dirs) # SKILL.md workflows
│   └── hooks/    (15 *.sh)       # shell hooks
├── book/
│   ├── main.tex                  # entry; \include order ≠ numeric order (see §3)
│   ├── preamble.tex
│   ├── bibliography.bib          # LIVE bib (332 entries)
│   ├── bibliography.bib.new      # STALE
│   ├── bibliography_bibertool.bib# STALE
│   ├── bibliography_test.bib     # STALE
│   ├── chapters/01..16-*/chapter.tex (+figures/)
│   ├── appendices/A..F-*/chapter.tex (+figures/)
│   ├── backmatter/about-author.tex
│   └── covers/ (TikZ cover variants)
├── course/lectures/01..16-*/     # notes.md, slides.tex, exercises.md (01-07 real, 08-16 stubs)
├── code/
│   ├── src/__init__.py           # EMPTY stub "shared package"
│   ├── tests/__init__.py         # NO tests
│   ├── requirements.txt
│   ├── run_illustrations.sh      # re-runs ch01-07 exercises.ipynb
│   └── notebooks/01..16-*/        # demo.ipynb + exercises.ipynb (+ exercises_executed for 01-07)
├── exercises/
│   └── valuation_example/        # ORPHANED Claude DCF+comps AAPL valuation project (see §5)
├── docs/
│   ├── STATUS.md                 # auto-generated chapter status
│   ├── quality/                  # score JSON + peer-review/editor-feedback md + audits
│   └── superpowers/specs/        # design spec
├── scripts/   (7 *.sh)           # build + validate helpers
├── hooks/     (15 *.sh)          # PORTABLE copies of .claude/hooks (for non-Claude runners)
└── tasks/00_generate_book_audit_context.md
```

**Note:** the top-level `hooks/` directory duplicates `.claude/hooks/` as portable copies for non-Claude AI runners (per README). The live hooks used by Claude Code are in `.claude/hooks/`.

---

# 2. `.claude` and Claude Code setup

All Claude Code configuration is **project-level** (inside the repo). No user-level (`~/.claude`) config was inspected or is required for the audit. No MCP servers are configured in this repo. `.claude/settings.json` contains **no secrets** (nothing to redact).

### Settings (`.claude/settings.json`)

* **PreToolUse · matcher `Bash`** → `hooks/pre-commit-checks.sh` (acts only on `git commit`; chains six sub-checks; blocks on failure).
* **PostToolUse · matcher `Write|Edit`** → in order: `auto-commit.sh`, `score-on-save.sh`, `scaffold-pairs.sh`, `notify-threshold.sh`, `compile-slides.sh`.
* **Stop** → `session-log.sh` (appends to `docs/SESSION_LOG.md` and commits).
* **permissions.allow:** `Bash(git *)`, `Bash(pdflatex *)`, `Bash(biber *)`, `Bash(bash scripts/*)`, `Bash(bash .claude/hooks/*)`, `Bash(python *)`, `Bash(pytest *)`, `Bash(jupyter *)`. No `deny` list.
* `auto_commit`, `quality_threshold` (8), `max_refine_iterations` (5) live in **`TOPIC.md`**, read at runtime by hooks — not in settings.json.

### Hooks (`.claude/hooks/` — all shell)

| Hook | Wired event | What it does |
|------|-------------|--------------|
| `pre-commit-checks.sh` | PreToolUse(Bash) | Dispatcher on `git commit`: runs the six checks below; blocks on exit 1 |
| `check-latex.sh` | (called by above) | Draft `pdflatex` of staged `.tex`; blocks on LaTeX errors |
| `check-refs.sh` | (called) | Flags `\ref`/`\eqref` with no matching `\label` in `book/`; blocks |
| `check-bib.sh` | (called) | Validates required BibTeX fields for `@article/@book/@inproceedings`; blocks |
| `check-notation.sh` | (called) | Advisory: unknown math commands not in preamble; never blocks |
| `check-numbering.sh` | (called) | Advisory: unpaired chapter↔lecture dirs; never blocks |
| `gate-check.sh` | (called) | Blocks commit if any staged file's `docs/quality/*-score.json` dimension < `quality_threshold` |
| `iterate.sh` | not wired | Maps lowest failing dimension → responsible agent; prints guidance |
| `auto-commit.sh` | PostToolUse(Write/Edit) | Auto-commits content file if `auto_commit: true` |
| `score-on-save.sh` | PostToolUse | Reminder to `/score-content` on saved `.tex/.md` |
| `scaffold-pairs.sh` | PostToolUse | On new `chapter.tex`, scaffolds paired lecture+notebook and adds `\include` |
| `notify-threshold.sh` | PostToolUse | Banner when a score JSON first flips `pass:true` |
| `compile-slides.sh` | PostToolUse | Auto-compiles edited `course/lectures/*/slides.tex` |
| `session-log.sh` | Stop | Appends session row to `docs/SESSION_LOG.md`; commits |
| `update-status.sh` | not wired | Regenerates `docs/STATUS.md` from score JSONs (called by `/score-content`) |

### Agents (`.claude/agents/`, 26 files)

| Name | Path (`.claude/agents/…`) | Type | Purpose | Strengths | Limitations | Reuse for book audit |
|------|------|------|---------|-----------|-------------|----------------------|
| scorer | `scorer.md` | agent | Score file on 5 dims → JSON in `docs/quality/` | Drives quality gate; deterministic | Scores only, no fixes; refuses code | **Reuse** (core engine) |
| critic | `critic.md` | agent | Ranked BLOCKER/MAJOR/MINOR issues + fixes | Severity + concrete locations | No rewrites | **Reuse** (skeptical reviewer) |
| peer-reviewer | `peer-reviewer.md` | agent | Referee report ACCEPT/MINOR/MAJOR/REJECT | Publication-grade | No line fixes | **Reuse** |
| hallucination-detector | `hallucination-detector.md` | agent | Fabricated stats/regs/quotes (H1–H6) + code (C1–C5) | Richest agent; text+code | Pattern-based; no live verify | **Reuse** (strongest asset) |
| fact-checker | `fact-checker.md` | agent | Flag claims OK/NEEDS_CITATION/OUTDATED/CHECK | Confidence levels | No internet; no math | **Reuse** (citation/desc accuracy) |
| cross-ref-checker | `cross-ref-checker.md` | agent | `\ref/\eqref/\cite` resolution + ch↔lec pairing | Whole-book; PASS/FAIL | No compile | **Reuse** |
| math-checker | `math-checker.md` | agent | Verify proofs/derivations step by step | Skeptical, notation-aware | No code/stats | **Reuse** (correctness) |
| consistency-checker | `consistency-checker.md` | agent | Cross-chapter symbol/term tables | Inventories; preamble adherence | Book only; no fixes | **Reuse** (notation) |
| code-reviewer | `code-reviewer.md` | agent | Review educational Python/notebooks | Traces logic; checks asserts | Doesn't execute | **Reuse** (code audit) |
| statistics-reviewer | `statistics-reviewer.md` | agent | Stat methodology / p-value / causal language | Catches stat fallacies | No computation | Partial |
| structure-reviewer | `structure-reviewer.md` | agent | Narrative arc, concept ordering, gaps, redundancy | Ordering + gap detection | High-level only | **Reuse** (ordering) |
| pedagogy-reviewer | `pedagogy-reviewer.md` | agent | Backward-design: LO coverage, difficulty curve | LO→content→exercise map | Lecture-focused | Partial |
| accessibility-reviewer | `accessibility-reviewer.md` | agent | Undefined terms, assumed background, captions | Audience-aware | No math/style | Partial (term-before-use) |
| literature-reviewer | `literature-reviewer.md` | agent | Suggest references + BibTeX | Knows when citation needed | Generative; from memory | Partial |
| outline-curator | `outline-curator.md` | agent | 4-pass outline audit (KEEP/MERGE/MOVE/…) | Placement/level labels | Design-time only | **Reuse** (ordering) |
| ssrn-researcher | `ssrn-researcher.md` | agent | Find recent SSRN papers (web) | Structured output | Needs web; abstracts only | No (enrichment) |
| book-writer | `book-writer.md` | agent | Write LaTeX prose/proofs | Uses preamble envs | Generative | No (writer) |
| chapter-surgeon | `chapter-surgeon.md` | agent | Apply minimal patches to a chapter | Surgical BEFORE/AFTER | Implements only | **Reuse** (implementer) |
| code-writer | `code-writer.md` | agent | Write `code/src` + notebook cells | PEP8, docstrings, asserts | Generative | No (writer) |
| cover-designer | `cover-designer.md` | agent | TikZ covers | — | Decorative | No |
| editor | `editor.md` | agent | Improve clarity/flow, preserve meaning | Kills passive/filler | No math | No (refiner) |
| exercise-designer | `exercise-designer.md` | agent | Design `[B]/[I]/[A]` exercises + solutions | 3-tier | Doesn't verify math | No (generative) |
| figure-designer | `figure-designer.md` | agent | TikZ/matplotlib figure code | Compilable; grayscale-safe | No raster gen | Partial (figure fixes) |
| humanizer | `humanizer.md` | agent | Strip AI-sounding patterns | Targets hedges/filler | Phrasing only | No |
| lecture-writer | `lecture-writer.md` | agent | Lecture notes + slides from chapter | Full deck spec | Generative | No |
| proofreader | `proofreader.md` | agent | Grammar/spelling/LaTeX balance | Env-matching | Style/math out of scope | Partial (release gate) |

### Skills (`.claude/skills/`, 29 dirs — selected; full set inventoried)

| Name | Path | Purpose | Reuse for book audit |
|------|------|---------|----------------------|
| audit-hallucinations | `skills/audit-hallucinations/` | **Parallel fan-out** of hallucination-detector over all chapters + SUMMARY | **Reuse** (only book-wide fan-out that exists) |
| audit-bibliography | `skills/audit-bibliography/` | `.bib` missing-field/dup/uncited/undefined-key report | **Reuse** (citation) |
| audit-cross-refs | `skills/audit-cross-refs/` | Broken `\ref/\cite` + unpaired dirs | **Reuse** |
| audit-notation | `skills/audit-notation/` | Symbol/term consistency | **Reuse** |
| full-review | `skills/full-review/` | Sequence score→critique→peer-review→verdict (single file) | **Reuse** (best existing orchestrator) |
| score-content | `skills/score-content/` | scorer → JSON + refresh STATUS.md | **Reuse** |
| refine-until-threshold | `skills/refine-until-threshold/` | Loop: score→fix lowest dim→rescore | **Reuse** (remediation arm) |
| revise-to-acceptance | `skills/revise-to-acceptance/` | Work an editor-feedback file to READY_TO_RELEASE | **Reuse** (remediation) |
| critique | `skills/critique/` | Run critic on one file | **Reuse** |
| peer-review | `skills/peer-review/` | Run peer-reviewer; save report | **Reuse** |
| release-chapter | `skills/release-chapter/` | Gate: score + cross-refs + proofread + compile | **Reuse** (final gate) |
| sync-lecture-chapter | `skills/sync-lecture-chapter/` | Gap report chapter↔lecture | **Reuse** (coverage) |
| split-dual-mode | `skills/split-dual-mode/` | Wrap sections in `context`/`deepdive` boxes | Partial |
| topic-status | `skills/topic-status/` | Status table per chapter/appendix | Partial (dashboard) |
| build-book | `skills/build-book/` | pdflatex+biber compile | Partial (compile check) |
| ssrn-enrich | `skills/ssrn-enrich/` | Add SSRN papers + prose | Partial (enrichment) |
| draft-chapter / draft-lecture / draft-exercises / draft-code / draft-figures | `skills/draft-*/` | Generative authoring pipelines | No (writers) |
| new-topic / interview-me / commit-progress / session-summary / build-slides | `skills/…/` | Scaffolding / config / housekeeping | No |

**Also present (separate, finance-domain, project-scoped):** `exercises/valuation_example/.claude/skills/` (`fetch-financials`, `compute-fcf`, `estimate-wacc`, `run-dcf`, `run-comps`, `validate-accuracy`, `iterate-to-target`) + 7 agents — tooling for the orphaned AAPL valuation exercise (§5), **not** part of the book-audit infrastructure.

### Key overlaps / consolidation notes

1. **Notation auditing in 3 layers:** `consistency-checker` agent / `audit-notation` skill / `check-notation.sh` hook.
2. **Cross-refs in 2–3 layers:** `cross-ref-checker` agent + `audit-cross-refs` skill + `check-refs.sh`/`check-numbering.sh` hooks.
3. **"Citation audit" means three different things:** bib hygiene (`audit-bibliography`), undefined `\cite` keys (`cross-ref-checker`), claim-level need-citation (`fact-checker`). A future workflow must disambiguate.
4. **Scoring is duplicated** in the `scorer` agent AND re-parsed by `gate-check.sh`/`update-status.sh`/`iterate.sh`.
5. **No single book-wide "audit everything" skill exists.** `audit-*` skills are per-dimension; `full-review` is per-file; only `audit-hallucinations` fans out across all chapters. **No figure-content auditor and no concept-ordering fan-out exist.**

---

# 3. Current book structure

The book has **16 chapters + 6 appendices**. Critically, **the printed/reading order in `book/main.tex` is NOT the numeric filename order.** The `\include` order is:

`01 → 16 → 02 → 03 → 08 → 04 → 09 → 14 → 05 → 06 → 10 → 11 → 12 → 13 → 07 → 15`

So filename numbers are essentially internal IDs; **reading position must be derived from `main.tex`, not from the directory name.** This is the single most important structural fact for an ordering audit.

| Reading # | File (`book/chapters/…`) | Title | Topic | Format | Depends on earlier? | Issues noticed |
|----|------|------|------|--------|---------------------|----------------|
| 1 | `01-intro/chapter.tex` (2161 ln) | Introduction | Motivation + condensed preview of the whole representational stack | LaTeX | No | Heavy deliberate overlap w/ ch02 (LSTM, attention, √d_k proof duplicated); forward ref to `def:corpus-vocab` |
| 2 | `16-ai-ml-finance-text/chapter.tex` (712 ln) | AI, ML, and Text in Finance | AI⊃ML⊃DL⊃LLM hierarchy + **book roadmap** | LaTeX | No | **Structural anomaly: numbered 16 but is an intro chapter.** Uses **biblatex `\parencite/\textcite`** while all other chapters use natbib `\citet/\citep` (inconsistent). Leftover TODO `% [CITE: …]` at line 284. Hard-coded "Chapter 2/11/12/13" refs instead of `\ref{ch:…}` |
| 3 | `02-llm-foundations/chapter.tex` (2613 ln, longest) | LLMs: Architecture and Practice | Embeddings → RNN → full Transformer → pretraining → production | LaTeX | ch01 | Long forward ref to `def:scaled-dot-product-attn`; duplicates ch01 RNN/attention |
| 4 | `03-llm-training-finetuning/chapter.tex` (1645 ln) | Training and Fine-Tuning | Data, scaling laws, PEFT/LoRA, RLHF/DPO, DAPT | LaTeX | ch02 | LoRA defined here, **re-derived in ch06 with different notation**; large overlap w/ ch08 |
| 5 | `08-domain-specific-llms/chapter.tex` (907 ln) | Domain-Specific Financial LLMs | FinBERT/BloombergGPT/FinGPT taxonomy, DAPT, benchmarks | LaTeX | ch03 | **No `fig_illustration`, empty `figures/`, no `\illustration` block — breaks the pattern of ch01–07.** Heavy overlap w/ ch03 |
| 6 | `04-llm-agents/chapter.tex` (1504 ln) | LLM Agents and Finance Applications | Agent loop, tools, multi-agent, RAG | LaTeX | ch02/03 | RAG/RRF/chunking duplicated in ch07 (identical k=60) |
| 7 | `09-financial-nlp-sentiment/chapter.tex` (599 ln) | Financial NLP and Sentiment Analysis | Lexicons, FinBERT, event studies | LaTeX | ch02 | Foundation reused by ch10/13/14; Tetlock/Bollen repeated downstream |
| 8 | `14-financial-text-summarization/chapter.tex` (944 ln) | Financial Text Summarization & Extraction | NER, RE, summarization, table extraction | LaTeX | ch09 | Hard-coded "Chapter 13" ref (line 943); overlaps ch09 |
| 9 | `05-business-valuation/chapter.tex` (1240 ln) | LLMs for Business Valuation | DCF, WACC, terminal value, comps, EDGAR/XBRL | LaTeX | ch04 | **Case study uses a stylised composite SaaS firm; the real AAPL Claude exercise (§5) is NOT linked.** Re-defines cosine similarity. Score JSON flags "WACC never derived" |
| 10 | `06-credit-risk/chapter.tex` (1067 ln) | LLMs for Credit Risk Analysis | Scoring, fairness, constrained decoding, calibration | LaTeX | ch03 | LoRA re-derived; AUROC used before defined; **`def:calibration` label collision with ch07** |
| 11 | `10-portfolio-quant-trading/chapter.tex` (927 ln) | Portfolio Optimization & Quant Trading | Markowitz, Black–Litterman, backtesting | LaTeX | ch09 | **Broken hard-coded ref "Chapter~7 on regulatory compliance" (line 923)** — in reading order Chapter 7 is the NLP chapter; compliance is ch11. Large overlap w/ ch13 |
| 12 | `11-regtech-compliance-aml/chapter.tex` (439 ln) | RegTech, Compliance, AML | EU AI Act, SR 11-7, GDPR, AML/RAG | LaTeX | ch04 | **Dangling `\ref{fig:ch11-rag-pipeline}` — figure never defined.** Regulatory content duplicated in ch12/ch15 |
| 13 | `12-xai-explainability/chapter.tex` (892 ln) | Explainability and Interpretability | SHAP/LIME/attention/counterfactuals | LaTeX | ch06 | Regulatory overlap w/ ch11; `def:calibration` collision counterpart |
| 14 | `13-llm-limitations-evaluation/chapter.tex` (976 ln) | LLM Limitations & Rigorous Evaluation | Calibration, leakage, eval rigor, hallucination | LaTeX | ch10/12 | Mis-citation: line 638 cites `fama1970efficient` for FF factors (should be `fama1993common`). Heavy overlap w/ ch10 |
| 15 | `07-applications-future/chapter.tex` (597 ln, shortest) | Other Applications & Future Trends | Synthesis/capstone, deployment patterns, governance | LaTeX | all | Intentional synthesis overlap; `def:calibration` collision counterpart |
| 16 | `15-privacy-local-models/chapter.tex` (459 ln) | Privacy, Local Models, De-identification | DP, federated learning, on-prem, NER de-id | LaTeX | ch03/04 | **Third independent re-introduction of GDPR/MiFID II** (after ch11, ch12) |

### Appendices (`book/appendices/`, reading order A–F, all after chapters)

| ID | File | Title | Lines | Figures |
|----|------|-------|-------|---------|
| A | `A-claude-code/chapter.tex` | Claude Code | 1066 | empty `figures/` |
| B | `B-codex-cli/chapter.tex` | Codex CLI | 688 | empty |
| C | `C-huggingface-local/chapter.tex` | Hugging Face & Local Models | 800 | empty |
| D | `D-sdk-commercial/chapter.tex` | Anthropic SDK & Claude Code SDK (Commercial) | 2271 | empty |
| E | `E-git-github/chapter.tex` | Git & GitHub | 446 | (no figures dir) |
| F | `F-cline/chapter.tex` | Cline | 485 | (no figures dir) |

**Front matter:** title/copyright pages inline in `main.tex`; `\tableofcontents` + `\listoffigures`. **Back matter:** `book/backmatter/about-author.tex` + `\printbibliography`.

**Draft/score status (from `docs/STATUS.md`, partially stale):** STATUS.md lists chapters 8–14 as "Draft: No" — **this is inaccurate**: all 16 chapter.tex files contain substantial content (439–2613 lines). STATUS.md reflects an older state and should not be trusted as a coverage signal.

---

# 4. Concept dependency map

Derived from the **reading order** in §3. "First appears" / "first explained" cite reading position and file.

| Concept | First appears (reading #) | First properly explained | Used before explained? | Notes |
|---------|---------------------------|--------------------------|------------------------|-------|
| AI/ML/DL hierarchy | #2 (ch16) | #2 (ch16) | No | ch16 is the de-facto overview |
| NLP / text-as-data | #1 (ch01) | #2 (ch16) / #7 (ch09) | Borderline | Introduced in ch01, deepened later |
| Tokens / tokenization | #1 (ch01) | #3 (ch02) | Minor | BPE/SentencePiece in ch03/ch08 |
| Embeddings | #1 (ch01, Word2Vec/GloVe) | #1–#3 | No | Re-defined again in ch05 (redundant) |
| Attention | #1 (ch01, full √d_k proof) | #1 and #3 | No | **Duplicated** ch01⇄ch02 |
| Transformers | #1 (ch01) | #3 (ch02, full derivation) | No | ch02 inline TikZ pipeline figure |
| Pretraining (CLM/MLM) | #1 (ch01 `def:mlm`) | #4 (ch03) | Minor | Overlaps ch08 |
| Scaling laws (Chinchilla) | #4 (ch03) | #4 (ch03, full theorem) | No | — |
| Fine-tuning / PEFT / LoRA | #4 (ch03) | #4 (ch03) | No | **Re-derived ch06 with different notation; reused ch05/ch08/ch13** |
| Instruction tuning / RLHF / DPO | #4 (ch03) | #4 (ch03) | No | — |
| Agents / tool use | #6 (ch04) | #6 (ch04) | No | — |
| RAG | #3 (ch02 mention) | #6 (ch04) | Minor | **Duplicated** ch04⇄ch07; reused ch11/13/15 |
| Constrained/structured decoding | #3 (ch02) | #3 (ch02) → #10 (ch06) | No | Re-developed in ch06 |
| Evaluation / metrics | scattered | #14 (ch13) | Yes | AUROC used in ch06 (#10) before its own def later in ch06; eval rigor centralized only at #14 |
| Calibration (ECE, reliability) | #10 (ch06) | #10 (ch06) & #14 (ch13) | No | **`def:calibration` defined twice (ch06 line 382, ch07 line 400) — label collision** |
| Hallucination | #1 (ch01 taxonomy) | #14 (ch13) | Borderline | Mentioned early, rigor late |
| Prompting / CoT / ReAct | #6 (ch04) | #6 (ch04) | No | Reused ch05 |
| Sentiment analysis | #1/#2 | #7 (ch09) | No | Lexicons (Loughran–McDonald) repeated across ch01/09/16 |
| Classification / NER / extraction | #7 (ch09) | #8 (ch14) | No | — |
| Credit risk | #10 (ch06) | #10 (ch06) | No | — |
| Valuation / DCF / WACC | #9 (ch05) | #9 (ch05) | **WACC used but never derived** (flagged in ch05 score) | Real AAPL exercise orphaned (§5) |
| Asset pricing / portfolio | #11 (ch10) | #11 (ch10) | No | Markowitz/BL self-contained |
| Backtesting | #11 (ch10) | #11 (ch10) | No | **Duplicated** ch10⇄ch13 |
| Risk management (CVaR/GARCH) | #11 (ch10) | #11 (ch10, GARCH glossed in one line) | Borderline | GARCH thin on first use |
| Explainability / SHAP | #12 (ch11 by name) | #13 (ch12) | **Yes** — ch11 (#12) references SHAP/attention caveats before ch12 (#13) defines SHAP | Reorder or back-reference |
| Regulatory (EU AI Act, SR 11-7, GDPR, MiFID) | #1 (ch01) | #12 (ch11) | Scattered | **Re-introduced from scratch 3×: ch11, ch12, ch15** |
| Privacy / DP / de-identification | #16 (ch15) | #16 (ch15) | No | Last chapter |
| Statistical primitives (KL divergence, n-gram, CAPM, cross-entropy, softmax) | various | **never / late** | **Yes** | `undefined-terms-audit.md` flags KL divergence, n-gram, CAPM as *never defined anywhere*; cross-entropy & softmax used before definition |

**Concepts used before introduced (priority flags):**
1. **Statistical primitives never defined** — KL divergence, n-gram, CAPM (per `docs/quality/undefined-terms-audit.md`).
2. **SHAP** referenced in ch11 (reading #12) before its definition in ch12 (#13).
3. **AUROC** used in ch06 before its own later subsection.
4. **WACC** used throughout ch05 but never derived (no CAPM/WACC subsection) — the orphaned exercise contains exactly this.
5. **Evaluation rigor** centralized only at reading #14, after many chapters that already make empirical claims.

---

# 5. Finance examples inventory

| Example | Location | Finance area | Technical concept | Complete/partial | Notes |
|---------|----------|--------------|-------------------|------------------|-------|
| AAPL DCF+comps valuation **using Claude** | `exercises/valuation_example/` | Equity valuation | Multi-agent + structured output | **Complete & passing** (2.56% error vs $226.84) | **ORPHANED — not referenced in any chapter/lecture (see below)** |
| Stylised SaaS DCF case study | ch05 §`subsec:bv-pipeline-casestudy` | Valuation | End-to-end pipeline | Complete (illustrative figures) | Composite company, not AAPL |
| AAPL DCF sensitivity heatmap | ch05 `fig_illustration.pdf` | Valuation | WACC×g sensitivity | Complete | matplotlib via notebook |
| Tetlock WSJ negativity → DJIA | ch01, ch09, ch16 | Sentiment/returns | Dictionary methods | Complete | Repeated 3× |
| Loughran–McDonald 10-K sentiment | ch01, ch08, ch09, ch16 | Sentiment | Finance lexicon | Complete | Repeated |
| EDGAR 10-K text-growth | ch01 `fig_edgar_text_growth` | Filings | Data trend | Complete | Live SEC fetch script |
| Apple Card gender-bias scandal | ch06 | Credit/fairness | Disparate impact | Complete | — |
| Constrained-decoding PD example | ch06 | Credit | Structured generation | Complete | verbatim grammar |
| Two-agent EPS beat/miss extractor | ch04 | Earnings | Tool-calling pipeline | Partial (notebook stub) | demo.ipynb |
| Multi-agent equity research (5 agents) | ch04 | Research | Multi-agent orchestration | Partial | conceptual |
| Tesla 10-K liquidity ReAct trace | ch04 | Filings | ReAct + retrieval | Complete (illustrative) | — |
| GameStop/WSB, SVB bank-run, NVIX | ch09 | Sentiment/risk | Event studies | Complete | — |
| Black–Litterman on 100 S&P 500 firms | ch10 | Portfolio | BL views from LLM | Complete (illustrative) | — |
| 8-K SEC-investigation auto position cut | ch10 | Trading/risk | Event-triggered agent | Complete | verbatim JSON |
| AML adverse-media / UBO chains | ch11 | Compliance/AML | RAG + entity resolution | Complete (illustrative) | — |
| Hybrid credit pipeline (GBT+BERT+GPT-4o) | ch12 | Credit/XAI | SHAP adverse action | Complete | verbatim prompt |
| ECE on credit classifier (worked to 0.115) | ch13 | Credit/eval | Calibration | Complete | — |
| Microsoft Q3-2023 earnings NER | ch14 | Earnings | NER/extraction | Complete | — |
| French mortgage NER de-identification | ch15 | Privacy | NER masking | Complete | — |

### The "business valuation exercise using Claude" — FOUND, but ORPHANED

* **It exists and is complete.** `exercises/valuation_example/` is a full Claude Code multi-agent project that values **Apple (AAPL)** to within 10% of the FY2024 reference price ($226.84). Methodology = **50% two-stage DCF + 50% comps**, triangulated: DCF per-share with **CAPM-derived WACC ~8.84%**, 5-yr FCF/share CAGR stage 1, 3% Gordon-growth terminal value; comps via NTM P/E and EV/EBITDA vs MSFT/GOOGL/META. The committed run **passed at 2.56% error** ($221.04 vs $226.84, 0 iterations — `results/accuracy.json`).
* **Mechanics:** 7 agents (`edgar-fetcher`, `financial-analyst`, `wacc-estimator`, `dcf-modeler`, `comps-analyst`, `assumption-auditor`, `accuracy-checker`), 7 skills (`fetch-financials`, `compute-fcf`, `estimate-wacc`, `run-dcf`, `run-comps`, `validate-accuracy`, `iterate-to-target`), and a master Workflow-API script `workflows/orchestrate-valuation.js` (5 phases, 6 JSON schemas, numeric fallbacks). Inputs in `data/`, outputs in `results/` (already populated), assumptions in `assumptions/base-case.md`. Parallel runner files for Claude/Cline/Codex (`CLAUDE.md`, `AGENTS.md`, `.clinerules`).
* **Integration status: NONE.** `grep -rn "valuation_example" book/ course/` → **0 matches**. ch05 never references `exercises/`. The chapter and the exercise independently cover the same methodology. **ch05's own score JSON flags "WACC never derived" as a completeness gap — the orphaned exercise is exactly the missing material.** Wiring it in is a concrete, high-value action item for the future workflow.

---

# 6. Code and figure-generation inventory

| File | Language | Purpose | Generates figures? | Used in chapter(s) | Tests? | Risks |
|------|----------|---------|--------------------|--------------------|--------|-------|
| `code/src/__init__.py` | Python | "Shared package" — **docstring only, no code** | No | (none import it) | No | Empty shell; intended architecture not built |
| `code/tests/__init__.py` | Python | Test marker — **no tests** | No | — | No | Zero coverage; pytest declared, unused |
| `code/requirements.txt` | text | Deps (numpy/pandas/matplotlib/scipy/sklearn/gensim/yfinance/scienceplots/nbconvert…) | — | — | — | No `setup.py`/`pyproject.toml` → `src` not installable |
| `code/notebooks/NN-*/demo.ipynb` (16) | Jupyter | Topic demos | No | referenced as stubs in chapters | No | Mostly TODO/placeholder |
| `code/notebooks/NN-*/exercises.ipynb` (16) | Jupyter | Exercises; ch01–07 embed matplotlib that writes `fig_illustration.pdf` | **Yes (ch01–07)** | ch01–07 | No | In-place execution; non-deterministic (yfinance) |
| `code/notebooks/01-07/exercises_executed.ipynb` | Jupyter | Committed executed copies | (output) | ch01–07 | No | Can diverge from source `.ipynb` |
| `code/notebooks/01-intro/gen_edgar_text_growth.py` (212 ln) | Python | SEC EDGAR fetch → text-growth plot | **Yes** | ch01 | No | **Live SEC fetch; hard-codes personal User-Agent email `jfimbett@gmail.com`** |
| `code/notebooks/01-intro/gen_king_analogy.py` (101 ln) | Python | GloVe PCA king–queen plot | **Yes** | ch01 | No | Downloads ~1GB GloVe; slow/non-deterministic |
| `code/notebooks/01-intro/edgar_text_stats_cache.json` | JSON | Cached EDGAR stats | — | ch01 | — | Committed cache; ages over time |
| `code/run_illustrations.sh` (25 ln) | bash | Re-runs ch01–07 `exercises.ipynb` to regen figures | Drives gen | ch01–07 | No | Covers only 7 chapters; mutates notebooks; 180s timeout |
| `book/chapters/02-*/chapter.tex` (lines 657–768) | LaTeX/TikZ | Inline Transformer pipeline figure | **Yes (TikZ)** | ch02 | n/a | Figure source is inline, not a file |
| `scripts/build-book.sh` | bash | pdflatex+biber compile | No | — | n/a | **Build does NOT regenerate figures** — relies on committed PDFs |

### Figure mechanics

* **Three figure mechanisms (hybrid):** (1) `fig_illustration.pdf` — matplotlib/scienceplots embedded **inside `exercises.ipynb`** (ch01–07 only); (2) ch01-specific figures — standalone `gen_*.py` scripts; (3) **inline TikZ** in `chapter.tex` (ch02 pipeline, covers, preamble).
* **Where stored / tracked:** each chapter's `figures/` subdir; PDFs are git-tracked via a `.gitignore` re-include (`!book/chapters/*/figures/*.pdf`). **Actual files present:** ch01 (`fig_edgar_text_growth.pdf/png`, `fig_illustration.pdf`, `fig_king_analogy.pdf/png`), ch02–07 (`fig_illustration.pdf` each). **ch08–16 and all appendices have only empty `.gitkeep`.**
* **Coverage gap:** 9 of 16 chapters (ch08–16) and all appendices ship **no figures**. ch08 uniquely also lacks the `\illustration` block that ch01–07 have.
* **Dangling reference:** ch11 cites `\ref{fig:ch11-rag-pipeline}` but no figure float is defined.
* **Reproducibility:** partial and fragile — depends on live SEC/EDGAR, ~1GB GloVe download, and live yfinance market data (output drifts). No deterministic seeds/snapshots.
* **Stale files:** committed `exercises_executed.ipynb` (ch01–07) and `edgar_text_stats_cache.json` age vs sources.
* **Tests/validation:** **none.** `code/tests/` is empty; no `def test_`/`import pytest` anywhere; `build-book.sh` never runs nbconvert; figure correctness is never validated.
* **Code in chapters:** chapters contain almost no typeset code — only ch03 and ch05 have a `minted` listing (both prompt strings); ch05/06/10/12/14 use `verbatim` for URLs/JSON/prompts. Everything else is externalized to notebook stubs. **No runnable `lstlisting`/`minted` code blocks of substance exist in the chapters.**

---

# 7. Bibliography and citation inventory

* **Live bibliography:** `book/bibliography.bib` (**332 entries**), loaded by `book/preamble.tex` (`\addbibresource{bibliography.bib}`). Engine = **biblatex + biber**.
* **Stale duplicates (delete candidates):** `book/bibliography.bib.new` (262), `book/bibliography_bibertool.bib` (308), `book/bibliography_test.bib` (178) — none referenced by the build; all last touched 2026-06-17 (older than the live file). Each holds 4–13 keys absent from the live file (none currently cited).
* **Usage:** **804** `\cite…` commands across chapters+appendices; **323 unique keys**.
* **Missing keys (cited, undefined): NONE** — all 323 resolve.
* **Duplicate key:** `wei2022emergent` defined **twice** (`bibliography.bib` lines 1727 & 3175; near-identical, one has an arXiv `note`). biber keeps one arbitrarily; delete the redundant block.
* **Uncited entries (defined, never cited): 9** — `bertsimas1998optimal`, `desai2020calibration`, `goodfellow2016deep`, `goyal2019counterfactual`, `huang2023finbert_tone`, `jegadeesh1993returns`, `kogan2021technology`, `wei2022emergent`, `zhong2021qmsum`.
* **Incomplete entry:** `xu2024stock` is a stub (`author = {Xu, Zhiyuan and others}`, `note = {… Author list and venue to be verified before final release}`) — unresolved.
* **Malformed keys / missing required fields: NONE** (all keys match `^[A-Za-z0-9_:.\-]+$`; required fields present throughout).

### Selected citation keys → chapters (sample for verification table)

| Citation key | Bib file | Cited in (sample) | Description in BibTeX | Obvious issue |
|--------------|----------|-------------------|-----------------------|---------------|
| `vaswani2017attention` | bibliography.bib | ch01,02,16 | Attention Is All You Need (2017) | OK |
| `hoffmann2022chinchilla` | bibliography.bib | ch03 | Chinchilla scaling (2022) | OK |
| `hu2022lora` | bibliography.bib | ch03,05,06,08 | LoRA (2022) | OK — but heavily reused |
| `loughran2011liability` | bibliography.bib | ch01,08,09,16 | Loughran–McDonald lexicon (2011) | OK |
| `fama1993common` | bibliography.bib | ch10 | FF 3-factor | **ch13 line 638 cites `fama1970efficient` where this is correct source** |
| `fama1970efficient` | bibliography.bib | ch13 | EMH (1970) | **Mis-applied to FF factors in ch13** |
| `wei2022emergent` | bibliography.bib | (uncited) | Emergent abilities | **Duplicate entry + uncited** |
| `xu2024stock` | bibliography.bib | (varies) | stub | **Incomplete — author/venue placeholder** |
| `kang2023hallucination` | bibliography.bib | ch13 | EDGAR numerical hallucination | **Prior hallucination audit flagged as possible phantom — verify it is real** |

### Papers needing **content** verification later (claims attributed to specific results)

These chapters make specific numeric claims attributed to papers — fact-check the described result against the source: `tetlock2007giving` (WSJ negativity), `KirtacGermano2024` (Sharpe 3.05 / 74.4% accuracy, ch09/10), `bollen2011twitter` (86.7% directional, ch09), `wu2023bloomberggpt` (708B-token corpus, benchmark numbers), `chen2021finqa` (FinQA accuracies, ch08), `kang2023hallucination` (15–30% wrong numbers, ch13), `VidalSSRN2024` (59.4%, ch13), `LopezLiraTang2023` (headline strategy), `zhang2024financebench` (~80%), `argyle2023out` (silicon sampling, ch06), `chouldechova2017fair` (impossibility theorem, ch07/12). The existing `docs/quality/bibliography-audit.md` is **stale** (297-entry snapshot, says "no duplicates" — no longer true).

---

# 8. Existing quality-control mechanisms

| Mechanism | Path / command | Checks | Usable now? | Gaps |
|-----------|----------------|--------|-------------|------|
| Pre-commit LaTeX/ref/bib/notation/numbering/gate | `.claude/hooks/pre-commit-checks.sh` + 6 sub-hooks | Compile, undefined refs, bib fields, notation lint, dir pairing, score gate | Yes (on `git commit`) | Notation/numbering advisory only; gate needs score JSON to exist |
| 5-dimension scorer | `scorer` agent + `/score-content` → `docs/quality/*-score.json` | clarity/rigor/completeness/pedagogy/style (0–10), threshold 8 | Yes | Subjective; no finance-orientation/ordering/repetition dimensions; **STATUS.md is stale** |
| Hallucination audit (book-wide) | `/audit-hallucinations` → `docs/quality/hallucination-audit/` | Fabricated stats/regs/quotes (H1–H6) + code (C1–C5) | Yes (only book-wide fan-out) | Pattern-based; no live web verification |
| Bibliography audit | `/audit-bibliography` → `docs/quality/bibliography-audit.md` | Missing fields, dupes, uncited, undefined keys | Yes | Current report is stale (see §7) |
| Cross-ref audit | `/audit-cross-refs` (cross-ref-checker) | `\ref/\cite` resolution + pairing | Yes | Won't catch hard-coded "Chapter N" prose refs |
| Notation audit | `/audit-notation` (consistency-checker) | Symbol/term consistency | Yes | Book chapters only |
| Undefined-terms audit | `docs/quality/undefined-terms-audit.md` (one-off) | Terms used before/without definition, in reading order | Report exists | Not a re-runnable skill |
| Full review (per file) | `/full-review` | score→critique→peer-review→verdict | Yes | Single file, serial; no book-level roll-up |
| Refine / revise loops | `/refine-until-threshold`, `/revise-to-acceptance` | Iterate to threshold / work feedback file | Yes | Dimension→agent maps overlap; can hit max-iter |
| Release gate | `/release-chapter` | score + cross-refs + proofread + compile | Yes | Per-chapter |
| Build compile | `/build-book`, `scripts/build-book.sh` | pdflatex+biber + error extraction | Yes | Does **not** regenerate figures or run notebooks |
| Chapter↔lecture sync | `/sync-lecture-chapter` | Heading-level gap report | Yes | Headings only |
| Figure-generation runner | `code/run_illustrations.sh` | Re-runs ch01–07 notebooks | Partial | 7 of 16 chapters; no validation |
| Code tests | `code/tests/` + pytest (in reqs) | (nothing) | **No — empty** | Zero tests despite pytest declared |
| Notebook execution check | — | — | **Missing** | No CI/nbconvert validation of demo/exercise notebooks |
| Link checker | — | — | **Missing** | No URL/DOI validation |
| Spell checker | — | — | **Missing** | Relies on proofreader agent |

**Missing mechanisms useful for the future workflow:** book-level (cross-chapter) score roll-up; finance-orientation scorer; concept-ordering / repetition fan-out auditor; figure-content auditor (does the figure match the prose claim?); notebook-execution CI; a re-runnable undefined-terms/ordering skill; hard-coded "Chapter N" prose-reference detector; description-accuracy (paper-claim) checker.

---

# 9. Proposed audit architecture (based only on current setup — not implemented)

The repo already has a strong **per-file, per-dimension** toolkit (scorer, critic, peer-reviewer, hallucination-detector, the audit-* skills). What is missing is a **book-wide orchestration layer**, **finance/ordering/repetition dimensions**, and a **two-contrarian-reviewer + editor + implementer** loop. Recommendations:

| Proposed component | New or modify? | Reason | Files likely affected |
|--------------------|----------------|--------|-----------------------|
| `/goal` (audit goal/rubric anchor) | New | No canonical rubric file exists; pin the 12 dimensions + 90% target | `.claude/skills/goal/`, `docs/quality/RUBRIC.md` |
| Chapter-level scoring (extended dims) | Modify `scorer` | Add correctness, concept-separation, ordering, repetition, finance-orientation, citation-accuracy, code-correctness to the existing 5 | `.claude/agents/scorer.md`, score JSON schema |
| Book-level scoring / roll-up | New | No cross-chapter aggregate exists; needed for "progressive path" + global repetition | `.claude/skills/audit-book/`, `docs/quality/BOOK_SCORE.md` |
| Constructive reviewer agent | New (sibling of `critic`) | Reward identifying what is correct/coherent/worth preserving (prevents over-rewriting) | `.claude/agents/constructive-reviewer.md` |
| Skeptical reviewer agent | Modify `critic` | Already blunt-flaw-oriented; extend to repetition/finance-gap/citation-weakness | `.claude/agents/critic.md` |
| Editor/orchestrator | New (reuse `revise-to-acceptance` patterns) | Diff the two reviews → implementation plan | `.claude/agents/audit-editor.md`, `.claude/skills/audit-chapter/` |
| Implementer | Reuse `chapter-surgeon` | Already does minimal patches | `.claude/agents/chapter-surgeon.md` |
| Citation auditor | Reuse `audit-bibliography` + `fact-checker` + new description-accuracy agent | Bib hygiene exists; **paper-description accuracy does not** | `.claude/skills/audit-bibliography/`, new `description-checker.md` |
| Code/figure auditor | New | No figure-content auditor; `code-reviewer` doesn't execute | `.claude/agents/figure-auditor.md`, notebook-exec skill |
| Finance-examples auditor | New | No agent checks finance density/quality/integration (e.g. orphaned valuation exercise) | `.claude/agents/finance-auditor.md` |
| Concept-ordering auditor | Reuse `structure-reviewer` + `outline-curator`, add fan-out | Exists per-file; needs book-wide ordering pass keyed to `main.tex` order | `.claude/skills/audit-ordering/` |
| Final regression workflow | New | Re-run all audits + compile after edits | `.claude/skills/audit-book/` (final phase) |
| Scorecard format | New | Standardize 12-dim 0–100 JSON per chapter + book | `docs/quality/RUBRIC.md`, schema |
| Loop until ≥90%/dimension | New (reuse `refine-until-threshold` shape) | Drive each chapter to target on every dimension | `.claude/skills/audit-chapter/`, `iterate.sh` |

**Strong build-on assets:** `audit-hallucinations` is the only existing book-wide parallel fan-out — model the new auditors on it. `full-review` is the best existing per-file orchestrator — generalize it. The Workflow API (already used in `exercises/valuation_example/workflows/orchestrate-valuation.js`) is a proven pattern in this repo for multi-agent fan-out.

---

# 10. Recommended scoring rubric draft (strict; 0–100 per dimension; ≥90 = release)

| Dimension | 0 | 50 | 90 | 100 | Evidence required |
|-----------|---|----|----|-----|-------------------|
| **Correctness of explanations** | Factually wrong claims | Mostly right, some imprecise | All claims correct & precise; no overclaiming | Independently re-derivable; every assertion sourced | math-checker + fact-checker pass; no H-class hallucinations |
| **Concept vs under-the-hood separation** | Mixes intuition & internals indiscriminately | Some signposting | Big-picture and technical clearly delineated (e.g. context/deepdive boxes) | Reader can follow either layer alone | Section-type tagging; structure-reviewer |
| **Code/figure correctness** | Code wrong or figures contradict prose | Runs but not validated | Code runs deterministically; figures match claims | Reproducible from seed; tested | Notebook executes; figure-auditor confirms claim↔figure |
| **Topic introduction & ordering** | Concepts used before defined | A few forward refs | Every concept defined before use **in reading order** | Optimal pedagogical order | Concept-ordering audit vs `main.tex` order; zero use-before-def |
| **Progressive learning path** | No build-up | Uneven jumps | Each chapter builds on prior, smooth difficulty curve | Explicit bridges between chapters | Dependency map; pedagogy-reviewer |
| **Non-repetition** | Same material re-derived verbatim | Some overlap | Overlap is intentional & cross-referenced, not re-derived | Single source of truth per concept | Cross-chapter dedup (LoRA, attention, RAG, regulatory) |
| **Finance orientation** | Generic ML, finance bolted on | Finance examples present but shallow | Finance-first framing; concepts motivated by finance problems | Every technique tied to a real finance use case | finance-auditor density + relevance |
| **Finance example quality** | Toy/fabricated | Illustrative but not grounded | Realistic, grounded, integrated (not orphaned) | Backed by data/exercise reader can run | finance-auditor; integration check (cf. orphaned valuation) |
| **BibTeX citation correctness** | Missing/malformed/duplicate keys | Minor field gaps | All keys resolve, no dupes/stubs, fields complete | Clean + DOIs verified | audit-bibliography pass; no stub/dup |
| **Paper-description accuracy** | Misattributes results | Roughly right | Described result matches source exactly | Verified against the paper | description-checker (e.g. fama1970 vs fama1993) |
| **Coverage / missing material** | Major gaps (e.g. WACC never derived) | Some gaps | No critical concept/warning/bridge missing | Comprehensive incl. caveats | undefined-terms audit; completeness pass |
| **Notation & cross-ref integrity** | Undefined refs, label collisions | Some inconsistency | All refs resolve; consistent notation; no collisions | Uniform symbols book-wide | cross-ref + notation audits (catch `def:calibration`, dangling fig) |

A chapter scores ≥90 **only** when correct, progressively ordered, non-repetitive, finance-oriented, properly cited with accurately described papers, and supported by working code/figures — not merely readable.

---

# 11. Risks and unknowns

| Risk | Evidence | Why it matters | Suggested next step |
|------|----------|----------------|---------------------|
| Reading order ≠ filename order | `main.tex` `\include` order is `01,16,02,03,08,04,…` | Every ordering/dependency audit must key off `main.tex`, not dir names | Parse `main.tex` order as ground truth in all auditors |
| ch16 is an intro but numbered/placed oddly + uses different cite package | ch16 uses `\parencite/\textcite`; others use `\citet/\citep` | Citation-style inconsistency; structural confusion | Decide ch16's role; unify cite commands |
| Orphaned valuation exercise | `grep valuation_example book/` → 0 hits; ch05 score flags "WACC never derived" | High-value finance asset disconnected; reader can't reach it | Wire `exercises/valuation_example/` into ch05 |
| No figures for ch08–16 + appendices | only `.gitkeep` present | Visual learning gaps; dangling `fig:ch11-rag-pipeline` | Generate figures; fix dangling ref |
| Figures not reproducible / no tests | live SEC/GloVe/yfinance; empty `code/tests/` | Can't regenerate or trust figures; numbers drift | Add seeds/snapshots + notebook-exec CI |
| Empty shared package | `code/src/__init__.py` is docstring only | Claimed architecture (notebooks→src) doesn't exist | Decide: build `src` or drop the claim |
| Stale bib files + duplicate key | 3 unused `.bib` + `wei2022emergent` dup | Confusion; biber picks arbitrarily | Delete stale bibs; dedupe |
| Stale audit reports / STATUS.md | bib audit says "no dup" (false); STATUS says ch08–14 undrafted (false) | Misleads any workflow that trusts them | Re-run audits fresh; regenerate STATUS |
| Heavy cross-chapter repetition | LoRA (×4), attention (ch01⇄02), RAG (ch04⇄07), regulatory (ch11/12/15) | Hurts non-repetition + progression dimensions | Designate single source per concept; back-reference |
| Use-before-define + label collision | SHAP (ch11 before ch12), AUROC, KL/n-gram/CAPM never defined; `def:calibration` ×2 | Correctness/ordering failures | Ordering pass + define primitives + fix labels |
| Hard-coded prose chapter refs | ch10 "Chapter~7 on regulatory compliance" (wrong); ch14 "Chapter 13"; ch16 several | Break silently when chapters reorder | Replace with `\ref{ch:…}`; add prose-ref detector |
| Agents/skills overlap | 3-layer notation/cross-ref/citation tooling | Future workflow may double-run or conflict | Consolidate per §2 overlaps before scaling |
| Paper-claim accuracy unverified | Many specific stats attributed to papers (§7) | Description-accuracy dimension can't pass without checks | Build description-checker with web access |
| No book-level scoring | Only per-file score JSON exists | Can't measure progression/global repetition | Add book-level roll-up |

---

# 12. Exact files another assistant should read next

| Priority | File/folder | Why it matters |
|----------|-------------|----------------|
| 1 | `book/main.tex` | Ground-truth reading order (≠ filename order) — basis for all ordering audits |
| 2 | `TOPIC.md` | Audience, quality threshold (8), auto-commit, max iterations |
| 3 | `.claude/CLAUDE.md` | Master conventions the workflow must respect |
| 4 | `.claude/agents/scorer.md`, `critic.md`, `hallucination-detector.md`, `structure-reviewer.md` | The reusable scoring/critique/ordering engines to extend |
| 5 | `.claude/skills/audit-hallucinations/SKILL.md` | The only book-wide parallel fan-out — template for new auditors |
| 6 | `.claude/skills/full-review/SKILL.md`, `refine-until-threshold/SKILL.md`, `revise-to-acceptance/SKILL.md` | Existing orchestration + remediation loops to generalize |
| 7 | `exercises/valuation_example/` (`workflows/orchestrate-valuation.js`, `.claude/`) | The orphaned valuation exercise + a proven multi-agent Workflow pattern in-repo |
| 8 | `book/chapters/05-business-valuation/chapter.tex` + its score JSON | Concrete case of a coverage gap (WACC) the exercise would fill |
| 9 | `docs/quality/undefined-terms-audit.md`, `hallucination-audit/SUMMARY.md`, `bibliography-audit.md` | Prior findings (some stale) — don't re-discover; do re-verify |
| 10 | `.claude/settings.json` + `.claude/hooks/` | Hook wiring (auto-commit, gate-check) the workflow runs inside |
| 11 | `book/preamble.tex` | Custom environments (context/deepdive/illustration), bib resource, notation `\newcommand`s |
| 12 | `book/bibliography.bib` | The 332-entry live bib for citation + description audits |
| 13 | `code/run_illustrations.sh`, `code/notebooks/01-intro/gen_*.py` | How figures are actually generated (and their fragility) |
| 14 | `docs/STATUS.md` | Useful as a dashboard target — but currently stale, regenerate |

---

# Executive summary for ChatGPT

**What the project is.** A single-author academic/practitioner **book** "Large Language Models in Finance" (LaTeX, `pdflatex`+biber/biblatex) with a parallel Markdown/Beamer **course** and Jupyter **code** companion. It is heavily instrumented for AI-assisted authoring via Claude Code (26 agents, 29 skills, 15 hooks). Config lives in `TOPIC.md` (quality threshold 8/10, auto-commit on). Root: `/Users/juan/Documents/llm-finance-book`, branch `master`.

**Book structure.** 16 chapters + 6 appendices, all substantively drafted (439–2613 lines each). **Crucial gotcha: reading order is set by `book/main.tex`'s `\include` list and is NOT the filename-number order** — it runs `01, 16, 02, 03, 08, 04, 09, 14, 05, 06, 10, 11, 12, 13, 07, 15`, then appendices A–F. ch16 is logically the intro despite its number, and it uses a different citation package (`\parencite/\textcite`) than the rest (`\citet/\citep`). Figures exist only for ch01–07; ch08–16 + appendices have none. The book compiles (`book/main.pdf` present).

**Claude setup that already exists and is reusable.** A strong **per-file, per-dimension** toolkit: `scorer` (5 dims → JSON), `critic`, `peer-reviewer`, `hallucination-detector` (richest agent), `fact-checker`, `cross-ref-checker`, `consistency-checker`, `math-checker`, `code-reviewer`, `structure-reviewer`, `outline-curator`, plus implementer `chapter-surgeon`. Skills: `audit-hallucinations` (**the only book-wide parallel fan-out** — the template to copy), `audit-bibliography/-cross-refs/-notation`, `full-review` (best per-file orchestrator), `refine-until-threshold` + `revise-to-acceptance` (remediation loops), `release-chapter` (gate). Hooks enforce compile/ref/bib/score gates at commit. The Workflow API is already used in-repo (`exercises/valuation_example/workflows/orchestrate-valuation.js`).

**What is missing.** (1) No **book-level** scoring/roll-up — only per-file JSON. (2) The 5-dim rubric lacks **correctness, concept-separation, ordering, repetition, finance-orientation, citation-description-accuracy, code/figure-correctness** dimensions. (3) No **two-contrarian-reviewer (constructive + skeptical) → editor → implementer** loop. (4) No **figure-content**, **finance-example**, **paper-description-accuracy**, or **book-wide concept-ordering** auditors. (5) No notebook-execution CI; `code/tests/` and `code/src/` are empty stubs; figures aren't reproducible. (6) Prior audit reports (bibliography, STATUS.md) are **stale**.

**Concrete defects already found (seed the first audit pass).** Orphaned **AAPL DCF+comps valuation-with-Claude exercise** under `exercises/valuation_example/` not linked from ch05 (which itself is flagged for "WACC never derived"); duplicate bib key `wei2022emergent`; mis-citation in ch13 (`fama1970efficient` for FF factors → should be `fama1993common`); dangling `\ref{fig:ch11-rag-pipeline}`; **`def:calibration` label defined twice** (ch06 & ch07); broken hard-coded prose ref "Chapter 7 on regulatory compliance" in ch10; statistical primitives (KL divergence, n-gram, CAPM) never defined; SHAP used in ch11 before its ch12 definition; heavy repetition of LoRA/attention/RAG/regulatory frameworks; 3 stale `.bib` files; `xu2024stock` stub citation.

**Highest-priority design decisions.** (a) Make `main.tex` reading order the ground truth for every ordering/dependency check. (b) Extend the rubric to the 12 dimensions and add **book-level** scoring. (c) Build the constructive+skeptical reviewer pair, an editor that diffs them into a plan, and reuse `chapter-surgeon` as implementer — fan out per chapter like `audit-hallucinations`. (d) Decide whether to wire in the orphaned valuation exercise and whether to build the empty `code/src`/tests or drop those claims. (e) Consolidate the overlapping notation/cross-ref/citation tooling before scaling.

**Recommended next steps.** 1) Read the §12 files (start with `book/main.tex`). 2) Write a canonical `docs/quality/RUBRIC.md` (12 dims, 0–100, ≥90 release) and a `/goal` anchor. 3) Author one book-wide fan-out skill modeled on `audit-hallucinations` that runs constructive+skeptical reviewers per chapter, then an editor→`chapter-surgeon` remediation loop iterating to ≥90/dimension, ending with a regression pass (re-run all `audit-*` + compile). 4) Re-run the stale bibliography/undefined-terms audits fresh rather than trusting the committed reports. 5) Treat the seed-defect list above as the first concrete backlog.
