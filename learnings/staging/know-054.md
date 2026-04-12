---
id: know-054
track: knowledge
status: active
name: Push notifications via scout hook replace manual status checking
description: Instead of checking dream results, async task status, or sync state manually, wire notifications into the UserPromptSubmit hook to surface them on first prompt
created: 2026-04-11
last_verified: 2026-04-11
repos: [memory-migration, agentbus]
tags: [notification, scout-hook, push-vs-pull, ux, dreaming]
use_count: 2
outcome_score: 0.0
rot_rate: slow
---

When building background processes (dream.py, async tasks, dependency watchers), make results push-based not pull-based. Wire a notification check into the UserPromptSubmit scout hook that shows results once per event (tracked by a .last-seen marker file), then goes quiet.

**Pattern:** Event writes result file → scout hook reads on next prompt → shows if unseen → marks as seen.

**Why:** Users don't check logs. cmux's notification rings work because they're push-based. Same principle applies to CLI — the scout hook is your notification center.

**How to apply:** For any new background process, add a check_*_notifications() function to knowledge-scout.py with a marker file for dedup.
