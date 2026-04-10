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

# Set autoMemoryDirectory — single SoT for all memory reads/writes
# This replaces the old symlink approach. Claude reads/writes directly to our repo.
MEMORY_DIR="$KNOWLEDGE_DIR/memory"
echo "  memory — autoMemoryDirectory: $MEMORY_DIR"

# Ensure settings.json exists and has autoMemoryDirectory set
if [ ! -f "$CLAUDE_DIR/settings.json" ]; then
    HOSTNAME_SHORT="$(hostname -s)"
    if [ -f "$KNOWLEDGE_DIR/settings/$HOSTNAME_SHORT.json" ]; then
        echo "  settings — using machine-specific: $HOSTNAME_SHORT.json"
        cp "$KNOWLEDGE_DIR/settings/$HOSTNAME_SHORT.json" "$CLAUDE_DIR/settings.json"
    elif [ -f "$KNOWLEDGE_DIR/settings/base.json" ]; then
        echo "  settings — using base settings"
        cp "$KNOWLEDGE_DIR/settings/base.json" "$CLAUDE_DIR/settings.json"
    else
        echo '{"autoMemoryDirectory": "'$MEMORY_DIR'", "autoDreamEnabled": false}' > "$CLAUDE_DIR/settings.json"
        echo "  settings — created with autoMemoryDirectory"
    fi
else
    echo "  settings — already exists"
fi

# Verify autoMemoryDirectory is set (warn if missing)
if ! grep -q "autoMemoryDirectory" "$CLAUDE_DIR/settings.json" 2>/dev/null; then
    echo "  WARNING: autoMemoryDirectory not set in settings.json"
    echo "  Add manually: \"autoMemoryDirectory\": \"$MEMORY_DIR\""
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
