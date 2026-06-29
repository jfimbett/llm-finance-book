"""llmfin — shared utilities for *Large Language Models in Finance*.

Two consumers import from this package so code is written once:

* ``code/figures/<chapter>/`` — deterministic generators that produce the
  figures embedded in the book (``llmfin.viz``).
* ``code/practicals/<chapter>/practical.ipynb`` — student notebooks
  (``llmfin.edgar``, ``llmfin.text``).

Install editable from the repo root:  ``pip install -e code``
"""

__version__ = "0.1.0"

from . import edgar, text, viz  # noqa: F401

__all__ = ["edgar", "text", "viz", "__version__"]
