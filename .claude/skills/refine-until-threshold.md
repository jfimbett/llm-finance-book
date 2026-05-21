# /refine-until-threshold

## Purpose

Iteratively improve a content file until all 5 quality score dimensions reach the configured threshold.

## When to Invoke

After `/score-content` finds failing dimensions, or automatically by the `iterate.sh` hook when a pre-commit gate fails.

## Inputs Required

- File path: a `.tex` or `.md` content file
- Optionally: a max iterations override (defaults to `max_refine_iterations` from `TOPIC.md`)

## Steps

1. Read `quality_threshold` and `max_refine_iterations` from `TOPIC.md`. Default to 7 and 5 respectively if not found.
2. Run `/score-content [file]` to get current scores.
3. If all 5 dimensions ≥ threshold: print `PASS — all dimensions meet threshold (N/10)` and exit.
4. Find the lowest-scoring dimension. Map it to the responsible agent:
   - `clarity` → **editor agent**
   - `rigor` → **math-checker agent**
   - `completeness` → **structure-reviewer agent** (for book chapters) or **lecture-writer agent** (for notes)
   - `pedagogy` → **pedagogy-reviewer agent**
   - `style` → **humanizer agent**, then **proofreader agent**
5. Invoke the responsible agent on the file with an explicit instruction: "Improve the [DIMENSION] of this file. The current score is N/10. Focus specifically on [dimension-specific guidance from the rubric]."
6. Write the improved content back to the file.
7. Increment iteration counter. If counter ≥ max_refine_iterations: print `MAX ITERATIONS REACHED — human review required for [file]` and exit with a non-zero status.
8. Return to step 2.

**Tie-breaking:** If two dimensions are tied for lowest, prioritize in this order: rigor > completeness > clarity > pedagogy > style.

**Loop-break guard:** If the same dimension fails after 2 consecutive passes by its primary agent, switch to the next-lowest dimension instead of looping on the same one.

## Expected Output

The file improved to meet the threshold (all dimensions ≥ threshold), or a clear human-review notification if max iterations reached.

## Error Handling

- If the file does not exist: print an error and exit.
- If `docs/quality/` reports are stale: re-run `/score-content` to refresh before starting the loop.
- If the score does not improve after an agent pass: log the iteration, switch to the next-lowest dimension, and continue.
