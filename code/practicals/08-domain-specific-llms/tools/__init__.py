"""Deterministic tools for the general-vs-domain comparison agent.

The agent (Claude Code / Cline) chooses *which* tool to call and *interprets*
the results; these modules do every bit of the actual classification and scoring
so the language model never has to compute anything itself.
"""
