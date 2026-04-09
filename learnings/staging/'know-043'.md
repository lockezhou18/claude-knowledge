---
id: 'know-043'
track: 'knowledge'
repos: ['*']
tags: ['claude-code', 'knowledge-sync', 'vm', 'infrastructure', 'devex']
severity: 'high'
created: '2026-04-07'
last_verified: '2026-04-07'
use_count: 0
outcome_score: 0.0
status: 'active'
rot_rate: 'slow'
graduated_to: ''
---

## Portable Claude Knowledge Architecture

When setting up Claude Code across multiple machines (laptop + VM), separate **durable knowledge** (~1MB) from **ephemeral state** (~500MB).

**Durable (sync via git):** rules/, commands/, skills/, learnings/, memory/
**Ephemeral (machine-local):** projects/conversations, file-history, plugins, image-cache, paste-cache

**Key design decisions:**
- `install.sh` symlinks knowledge dirs into `~/.claude/` — never copy (single source of truth)
- Settings.json stays machine-specific (hooks may differ per machine) — `install.sh` only copies if none exists
- Project memory path-key mismatch (`-Users-` vs `-home-`) solved via cross-symlink in install.sh
- Auto-sync via SessionEnd (push) and UserPromptSubmit (pull) hooks
- Hourly cron as backup sync
- GitHub as the durable remote — survives both VM and laptop failures

**How to apply:** When provisioning any new machine for Claude Code, clone the knowledge repo and run `install.sh`. Full environment in one command.
