---
id: 'bug-006'
track: 'bug'
repos: ['*']
tags: ['claude-code', 'settings', 'hooks', 'install', 'config']
severity: 'medium'
created: '2026-04-07'
last_verified: '2026-04-07'
use_count: 0
outcome_score: 0.0
status: 'active'
rot_rate: 'medium'
graduated_to: ''
---

## install.sh overwrote settings.json, wiping custom hooks

**Symptoms:** After running install.sh, SessionEnd and UserPromptSubmit sync hooks disappeared from settings.json.

**Root Cause:** install.sh unconditionally copied base.json over settings.json. The base.json was snapshotted before hooks were added.

**Fix:** Changed install.sh to skip settings.json if it already exists. Settings are machine-specific (hooks, paths, permissions differ per machine).

**Prevention:** When writing install/setup scripts for config files, always check-before-write. Machine-specific configs should never be overwritten by a generic template. Use `[ ! -f target ] && cp` pattern.

**How to apply:** Any future changes to install.sh or setup scripts — never overwrite settings.json unconditionally.
