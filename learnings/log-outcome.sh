#!/usr/bin/env bash
# log-outcome.sh — Log an insight outcome (+1 helped, -1 misled)
# Usage: ./log-outcome.sh <insight_id> <+1|-1> [note]
# Example: ./log-outcome.sh bug-001 +1 "Saved 10 min debugging"
# Example: ./log-outcome.sh know-023 -1 "Advice was outdated"

set -euo pipefail

LOGS_DIR="$(cd "$(dirname "$0")/logs" && pwd)"
OUTCOME_LOG="$LOGS_DIR/outcome-log.jsonl"

ID="${1:?Usage: log-outcome.sh <insight_id> <+1|-1> [note]}"
DELTA="${2:?Usage: log-outcome.sh <insight_id> <+1|-1> [note]}"
NOTE="${3:-}"

# Validate delta
if [[ "$DELTA" != "+1" && "$DELTA" != "-1" && "$DELTA" != "1" && "$DELTA" != "-1" ]]; then
    echo "Error: delta must be +1 or -1" >&2
    exit 1
fi

# Normalize +1 to 1
DELTA="${DELTA#+}"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
ENTRY="{\"insight_id\":\"$ID\",\"delta\":$DELTA,\"timestamp\":\"$TIMESTAMP\",\"note\":\"$NOTE\"}"

echo "$ENTRY" >> "$OUTCOME_LOG"
echo "Logged: $ID ${DELTA:+$DELTA} ($NOTE)"
