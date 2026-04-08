---
id: 'know-044'
track: 'knowledge'
repos: ['*']
tags: ['claude-code', 'permissions', 'settings', 'session']
severity: 'medium'
created: '2026-04-07'
last_verified: '2026-04-07'
use_count: 0
outcome_score: 0.0
status: 'active'
rot_rate: 'medium'
graduated_to: ''
---

## Claude Code permission changes require session restart

When adding new `Bash(tool:*)` entries to `settings.json` permissions allowlist, the changes do NOT take effect in the current session. The user must start a new Claude Code session for the permissions to be active.

**Why:** Claude Code reads permissions at startup, not dynamically.

**How to apply:** When adding permissions mid-session (like `ssh`, `scp`, `mutagen`), tell the user upfront that a session restart is needed. Provide `!` commands as a workaround for the current session, and defer automated execution to the next session.
