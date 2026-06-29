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
