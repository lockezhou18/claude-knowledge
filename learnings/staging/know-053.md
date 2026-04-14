---
id: know-053
track: knowledge
status: active
name: Rules files without globs/paths load every prompt
description: Files in .claude/rules/ without paths or globs frontmatter are loaded at every session start. Move on-demand files out of rules/ to reduce context window cost.
created: 2026-04-10
last_verified: 2026-04-10
repos: [memory-migration]
tags: [claude-code, rules, context-window, optimization, loading]
use_count: 1
outcome_score: 0.0
rot_rate: slow
---

When organizing Claude Code rules, know that ALL files in `.claude/rules/` without `paths:` or `globs:` frontmatter load at every session start. Removing `globs:` from a file does NOT make it on-demand — it makes it load MORE (every prompt instead of on file match).

**To make a rules file on-demand:** Move it OUT of `rules/` entirely (e.g., to `guides/`). Reference it from rules/MEMORY.md so Claude knows it exists and can read it when needed.

**How to apply:** Keep only essential rules in rules/ (behavioral gates, engineering principles, routing). Move detailed specs (pipeline details, compound learning, skill tiers) to guides/.
