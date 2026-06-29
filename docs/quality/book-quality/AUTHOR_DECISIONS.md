# AUTHOR_DECISIONS.md — Decisions you need to make

> **ALL RESOLVED & APPLIED (2026-06-20).** Status of each:
> - **A1** chen2025aml → replaced with the real `lin2025risktagger` (RiskTagger,
>   arXiv:2510.17848) you found; cited honestly in ch11 Further Reading as an
>   LLM-agent-for-AML example (it is a Web3/crypto annotation paper, *not* the Adverse
>   Media Index, so AMI stays the book's own construct). ✅
> - **A2** keep all numerics hedged. ✅ (no change)
> - **A3** keep `claude-opus-4-5` placeholder id. ✅ (no change)
> - **B1** deleted `bibliography_bibertool.bib` + `bibliography_test.bib`. ✅
> - **B2** dropped the "shared package" claim (README + `code/src/__init__.py`). ✅
> - **C1** leave king-analogy figure pinned-documented. ✅ (no change)
> - **D1** keep ch16 as Chapter 2 (already its conventional background slot). ✅ (no change)
> - **D2** fixed the doubled title on the title page; added a frontmatter "About This Book"
>   section. ✅
>
> Book still passes the full regression after these edits (628 pp, clean). The original
> decision text is kept below for reference.

---

> The book passed the release-quality gate (16/16 chapters ≥90, clean compile). None of the
> items below block that pass. They are decisions only **you** can make — citation
> verification, repo hygiene, and a few style/structure calls. Write your answer on the
> `Your decision:` line under each item. Where I had to choose a safe default to keep the
> book consistent, I say so and you can override it.

---

## A. Citation integrity (please decide before publishing)

### A1. The fabricated-looking `chen2025aml` entry
**Context.** `bibliography.bib` had `@article{chen2025aml}` with arXiv id `2602.23373`,
which decodes to **February 2026** (a future date, inconsistent with `year=2025`). I could
not verify the paper exists. It was the *sole* source backing the "Adverse Media Index"
(AMI) construct in ch11.
**What I did (safe default).** Removed all 3 citations to it; the AMI is now presented as
*this book's own construct* ("a practical template; calibrate before relying on it"). The
bib entry is now `@unpublished`, the fake id stripped, marked `NEEDS_EXTERNAL_VERIFICATION`,
and **uncited**.
**Options.** (a) Confirm the paper is real → give me the correct title/authors/id and I'll
restore the citation and the AMI attribution. (b) It does not exist / you can't find it →
I delete the entry entirely and the AMI stays as the book's construct (recommended if
unverifiable).
**My recommendation:** (b) unless you can produce a real source.
**Your decision:**

I found this on arxiv, if its real then keep it as a working paper

RiskTagger: An LLM-based Agent for Automatic Annotation of Web3 Crypto Money Laundering Behaviors
Dan Lin, Yanli Ding, Weipeng Zou, Jiachi Chen, Xiapu Luo, Jiajing Wu, Zibin Zheng

    While the rapid growth of Web3 has driven the development of decentralized finance, user anonymity and cross-chain asset flows make on-chain laundering behaviors more covert and complex. In this context, constructing high-quality anti-money laundering(AML) datasets has become essential for risk-control systems and on-chain forensic analysis, yet current practices still rely heavily on manual efforts with limited efficiency and coverage. In this paper, we introduce RiskTagger, a large-language-model-based agent for the automatic annotation of crypto laundering behaviors in Web3. RiskTagger is designed to replace or complement human annotators by addressing three key challenges: extracting clues from complex unstructured reports, reasoning over multichain transaction paths, and producing auditor-friendly explanations. RiskTagger implements an end-to-end multi-module agent, integrating a key-clue extractor, a multichain fetcher with a laundering-behavior reasoner, and a data explainer, forming a data annotation pipeline. Experiments on the real case Bybit Hack (with the highest stolen asset value) demonstrate that RiskTagger achieves 100% accuracy in clue extraction, 84.1% consistency with expert judgment, and 90% coverage in explanation generation. Overall, RiskTagger automates laundering behavior annotation while improving transparency and scalability in AML research. 

Comments: 	8 pages(not including appendix), 11 figures
Subjects: 	Cryptography and Security (cs.CR); Software Engineering (cs.SE)
Cite as: 	arXiv:2510.17848 [cs.CR]
  	(or arXiv:2510.17848v1 [cs.CR] for this version)
  	
https://doi.org/10.48550/arXiv.2510.17848
Submission history
From: Weipeng Zou [view email]
[v1] Sun, 12 Oct 2025 08:54:28 UTC (776 KB)

---

### A2. Hedged working-paper numerics — verify or leave qualitative?
**Context.** Many precise figures attributed to SSRN/arXiv working papers were stated as
established fact. Per the "never assert unverifiable numbers" rule I **softened them to
qualitative claims** (e.g. "Sharpe ratio of 3.05" → "a high Sharpe ratio"). If you verify a
number against its source, I can restore the exact value (this only *raises* citation
accuracy). The full list, by chapter:

| Chapter | Hedged claim(s) — restore if you verify |
|---------|------------------------------------------|
| ch01 (intro) | `hampole2025ai` 2% / 14% labour-demand figures; CoT "may triple" tokens; prompt-cost "80% less" |
| ch02 (foundations) | FinBERT ">97% / +8pp over BERT-base" |
| ch03 (training) | `LopezLiraTang2023` "Sharpe >6 in 2021 → ~1 by 2024"; "4,123 stocks"; (also: it says GPT-4 — the paper centres on ChatGPT/GPT-3.5) |
| ch04 (agents) | `kim2024financial` 60%/53%; `zhang2024financebench` 10,231 Qs / 81%; `wang2025finsage` 92.51% recall / +24% |
| ch08 (domain LLMs) | FinBERT F1 0.88/0.72/0.80 & "+15pp"; `RahimikiaDrinkall2024` "up to 50× parameter count" |
| ch09 (sentiment) | `KirtacGermano2024` Sharpe 3.05 / 74.4% / 965,375 articles; `bollen2011twitter` 86.7% / 9.7M tweets; `Siano2025` "3×" / "double R²"; `cookson2026bankrun` 4.3pp; `loughran2011liability` 0.5pp |
| ch10 (portfolio) | `KirtacGermano2024` 965,375 / 74.4% / Sharpe 3.05; `CoriatBenhamou2025` HARLF 26% / Sharpe 1.2 |
| ch13 (limitations) | `VidalSSRN2024` 59.4%; `xu2024stock` ~59% / 51–65%; `zhao2025frontiers` 59% / 84-study meta; `kang2023hallucination` 15–30% |
| ch14 (summarization) | `LiGao2023` "96–99.5% accuracy"; `Siano2025` "3×" / "double R²" |
| ch15 (privacy) | Mistral-7B "outperforms Llama-2-13B on most benchmarks / <half memory"; Phi-3 "comparable to models several × its size"; canary "extraction >1%" |
| ch07 (applications) | `chen2024uncertainty`, `didisheim2025memory`, `FSB2024stability` qualitative claims (verbs softened to "report/argues") |

**Options.** (a) Leave all hedged (safe, publishable as-is). (b) Send me the verified
numbers for any subset and I restore them precisely.
**My recommendation:** (a) for anything you can't quickly verify; (b) for the few you can.
**Your decision (which, if any, to restore):**

keep all as (a)

---

### A3. `claude-opus-4-5` example model id
**Context.** Code examples use the placeholder model id `claude-opus-4-5` (and ch07 has a
remark noting model ids change). The current Anthropic Opus id is `claude-opus-4-8`.
**Options.** (a) Keep `claude-opus-4-5` as the book's consistent illustrative id (the remark
already says to update for the current model). (b) Update all examples to `claude-opus-4-8`.
**My recommendation:** (a) — consistent and explicitly flagged as illustrative.
**Your decision:**
ok, a
---

## B. Repository hygiene

### B1. Delete the unused `.bib` files?
**Context.** `book/bibliography_bibertool.bib` and `book/bibliography_test.bib` exist but are
**not loaded** by `preamble.tex` (only `bibliography.bib` is). They are stale and can cause
confusion (e.g. an old id lingers in the bibertool one).
**My recommendation:** delete both.
**Your decision (delete / keep):**
delete

---

### B2. Empty `code/src/__init__.py` and `code/tests/`
**Context.** The repo implies a "shared Python package" and a test suite, but
`code/src/__init__.py` is empty and `code/tests/` has no tests.
**Options.** (a) Drop the "shared package / tests" claim from the prose/README. (b) You want
me to scaffold a real shared package + minimal tests (larger effort).
**My recommendation:** (a) for now (the chapter code lives in the notebooks/generators).
**Your decision:**
a

---

## C. Reproducibility polish (optional — already passes)

### C1. Offline snapshot for the ch01 king-analogy figure
**Context.** Ten of the eleven figure generators are fully offline-deterministic. The one
exception, `gen_king_analogy.py`, regenerates from the pinned `glove-wiki-gigaword-300`
release (~1 GB, downloaded once then cached). It is *documented* as such (which is why ch01
still passes), but not offline out-of-the-box.
**Options.** (a) Leave as documented-pinned (passes). (b) I commit a tiny pruned `.npz` of
just the ~12 plotted word vectors (a few KB) so it runs fully offline like the others —
**this needs the GloVe vectors to be downloaded once on a machine that has them** (I can't
download 1 GB in this environment).
**My recommendation:** (b) if convenient on your machine; otherwise (a) is fine.
**Your decision:**
a
---

## D. Structure / style (optional)

### D1. Reading-order placement of ch16 (AI/ML/Text in Finance)
**Context.** `16-ai-ml-finance-text` reads as introductory material but sits at **reading
position 2** in `main.tex` (right after ch01). It passes all dimensions where it is. The
original audit (A15) flagged whether its `\include` order is ideal.
**Options.** (a) Keep current order (no change; it passes). (b) You want it moved (tell me
where) — this is a `\include` reorder in `main.tex`, which I'd do carefully and re-check
cross-refs.
**My recommendation:** (a) — it works and reorders are risky for little gain.
**Your decision:**
b, move it where it makes sense based on the structure of the book
---

### D2. Anything else you want changed
Use this space for any other call (a figure you'd design differently, a claim you'd phrase
another way, a section to expand, etc.):
**Your notes:**
the first page says twice the title of the book, add also like a about this book section before eveything, explaining the format, what to expect, course material etc
---

## How to use this file

Fill in the `Your decision:` lines, then tell me "apply the decisions in AUTHOR_DECISIONS.md"
and I'll implement each, re-verify the build, and update the scorecards. Items left blank
keep the safe default I noted.
