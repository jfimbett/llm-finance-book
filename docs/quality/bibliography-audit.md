# Bibliography Audit Report

**Date:** 2026-05-31  
**Bib file:** `book/bibliography.bib`  
**Total entries:** 297  
**Total cited keys (across all .tex files):** 291  

---

## 1. Duplicate Keys

**Result: NONE** ✓

---

## 2. Missing Required Fields

**Result: NONE** ✓

Six entries were flagged by the automated parser but on manual inspection all have
correct `author` fields — the parser failed to handle LaTeX-encoded special characters
(e.g. `{\'e}`, `{\"{u}}`) in multi-line author strings. Affected keys confirmed clean:
`mikolov2013efficient`, `hochreiter1997long`, `chung2014empirical`, `pascanu2013gradient`,
`dao2022flashattention`, `kolbel2020esg`.

---

## 3. Undefined Cite Keys

**Result: NONE** ✓

Every `\cite{KEY}` in every `.tex` file has a matching entry in `bibliography.bib`.

---

## 4. Uncited Entries

**6 entries never cited in any `.tex` file — monitor, remove before final release if still uncited:**

`bertsimas1998optimal`, `desai2020calibration`, `goyal2019counterfactual`,
`huang2023finbert_tone`, `jegadeesh1993returns`, `zhong2021qmsum`

---

## 5. SSRN Fields on Published Papers

**Policy:** Published `@article` entries must not contain SSRN `url`, `note`, or `eprint`
fields. Only official journal doi/volume/pages should appear.

### Fixed this run

| Key | Journal | Fix applied |
|-----|---------|-------------|
| `cookson2026bankrun` | *Journal of Financial Economics*, vol. 176, 2026 | Removed `url = {https://papers.ssrn.com/...}` |
| `xu2024stock` | Was mistyped as `journal = {SSRN Working Paper}` | Converted to `@unpublished`; note flagged for author-list verification |

### Outstanding: `xu2024stock` needs full author list

Currently `author = {Xu, Zhiyuan and others}`. Full co-author list and SSRN ID could
not be located during this audit. **Must be resolved before final release.**

---

## Summary

| Check | Status |
|-------|--------|
| Duplicate keys | ✓ Clean |
| Missing required fields | ✓ Clean |
| Undefined cite keys | ✓ Clean |
| Uncited entries | ⚠ 6 — monitor until final release |
| SSRN on published papers | ✅ 2 violations fixed |
| `xu2024stock` author list | ⚠ Incomplete — verify before final release |
