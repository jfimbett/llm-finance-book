#!/bin/bash
# iterate.sh — find lowest-scoring dimension and print action instruction
# Called with FILE=$1 when gate-check fails on a specific file.
# Exit 0 = instruction printed, Exit 2 = needs AI intervention.

FILE="$1"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    echo "Usage: iterate.sh <content-file>"
    exit 1
fi

# Read max iterations
MAX_ITER=$(grep 'max_refine_iterations:' TOPIC.md 2>/dev/null | sed 's/max_refine_iterations://' | tr -d ' \r\n')
MAX_ITER="${MAX_ITER:-5}"

# Derive score report path
SAFE=$(echo "$FILE" | sed 's/\.[^.]*$//' | tr '/' '_')
REPORT="docs/quality/${SAFE}-score.json"

if [ ! -f "$REPORT" ]; then
    echo "No quality report found for $FILE. Run /score-content first."
    exit 2
fi

# Find lowest-scoring dimension
python3 << PYEOF
import json

with open("$REPORT") as f:
    report = json.load(f)

scores = report.get("scores", {})
if not scores:
    print("No scores found in report.")
    exit(2)

# Find lowest dimension
lowest_dim = min(scores, key=scores.get)
lowest_score = scores[lowest_dim]

# Map dimension to agent
agent_map = {
    "clarity": "editor agent",
    "rigor": "math-checker agent",
    "completeness": "structure-reviewer agent (for book chapters) or lecture-writer agent (for lecture notes)",
    "pedagogy": "pedagogy-reviewer agent",
    "style": "humanizer agent, then proofreader agent",
}

agent = agent_map.get(lowest_dim, "editor agent")

print(f"")
print(f"ITERATE: {lowest_dim} is lowest ({lowest_score}/10) in $FILE")
print(f"ACTION REQUIRED: invoke the {agent} on $FILE")
print(f"  Focus: improve '{lowest_dim}' — see .claude/skills/refine-until-threshold.md for guidance")
print(f"  After agent pass: run /score-content $FILE to re-check")
print(f"  Max iterations remaining: $MAX_ITER")
PYEOF

exit 2
