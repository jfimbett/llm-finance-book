"""Deterministic tools for the filing Q&A agent.

The agent (Claude Code / Cline) chooses *which* tool to call and *interprets*
the results; these modules do every bit of the actual retrieval and scoring so
the language model never has to compute anything itself.
"""
