#!/bin/bash
# iterate.sh — find lowest-scoring dimension and print action instruction
# Called with FILE=$1 when gate-check fails on a specific file.
# Exit 0 = no action needed, Exit 1 = hard failure, Exit 2 = AI intervention required.
# Trigger: programmatic (called by gate-check or /refine-until-threshold)

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

# Read threshold to determine if all dimensions pass
THRESHOLD=$(grep 'quality_threshold:' TOPIC.md 2>/dev/null | sed 's/quality_threshold://' | tr -d ' \r\n')
THRESHOLD="${THRESHOLD:-7}"

# Find lowest-scoring dimension
DIMENSION=$(python3 << PYEOF
import json, sys

try:
    with open("$REPORT") as f:
        report = json.load(f)
except Exception:
    print("error")
    sys.exit(0)

scores = report.get("scores", {})
if not scores:
    print("error")
    sys.exit(0)

threshold = int("$THRESHOLD")

# Check if all dimensions are at or above threshold
if all(v >= threshold for v in scores.values()):
    print("none")
    sys.exit(0)

# Find lowest dimension below threshold
below = {k: v for k, v in scores.items() if v < threshold}
lowest_dim = min(below, key=below.get)
print(lowest_dim)
PYEOF
)

if [ "$DIMENSION" = "none" ]; then
  echo "iterate.sh: all dimensions at threshold or above — no action needed"
  exit 0
fi

if [ "$DIMENSION" = "error" ]; then
  echo "iterate.sh: could not parse score file $SCORE_FILE"
  exit 1
fi

# Map dimension to agent and print instruction
python3 << PYEOF
import json

with open("$REPORT") as f:
    report = json.load(f)

scores = report.get("scores", {})
lowest_dim = "$DIMENSION"
lowest_score = scores.get(lowest_dim, "?")

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
