#!/usr/bin/env bash
# install-skills.sh — Selective install of portable commands + gstack safety trio
#
# Complements the main install.sh. Use this when you want the synthesis
# recommendations from guides/skill-synthesis.md without full-repo symlinks.
#
# Usage: ./install-skills.sh [--with-gstack]

set -euo pipefail

KNOWLEDGE_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_COMMANDS="$HOME/.claude/commands"
CLAUDE_SKILLS="$HOME/.claude/skills"

mkdir -p "$CLAUDE_COMMANDS" "$CLAUDE_SKILLS"

echo "=== Installing portable commands from claude-knowledge ==="

# Portable tier capture — no LinkedIn-specific refs
PORTABLE_COMMANDS=(learn aha eureka)

# Orchestrator + utilities (may have some LinkedIn refs — review before using heavily)
ORCHESTRATOR_COMMANDS=(kickoff explore scope find)

for cmd in "${PORTABLE_COMMANDS[@]}"; do
    src="$KNOWLEDGE_DIR/commands/$cmd.md"
    dst="$CLAUDE_COMMANDS/$cmd.md"
    if [ -L "$dst" ] || [ -f "$dst" ]; then
        echo "  /$cmd — already exists, skipping"
    else
        ln -sf "$src" "$dst"
        echo "  /$cmd — symlinked (portable)"
    fi
done

for cmd in "${ORCHESTRATOR_COMMANDS[@]}"; do
    src="$KNOWLEDGE_DIR/commands/$cmd.md"
    dst="$CLAUDE_COMMANDS/$cmd.md"
    if [ -L "$dst" ] || [ -f "$dst" ]; then
        echo "  /$cmd — already exists, skipping"
    else
        ln -sf "$src" "$dst"
        echo "  /$cmd — symlinked (may contain LinkedIn refs — review)"
    fi
done

# Gstack safety trio (optional)
if [ "${1:-}" = "--with-gstack" ]; then
    echo ""
    echo "=== Installing gstack safety trio ==="
    GSTACK_DIR="$HOME/gstack"
    if [ ! -d "$GSTACK_DIR" ]; then
        echo "  gstack not cloned at $GSTACK_DIR — cloning..."
        git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git "$GSTACK_DIR"
    fi

    for skill in careful freeze guard; do
        src="$GSTACK_DIR/$skill"
        dst="$CLAUDE_SKILLS/$skill"
        if [ -L "$dst" ] || [ -d "$dst" ]; then
            echo "  /$skill — already exists, skipping"
        else
            ln -sf "$src" "$dst"
            echo "  /$skill — symlinked from gstack"
        fi
    done
fi

echo ""
echo "✓ Done. Restart Claude Code to pick up new skills."
echo ""
echo "See guides/skill-synthesis.md for the full synthesis recommendations."
