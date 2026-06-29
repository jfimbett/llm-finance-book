#!/usr/bin/env bash
# Deprecated entry point. The project moved to a two-track layout: book figures are
# produced by deterministic generators in code/figures/<chapter>/gen_*.py, and student
# code lives in code/practicals/<chapter>/. This script now just delegates to the
# figures pipeline. Run:  bash code/build_figures.sh [chapter]
exec bash "$(dirname "$0")/build_figures.sh" "$@"
