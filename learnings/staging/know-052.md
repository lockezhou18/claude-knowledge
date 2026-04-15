---
id: know-052
track: knowledge
status: active
name: Claude Auto Dream is broken — own the maintenance
description: Auto Dream is feature-flagged behind KAIROS, /dream returns Unknown skill. Disable with autoDreamEnabled:false and build your own consolidation.
created: 2026-04-10
last_verified: 2026-04-10
repos: [memory-migration]
tags: [claude-code, auto-dream, memory, consolidation, broken]
use_count: 14
outcome_score: 0.0
rot_rate: fast
---

When planning to use Claude's Auto Dream for memory consolidation, know that it's broken as of v2.1.98. The UI shows "Auto-dream: on" but /dream returns "Unknown skill." Feature-flagged behind KAIROS/KAIROS_DREAM internal flags.

**What to do:** Set `autoDreamEnabled: false`, build your own consolidation (dream.py). The memory system is plain markdown — no structured metadata awareness, 200-line MEMORY.md truncation loses newest entries first (#40210).

**How to apply:** Check GitHub issues #38461, #42015, #42237 for Dream status. Use feature probes (probe_features.py) to auto-detect when it ships.
