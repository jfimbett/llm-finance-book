# Reshape Report: 02-llm-foundations (Chapter 3 in reading order)

## User Request

> Figure 3.1 is not good enough, not enough details, and very badly explained;
> there is also no explanation of encoder/decoder when explaining transformers;
> the figure should look more like the original paper one but without the crazy
> small details.

Figure 3.1 is `fig:ch02-transformer-pipeline`, the first figure of the
"Large Language Models: Architecture and Practice" chapter.

## Main Changes Applied

- **Replaced Figure 3.1.** The previous figure was a Transformer-vs-RNN
  connectivity contrast (largely redundant with the three-bottlenecks list that
  already precedes it). It is now the canonical *Attention Is All You Need*
  encoder–decoder architecture, simplified to the recognizable elements:
  input/output embeddings + positional encoding, the encoder stack
  (self-attention → Add & Norm → feed-forward → Add & Norm, `N×`), the decoder
  stack with its three sub-layers (masked self-attention, cross-attention,
  feed-forward), the cross-attention "keys & values H" bridge, and the final
  Linear → Softmax → output-probabilities head. Anchored on a sequence-to-sequence
  finance example ("Revenue fell sharply" → "Sales dropped"). Color-coded,
  no "Add & Norm" residual-loop clutter — the iconic structure without the tiny
  details.
- **Added an explicit encoder/decoder explanation** at the point where the
  Transformer is first introduced (previously the only encoder/decoder prose sat
  at the very end of the section, after all the attention math, with no figure).
  New "two halves" walk-through explains: what the encoder does (bidirectional
  self-attention over the whole input), what the decoder does (left-to-right
  generation with masked self-attention + cross-attention), Add & Norm,
  the linear+softmax head, and a roadmap to the component subsections.
- **Connected the configurations to finance:** brief note that BERT keeps only
  the encoder, GPT only the decoder, T5/BART the full stack, with a forward
  pointer to the pre-training subsection.
- **Back-referenced the figure** from the detailed Encoder–Decoder Structure
  subsection so the equations and the diagram are tied together.

## Sections Modified

- §3.3 The Transformer Architecture (motivation/overview + Figure 3.1)
- §3.3.5 Encoder–Decoder Structure (back-reference to the figure)

## New References Added

- None (figure and exposition reuse `vaswani2017attention` and existing labels).

## Math Checker

NOT RUN — no equations, derivations, or model definitions were changed; only
section and equation cross-references were added.

## Score Summary

Not re-scored via `/score-content` in this pass. Build and cross-reference checks
pass (see below).

## Build / Reference Checks

- Full book builds: `main.pdf`, 574 pages, no LaTeX errors.
- No undefined references or citations introduced.
- Label preserved: `fig:ch02-transformer-pipeline` still resolves to **Figure 3.1**
  (page 73); the single `\ref` to it remains valid and now matches the new figure.

## Remaining Issues

- None blocking. The figure deliberately omits the per-sub-layer residual loops
  (represented by the "Add & Norm" bars and described in the caption) to keep it
  uncluttered, as requested.
