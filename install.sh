#!/usr/bin/env bash
# install.sh — Symlink claude-knowledge into ~/.claude on any machine
# Usage: git clone <repo> ~/claude-knowledge && cd ~/claude-knowledge && ./install.sh

set -euo pipefail

KNOWLEDGE_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "Installing claude-knowledge from: $KNOWLEDGE_DIR"
echo "Target: $CLAUDE_DIR"

# Ensure ~/.claude exists
mkdir -p "$CLAUDE_DIR"

# Directories to symlink
DIRS=(rules commands skills learnings)

for dir in "${DIRS[@]}"; do
    target="$CLAUDE_DIR/$dir"
    source="$KNOWLEDGE_DIR/$dir"

    if [ -L "$target" ]; then
        echo "  $dir/ — already symlinked, skipping"
    elif [ -d "$target" ]; then
        # Back up existing dir
        backup="$target.bak.$(date +%Y%m%d%H%M%S)"
        echo "  $dir/ — backing up existing to $backup"
        mv "$target" "$backup"
        ln -sf "$source" "$target"
        echo "  $dir/ — symlinked"
    else
        ln -sf "$source" "$target"
        echo "  $dir/ — symlinked"
    fi
done

# Symlink global project memory
# Handle path-key differences: local=/Users/<user>, VM=/home/<user>
MEMORY_SOURCE="$KNOWLEDGE_DIR/memory"
LOCAL_KEY="-Users-$(whoami)"
VM_KEY="-home-$(whoami)"

# Determine which path key this machine uses
if [[ "$HOME" == /Users/* ]]; then
    MY_KEY="$LOCAL_KEY"
    OTHER_KEY="$VM_KEY"
else
    MY_KEY="$VM_KEY"
    OTHER_KEY="$LOCAL_KEY"
fi

PROJ_DIR="$CLAUDE_DIR/projects/$MY_KEY"
mkdir -p "$PROJ_DIR"

if [ -L "$PROJ_DIR/memory" ]; then
    echo "  memory/ — already symlinked, skipping"
elif [ -d "$PROJ_DIR/memory" ]; then
    backup="$PROJ_DIR/memory.bak.$(date +%Y%m%d%H%M%S)"
    echo "  memory/ — backing up existing to $backup"
    mv "$PROJ_DIR/memory" "$backup"
    ln -sf "$MEMORY_SOURCE" "$PROJ_DIR/memory"
    echo "  memory/ — symlinked"
else
    ln -sf "$MEMORY_SOURCE" "$PROJ_DIR/memory"
    echo "  memory/ — symlinked"
fi

# Also create symlink for the other machine's path key (cross-machine memory access)
OTHER_PROJ_DIR="$CLAUDE_DIR/projects/$OTHER_KEY"
mkdir -p "$OTHER_PROJ_DIR"
if [ ! -L "$OTHER_PROJ_DIR/memory" ]; then
    ln -sf "$MEMORY_SOURCE" "$OTHER_PROJ_DIR/memory"
    echo "  memory/ — cross-linked for other machine path key ($OTHER_KEY)"
fi

# Settings: only copy if no settings.json exists (never overwrite — hooks may differ per machine)
if [ ! -f "$CLAUDE_DIR/settings.json" ]; then
    HOSTNAME_SHORT="$(hostname -s)"
    if [ -f "$KNOWLEDGE_DIR/settings/$HOSTNAME_SHORT.json" ]; then
        echo "  settings — using machine-specific: $HOSTNAME_SHORT.json"
        cp "$KNOWLEDGE_DIR/settings/$HOSTNAME_SHORT.json" "$CLAUDE_DIR/settings.json"
    elif [ -f "$KNOWLEDGE_DIR/settings/base.json" ]; then
        echo "  settings — using base settings"
        cp "$KNOWLEDGE_DIR/settings/base.json" "$CLAUDE_DIR/settings.json"
    fi
else
    echo "  settings — already exists, skipping (edit manually if needed)"
fi

# Set up auto-sync cron (hourly push)
CRON_CMD="cd $KNOWLEDGE_DIR && git add -A && git diff --cached --quiet || git commit -m 'auto: sync $(hostname -s) $(date +\%Y-\%m-\%d_\%H:\%M)' && git push origin main 2>/dev/null"
if crontab -l 2>/dev/null | grep -q "claude-knowledge"; then
    echo "  cron — already set up, skipping"
else
    (crontab -l 2>/dev/null; echo "0 * * * * $CRON_CMD # claude-knowledge auto-sync") | crontab -
    echo "  cron — hourly auto-sync installed"
fi

echo ""
echo "Done! Claude knowledge is now linked."
echo "Run 'claude' to start a session with all your knowledge intact."
