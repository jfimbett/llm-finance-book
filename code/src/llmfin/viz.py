"""Figure helpers shared by every ``code/figures/<chapter>`` generator.

Centralises the "where do book figures live" boilerplate so each generator
just calls :func:`save_book_figure`.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

# Repo root resolved from this file: code/src/llmfin/viz.py -> parents[3]
_REPO_ROOT = Path(__file__).resolve().parents[3]


def use_headless() -> None:
    """Select the non-interactive Agg backend (deterministic, no display)."""
    matplotlib.use("Agg")


def book_figures_dir(chapter: str) -> Path:
    """Return (and create) ``book/chapters/<chapter>/figures``."""
    d = _REPO_ROOT / "book" / "chapters" / chapter / "figures"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_book_figure(fig, chapter: str, stem: str, *, png: bool = True,
                     dpi: int = 160) -> Path:
    """Save *fig* as ``<stem>.pdf`` (and ``.png``) into the chapter's figures dir.

    Returns the path to the written PDF.
    """
    d = book_figures_dir(chapter)
    pdf = d / f"{stem}.pdf"
    fig.savefig(pdf, bbox_inches="tight")
    if png:
        fig.savefig(d / f"{stem}.png", dpi=dpi, bbox_inches="tight")
    return pdf
