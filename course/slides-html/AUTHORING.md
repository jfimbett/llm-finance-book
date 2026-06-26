# HTML Slides — Authoring Spec

These slides re-present the Beamer course decks as **MBA-facing HTML/JS presentations**:
plain-language narrative on the surface, with the math/mechanism one click away.

## How a deck works
- One self-contained `index.html` per lecture in `course/slides-html/<NN>-name/`.
- It loads the shared engine: `../assets/slides.css` and `../assets/slides.js` (+ KaTeX from CDN).
- The engine handles navigation, fragments, the "Under the hood" panels, overview, math.
- **Do not** edit the shared assets; only write the per-deck `index.html`.

## Required boilerplate (head)
```html
<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lecture N — Title</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<link rel="stylesheet" href="../assets/slides.css">
<script>window.DECK_META = { course: "LLM in Finance", lecture: N };</script>
<script defer src="../assets/slides.js"></script>
</head><body><div class="deck"><div class="stage">
  ... slides ...
</div></div></body></html>
```

## Slide types
- **Title:** `<section class="slide title-slide current">` with `.kicker`, `<h1>`, `.sub`, `.meta`, `.badge`.
  The FIRST slide must carry the `current` class.
- **Section divider:** `<section class="slide section-slide">` with `.secnum` (e.g. `01`), `<h2>`, `.secsub`.
- **Content:** `<section class="slide">` with `.eyebrow`, `<h2>`, `<div class="title-rule"></div>`, then body.

## Component vocabulary (use these classes)
- `.lead` — opening narrative sentence (one or two lines, plain English).
- `.cols` (two col) or `.cols.c3` (three), each child `<div class="col">`.
- `.block` with a `.block-title` child — a neutral labelled box.
- Callouts: `<div class="CLASS callout"><span class="callout-tag">LABEL</span> text</div>` where CLASS is:
  - `bigpicture` — warm "the bigger picture" intuition (the MBA story).
  - `takeaway` — blue "why this matters / the move that follows".
  - `alert` — red caution / the catch / the limitation.
- `.frag` on any element → it reveals on the next arrow press (progressive build). Use for
  list items, callouts that land a punchline, second columns. Don't fragment the `.lead` or the title.
- Tables: plain `<table><tr><th>…</th></tr>…</table>` (engine styles them).
- Stats row: `<div class="statrow"><div class="stat"><div class="num">42%</div><div class="lbl">…</div></div>…</div>`.
- Pills: `<span class="pill b">…</span>` (variants: `b` blue, `g` green, `r` red, `o` orange).
- Code: `<pre class="code">…</pre>`; inline `<code class="inline">…</code>`.

## The signature feature — "Under the hood"
Every equation, proof, derivation, or heavy formalism goes inside:
```html
<aside class="underhood" data-title="short label">
  ... the math / mechanism, with $...$ and \[ ... \] ...
</aside>
```
The engine renders it as a collapsed pill "⚙ Under the hood — <label>" that expands in place,
with a "‹ back to the big picture" link. Pressing `m` opens/closes all of them.
**On the surface, restate the idea in plain words; put the formal version in the aside.**

## Math
- Use KaTeX syntax: inline `$x$`, display `\[ ... \]` or `$$ ... $$`.
- Macros available: `\R`, `\E`, `\1`. Avoid LaTeX that KaTeX can't parse (no `\begin{tabular}` inside math,
  no custom `\newcommand`). Use HTML tables for tabular data, KaTeX only for equations.

## Editorial rules (the whole point)
1. **MBA first.** Lead every content slide with a plain-language sentence a non-technical exec understands.
   Translate jargon: "orthogonal one-hot vectors" → "to a computer these words are total strangers".
2. **Math close by, not gone.** Move formulas into `aside.underhood`. Keep the source's rigor — don't
   delete equations, relocate them. Preserve numbers, citations (Author, year), and named results.
3. **Keep the bigpicture / underhood split** the Beamer decks already use: `bigpicture` env → `.bigpicture`
   callout; `underhood` env → `aside.underhood`; `alertblock` → `.alert`; `block` → `.block`.
4. **One idea per slide; breathe.** Prefer 4–7 bullets. Split a dense Beamer frame into two slides if needed.
5. **Faithful content.** Do not invent data, results, or citations. Use only what the source `.tex` contains.
6. Title every slide with a *claim or question*, not a noun ("Why text predicts returns", not "Text & Returns").
7. End the deck with the source's wrap-up / "what's next", and put appendix frames after an `A` section divider.

The canonical example is `course/slides-html/01-intro/index.html`. Match its quality and structure.
