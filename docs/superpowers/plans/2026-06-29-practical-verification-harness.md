# Practical Verification Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `code/practicals/verify.py`, a single local command that verifies every practical (notebook and agentic) works before a teaching session or course release.

**Architecture:** A small Python package `code/practicals/_verify/` holds the harness logic; `verify.py` is the CLI entry that discovers practicals, copies each to a throwaway temp dir, and runs a layered pyramid — Layer A (deterministic: fresh-venv install, config lint, reference integrity, pytest, smoke commands) always, and Layer B (live `claude -p` headless skill calls with deterministic assertions) only with `--live`. Subprocess boundaries (venv, pytest, claude) are injected so logic is unit-testable without real installs or API calls; the real boundaries are exercised in a final manual end-to-end task.

**Tech Stack:** Python 3.9 standard library + `pyyaml` (manifest parsing) + `nbconvert` (notebook execution) — all already present in the base environment. The `claude` CLI (v2.1.195) for Layer B.

## Global Constraints

- **Python 3.9.19** — put `from __future__ import annotations` at the top of every module so `X | None` and `list[X]` annotations are legal; never use `match` statements.
- **Never dirty the tracked tree** — all execution happens on a copy made under the system temp dir (`tempfile.mkdtemp()`), never inside the repo. Generated venvs/`reports/`/`__pycache__` must never land in `code/practicals/`.
- **No new third-party dependencies** — use only stdlib + the already-installed `pyyaml` and `nbconvert`.
- **Harness package dir is `code/practicals/_verify/`** — it does not match the `NN-` discovery pattern, so discovery ignores it.
- **All paths in this plan are relative to the repo root** `/Users/juan/Documents/llm-finance-book` unless absolute.
- **Run harness tests** with: `python -m pytest code/practicals/_verify/tests -q`
- **Commit style:** `feat(code): <summary>` per the project's commit convention (scope `code`).

---

### Task 1: Package scaffold + data model

**Files:**
- Create: `code/practicals/_verify/__init__.py`
- Create: `code/practicals/_verify/model.py`
- Create: `code/practicals/_verify/tests/__init__.py`
- Create: `code/practicals/_verify/tests/conftest.py`
- Test: `code/practicals/_verify/tests/test_model.py`

**Interfaces:**
- Produces:
  - `Kind` enum with members `NOTEBOOK = "notebook"`, `AGENTIC = "agentic"`.
  - `Practical(slug: str, path: Path, kind: Kind)` dataclass.
  - `CheckResult(name: str, passed: bool, detail: str = "", skipped: bool = False)` dataclass.
  - `PracticalResult(slug: str, kind: str, checks: list)` dataclass with property `ok: bool` — True when every check `passed or skipped`.

- [ ] **Step 1: Create the package init files**

`code/practicals/_verify/__init__.py`:
```python
"""Verification harness for code/practicals/. See docs/superpowers/plans."""
```

`code/practicals/_verify/tests/__init__.py`:
```python
```
(empty file)

- [ ] **Step 2: Create the test conftest that makes `_verify` importable**

`code/practicals/_verify/tests/conftest.py`:
```python
from __future__ import annotations

import sys
from pathlib import Path

# Put code/practicals/ on sys.path so `import _verify...` works under pytest.
PRACTICALS_DIR = Path(__file__).resolve().parents[2]
if str(PRACTICALS_DIR) not in sys.path:
    sys.path.insert(0, str(PRACTICALS_DIR))
```

- [ ] **Step 3: Write the failing test**

`code/practicals/_verify/tests/test_model.py`:
```python
from __future__ import annotations

from pathlib import Path

from _verify.model import Kind, Practical, CheckResult, PracticalResult


def test_practical_holds_slug_path_kind():
    p = Practical(slug="04-llm-agents", path=Path("/tmp/04"), kind=Kind.AGENTIC)
    assert p.slug == "04-llm-agents"
    assert p.kind is Kind.AGENTIC


def test_practical_result_ok_true_when_all_pass_or_skip():
    checks = [
        CheckResult(name="config-lint", passed=True),
        CheckResult(name="pytest", passed=False, skipped=True),
    ]
    result = PracticalResult(slug="04-llm-agents", kind="agentic", checks=checks)
    assert result.ok is True


def test_practical_result_ok_false_on_real_failure():
    checks = [CheckResult(name="config-lint", passed=False, detail="bad json")]
    result = PracticalResult(slug="04-llm-agents", kind="agentic", checks=checks)
    assert result.ok is False
```

- [ ] **Step 4: Run the test to verify it fails**

Run: `python -m pytest code/practicals/_verify/tests/test_model.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named '_verify.model'`

- [ ] **Step 5: Write the implementation**

`code/practicals/_verify/model.py`:
```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Kind(Enum):
    NOTEBOOK = "notebook"
    AGENTIC = "agentic"


@dataclass
class Practical:
    slug: str
    path: Path
    kind: Kind


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""
    skipped: bool = False


@dataclass
class PracticalResult:
    slug: str
    kind: str
    checks: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(c.passed or c.skipped for c in self.checks)
```

- [ ] **Step 6: Run the test to verify it passes**

Run: `python -m pytest code/practicals/_verify/tests/test_model.py -q`
Expected: PASS (3 passed)

- [ ] **Step 7: Commit**

```bash
git add code/practicals/_verify/__init__.py code/practicals/_verify/model.py code/practicals/_verify/tests/
git commit -m "feat(code): scaffold practical-verify package and data model"
```

---

### Task 2: Discovery & classification

**Files:**
- Create: `code/practicals/_verify/discovery.py`
- Test: `code/practicals/_verify/tests/test_discovery.py`

**Interfaces:**
- Consumes: `Practical`, `Kind` from Task 1.
- Produces:
  - `discover(root: Path) -> list[Practical]` — immediate subdirs of `root` whose name matches `^\d{2}-`, sorted by name, classified.
  - `classify(path: Path) -> Kind` — `AGENTIC` if `path/".claude"` is a dir, else `NOTEBOOK`.
  - `select(practicals: list, only: str | None) -> list` — when `only` is a comma-separated list like `"04,09"` or `"04-llm-agents"`, keep practicals whose slug starts with any token; `None`/empty keeps all.

- [ ] **Step 1: Write the failing test**

`code/practicals/_verify/tests/test_discovery.py`:
```python
from __future__ import annotations

from pathlib import Path

from _verify.discovery import discover, classify, select
from _verify.model import Kind


def _make_tree(tmp_path: Path) -> Path:
    root = tmp_path / "practicals"
    (root / "01-intro").mkdir(parents=True)
    (root / "01-intro" / "practical.ipynb").write_text("{}")
    (root / "04-llm-agents" / ".claude").mkdir(parents=True)
    (root / "_verify").mkdir()           # must be ignored (no NN- prefix)
    (root / "notes.md").write_text("x")  # files ignored
    return root


def test_discover_finds_and_classifies(tmp_path):
    found = discover(_make_tree(tmp_path))
    slugs = [p.slug for p in found]
    assert slugs == ["01-intro", "04-llm-agents"]
    kinds = {p.slug: p.kind for p in found}
    assert kinds["01-intro"] is Kind.NOTEBOOK
    assert kinds["04-llm-agents"] is Kind.AGENTIC


def test_classify_agentic_when_claude_dir_present(tmp_path):
    d = tmp_path / "04-x"
    (d / ".claude").mkdir(parents=True)
    assert classify(d) is Kind.AGENTIC


def test_select_filters_by_prefix(tmp_path):
    found = discover(_make_tree(tmp_path))
    picked = select(found, "04")
    assert [p.slug for p in picked] == ["04-llm-agents"]
    assert select(found, None) == found
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest code/practicals/_verify/tests/test_discovery.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named '_verify.discovery'`

- [ ] **Step 3: Write the implementation**

`code/practicals/_verify/discovery.py`:
```python
from __future__ import annotations

import re
from pathlib import Path

from .model import Practical, Kind

_PRACTICAL_RE = re.compile(r"^\d{2}-")


def classify(path: Path) -> Kind:
    if (path / ".claude").is_dir():
        return Kind.AGENTIC
    return Kind.NOTEBOOK


def discover(root: Path) -> list:
    out = []
    for child in sorted(root.iterdir(), key=lambda p: p.name):
        if not child.is_dir() or not _PRACTICAL_RE.match(child.name):
            continue
        out.append(Practical(slug=child.name, path=child.resolve(), kind=classify(child)))
    return out


def select(practicals: list, only: str | None) -> list:
    if not only:
        return practicals
    tokens = [t.strip() for t in only.split(",") if t.strip()]
    return [p for p in practicals if any(p.slug.startswith(t) for t in tokens)]
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest code/practicals/_verify/tests/test_discovery.py -q`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
git add code/practicals/_verify/discovery.py code/practicals/_verify/tests/test_discovery.py
git commit -m "feat(code): discover and classify practicals"
```

---

### Task 3: Manifest loading & validation

**Files:**
- Create: `code/practicals/_verify/manifest.py`
- Test: `code/practicals/_verify/tests/test_manifest.py`

**Interfaces:**
- Produces:
  - `LiveCheck(prompt: str, expect_file: str | None = None, expect_contains: list = [], expect_not_contains: list = [])` dataclass.
  - `Manifest(smoke: list, live: list)` dataclass (`smoke` is `list[str]`, `live` is `list[LiveCheck]`).
  - `load_manifest(practical_path: Path) -> Manifest` — reads `practical_path/"verify.yaml"`; returns an empty `Manifest(smoke=[], live=[])` when the file is absent. Raises `ValueError` with a clear message if a `live` item lacks a `prompt`.

- [ ] **Step 1: Write the failing test**

`code/practicals/_verify/tests/test_manifest.py`:
```python
from __future__ import annotations

import pytest

from _verify.manifest import load_manifest, Manifest, LiveCheck


def test_missing_manifest_returns_empty(tmp_path):
    m = load_manifest(tmp_path)
    assert m == Manifest(smoke=[], live=[])


def test_loads_smoke_and_live(tmp_path):
    (tmp_path / "verify.yaml").write_text(
        "smoke:\n"
        "  - python -m tools.retrieve \"q\" -k 4 > reports/_context.json\n"
        "live:\n"
        "  - prompt: '/ask \"risk?\"'\n"
        "    expect_file: 'reports/*.md'\n"
        "    expect_contains: ['concentration']\n"
        "  - prompt: '/ask \"net income?\"'\n"
        "    expect_not_contains: ['$']\n"
    )
    m = load_manifest(tmp_path)
    assert m.smoke == ['python -m tools.retrieve "q" -k 4 > reports/_context.json']
    assert m.live[0] == LiveCheck(prompt='/ask "risk?"', expect_file='reports/*.md',
                                  expect_contains=['concentration'])
    assert m.live[1].expect_not_contains == ['$']


def test_live_item_without_prompt_raises(tmp_path):
    (tmp_path / "verify.yaml").write_text("live:\n  - expect_contains: ['x']\n")
    with pytest.raises(ValueError, match="prompt"):
        load_manifest(tmp_path)
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest code/practicals/_verify/tests/test_manifest.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named '_verify.manifest'`

- [ ] **Step 3: Write the implementation**

`code/practicals/_verify/manifest.py`:
```python
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class LiveCheck:
    prompt: str
    expect_file: str | None = None
    expect_contains: list = field(default_factory=list)
    expect_not_contains: list = field(default_factory=list)


@dataclass
class Manifest:
    smoke: list = field(default_factory=list)
    live: list = field(default_factory=list)


def _parse_live(item: dict) -> LiveCheck:
    if not isinstance(item, dict) or "prompt" not in item:
        raise ValueError(f"live check is missing required 'prompt': {item!r}")
    return LiveCheck(
        prompt=item["prompt"],
        expect_file=item.get("expect_file"),
        expect_contains=list(item.get("expect_contains", []) or []),
        expect_not_contains=list(item.get("expect_not_contains", []) or []),
    )


def load_manifest(practical_path: Path) -> Manifest:
    f = practical_path / "verify.yaml"
    if not f.exists():
        return Manifest(smoke=[], live=[])
    data = yaml.safe_load(f.read_text()) or {}
    smoke = [str(c) for c in (data.get("smoke", []) or [])]
    live = [_parse_live(item) for item in (data.get("live", []) or [])]
    return Manifest(smoke=smoke, live=live)
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest code/practicals/_verify/tests/test_manifest.py -q`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
git add code/practicals/_verify/manifest.py code/practicals/_verify/tests/test_manifest.py
git commit -m "feat(code): load and validate verify.yaml manifests"
```

---

### Task 4: Config lint + reference integrity

**Files:**
- Create: `code/practicals/_verify/static_checks.py`
- Test: `code/practicals/_verify/tests/test_static_checks.py`

**Interfaces:**
- Consumes: `CheckResult` from Task 1.
- Produces:
  - `parse_frontmatter(text: str) -> dict | None` — returns the parsed YAML mapping between a leading `---` / `---` fence, or `None` if there is no frontmatter.
  - `lint_config(practical_dir: Path) -> CheckResult` (name `"config-lint"`): passes when `.claude/settings.json` (if present) is valid JSON **and** every `.claude/skills/*/SKILL.md` and `.claude/agents/*.md` has frontmatter containing non-empty `name` and `description`. A missing `settings.json` is fine. Detail lists each offending file.
  - `check_references(practical_dir: Path) -> CheckResult` (name `"references"`): scans the text of `CLAUDE.md` and every `SKILL.md` for `tools.<module>` references and `data/<path>` references and confirms each exists on disk (`tools/<module>.py` and `<practical_dir>/data/<path>`). Detail lists missing targets. Passes vacuously when nothing is referenced.

- [ ] **Step 1: Write the failing test**

`code/practicals/_verify/tests/test_static_checks.py`:
```python
from __future__ import annotations

from pathlib import Path

from _verify.static_checks import parse_frontmatter, lint_config, check_references


def _agentic(tmp_path: Path) -> Path:
    d = tmp_path / "04-x"
    (d / ".claude" / "skills" / "ask").mkdir(parents=True)
    (d / ".claude" / "agents").mkdir(parents=True)
    (d / "tools").mkdir()
    (d / "data" / "corpus").mkdir(parents=True)
    (d / ".claude" / "settings.json").write_text('{"permissions": {}}')
    (d / ".claude" / "skills" / "ask" / "SKILL.md").write_text(
        "---\nname: ask\ndescription: Ask a question\n---\nRun python -m tools.retrieve and read data/corpus/x.txt\n"
    )
    (d / ".claude" / "agents" / "retriever.md").write_text(
        "---\nname: retriever\ndescription: Retrieves chunks\n---\nbody\n"
    )
    (d / "tools" / "retrieve.py").write_text("x = 1\n")
    (d / "data" / "corpus" / "x.txt").write_text("hello")
    (d / "CLAUDE.md").write_text("Use tools.retrieve only.\n")
    return d


def test_parse_frontmatter_reads_mapping():
    fm = parse_frontmatter("---\nname: ask\ndescription: d\n---\nbody")
    assert fm == {"name": "ask", "description": "d"}
    assert parse_frontmatter("no frontmatter here") is None


def test_lint_config_passes_on_good_tree(tmp_path):
    assert lint_config(_agentic(tmp_path)).passed is True


def test_lint_config_fails_on_bad_json(tmp_path):
    d = _agentic(tmp_path)
    (d / ".claude" / "settings.json").write_text("{not json")
    res = lint_config(d)
    assert res.passed is False
    assert "settings.json" in res.detail


def test_lint_config_fails_on_missing_description(tmp_path):
    d = _agentic(tmp_path)
    (d / ".claude" / "skills" / "ask" / "SKILL.md").write_text("---\nname: ask\n---\nbody")
    res = lint_config(d)
    assert res.passed is False
    assert "description" in res.detail


def test_check_references_passes_when_targets_exist(tmp_path):
    assert check_references(_agentic(tmp_path)).passed is True


def test_check_references_fails_on_dangling_tool(tmp_path):
    d = _agentic(tmp_path)
    (d / "tools" / "retrieve.py").unlink()
    res = check_references(d)
    assert res.passed is False
    assert "retrieve" in res.detail
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest code/practicals/_verify/tests/test_static_checks.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named '_verify.static_checks'`

- [ ] **Step 3: Write the implementation**

`code/practicals/_verify/static_checks.py`:
```python
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from .model import CheckResult

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_TOOLS_RE = re.compile(r"tools\.([a-zA-Z_][a-zA-Z0-9_]*)")
_DATA_RE = re.compile(r"(data/[A-Za-z0-9_./-]+\.[A-Za-z0-9]+)")


def parse_frontmatter(text: str) -> dict | None:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None
    loaded = yaml.safe_load(m.group(1))
    return loaded if isinstance(loaded, dict) else None


def _doc_files(practical_dir: Path) -> list:
    docs = []
    claude_md = practical_dir / "CLAUDE.md"
    if claude_md.exists():
        docs.append(claude_md)
    docs.extend(sorted((practical_dir / ".claude" / "skills").rglob("SKILL.md")))
    return docs


def lint_config(practical_dir: Path) -> CheckResult:
    problems = []

    settings = practical_dir / ".claude" / "settings.json"
    if settings.exists():
        try:
            json.loads(settings.read_text())
        except json.JSONDecodeError as exc:
            problems.append(f".claude/settings.json: invalid JSON ({exc})")

    md_files = sorted((practical_dir / ".claude" / "skills").rglob("SKILL.md"))
    md_files += sorted((practical_dir / ".claude" / "agents").glob("*.md"))
    for md in md_files:
        fm = parse_frontmatter(md.read_text())
        rel = md.relative_to(practical_dir)
        if fm is None:
            problems.append(f"{rel}: no frontmatter")
            continue
        for key in ("name", "description"):
            if not str(fm.get(key, "")).strip():
                problems.append(f"{rel}: missing '{key}'")

    return CheckResult(name="config-lint", passed=not problems, detail="; ".join(problems))


def check_references(practical_dir: Path) -> CheckResult:
    missing = []
    for doc in _doc_files(practical_dir):
        text = doc.read_text()
        for mod in sorted(set(_TOOLS_RE.findall(text))):
            if not (practical_dir / "tools" / f"{mod}.py").exists():
                missing.append(f"tools.{mod} (in {doc.name})")
        for data_ref in sorted(set(_DATA_RE.findall(text))):
            if not (practical_dir / data_ref).exists():
                missing.append(f"{data_ref} (in {doc.name})")
    return CheckResult(name="references", passed=not missing, detail="; ".join(sorted(set(missing))))
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest code/practicals/_verify/tests/test_static_checks.py -q`
Expected: PASS (6 passed)

- [ ] **Step 5: Commit**

```bash
git add code/practicals/_verify/static_checks.py code/practicals/_verify/tests/test_static_checks.py
git commit -m "feat(code): add config-lint and reference-integrity checks"
```

---

### Task 5: Sandbox — repo-safe temp copy + venv

**Files:**
- Create: `code/practicals/_verify/sandbox.py`
- Test: `code/practicals/_verify/tests/test_sandbox.py`

**Interfaces:**
- Produces:
  - `copy_practical(src: Path, dest: Path) -> Path` — copies the practical tree to `dest`, ignoring `__pycache__`, `.pytest_cache`, `.venv`, `*.pyc`, `.git`. Returns `dest`.
  - `venv_python(venv_dir: Path) -> Path` — returns the venv's `bin/python` path (POSIX).
  - `make_venv(venv_dir: Path) -> Path` — creates a venv with pip at `venv_dir`, returns `venv_python(venv_dir)`.
  - `pip_install(py: Path, requirements: Path) -> subprocess.CompletedProcess` — runs `<py> -m pip install -q -r <requirements>`, captured.

- [ ] **Step 1: Write the failing test**

`code/practicals/_verify/tests/test_sandbox.py`:
```python
from __future__ import annotations

from pathlib import Path

from _verify.sandbox import copy_practical, make_venv, venv_python


def test_copy_practical_excludes_caches(tmp_path):
    src = tmp_path / "04-x"
    (src / "tools").mkdir(parents=True)
    (src / "tools" / "a.py").write_text("x = 1\n")
    (src / "__pycache__").mkdir()
    (src / "__pycache__" / "junk.pyc").write_text("junk")
    dest = copy_practical(src, tmp_path / "copy")
    assert (dest / "tools" / "a.py").exists()
    assert not (dest / "__pycache__").exists()


def test_make_venv_creates_python(tmp_path):
    py = make_venv(tmp_path / ".venv")
    assert py == venv_python(tmp_path / ".venv")
    assert py.exists()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest code/practicals/_verify/tests/test_sandbox.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named '_verify.sandbox'`

- [ ] **Step 3: Write the implementation**

`code/practicals/_verify/sandbox.py`:
```python
from __future__ import annotations

import shutil
import subprocess
import venv
from pathlib import Path

_IGNORE = shutil.ignore_patterns("__pycache__", ".pytest_cache", ".venv", "*.pyc", ".git")


def copy_practical(src: Path, dest: Path) -> Path:
    shutil.copytree(src, dest, ignore=_IGNORE)
    return dest


def venv_python(venv_dir: Path) -> Path:
    return venv_dir / "bin" / "python"


def make_venv(venv_dir: Path) -> Path:
    venv.create(venv_dir, with_pip=True)
    return venv_python(venv_dir)


def pip_install(py: Path, requirements: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(py), "-m", "pip", "install", "-q", "-r", str(requirements)],
        capture_output=True,
        text=True,
    )
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest code/practicals/_verify/tests/test_sandbox.py -q`
Expected: PASS (2 passed). Note: `test_make_venv_creates_python` takes a few seconds (it builds a real venv).

- [ ] **Step 5: Commit**

```bash
git add code/practicals/_verify/sandbox.py code/practicals/_verify/tests/test_sandbox.py
git commit -m "feat(code): repo-safe temp copy and throwaway venv helpers"
```

---

### Task 6: pytest + smoke command runners

**Files:**
- Create: `code/practicals/_verify/run_checks.py`
- Test: `code/practicals/_verify/tests/test_run_checks.py`

**Interfaces:**
- Consumes: `CheckResult` (Task 1), `Manifest` (Task 3).
- Produces:
  - `run_pytest(practical_dir: Path, py: Path) -> CheckResult` (name `"pytest"`): if `practical_dir/"tests"` is not a dir, return a skipped pass (`skipped=True`); else run `<py> -m pytest -q` with `cwd=practical_dir` and pass/fail on exit code; on failure the detail is the last ~500 chars of combined output.
  - `run_smoke(practical_dir: Path, py: Path, smoke: list) -> list` — for each shell command string, run it with `shell=True`, `cwd=practical_dir`, and a `PATH` that puts `py.parent` first (so bare `python` resolves to the venv). Returns one `CheckResult` per command (name `"smoke[i]"`), failing on non-zero exit.

- [ ] **Step 1: Write the failing test**

`code/practicals/_verify/tests/test_run_checks.py`:
```python
from __future__ import annotations

import sys
from pathlib import Path

from _verify.run_checks import run_pytest, run_smoke


def test_run_pytest_skips_without_tests_dir(tmp_path):
    res = run_pytest(tmp_path, Path(sys.executable))
    assert res.skipped is True
    assert res.passed is True


def test_run_pytest_passes_on_green_suite(tmp_path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_ok.py").write_text("def test_ok():\n    assert 1 == 1\n")
    res = run_pytest(tmp_path, Path(sys.executable))
    assert res.passed is True
    assert res.skipped is False


def test_run_pytest_fails_on_red_suite(tmp_path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_bad.py").write_text("def test_bad():\n    assert 1 == 2\n")
    res = run_pytest(tmp_path, Path(sys.executable))
    assert res.passed is False


def test_run_smoke_reports_per_command(tmp_path):
    results = run_smoke(tmp_path, Path(sys.executable),
                        ["python -c \"print('hi')\"", "python -c \"import sys; sys.exit(3)\""])
    assert results[0].passed is True
    assert results[1].passed is False
    assert results[0].name == "smoke[0]"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest code/practicals/_verify/tests/test_run_checks.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named '_verify.run_checks'`

- [ ] **Step 3: Write the implementation**

`code/practicals/_verify/run_checks.py`:
```python
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .model import CheckResult


def run_pytest(practical_dir: Path, py: Path) -> CheckResult:
    if not (practical_dir / "tests").is_dir():
        return CheckResult(name="pytest", passed=True, skipped=True, detail="no tests/ dir")
    proc = subprocess.run(
        [str(py), "-m", "pytest", "-q"],
        cwd=str(practical_dir),
        capture_output=True,
        text=True,
    )
    detail = "" if proc.returncode == 0 else (proc.stdout + proc.stderr)[-500:]
    return CheckResult(name="pytest", passed=proc.returncode == 0, detail=detail)


def _venv_env(py: Path) -> dict:
    env = os.environ.copy()
    env["PATH"] = str(py.parent) + os.pathsep + env.get("PATH", "")
    return env


def run_smoke(practical_dir: Path, py: Path, smoke: list) -> list:
    results = []
    for i, cmd in enumerate(smoke):
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=str(practical_dir),
            capture_output=True,
            text=True,
            env=_venv_env(py),
        )
        detail = "" if proc.returncode == 0 else f"$ {cmd}\n" + (proc.stdout + proc.stderr)[-400:]
        results.append(CheckResult(name=f"smoke[{i}]", passed=proc.returncode == 0, detail=detail))
    return results
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest code/practicals/_verify/tests/test_run_checks.py -q`
Expected: PASS (4 passed)

- [ ] **Step 5: Commit**

```bash
git add code/practicals/_verify/run_checks.py code/practicals/_verify/tests/test_run_checks.py
git commit -m "feat(code): pytest and smoke-command runners"
```

---

### Task 7: Notebook execution check

**Files:**
- Create: `code/practicals/_verify/notebook.py`
- Test: `code/practicals/_verify/tests/test_notebook.py`

**Interfaces:**
- Consumes: `CheckResult` (Task 1).
- Produces:
  - `run_notebook(practical_dir: Path) -> CheckResult` (name `"notebook"`): finds the first `*.ipynb` in `practical_dir`; executes it with nbconvert's `ExecutePreprocessor` (`timeout=600`, `kernel_name="python3"`, working dir = `practical_dir`). Passes if all cells run; on a cell error returns failure with the error summary; if there is no kernel/execution infra (e.g. `ipykernel` missing) returns a skipped result with remediation detail; skipped pass when no notebook is present.

- [ ] **Step 1: Write the failing test**

`code/practicals/_verify/tests/test_notebook.py`:
```python
from __future__ import annotations

import json
from pathlib import Path

import pytest

from _verify.notebook import run_notebook

pytest.importorskip("ipykernel")  # execution needs a python3 kernel


def _nb(cells):
    return json.dumps({
        "cells": [{"cell_type": "code", "metadata": {}, "source": c,
                   "outputs": [], "execution_count": None} for c in cells],
        "metadata": {}, "nbformat": 4, "nbformat_minor": 5,
    })


def test_notebook_skips_when_absent(tmp_path):
    res = run_notebook(tmp_path)
    assert res.skipped is True


def test_notebook_passes_on_clean_cells(tmp_path):
    (tmp_path / "practical.ipynb").write_text(_nb(["x = 1 + 1\n", "assert x == 2\n"]))
    res = run_notebook(tmp_path)
    assert res.passed is True and res.skipped is False


def test_notebook_fails_on_cell_error(tmp_path):
    (tmp_path / "practical.ipynb").write_text(_nb(["raise ValueError('boom')\n"]))
    res = run_notebook(tmp_path)
    assert res.passed is False
    assert "boom" in res.detail or "ValueError" in res.detail
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest code/practicals/_verify/tests/test_notebook.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named '_verify.notebook'`

- [ ] **Step 3: Write the implementation**

`code/practicals/_verify/notebook.py`:
```python
from __future__ import annotations

from pathlib import Path

from .model import CheckResult


def run_notebook(practical_dir: Path) -> CheckResult:
    notebooks = sorted(practical_dir.glob("*.ipynb"))
    if not notebooks:
        return CheckResult(name="notebook", passed=True, skipped=True, detail="no .ipynb")

    try:
        import nbformat
        from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
    except ImportError as exc:
        return CheckResult(name="notebook", passed=True, skipped=True,
                           detail=f"nbconvert unavailable: {exc}")

    nb_path = notebooks[0]
    nb = nbformat.read(str(nb_path), as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    try:
        ep.preprocess(nb, {"metadata": {"path": str(practical_dir)}})
    except CellExecutionError as exc:
        return CheckResult(name="notebook", passed=False, detail=str(exc)[-500:])
    except Exception as exc:  # missing kernel, dead kernel, etc.
        msg = str(exc)
        if "kernel" in msg.lower() or "ipykernel" in msg.lower():
            return CheckResult(name="notebook", passed=True, skipped=True,
                               detail=f"no python3 kernel: install ipykernel ({msg[-150:]})")
        return CheckResult(name="notebook", passed=False, detail=msg[-500:])
    return CheckResult(name="notebook", passed=True, detail=str(nb_path.name))
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest code/practicals/_verify/tests/test_notebook.py -q`
Expected: PASS (3 passed), or SKIPPED if `ipykernel` is not installed (the `importorskip` guard). If skipped, run `python3 -m pip install ipykernel` and re-run to confirm green.

- [ ] **Step 5: Commit**

```bash
git add code/practicals/_verify/notebook.py code/practicals/_verify/tests/test_notebook.py
git commit -m "feat(code): notebook execution check via nbconvert"
```

---

### Task 8: Live-Claude assertion evaluation + injectable runner

**Files:**
- Create: `code/practicals/_verify/live.py`
- Test: `code/practicals/_verify/tests/test_live.py`

**Interfaces:**
- Consumes: `CheckResult` (Task 1), `LiveCheck` (Task 3).
- Produces:
  - `evaluate_live(result_json: dict, check: LiveCheck, work_dir: Path) -> CheckResult` — pure assertion logic: fails if `result_json.get("is_error")` is truthy, if any `expect_contains` substring is absent from `result_json.get("result", "")`, if any `expect_not_contains` substring is present, or if `expect_file` glob matches nothing under `work_dir`. Check name is `"live:" + check.prompt[:48]`.
  - `claude_runner(prompt: str, cwd: Path) -> dict` — default subprocess boundary: runs `claude -p <prompt> --permission-mode bypassPermissions --max-turns 15 --output-format json` with `cwd`, parses stdout as JSON; on non-JSON output returns `{"is_error": True, "result": <stderr/stdout tail>}`.
  - `run_live(work_dir: Path, checks: list, runner=claude_runner) -> list` — runs each `LiveCheck` through `runner` then `evaluate_live`, returning a `CheckResult` list. The `runner` parameter is injected so tests never call the real CLI.

- [ ] **Step 1: Write the failing test**

`code/practicals/_verify/tests/test_live.py`:
```python
from __future__ import annotations

from pathlib import Path

from _verify.live import evaluate_live, run_live
from _verify.manifest import LiveCheck


def test_evaluate_live_passes(tmp_path):
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / "out.md").write_text("ok")
    check = LiveCheck(prompt='/ask "risk?"', expect_file="reports/*.md",
                      expect_contains=["concentration"])
    res = evaluate_live({"is_error": False, "result": "the concentration risk is high"},
                        check, tmp_path)
    assert res.passed is True


def test_evaluate_live_fails_on_is_error(tmp_path):
    check = LiveCheck(prompt="/ask x")
    res = evaluate_live({"is_error": True, "result": ""}, check, tmp_path)
    assert res.passed is False
    assert "is_error" in res.detail


def test_evaluate_live_fails_on_missing_substring_and_file(tmp_path):
    check = LiveCheck(prompt="/ask x", expect_file="reports/*.md",
                      expect_contains=["concentration"])
    res = evaluate_live({"is_error": False, "result": "unrelated text"}, check, tmp_path)
    assert res.passed is False
    assert "concentration" in res.detail
    assert "reports/*.md" in res.detail


def test_evaluate_live_not_contains(tmp_path):
    check = LiveCheck(prompt="/ask x", expect_not_contains=["$"])
    ok = evaluate_live({"is_error": False, "result": "Not answerable"}, check, tmp_path)
    bad = evaluate_live({"is_error": False, "result": "net income was $5M"}, check, tmp_path)
    assert ok.passed is True and bad.passed is False


def test_run_live_uses_injected_runner(tmp_path):
    calls = []

    def fake_runner(prompt, cwd):
        calls.append((prompt, cwd))
        return {"is_error": False, "result": "concentration risk"}

    checks = [LiveCheck(prompt="/ask a", expect_contains=["concentration"])]
    results = run_live(tmp_path, checks, runner=fake_runner)
    assert results[0].passed is True
    assert calls == [("/ask a", tmp_path)]
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest code/practicals/_verify/tests/test_live.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named '_verify.live'`

- [ ] **Step 3: Write the implementation**

`code/practicals/_verify/live.py`:
```python
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .model import CheckResult


def claude_runner(prompt: str, cwd: Path) -> dict:
    proc = subprocess.run(
        ["claude", "-p", prompt,
         "--permission-mode", "bypassPermissions",
         "--max-turns", "15",
         "--output-format", "json"],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"is_error": True, "result": (proc.stderr or proc.stdout)[-400:]}


def evaluate_live(result_json: dict, check, work_dir: Path) -> CheckResult:
    problems = []
    if result_json.get("is_error"):
        problems.append("is_error=true")
    text = result_json.get("result", "") or ""
    for needle in check.expect_contains:
        if needle not in text:
            problems.append(f"missing {needle!r}")
    for needle in check.expect_not_contains:
        if needle in text:
            problems.append(f"unexpected {needle!r}")
    if check.expect_file and not list(work_dir.glob(check.expect_file)):
        problems.append(f"no file matching {check.expect_file}")
    name = "live:" + check.prompt[:48]
    return CheckResult(name=name, passed=not problems, detail="; ".join(problems))


def run_live(work_dir: Path, checks: list, runner=claude_runner) -> list:
    results = []
    for check in checks:
        result_json = runner(check.prompt, work_dir)
        results.append(evaluate_live(result_json, check, work_dir))
    return results
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m pytest code/practicals/_verify/tests/test_live.py -q`
Expected: PASS (5 passed)

- [ ] **Step 5: Commit**

```bash
git add code/practicals/_verify/live.py code/practicals/_verify/tests/test_live.py
git commit -m "feat(code): live-Claude assertion evaluation with injectable runner"
```

---

### Task 9: CLI orchestration, table/JSON output, gitignore

**Files:**
- Create: `code/practicals/verify.py`
- Create: `code/practicals/_verify/orchestrate.py`
- Modify: `.gitignore` (append two lines at end)
- Test: `code/practicals/_verify/tests/test_orchestrate.py`

**Interfaces:**
- Consumes: everything from Tasks 1–8 (`discover`, `select`, `load_manifest`, `lint_config`, `check_references`, `copy_practical`, `make_venv`, `pip_install`, `run_pytest`, `run_smoke`, `run_notebook`, `run_live`).
- Produces (in `orchestrate.py`):
  - `verify_practical(practical, *, run_a: bool, run_b: bool, fast: bool, shared_py: Path | None, workspace: Path, live_runner=None) -> PracticalResult` — copies the practical into `workspace`, builds (or reuses) a venv, runs the applicable checks, returns a `PracticalResult`. For notebook practicals only the notebook check runs (Layer A); Layer B is skipped.
  - `render_table(results: list) -> str` — a fixed-width text table, one row per practical: slug, kind, `PASS`/`FAIL`, and a compact list of failed check names.
  - `to_report(results: list) -> dict` — JSON-serializable summary `{"ok": bool, "practicals": [{"slug","kind","ok","checks":[{"name","passed","skipped","detail"}]}]}`.
- Produces (in `verify.py`): a `main(argv=None) -> int` CLI with flags `--live`, `--only`, `--fast`/`--shared-env`, `--layer {a,b}`; writes `code/practicals/.verify-report.json`; returns non-zero if any practical failed.

- [ ] **Step 1: Write the failing test** (orchestration logic with injected boundaries — no real venv/claude)

`code/practicals/_verify/tests/test_orchestrate.py`:
```python
from __future__ import annotations

from pathlib import Path

from _verify.orchestrate import render_table, to_report
from _verify.model import CheckResult, PracticalResult


def _results():
    return [
        PracticalResult("04-llm-agents", "agentic",
                        [CheckResult("config-lint", True), CheckResult("pytest", False, "boom")]),
        PracticalResult("01-intro", "notebook", [CheckResult("notebook", True)]),
    ]


def test_render_table_marks_pass_and_fail():
    table = render_table(_results())
    assert "04-llm-agents" in table
    assert "FAIL" in table
    assert "pytest" in table          # failed check named
    assert "01-intro" in table and "PASS" in table


def test_to_report_round_trips():
    report = to_report(_results())
    assert report["ok"] is False
    slugs = [p["slug"] for p in report["practicals"]]
    assert slugs == ["04-llm-agents", "01-intro"]
    assert report["practicals"][0]["checks"][1]["detail"] == "boom"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest code/practicals/_verify/tests/test_orchestrate.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named '_verify.orchestrate'`

- [ ] **Step 3: Write `orchestrate.py`**

`code/practicals/_verify/orchestrate.py`:
```python
from __future__ import annotations

import sys
from pathlib import Path

from .model import Kind, PracticalResult
from .manifest import load_manifest
from .static_checks import lint_config, check_references
from .sandbox import copy_practical, make_venv, pip_install, venv_python
from .run_checks import run_pytest, run_smoke
from .notebook import run_notebook
from .live import run_live, claude_runner


def _prepare_env(work_dir: Path, fast: bool, shared_py: Path | None) -> Path:
    """Return the python interpreter to use for this practical."""
    req = work_dir / "requirements.txt"
    if fast and shared_py is not None:
        if req.exists():
            pip_install(shared_py, req)
        return shared_py
    py = make_venv(work_dir / ".venv")
    if req.exists():
        pip_install(py, req)
    return py


def verify_practical(practical, *, run_a: bool, run_b: bool, fast: bool,
                     shared_py: Path | None, workspace: Path,
                     live_runner=claude_runner) -> PracticalResult:
    work_dir = copy_practical(practical.path, workspace / practical.slug)
    checks = []

    if practical.kind is Kind.NOTEBOOK:
        if run_a:
            checks.append(run_notebook(work_dir))
        return PracticalResult(practical.slug, practical.kind.value, checks)

    manifest = load_manifest(work_dir)
    if run_a:
        checks.append(lint_config(work_dir))
        checks.append(check_references(work_dir))
        py = _prepare_env(work_dir, fast, shared_py)
        checks.append(run_pytest(work_dir, py))
        checks.extend(run_smoke(work_dir, py, manifest.smoke))
    if run_b:
        checks.extend(run_live(work_dir, manifest.live, runner=live_runner))

    return PracticalResult(practical.slug, practical.kind.value, checks)


def _failed_names(result: PracticalResult) -> str:
    return ",".join(c.name for c in result.checks if not (c.passed or c.skipped))


def render_table(results: list) -> str:
    width = max([len(r.slug) for r in results] + [12])
    lines = [f"{'PRACTICAL'.ljust(width)}  KIND      STATUS  FAILED"]
    for r in results:
        status = "PASS" if r.ok else "FAIL"
        lines.append(f"{r.slug.ljust(width)}  {r.kind.ljust(8)}  {status:<6}  {_failed_names(r)}")
    passed = sum(1 for r in results if r.ok)
    lines.append(f"\n{passed}/{len(results)} practicals passed")
    return "\n".join(lines)


def to_report(results: list) -> dict:
    return {
        "ok": all(r.ok for r in results),
        "practicals": [
            {
                "slug": r.slug,
                "kind": r.kind,
                "ok": r.ok,
                "checks": [
                    {"name": c.name, "passed": c.passed, "skipped": c.skipped, "detail": c.detail}
                    for c in r.checks
                ],
            }
            for r in results
        ],
    }
```

- [ ] **Step 4: Run the orchestrate test to verify it passes**

Run: `python -m pytest code/practicals/_verify/tests/test_orchestrate.py -q`
Expected: PASS (2 passed)

- [ ] **Step 5: Write the CLI entry `verify.py`**

`code/practicals/verify.py`:
```python
#!/usr/bin/env python3
"""Verify that practicals work. See docs/superpowers/plans/2026-06-29-practical-verification-harness.md."""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _verify.discovery import discover, select
from _verify.orchestrate import verify_practical, render_table, to_report
from _verify.sandbox import make_venv

HERE = Path(__file__).resolve().parent
REPORT_PATH = HERE / ".verify-report.json"


def _layers(args) -> tuple:
    if args.layer == "a":
        return True, False
    if args.layer == "b":
        return False, True
    return True, args.live  # default: A always, B only with --live


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Verify code/practicals/ exercises.")
    parser.add_argument("--live", action="store_true", help="also run live-Claude (Layer B)")
    parser.add_argument("--only", default=None, help="comma-separated slugs/prefixes, e.g. 04,09")
    parser.add_argument("--fast", "--shared-env", dest="fast", action="store_true",
                        help="reuse one shared venv instead of a fresh one per practical")
    parser.add_argument("--layer", choices=["a", "b"], default=None,
                        help="run only one layer (default: A, plus B if --live)")
    args = parser.parse_args(argv)

    run_a, run_b = _layers(args)
    practicals = select(discover(HERE), args.only)
    if not practicals:
        print("No practicals matched.")
        return 1

    shared_py = None
    workspace_root = Path(tempfile.mkdtemp(prefix="verify-practicals-"))
    if args.fast:
        shared_py = make_venv(workspace_root / ".shared-venv")

    results = []
    for p in practicals:
        print(f"… {p.slug}", flush=True)
        results.append(verify_practical(
            p, run_a=run_a, run_b=run_b, fast=args.fast,
            shared_py=shared_py, workspace=workspace_root,
        ))

    print("\n" + render_table(results))
    report = to_report(results)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(f"\nReport: {REPORT_PATH}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 6: Add the gitignore lines**

Append to the end of `.gitignore` (repo root):
```
# practical verification harness
code/practicals/.verify-report.json
```

- [ ] **Step 7: Run the full harness test suite + a real Layer-A dry run on one practical**

Run: `python -m pytest code/practicals/_verify/tests -q`
Expected: PASS (all tests green).

Run: `python code/practicals/verify.py --only 04 --layer a`
Expected: prints `… 04-llm-agents`, then a table row `04-llm-agents  agentic  PASS`. Takes ~1 min (it builds a venv and installs `pytest`). If config-lint/references/pytest surface a real problem in the practical, capture it — that is the harness doing its job.

- [ ] **Step 8: Confirm the working tree is clean apart from the new harness files**

Run: `git status --porcelain code/practicals | grep -v '_verify/\|verify.py'`
Expected: no output (the temp-copy design means no `reports/`, `.venv`, or `__pycache__` appear under `code/practicals/<slug>/`). If anything appears, the sandbox copy is leaking — fix before committing.

- [ ] **Step 9: Commit**

```bash
git add code/practicals/verify.py code/practicals/_verify/orchestrate.py code/practicals/_verify/tests/test_orchestrate.py .gitignore
git commit -m "feat(code): verify.py CLI orchestration, table/JSON output"
```

---

### Task 10: Wire the first real manifest (04-llm-agents) end-to-end, incl. `--live`

**Files:**
- Create: `code/practicals/04-llm-agents/verify.yaml`

**Interfaces:**
- Consumes: `load_manifest`, `run_smoke`, `run_live` (already built). This task authors data, not code.

- [ ] **Step 1: Read the practical's real skill + tools to ground the manifest**

Run: `sed -n '1,40p' code/practicals/04-llm-agents/.claude/skills/ask/SKILL.md` and `ls code/practicals/04-llm-agents/tools`.
Confirm the real entry points: `/ask "<question>"`, `python -m tools.retrieve "<q>" -k 4`, `python -m tools.grade ...`, corpus company is **NovaCorp**, and "net income" is the unanswerable probe.

- [ ] **Step 2: Write the manifest**

`code/practicals/04-llm-agents/verify.yaml`:
```yaml
# Layer A — deterministic "run by hand" commands; must exit 0.
smoke:
  - python -m tools.retrieve "How did gross margin change?" -k 4 > reports/_context.json
  - python -m tools.grade --question "How did gross margin change?" --answer "Gross margin expanded to 64%." --context reports/_context.json

# Layer B — live Claude; only runs with --live.
live:
  - prompt: '/ask "What is NovaCorp customer concentration risk?"'
    expect_file: 'reports/*.md'
    expect_contains: ['concentration']
  - prompt: '/ask "What was NovaCorp net income?"'
    expect_contains: ['Not answerable']
```

- [ ] **Step 3: Run Layer A with the manifest's smoke commands**

Run: `python code/practicals/verify.py --only 04 --layer a`
Expected: table row `04-llm-agents  agentic  PASS`; the `smoke[0]`/`smoke[1]` checks now run and pass. If a smoke command fails, fix the command text in `verify.yaml` to match the real tool CLI (check `python -m tools.retrieve --help` inside the practical).

- [ ] **Step 4: Run the live layer end-to-end (real API; costs ~$0.20–0.50)**

Run: `python code/practicals/verify.py --only 04 --live`
Expected: both `live:/ask ...` checks pass — the concentration question writes a `reports/*.md` containing "concentration"; the net-income question's result contains "Not answerable". If the refusal wording differs, adjust `expect_contains` to the actual phrase the agent uses (read `.verify-report.json` for the captured `result` text).

- [ ] **Step 5: Confirm no working-tree leakage, then commit**

```bash
git status --porcelain code/practicals/04-llm-agents
# Expected: only 'A/?? code/practicals/04-llm-agents/verify.yaml' — no reports/, no .venv
git add code/practicals/04-llm-agents/verify.yaml
git commit -m "feat(code): verify.yaml manifest for 04-llm-agents (smoke + live)"
```

---

### Task 11: Author manifests for the remaining agentic practicals + the oddball

**Files:**
- Create: `code/practicals/<slug>/verify.yaml` for each slug below.

**Interfaces:**
- Consumes: same harness. Pure data authoring, one practical at a time. A practical with no `verify.yaml` still passes its auto-discovered Layer A checks, so this task *enriches* coverage; it is not a prerequisite for the harness working.

The slugs to cover (the single headline skill for each is in `.claude/skills/<name>/`):
`05-business-valuation` (`/valuation`), `06-credit-risk` (`/credit`), `07-applications-future` (`/brief`), `08-domain-specific-llms` (`/compare`), `09-financial-nlp-sentiment` (`/sentiment`), `10-portfolio-quant-trading` (`/portfolio`), `11-regtech-compliance-aml` (`/screen`), `12-xai-explainability` (`/explain`), `13-llm-limitations-evaluation` (`/evaluate`), `14-financial-text-summarization` (`/summarize`), `15-privacy-local-models` (`/deidentify`), `16-ai-ml-finance-text` (`/pipeline`), `17-loops-goals-iterations` (`/iterate`), plus the oddball `05-business-valuation-example` (config-lint only, one representative live flow, no smoke/pytest).

- [ ] **Step 1: For each slug, read its skill + README to find real entry points**

For a slug `SLUG`, run:
`sed -n '1,40p' code/practicals/SLUG/.claude/skills/*/SKILL.md` and `cat code/practicals/SLUG/README.md` and `ls code/practicals/SLUG/tools 2>/dev/null`.
Note: the headline skill invocation, the deterministic `python -m tools.*` commands the README documents, and one input the agent should handle plus one it should refuse or flag.

- [ ] **Step 2: Write that slug's `verify.yaml`** using this template (fill from Step 1; drop `smoke` if the practical has no `tools/`, drop `expect_file` if the skill writes no report):

```yaml
smoke:
  - python -m tools.<entrypoint> <args>          # a real "run by hand" command from the README
live:
  - prompt: '/<skill> "<a question the practical SHOULD handle>"'
    expect_file: '<glob the skill writes, e.g. reports/*.md>'
    expect_contains: ['<a term that must appear>']
  - prompt: '/<skill> "<an out-of-scope / unanswerable input>"'
    expect_contains: ['<the refusal/flag phrase>']
```

For `05-business-valuation-example` (no `tools/`, no `tests/`), write only a `live:` block (one representative flow); the harness will still run config-lint automatically and skip pytest/smoke.

- [ ] **Step 3: Verify that slug's Layer A**

Run: `python code/practicals/verify.py --only SLUG --layer a`
Expected: `SLUG  agentic  PASS`. Fix smoke command text to match the real tool CLI if any `smoke[i]` fails.

- [ ] **Step 4: Commit that slug** (commit per-practical so a bad manifest is easy to bisect)

```bash
git add code/practicals/SLUG/verify.yaml
git commit -m "feat(code): verify.yaml manifest for SLUG"
```

- [ ] **Step 5: After all slugs are authored, run the full deterministic sweep**

Run: `python code/practicals/verify.py`
Expected: every practical row shows `PASS`; final line `18/18 practicals passed` (15 agentic + 3 notebook). Investigate any `FAIL` — it is either a real practical bug (fix the practical, separate commit) or a manifest mismatch (fix `verify.yaml`).

- [ ] **Step 6: Spot-check the live layer on two or three critical practicals**

Run: `python code/practicals/verify.py --only 04,09,11 --live`
Expected: their `live:` checks pass. This confirms Layer B generalizes beyond `04`. (Running `--live` across all 15 is fine before a release but costs a few dollars and minutes — not required here.)

---

### Task 12: Document the harness

**Files:**
- Create: `code/practicals/VERIFY.md`

**Interfaces:** none (docs).

- [ ] **Step 1: Write the usage doc**

`code/practicals/VERIFY.md`:
```markdown
# Verifying the practicals

`verify.py` checks every practical in this directory before a teaching session or release.
Each practical is copied to a system temp dir first, so running it never touches your
working tree.

## Usage

```bash
python code/practicals/verify.py                 # Layer A (deterministic) on all practicals
python code/practicals/verify.py --only 04,09    # just these
python code/practicals/verify.py --layer a       # deterministic only (explicit)
python code/practicals/verify.py --live          # add Layer B (real claude -p calls, costs $)
python code/practicals/verify.py --fast          # reuse one shared venv (quicker, less faithful)
```

A machine-readable summary is written to `code/practicals/.verify-report.json` (gitignored).
Exit code is non-zero if any check fails.

## Layers

- **Layer A (always):** fresh venv + `pip install -r requirements.txt`, `.claude` config
  lint, reference integrity, `pytest`, and the `smoke:` commands from each `verify.yaml`.
  Notebook practicals (01–03) are executed end-to-end instead.
- **Layer B (`--live`):** runs each `live:` skill call headlessly via
  `claude -p ... --output-format json` and asserts on the result. Critical-path only.

## Manifests

Each agentic practical may carry a `verify.yaml` (`smoke:` + `live:` blocks). A practical
without one still gets all auto-discovered Layer A checks. See `04-llm-agents/verify.yaml`
for the reference example.

## Harness internals

The logic lives in `_verify/` (one module per concern) with its own tests:
`python -m pytest code/practicals/_verify/tests -q`.
```

- [ ] **Step 2: Commit**

```bash
git add code/practicals/VERIFY.md
git commit -m "docs(code): how to run the practical verification harness"
```

---

## Self-Review

**Spec coverage:**
- CLI `verify.py` + flags (`--live`, `--only`, `--fast`/`--shared-env`, `--layer`) → Task 9. ✓
- Discovery + notebook/agentic classification → Task 2. ✓
- Repo-safe temp copy (Component 2) → Task 5 (`copy_practical`) + Task 9 (system `tempfile.mkdtemp`) + leak checks in Tasks 9/10. ✓
- Layer A: fresh venv + install → Task 5 + `_prepare_env` in Task 9; config lint → Task 4; reference integrity → Task 4; pytest → Task 6; smoke → Task 6 + manifests Tasks 10–11. ✓
- Layer B: validated `claude -p` recipe + deterministic assertions (`is_error`, `expect_file`, `expect_contains`/`expect_not_contains`) → Task 8; end-to-end → Task 10. ✓
- Per-practical `verify.yaml` → Task 3 (load) + Tasks 10–11 (author). ✓
- Notebook practicals via execution → Task 7. ✓
- Oddball `05-business-valuation-example` (config-lint + one live flow, no pytest/smoke) → Task 11 Step 2. ✓
- `.verify-report.json` gitignored → Task 9 Step 6. ✓
- Output table + JSON report + non-zero exit → Task 9. ✓
- Open item (notebook practicals lack `requirements.txt`): handled by running the notebook in the harness base env (Task 7), documented in VERIFY.md (Task 12); no per-practical install needed for notebooks. ✓

**Placeholder scan:** No TBD/TODO. The only intentional fill-in-the-blank is Task 11's per-practical template, which is unavoidable data authoring with an explicit per-slug recipe (read skill/README → fill template → verify → commit) and a worked reference example in Task 10. ✓

**Type consistency:** `CheckResult(name, passed, detail, skipped)` and `PracticalResult(slug, kind, checks)` are used identically across Tasks 4/6/7/8/9. `LiveCheck` fields (`prompt`, `expect_file`, `expect_contains`, `expect_not_contains`) match between Task 3 (definition) and Task 8 (consumption). `venv_python`/`make_venv`/`pip_install` signatures match between Task 5 (definition) and Task 9 (`_prepare_env`). `runner(prompt, cwd) -> dict` matches between Task 8 default and Task 9 injection. ✓
