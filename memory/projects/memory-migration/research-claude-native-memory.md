---
name: Claude Native Memory Research
description: Auto Dream is broken (KAIROS feature-flagged), memory is plain markdown with no structured metadata, 200-line truncation loses newest first
type: project
originSessionId: c76c22a5-e5ad-4b55-8770-d8be7f3d89cd
---
Auto Dream is non-functional as of v2.1.89+. The `/dream` command returns "Unknown skill" (#38461, #42237). Feature-flagged behind KAIROS/KAIROS_DREAM. No background consolidation is running despite UI showing "last ran Xd ago."

Native memory is plain markdown — no structured YAML frontmatter support beyond name/description. The 200-line MEMORY.md cap truncates newest entries first (#40210), meaning the most relevant memories are lost.

**Phase 0 answer:** Dream will NOT preserve custom frontmatter. Proceed with Option B — disable Dream, own maintenance ourselves.

**Critical bugs:** truncation loses newest (#40210), rules ignored (#45322), inline bloat (#41671), worktree divergence (#44130), no re-load after /compact (#44166).

Full research: `docs/research-claude-native-memory.md` in this repo.
