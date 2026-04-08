#!/usr/bin/env bash
# vm-bootstrap.sh — Run from local machine to set up VM
# Usage: ./vm-bootstrap.sh bizhou-ld2.linkedin.biz

set -euo pipefail

HOST="${1:-bizhou-ld2.linkedin.biz}"

echo "=== Step 1: Test SSH ==="
ssh "$HOST" 'echo "SSH OK: $(hostname) $(uname -s) $(uname -m)"'

echo ""
echo "=== Step 2: Configure tmux ==="
ssh "$HOST" 'cat > ~/.tmux.conf << "TMUX"
set -g mouse on
set -g history-limit 50000
set -g status-right "#H | %Y-%m-%d %H:%M"
set -g default-terminal "screen-256color"
TMUX
echo "tmux: OK"'

echo ""
echo "=== Step 3: Install Claude Code CLI ==="
ssh "$HOST" 'curl -fsSL https://claude.ai/install.sh | sh'

echo ""
echo "=== Step 4: Clone knowledge repo + install ==="
ssh "$HOST" 'git clone git@github.com:bizhou_LinkedIn/claude-knowledge.git ~/claude-knowledge 2>/dev/null || (cd ~/claude-knowledge && git pull); cd ~/claude-knowledge && ./install.sh'

echo ""
echo "=== Step 5: Start Claude in tmux ==="
ssh "$HOST" 'tmux new-session -d -s claude "claude" 2>/dev/null && echo "tmux session started" || echo "tmux session already exists"'
ssh "$HOST" 'tmux list-sessions'

echo ""
echo "=== Step 6: Verify ==="
ssh "$HOST" 'ls -la ~/.claude/rules ~/.claude/commands ~/.claude/skills ~/.claude/learnings && which claude && echo "" && echo "All good! VM is ready."'
