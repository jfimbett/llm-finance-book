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
