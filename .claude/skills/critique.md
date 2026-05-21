# /critique

## Purpose

Get a blunt, ranked critique of a content file using the critic agent.

## When to Invoke

When you want honest, actionable feedback before or after scoring. Can be run at any time on any content file.

## Inputs Required

- File path: a `.tex` or `.md` content file

## Steps

1. Verify the file exists. If it is a placeholder (no real content), print "File is a placeholder — critique not meaningful" and exit.
2. **Invoke the critic agent**: provide the file content and ask for a ranked issue list (BLOCKER / MAJOR / MINOR) with specific locations and concrete fix suggestions.
3. Print the full ranked issue list.
4. Print the critic's one-paragraph overall assessment.
5. Print a summary count: `N BLOCKERs, N MAJORs, N MINORs`.
6. If there are BLOCKERs: ask the user "Would you like to run /refine-until-threshold to address these automatically?"

## Expected Output

A printed ranked issue list with severity labels, locations, and concrete fixes. A summary count.

## Error Handling

- If the file does not exist: print an error with the expected path.
- If the file is empty: print a warning and exit.
