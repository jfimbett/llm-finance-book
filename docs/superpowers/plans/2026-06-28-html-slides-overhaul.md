# HTML Slides Overhaul Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring all 34 HTML slide decks to a consistent bar — reframed for a summer-school audience, with an embedded figure in every chapter, complete coverage of every book-chapter concept — and delete the legacy Beamer artifacts.

**Architecture:** Shared-asset edits first (CSS figure support, de-MBA the engine/spec, a dependency-free Node validator, a figure pipeline). Then a figure-asset build that converts/generates a PNG or authors an inline-SVG diagram per chapter. Then a per-chapter deck overhaul (lesson + practical) driven by a concept checklist extracted from each book chapter. Finally, delete all Beamer artifacts once HTML passes the gate.

**Tech Stack:** Static HTML/CSS/JS slide engine (KaTeX from CDN), Python 3 + matplotlib for data figures, `pdftoppm` (poppler) for PDF→PNG fallback, Node (built-in `fs` only) for the validator, headless Google Chrome for a visual spot-check.

## Global Constraints

- **Audience:** summer school, mixed grad/practitioner. Plain-language lead sentence on every content slide; math/derivations stay collapsed in `aside.underhood`. Surface may carry slightly more formalism than exec-level, but never lead with a formula.
- **Zero "MBA":** no occurrence of `/mba/i` anywhere under `course/slides-html/` after completion.
- **Faithful content:** do not invent data, results, or citations. Use only what the book chapter `.tex` contains. Authored figures must be conceptual diagrams (no fabricated numbers).
- **Authoring contract:** every deck follows `course/slides-html/AUTHORING.md` component vocabulary and editorial rules.
- **Source of truth for completeness:** `book/chapters/<NN>/chapter.tex`. Every major concept must appear in the lesson deck; not verbatim.
- **Do not edit** `book/chapters/**` content (book is the source, not a target).
- **Working-tree integrity:** `auto_commit` is on and a mass deletion has happened before. Review `git diff --stat` before each commit; stage deletions deliberately.
- **Deck name mapping:** `course/slides-html/<NN>-name` ↔ `book/chapters/<NN>-name` ↔ `code/notebooks/<NN>-name` (verified 1:1 for all 17).
- **Chrome path:** `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.

---

## Figure inventory (drives Task 2)

| Chapter | Figure source | Action |
|---|---|---|
| 01-intro | `gen_king_analogy.py`, `gen_edgar_text_growth.py`, `gen_tfidf_headlines.py` | run generator → PNG (PNGs already exist for king/edgar) |
| 02-llm-foundations | `gen_positional_encoding.py` | run generator → PNG |
| 03-llm-training-finetuning | none | author inline SVG: pretraining → SFT → RLHF pipeline |
| 04-llm-agents | none | author inline SVG: agent loop (observe → think → act, LLM ↔ tools ↔ memory) |
| 05-business-valuation | `gen_dcf_sensitivity.py` | run generator → PNG |
| 06-credit-risk | none | author inline SVG: text → features → PD model → decision pipeline |
| 07-applications-future | `gen_benchmark_comparison.py` | run generator → PNG |
| 08-domain-specific-llms | `fig_corpus.pdf` (+ generator) | run generator → PNG; fallback `pdftoppm` |
| 09-financial-nlp-sentiment | `fig_lm_lexicon.pdf` (+ generator) | run generator → PNG; fallback `pdftoppm` |
| 10-portfolio-quant-trading | `fig_frontier.pdf` (+ generator) | run generator → PNG; fallback `pdftoppm` |
| 11-regtech-compliance-aml | `fig_rrf.pdf` (+ generator) | run generator → PNG; fallback `pdftoppm` |
| 12-xai-explainability | `fig_shap_attribution.pdf` (+ generator) | run generator → PNG; fallback `pdftoppm` |
| 13-llm-limitations-evaluation | `fig_reliability.pdf` (+ generator) | run generator → PNG; fallback `pdftoppm` |
| 14-financial-text-summarization | none | author inline SVG: 10-K → chunk → map-reduce summarize → exec summary |
| 15-privacy-local-models | `fig_privacy_utility.pdf` (+ generator) | run generator → PNG; fallback `pdftoppm` |
| 16-ai-ml-finance-text | none | author inline SVG: AI ⊃ ML ⊃ DL ⊃ NLP ⊃ LLM nesting + text-as-data flow |
| 17-loops-goals-iterations | none | author inline SVG: plan → act → observe → reflect goal loop |

---

## Task 1: Shared CSS — figure support

**Files:**
- Modify: `course/slides-html/assets/slides.css` (append a figure block; this is an allowed engine edit — supporting figures)

**Interfaces:**
- Produces: CSS classes consumed by every deck — `figure.deckfig`, `figure.deckfig img`, `figure.deckfig svg`, `figure.deckfig figcaption`, `figure.deckfig .src`.

- [ ] **Step 1: Add the figure styles**

Append to `course/slides-html/assets/slides.css`:

```css
/* ---- figures (added for the figure overhaul) ---- */
figure.deckfig { margin: 0.6rem auto; text-align: center; max-width: 92%; }
figure.deckfig img,
figure.deckfig svg { max-width: 100%; max-height: 52vh; height: auto; border-radius: 8px; }
figure.deckfig figcaption { margin-top: .5rem; font-size: .72em; color: #5b6472; line-height: 1.35; }
figure.deckfig figcaption b { color: #2a3340; }
figure.deckfig .src { display: block; margin-top: .2rem; font-size: .9em; opacity: .7; font-style: italic; }
.cols .col figure.deckfig img,
.cols .col figure.deckfig svg { max-height: 40vh; }
```

- [ ] **Step 2: Verify CSS is syntactically intact**

Run: `node -e "const c=require('fs').readFileSync('course/slides-html/assets/slides.css','utf8');const o=(c.match(/{/g)||[]).length,cl=(c.match(/}/g)||[]).length;if(o!==cl)throw new Error('brace mismatch '+o+'/'+cl);console.log('css braces balanced',o)"`
Expected: `css braces balanced <N>` (no throw)

- [ ] **Step 3: Commit**

```bash
git add course/slides-html/assets/slides.css
git commit -m "feat(slides): add figure styling to shared HTML slide engine"
```

---

## Task 2: De-MBA the shared assets, spec, and landing page

**Files:**
- Modify: `course/slides-html/assets/slides.css:9` (comment)
- Modify: `course/slides-html/assets/slides.js:66` (help-overlay text)
- Modify: `course/slides-html/AUTHORING.md` (lines 3, 39, 66 and any other MBA wording)
- Modify: `course/slides-html/index.html:54` (pill text) and title/intro copy

**Interfaces:**
- Produces: an MBA-free shared layer + an updated authoring contract that downstream chapter tasks follow.

- [ ] **Step 1: Replace the engine comment and help text**

In `course/slides-html/assets/slides.css` line ~9, change:
`The audience is MBA-first: each slide reads as plain-language narrative,`
to:
`The audience is a mixed grad/practitioner summer school: each slide reads as plain-language narrative,`

In `course/slides-html/assets/slides.js` line ~66, change the help text:
`Tip: the warm <b style="color:#B48228">◆ bigger picture</b> boxes are the MBA story;`
to:
`Tip: the warm <b style="color:#B48228">◆ bigger picture</b> boxes are the intuition;`

- [ ] **Step 2: Update AUTHORING.md audience framing**

In `course/slides-html/AUTHORING.md`:
- Line ~3: `re-present the Beamer course decks as **MBA-facing HTML/JS presentations**` → `re-present the course material as **summer-school HTML/JS presentations** (mixed grad/practitioner audience)`.
- Line ~39: `` `bigpicture` — warm "the bigger picture" intuition (the MBA story). `` → `` `bigpicture` — warm "the bigger picture" intuition (the plain-language story). ``
- Line ~66: replace the `**MBA first.**` editorial rule with:
  `1. **Intuition first.** Lead every content slide with a plain-language sentence a quantitatively comfortable non-specialist understands.`
- Add to the figure conventions section (after rule 7) a new rule:
  `8. **One figure per chapter, minimum.** Every chapter's deck embeds at least one on-topic figure using \`<figure class="deckfig">\` with an \`<img>\` (PNG under \`../assets/figures/<NN>/\`) or inline \`<svg>\`, plus a \`<figcaption>\` and a \`.src\` credit line.`
- Replace any remaining "Beamer" source-of-truth references with "book chapter (`book/chapters/<NN>/chapter.tex`)".

- [ ] **Step 3: De-MBA the landing page**

In `course/slides-html/index.html`, replace the `<span class="pill b">MBA-friendly narrative</span>` with `<span class="pill b">plain-language narrative</span>`, and reword any header/intro copy that says "MBA" to "summer school".

- [ ] **Step 4: Verify zero MBA in the shared layer**

Run: `grep -rni "mba" course/slides-html/assets course/slides-html/AUTHORING.md course/slides-html/index.html; echo "exit=$?"`
Expected: no matches (grep prints nothing, `exit=1`).

- [ ] **Step 5: Commit**

```bash
git add course/slides-html/assets/slides.css course/slides-html/assets/slides.js course/slides-html/AUTHORING.md course/slides-html/index.html
git commit -m "refine(slides): reframe shared HTML slide layer for summer-school audience"
```

---

## Task 3: Deck validator (dependency-free Node)

**Files:**
- Create: `course/slides-html/tools/validate.mjs`

**Interfaces:**
- Produces: CLI `node course/slides-html/tools/validate.mjs <deck.html>` exiting 0 on pass, 1 on fail, printing one `FAIL: <reason>` line per problem. Consumed as the validation gate in every chapter task.
- Checks: exactly one `class="...current..."`; ≥1 `<figure` or `<img` or `<svg` figure; zero `/mba/i`; every `<img src=...>` resolves to an existing file (relative to the deck); balanced `$`-delimiter count (even number of un-escaped `$`).

- [ ] **Step 1: Write the validator**

Create `course/slides-html/tools/validate.mjs`:

```js
import { readFileSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const file = process.argv[2];
if (!file) { console.error('usage: validate.mjs <deck.html>'); process.exit(2); }
const html = readFileSync(file, 'utf8');
const dir = dirname(file);
const fails = [];

// exactly one current slide
const current = (html.match(/class="[^"]*\bcurrent\b[^"]*"/g) || []).length;
if (current !== 1) fails.push(`expected exactly 1 current slide, found ${current}`);

// at least one figure
if (!/<figure|<img|<svg/i.test(html)) fails.push('no figure/img/svg present');

// zero MBA
if (/mba/i.test(html)) fails.push('contains "MBA"');

// every img src resolves (skip remote URLs and data URIs)
for (const m of html.matchAll(/<img[^>]*\ssrc="([^"]+)"/g)) {
  const src = m[1];
  if (/^(https?:)?\/\//.test(src) || src.startsWith('data:')) continue;
  if (!existsSync(resolve(dir, src))) fails.push(`missing image: ${src}`);
}

// balanced KaTeX $ delimiters (count un-escaped $)
const dollars = (html.match(/(?<!\\)\$/g) || []).length;
if (dollars % 2 !== 0) fails.push(`odd number of $ delimiters (${dollars}) — KaTeX will mis-render`);

if (fails.length) { for (const f of fails) console.log(`FAIL: ${f}`); process.exit(1); }
console.log(`OK: ${file}`);
```

- [ ] **Step 2: Run it against an unmodified deck to see it report the expected gaps**

Run: `node course/slides-html/tools/validate.mjs course/slides-html/02-llm-foundations/index.html; echo "exit=$?"`
Expected: `FAIL: no figure/img/svg present` and `FAIL: contains "MBA"`, `exit=1` (proves the checks fire).

- [ ] **Step 3: Commit**

```bash
git add course/slides-html/tools/validate.mjs
git commit -m "feat(slides): add dependency-free HTML deck validator"
```

---

## Task 4: Figure assets — generate/convert/author one figure per chapter

**Files:**
- Create: `course/slides-html/assets/figures/<NN>-name/*.png` (chapters using a generator or PDF)
- Create: `course/slides-html/assets/figures/<NN>-name/*.svg` (chapters authoring a diagram: 03, 04, 06, 14, 16, 17)
- Create: `course/slides-html/tools/build-figures.sh`

**Interfaces:**
- Produces: at least one figure file per chapter under `assets/figures/<NN>-name/`, referenced by the chapter decks in later tasks.

- [ ] **Step 1: Write the figure build script (generators + PDF fallback)**

Create `course/slides-html/tools/build-figures.sh`:

```bash
#!/usr/bin/env bash
# Build web PNGs for chapters that have a matplotlib generator or an existing figure PDF.
# Inline-SVG chapters (03 04 06 14 16 17) are authored by hand, not here.
set -u
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
OUT_ROOT="$ROOT/course/slides-html/assets/figures"

for ch in 01-intro 02-llm-foundations 05-business-valuation 07-applications-future \
          08-domain-specific-llms 09-financial-nlp-sentiment 10-portfolio-quant-trading \
          11-regtech-compliance-aml 12-xai-explainability 13-llm-limitations-evaluation \
          15-privacy-local-models; do
  out="$OUT_ROOT/$ch"; mkdir -p "$out"
  nbdir="$ROOT/code/notebooks/$ch"
  if compgen -G "$nbdir/gen_*.py" > /dev/null; then
    for g in "$nbdir"/gen_*.py; do
      echo "RUN  $ch/$(basename "$g")"
      ( cd "$nbdir" && python3 "$(basename "$g")" ) || echo "WARN generator failed: $g"
    done
  fi
  # collect any PNGs the generators wrote into the book figures dir
  figdir="$ROOT/book/chapters/$ch/figures"
  if compgen -G "$figdir/*.png" > /dev/null; then cp -f "$figdir"/*.png "$out"/; fi
  # fallback: convert any figure PDF (except the generic illustration) to PNG
  if compgen -G "$figdir"/*.pdf > /dev/null; then
    for pdf in "$figdir"/*.pdf; do
      base="$(basename "${pdf%.pdf}")"
      [ "$base" = "fig_illustration" ] && continue
      [ -f "$out/$base.png" ] && continue
      echo "CONV $ch/$base.pdf -> png"
      pdftoppm -png -r 160 -singlefile "$pdf" "$out/$base"
    done
  fi
  echo "DONE $ch -> $(ls "$out" 2>/dev/null | tr '\n' ' ')"
done
```

- [ ] **Step 2: Make it executable and run it**

Run: `chmod +x course/slides-html/tools/build-figures.sh && bash course/slides-html/tools/build-figures.sh`
Expected: a `DONE <chapter> -> ...png` line per chapter, each listing ≥1 `.png`. If a generator errors (e.g. missing `gensim`), the PDF-fallback line (`CONV ...`) must still produce a PNG. For chapter 01, the king/edgar PNGs are copied.

- [ ] **Step 3: Verify every generator/convert chapter has at least one PNG**

Run:
```bash
for ch in 01-intro 02-llm-foundations 05-business-valuation 07-applications-future 08-domain-specific-llms 09-financial-nlp-sentiment 10-portfolio-quant-trading 11-regtech-compliance-aml 12-xai-explainability 13-llm-limitations-evaluation 15-privacy-local-models; do n=$(ls course/slides-html/assets/figures/$ch/*.png 2>/dev/null | wc -l | tr -d ' '); echo "$n  $ch"; [ "$n" = "0" ] && echo "  !! MISSING"; done
```
Expected: every line ≥1; no `!! MISSING`. If any is missing, re-run the relevant generator manually or `pdftoppm` the source PDF before proceeding.

- [ ] **Step 4: Author the 6 inline-SVG diagram files**

For each of `03-llm-training-finetuning`, `04-llm-agents`, `06-credit-risk`, `14-financial-text-summarization`, `16-ai-ml-finance-text`, `17-loops-goals-iterations`, create `course/slides-html/assets/figures/<NN>/diagram.svg` as a clean, self-contained SVG matching the figure concept in the inventory table. Use the deck palette: ink `#2a3340`, blue `#2f6fed`, gold `#B48228`, muted `#5b6472`, light fill `#eef2fb`. Each SVG sets `viewBox="0 0 720 360"` and `font-family="system-ui, sans-serif"`. Example for `04-llm-agents/diagram.svg` (the agent loop):

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 360" font-family="system-ui, sans-serif">
  <rect x="280" y="150" width="160" height="60" rx="10" fill="#eef2fb" stroke="#2f6fed"/>
  <text x="360" y="185" text-anchor="middle" fill="#2a3340" font-size="18">LLM (reason)</text>
  <rect x="60"  y="40"  width="160" height="56" rx="10" fill="#fff" stroke="#5b6472"/>
  <text x="140" y="74" text-anchor="middle" fill="#2a3340" font-size="15">Observation</text>
  <rect x="500" y="40"  width="160" height="56" rx="10" fill="#fff" stroke="#5b6472"/>
  <text x="580" y="74" text-anchor="middle" fill="#2a3340" font-size="15">Action / Tool call</text>
  <rect x="500" y="270" width="160" height="56" rx="10" fill="#fff" stroke="#B48228"/>
  <text x="580" y="304" text-anchor="middle" fill="#2a3340" font-size="15">Tools · Memory</text>
  <rect x="60"  y="270" width="160" height="56" rx="10" fill="#fff" stroke="#5b6472"/>
  <text x="140" y="304" text-anchor="middle" fill="#2a3340" font-size="15">Environment</text>
  <g stroke="#2f6fed" fill="none" stroke-width="2" marker-end="url(#a)">
    <path d="M140,96 C140,150 240,170 280,178"/>
    <path d="M440,178 C500,160 560,140 580,96"/>
    <path d="M580,96 L580,270"/>
    <path d="M500,300 L220,300"/>
    <path d="M140,270 C140,230 200,200 280,190"/>
  </g>
  <defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L6,3 L0,6 Z" fill="#2f6fed"/></marker></defs>
</svg>
```

Author the other five analogously to their inventory concepts (pipelines = left-to-right boxes + arrows; nesting = concentric rounded rects). Keep each under ~60 lines, no external refs, no fabricated numbers.

- [ ] **Step 5: Verify all 17 chapters now have a figure asset**

Run:
```bash
for ch in $(ls book/chapters); do n=$(ls course/slides-html/assets/figures/$ch/* 2>/dev/null | wc -l | tr -d ' '); echo "$n  $ch"; [ "$n" = "0" ] && echo "  !! MISSING FIGURE"; done
```
Expected: every chapter ≥1 asset; no `!! MISSING FIGURE`.

- [ ] **Step 6: Commit**

```bash
git add course/slides-html/tools/build-figures.sh course/slides-html/assets/figures
git status --short | head -40   # review what is staged before committing
git commit -m "feat(slides): build one web figure per chapter (PNG generators + inline-SVG diagrams)"
```

---

## Per-Chapter Deck Procedure (applied in Tasks 5–21)

Tasks 5–21 each apply this identical procedure to one chapter `<NN>-name`. The procedure is fully specified here; each task supplies only its chapter id and the figure file(s) to embed (from the inventory table). This is DRY, not a placeholder — every step below is concrete.

For chapter `<NN>-name`:

- [ ] **P1: Extract the concept checklist from the book chapter**

Read `book/chapters/<NN>-name/chapter.tex` (and any `\input` files it pulls). Produce `docs/quality/slide-coverage/<NN>-name.md` listing, as checkboxes: every `\section`/`\subsection` heading; every named method/result/model; every key number; every citation `\cite{...}` (as Author, year). This file is the completeness contract for the chapter.

- [ ] **P2: Diff the checklist against the current lesson deck**

Open `course/slides-html/<NN>-name/index.html`. For each checklist item, mark whether it already appears. List the omissions explicitly in the coverage file under a `## Omissions` heading.

- [ ] **P3: Rewrite the lesson deck for completeness + audience + figure**

Edit `course/slides-html/<NN>-name/index.html`:
- Add slides so **every** checklist item is covered. One idea per slide (4–7 bullets); split dense frames. Plain-language `.lead`; equations/derivations inside `aside.underhood`; preserve numbers and citations.
- Embed the chapter figure on the most relevant slide using:
  ```html
  <figure class="deckfig">
    <img src="../assets/figures/<NN>-name/<file>.png" alt="...">
    <figcaption><b>Figure.</b> one-line plain-language reading of the figure.
      <span class="src">Source: …</span></figcaption>
  </figure>
  ```
  For inline-SVG chapters (03, 04, 06, 14, 16, 17), inline the SVG inside `<figure class="deckfig">` instead of `<img>` (paste the SVG markup or use `<img src=".../diagram.svg">`).
- Remove every "MBA" mention; reword the title-slide `.badge` from `MBA-friendly · …` to `Summer school · math one click away — press <b>m</b> …`.
- Update the head `<title>`/`DECK_META` if needed; keep the first slide carrying `current`.

- [ ] **P4: Rewrite the practical deck**

Edit `course/slides-html/<NN>-name/practical.html`: same de-MBA pass, embed the chapter figure (or a second relevant one) once, ensure it covers the chapter's applied/worked material. Keep it practical-session scoped (guided problems + worked case), not a duplicate of the lesson.

- [ ] **P5: Validate both decks**

Run:
```bash
node course/slides-html/tools/validate.mjs course/slides-html/<NN>-name/index.html
node course/slides-html/tools/validate.mjs course/slides-html/<NN>-name/practical.html
```
Expected: `OK: …` for both. Fix any `FAIL:` line and re-run.

- [ ] **P6: Visual spot-check with headless Chrome**

Run:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --screenshot="/private/tmp/claude-502/-Users-juan-Documents-llm-finance-book/cd4d5ad1-f340-49bc-961a-67cfb8675e09/scratchpad/<NN>.png" \
  --window-size=1280,720 --virtual-time-budget=4000 \
  "file://$PWD/course/slides-html/<NN>-name/index.html"
```
Then Read the screenshot to confirm the first slide renders (title visible, no raw `$…$`, no overflow). It only captures slide 1; that is enough as a smoke test that the engine + KaTeX load.

- [ ] **P7: Commit**

```bash
git add course/slides-html/<NN>-name/index.html course/slides-html/<NN>-name/practical.html docs/quality/slide-coverage/<NN>-name.md
git diff --cached --stat
git commit -m "feat(slides): complete + de-MBA + figure <NN>-name HTML decks"
```

---

## Task 5: Chapter 01-intro decks

Apply the Per-Chapter Deck Procedure to `01-intro`. Figure(s): `fig_king_analogy.png` (and `fig_edgar_text_growth.png` on the "why text grew" slide). This chapter is the canonical example in `AUTHORING.md` — match its tone.

## Task 6: Chapter 02-llm-foundations decks

Apply the procedure to `02-llm-foundations`. Figure: the PNG from `gen_positional_encoding.py`.

## Task 7: Chapter 03-llm-training-finetuning decks

Apply the procedure to `03-llm-training-finetuning`. Figure: inline-SVG training-pipeline diagram (`diagram.svg`).

## Task 8: Chapter 04-llm-agents decks

Apply the procedure to `04-llm-agents`. Figure: inline-SVG agent-loop diagram (`diagram.svg`).

## Task 9: Chapter 05-business-valuation decks

Apply the procedure to `05-business-valuation`. Figure: the PNG from `gen_dcf_sensitivity.py`.

## Task 10: Chapter 06-credit-risk decks

Apply the procedure to `06-credit-risk`. Figure: inline-SVG PD-pipeline diagram (`diagram.svg`).

## Task 11: Chapter 07-applications-future decks

Apply the procedure to `07-applications-future`. Figure: the PNG from `gen_benchmark_comparison.py`.

## Task 12: Chapter 08-domain-specific-llms decks

Apply the procedure to `08-domain-specific-llms`. Figure: `fig_corpus.png`.

## Task 13: Chapter 09-financial-nlp-sentiment decks

Apply the procedure to `09-financial-nlp-sentiment`. Figure: `fig_lm_lexicon.png`.

## Task 14: Chapter 10-portfolio-quant-trading decks

Apply the procedure to `10-portfolio-quant-trading`. Figure: `fig_frontier.png`.

## Task 15: Chapter 11-regtech-compliance-aml decks

Apply the procedure to `11-regtech-compliance-aml`. Figure: `fig_rrf.png`.

## Task 16: Chapter 12-xai-explainability decks

Apply the procedure to `12-xai-explainability`. Figure: `fig_shap_attribution.png`.

## Task 17: Chapter 13-llm-limitations-evaluation decks

Apply the procedure to `13-llm-limitations-evaluation`. Figure: `fig_reliability.png`.

## Task 18: Chapter 14-financial-text-summarization decks

Apply the procedure to `14-financial-text-summarization`. Figure: inline-SVG summarization-pipeline diagram (`diagram.svg`).

## Task 19: Chapter 15-privacy-local-models decks

Apply the procedure to `15-privacy-local-models`. Figure: `fig_privacy_utility.png`.

## Task 20: Chapter 16-ai-ml-finance-text decks

Apply the procedure to `16-ai-ml-finance-text`. Figure: inline-SVG AI/ML/DL/NLP/LLM-nesting diagram (`diagram.svg`).

## Task 21: Chapter 17-loops-goals-iterations decks

Apply the procedure to `17-loops-goals-iterations`. Figure: inline-SVG goal-loop diagram (`diagram.svg`).

---

## Task 22: Book-wide consistency gate

**Files:** none modified (verification only)

- [ ] **Step 1: Zero MBA anywhere under slides-html**

Run: `grep -rni "mba" course/slides-html; echo "exit=$?"`
Expected: nothing, `exit=1`.

- [ ] **Step 2: Validate all 34 decks**

Run:
```bash
fail=0; for f in course/slides-html/*/index.html course/slides-html/*/practical.html; do node course/slides-html/tools/validate.mjs "$f" || fail=1; done; echo "overall fail=$fail"
```
Expected: `OK:` for all 34, `overall fail=0`.

- [ ] **Step 3: Every chapter coverage file exists with no open omissions**

Run:
```bash
for ch in $(ls book/chapters); do f=docs/quality/slide-coverage/$ch.md; [ -f "$f" ] || { echo "MISSING $f"; continue; }; grep -q "## Omissions" "$f" && grep -A50 "## Omissions" "$f" | grep -q "\- \[ \]" && echo "OPEN OMISSIONS: $ch"; done; echo done
```
Expected: no `MISSING`, no `OPEN OMISSIONS`.

- [ ] **Step 4: Commit (if any coverage files were touched)**

```bash
git add -A docs/quality/slide-coverage
git commit -m "docs(slides): chapter coverage checklists for HTML decks" || echo "nothing to commit"
```

---

## Task 23: Delete all legacy Beamer artifacts

Performed **only after Task 22 passes** — so nothing is lost prematurely.

**Files:**
- Delete: `course/lectures/<NN>/slides.pdf`, `course/lectures/<NN>/slides.tex`, `course/lectures/<NN>/practical.pdf`, `course/lectures/<NN>/practical.tex` (all 17)
- Delete: `course/lectures/_style/finance-beamer.tex` (Beamer-only style — verified exclusive)
- Delete: `.claude/skills/build-slides/` (builds Beamer PDFs)
- Modify/Delete: `.claude/skills/slides-from-chapter/` (Beamer generator) — delete or repurpose
- Modify: `.claude/CLAUDE.md`, `course/` READMEs — remove references to Beamer slides / build-slides

- [ ] **Step 1: Confirm HTML coverage before deleting (safety check)**

Run: `for c in $(ls course/slides-html | grep -v assets | grep -v tools | grep -v '\.'); do [ -f "course/slides-html/$c/index.html" ] && [ -f "course/slides-html/$c/practical.html" ] && echo "OK $c" || echo "MISSING HTML $c"; done`
Expected: `OK` for all 17; no `MISSING HTML`. Do not proceed if any are missing.

- [ ] **Step 2: Delete the rendered PDFs and Beamer .tex**

```bash
git rm course/lectures/*/slides.pdf course/lectures/*/slides.tex course/lectures/*/practical.pdf course/lectures/*/practical.tex
git rm course/lectures/_style/finance-beamer.tex
```

- [ ] **Step 3: Delete the Beamer tooling skills**

```bash
git rm -r .claude/skills/build-slides .claude/skills/slides-from-chapter
```

- [ ] **Step 4: Remove dangling references**

In `.claude/CLAUDE.md`, remove the `/build-slides` and `/slides-from-chapter` entries and any "Beamer" / `slides.tex` mentions. Run `grep -rni "build-slides\|slides-from-chapter\|finance-beamer\|slides\.tex\|practical\.tex" .claude course --include="*.md"` and fix every hit (point them at `course/slides-html/` instead).

- [ ] **Step 5: Verify nothing references deleted artifacts**

Run: `grep -rni "build-slides\|finance-beamer\|slides\.tex\|practical\.tex" .claude course --include="*.md"; echo "exit=$?"`
Expected: nothing, `exit=1`.

- [ ] **Step 6: Review and commit**

```bash
git status --short
git diff --cached --stat
git commit -m "chore(slides): delete legacy Beamer slide artifacts and tooling; HTML is the single source of truth"
```

---

## Self-Review notes

- **Spec coverage:** Audience reframe → Tasks 2 + P3/P4. Figures (real + authored) → Task 4 + P3. Completeness vs book chapter → P1–P3 + Task 22 step 3. Lesson+practical scope → P3 + P4 across Tasks 5–21. Delete Beamer artifacts → Task 23. Validation gate → Task 3 + P5/P6 + Task 22. `AUTHORING.md` update → Task 2 step 2. All 6 acceptance criteria map to Task 22 (1,2,4), P1–P3 (3), Task 23 (5), Task 2 (6).
- **Risks honored:** premature deletion guarded by Task 23 step 1 + ordering; figure-toolchain failure handled by the PDF-fallback in Task 4 step 1; working-tree integrity via `git diff --cached --stat` before every commit.
- **No placeholders:** the per-chapter procedure is fully specified once and parameterized by chapter id + figure file; each chapter task names its exact figure.
