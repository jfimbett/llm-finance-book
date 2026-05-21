# /draft-figures

## Purpose

Generate TikZ or matplotlib figure code for a chapter section using the figure-designer agent.

## When to Invoke

When a chapter has a concept that would benefit from a diagram or plot. Can be run at any time after a chapter draft exists.

## Inputs Required

- Target chapter (e.g., `01-intro`) and the specific section needing a figure
- Description of the figure type: conceptual diagram, geometric figure, data plot, function graph
- `book/chapters/NN-name/chapter.tex` — for notation context

## Steps

1. Read the target section from `chapter.tex` to understand the notation and context.
2. Ask the user to describe the figure (or read it from context if the chapter already contains a `% FIGURE NEEDED:` comment).
3. **Invoke the figure-designer agent**: provide the section content, figure description, and whether TikZ or matplotlib is preferred.
4. For TikZ output: insert the `\begin{figure}...\end{figure}` block at the appropriate location in `chapter.tex`.
5. For matplotlib output: save the Python script as `code/notebooks/NN-name/figures/figure_name.py` and insert the `\includegraphics{figures/figure_name}` snippet in `chapter.tex`.
6. Run `/build-book` to verify the figure compiles without errors.
7. Commit: `git add book/chapters/NN-name/ code/notebooks/NN-name/ && git commit -m "feat(chNN): add [description] figure"`

## Expected Output

A compilable figure in `chapter.tex` (TikZ block or `\includegraphics` reference), plus a Python script in `code/notebooks/NN-name/figures/` if matplotlib was used.

## Error Handling

- If TikZ fails to compile: try simplifying the figure or switching to matplotlib.
- If `/build-book` fails due to the new figure: revert the figure insertion and report the LaTeX error.
