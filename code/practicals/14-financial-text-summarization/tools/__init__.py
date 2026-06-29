"""Deterministic tools for the summarize-and-extract agent.

The agent (Claude Code / Cline) chooses *which* tool to call and *interprets*
the results; these modules do every bit of the actual extraction and scoring so
the language model never has to read a figure off the page or invent one itself.
"""
