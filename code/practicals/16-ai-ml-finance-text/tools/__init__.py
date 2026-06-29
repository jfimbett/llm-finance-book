"""Deterministic tools for the text-to-signal ML pipeline.

The agent (Claude Code / Cline) chooses *which* tool to call and *interprets*
the results; these modules do every bit of the feature extraction, training,
and evaluation, so the language model never fits a model or computes a score
itself. Standard library plus NumPy only — fully offline.
"""
