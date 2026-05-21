# /interview-me

## Purpose

Configure the entire project through an interactive interview and write all answers to `TOPIC.md`.

## When to Invoke

First thing after cloning the template. Also run to update any project settings.

## Inputs Required

- None — the skill asks for everything it needs.

## Steps

1. Print: "Welcome to the book-course template. I will ask you 11 questions to configure this project. You can re-run /interview-me at any time to update settings."

2. **Q1** — Ask: "What is your course/book about?" (free text). Store as `title`.

3. **Q2** — Ask: "Who is the primary audience?" Offer choices:
   - A) Academic (researchers, students in a formal course)
   - B) Industry practitioners (engineers, data scientists)
   - C) Both equally
   Store the choice as `audience` (values: `academic` / `industry` / `both`).

4. **Q3** — Ask: "How many chapters/lectures are you planning?" (free text number). Store as `chapters_planned`.

5. **Q4** — Ask: "Should the book go deeper than the course (more proofs, references, appendices), or should they be 1-to-1?" Offer choices:
   - A) Loosely coupled — book goes deeper
   - B) Tightly coupled — 1-to-1
   Store as `book_depth` (`loose` / `coupled`).

6. **Q5** — Ask: "What programming language for companion code?" Offer choices:
   - A) Python
   - B) R
   - C) Julia
   - D) None (no code companion)
   Store as `language`.

7. **Q6** — Ask: "What minimum quality score (per dimension, 0–10) must content reach before it can be committed?" Offer choices: 6 / 7 / 8 / 9. Store as `quality_threshold`.

8. **Q7** — Ask: "How many auto-refinement iterations before human review is required?" Offer choices: 3 / 5 / 10 / unlimited (stores 999). Store as `max_refine_iterations`.

9. **Q8** — Ask: "Should the AI auto-commit after every file write?" Offer choices: Yes / No. Store as `auto_commit` (true / false).

10. **Q9** — Ask: "Git remote URL (GitHub, GitLab, etc.)? Type the URL or 'skip'." Store as `git_remote`.

11. **Q10** — Ask: "Your name, institution, and email (used in the book's title page)?" (free text, e.g., "Jane Smith, MIT, jsmith@mit.edu"). Parse into `author`, `institution`, `email`.

12. **Q11** — Ask: "License for this work?" Offer choices:
    - A) CC-BY (Creative Commons Attribution)
    - B) CC-BY-NC (Non-Commercial)
    - C) MIT
    - D) All rights reserved
    Store as `license`.

13. Write all answers to `TOPIC.md`, replacing the YAML front matter with the collected values. Preserve the body text below the `---` delimiter.

14. Update `book/preamble.tex`: find `\title{COURSE TITLE}`, `\author{AUTHOR NAME \\ INSTITUTION}` and replace with the actual values from Q1 and Q10.

15. If Q9 provided a URL (not 'skip'): run `git remote add origin [url]` (or `git remote set-url origin [url]` if remote already exists).

16. If the git repo has no commits yet: run `git add -A && git commit -m "chore: initialize project via /interview-me"`.

17. Print setup summary:
    ```
    === Project Configured ===
    Title:      [title]
    Author:     [author], [institution]
    Audience:   [audience]
    Chapters:   [chapters_planned] planned
    Language:   [language]
    Threshold:  [quality_threshold]/10
    
    Next steps:
    1. /new-topic — scaffold your first chapter
    2. /draft-chapter — write the first chapter
    3. /topic-status — check overall progress
    ```

## Expected Output

`TOPIC.md` fully populated with all 12 YAML fields. `book/preamble.tex` updated. Git remote configured if provided. Setup summary printed.

## Error Handling

- If `TOPIC.md` already has non-empty values: ask "TOPIC.md is already configured. Update all settings (start over) or update a specific field?" — if specific field, ask which one and update only that field's YAML value.
- If `book/preamble.tex` does not exist: warn "preamble.tex not found — update it manually with your title and author."
- If git remote already exists and a new URL is provided: use `git remote set-url` instead of `git remote add`.
