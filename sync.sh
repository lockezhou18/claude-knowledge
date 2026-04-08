#!/usr/bin/env bash
# sync.sh — Auto-sync claude-knowledge repo
# Called by SessionEnd hook or cron
# Usage: ./sync.sh [push|pull]

set -euo pipefail

KNOWLEDGE_DIR="$(cd "$(dirname "$0")" && pwd)"
ACTION="${1:-push}"

cd "$KNOWLEDGE_DIR"

# Ensure we're in a git repo
if [ ! -d .git ]; then
    echo "SYNC: Not a git repo yet, skipping"
    exit 0
fi

case "$ACTION" in
    pull)
        echo "SYNC: Pulling latest knowledge..."
        git pull --rebase --quiet origin main 2>/dev/null || echo "SYNC: Pull failed (offline or conflict)"
        ;;
    push)
        echo "SYNC: Pushing knowledge changes..."
        git add -A
        if ! git diff --cached --quiet 2>/dev/null; then
            git commit -m "auto: sync $(hostname -s) $(date +%Y-%m-%d_%H:%M)" --quiet
            git push origin main --quiet 2>/dev/null || echo "SYNC: Push failed (offline?), will retry next sync"
        else
            echo "SYNC: No changes to push"
        fi
        ;;
    *)
        echo "Usage: sync.sh [push|pull]"
        exit 1
        ;;
esac
