"""Deterministic tools for the credit-memo agent.

The agent (Claude Code / Cline) chooses *which* company to analyse and *interprets*
the results; these modules do every bit of the actual arithmetic — ratios and the
default-risk score — so the language model never computes or recalls a number itself.
"""
