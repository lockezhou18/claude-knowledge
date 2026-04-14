---
id: know-051
track: knowledge
status: active
name: autoMemoryDirectory unifies Claude memory read/write
description: Setting autoMemoryDirectory redirects ALL Claude memory reads and writes to a custom directory, achieving single SoT without complex symlinks
created: 2026-04-10
last_verified: 2026-04-10
repos: [memory-migration]
tags: [claude-code, memory, architecture, autoMemoryDirectory, settings]
use_count: 8
outcome_score: 0.0
rot_rate: slow
---

When migrating Claude memory to a custom store, use `autoMemoryDirectory` in settings.json instead of symlinking `~/.claude/projects/*/memory/`. It redirects ALL auto memory reads and writes to one directory.

**However:** Claude still reads per-project memory from `~/.claude/projects/<project>/memory/` separately. You need BOTH autoMemoryDirectory (for global) AND symlinks (for per-project) to achieve true single SoT.

**How to apply:** Set `"autoMemoryDirectory": "/path/to/memory"` in user settings (not project settings). Then symlink each active project's memory path to subdirs within that directory.
