# /sync-lecture-chapter

## Purpose

Compare a lecture and its paired book chapter to identify gaps in either direction.

## When to Invoke

After editing either the chapter or the lecture notes, to ensure they remain aligned.

## Inputs Required

- Topic number/name (e.g., `01-intro`)
- `book/chapters/NN-name/chapter.tex` and `course/lectures/NN-name/notes.md`

## Steps

1. Read `book/chapters/NN-name/chapter.tex` and extract all `\section{}` and `\subsection{}` headings.
2. Read `course/lectures/NN-name/notes.md` and extract all `##` and `###` headings.
3. Print: **In chapter but not in lecture** — topics in the chapter that have no corresponding lecture section. Note these are expected for deep content (proofs, advanced extensions).
4. Print: **In lecture but not in chapter** — topics in the lecture notes with no corresponding chapter section. Flag these as gaps: the book should cover everything in the course.
5. Print: **Learning objectives not addressed** — objectives in `notes.md` that have no corresponding section in either document.

## Expected Output

Three-section gap report printed to console.

## Error Handling

- If either file is still a placeholder: note this and exit.
- If the topic does not exist in both domains: print which one is missing and suggest running `/new-topic`.
