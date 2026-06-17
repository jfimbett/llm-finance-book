# Peer Review — Chapter 2: Large Language Models: Architecture and Practice

**Manuscript:** *Large Language Models in Finance* (Chapter 2)
**Author:** Juan F. Imbet (Paris Dauphine - PSL University)
**Review date:** 2026-05-31
**Reviewer:** Anonymous

---

```
REFEREE REPORT
==============

Summary:
This chapter provides a technically rigorous and pedagogically well-structured
introduction to the architecture and practice of large language models, with
consistent grounding in financial applications throughout. Starting from
document-level representations and recurrent architectures, the chapter
derives the mathematics of self-attention and the Transformer in detail, then
pivots to the practical landscape of modern LLMs, sampling strategies,
structured generation, API usage, retrieval-augmented generation, model
compression, hallucination, and regulatory limitations. The chapter is
unusually comprehensive for a single chapter and would serve a mixed
academic-practitioner audience well.

Verdict: MINOR_REVISION

Major Comments:
1. Missing Transformer architecture figure. The text (in the Encoder-Decoder
   subsection, Remark at ~line 823) references \ref{fig:transformer-architecture},
   but no corresponding figure environment exists in the file — only a LaTeX
   comment placeholder. In the compiled PDF this will produce a "??" undefined
   reference. Either a schematic figure should be added, or the remark should
   be rewritten to reference the existing sinusoidal PE figure
   (fig:ch02-illustration) or eliminated. For a chapter used in teaching, a
   Transformer architecture diagram is genuinely valuable and its absence is
   notable.

2. Grammar-based generation section (Section 6.3) lacks a code example.
   Sections 6.1 and 6.2 on constrained decoding and JSON mode include working
   Python listings, which is appropriate for the stated audience. Section 6.3
   on grammar-based generation using the outlines library and GBNF/llama.cpp
   describes these tools in prose only. Given the stated learning objective
   ("implement structured JSON extraction from an LLM using Python") and the
   book's applied orientation, a minimal listing demonstrating an EBNF-grammar
   constraint — even for a simple financial schema — would make the section
   complete and actionable. The current treatment reads as a survey paragraph
   that could be condensed or expanded; its current middle-ground length invites
   a code example.

3. SBERT mean-pooling formula (Definition 6, eq. 3). The formula divides
   sum_i (h_i * m_i) by n, where n is the total sequence length and m_i is
   a binary mask excluding padding tokens. When padding is present, the correct
   denominator is sum_i m_i (number of non-padding tokens), not n. As written,
   the formula produces an embedding that decreases in magnitude with the amount
   of padding, which does not match standard SBERT implementations. The standard
   practice is to divide by the number of non-padding tokens. This should be
   corrected for technical accuracy.

Minor Comments:
1. Chapter roadmap table (Table 5, Summary section). The table caption reads
   "Overview of book chapters and their relationship to Chapter 1 foundations"
   and the column header reads "Key Connection to Ch. 1." Since this is Chapter
   2, the references should be "Chapter 2" and "Ch. 2." This appears to be a
   copy-paste artifact from a Chapter 1 roadmap table.

2. Internal cross-reference (line ~1215). The text states "This dataset is used
   in Chapter 2 as the primary benchmark for sentiment analysis experiments."
   Since the reader is already in Chapter 2, this should read "later in this
   chapter" or cite the relevant section. The current phrasing is self-referential
   in a confusing way.

3. Table formatting. Five tables (model families, benchmarks, sampling
   strategies, API comparison, pricing) use \captionof inside bare \begin{center}
   environments rather than proper \begin{table} float environments. This is
   non-standard LaTeX that will produce incorrect or missing entries in the
   List of Tables, may cause numbering issues, and is fragile. The tables should
   be converted to standard table floats.

4. Unnumbered summary subsections. The chapter concludes with two unnumbered
   subsections (\subsection*) which are inconsistent with the numbered structure
   used throughout the rest of the chapter. Consider using \section*{} (consistent
   with a concluding section convention) or making them numbered.

5. RoBERTa citation key. The citation \citet{liu2018} on line ~871 refers to the
   RoBERTa paper (Liu et al., 2019). While the bibliography entry may be correct,
   a key named "liu2018" for a 2019 paper is error-prone. Consider renaming to
   "liu2019roberta" to avoid confusion.

6. Reasoning model marginalisation (eq. 5). The equation P(a|x) = sum_r P(a|x,r)
   P(r|x) correctly shows exact marginalisation, but the surrounding text says the
   model "samples" a reasoning trace, which corresponds to a Monte Carlo
   approximation rather than exact marginalisation. A brief remark clarifying the
   distinction would prevent confusion for mathematically careful readers.

7. Table 5 context: the "Chapter-by-Chapter Overview" subsection, which maps
   chapters 2-14 to this chapter's concepts, is a useful navigational aid but
   its placement inside the chapter summary (as an unnumbered subsection) rather
   than as a remark or standalone section makes it harder to locate via the table
   of contents. Consider promoting it to a named remark or placing it in the
   introduction section of the chapter.

Additional Observations (not revision-required):

The treatment of the BM25 formula (eq. 23), hybrid retrieval (RRF, eq. 24),
and two-stage re-ranking (ColBERT) in the RAG section is more thorough than
most textbooks at this level and should be commended. The hallucination taxonomy
and the concrete example (debt-to-equity ratio transcription error) are well-
chosen and appropriately motivate the mitigation techniques that follow.

The look-ahead bias discussion citing Didisheim et al. (2025) is a timely and
important addition that distinguishes this chapter from standard LLM textbooks.
This section is a genuine contribution to the pedagogical literature on LLMs in
finance and should be retained and possibly expanded.

The financial cost-of-API worked example (eq. 25, Anthropic vs. GPT-4o cost
comparison) is practically valuable and appropriately quantitative.

Summary of revisions required:
- Add Transformer architecture figure or remove undefined reference (major)
- Add code example for grammar-based generation (major)
- Correct SBERT mean-pool denominator (major, though impact is narrow)
- Fix chapter roadmap table header (minor)
- Fix internal self-reference in benchmark description (minor)
- Convert captionof tables to standard float environments (minor)
- Standardise summary section structure (minor)
- Clarify reasoning model marginalisation notation (minor)
```
