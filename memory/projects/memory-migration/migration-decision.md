---
name: Migration Decision — Option B
description: Disable Auto Dream, use memory/ as dumb storage, our engines (compound, eval, behavior) do all intelligent maintenance
type: project
originSessionId: c76c22a5-e5ad-4b55-8770-d8be7f3d89cd
---
**Decision:** Option B — use native memory/ as storage layer with `autoDreamEnabled: false`. Our engines handle all intelligence.

**Why:** Auto Dream is broken (KAIROS-flagged, /dream doesn't work), memory is plain markdown with no metadata awareness, 200-line truncation loses newest entries first. We can't depend on it.

**How to apply:**
1. Set `autoDreamEnabled: false` in settings — prevents Dream from interfering
2. Keep Auto Memory on — let Claude write observations, our hooks post-process
3. We own MEMORY.md — scout hook writes curated index
4. Subdirectories work fine — Claude can Read any path, Dream's flat-structure limit irrelevant when Dream is off
5. Custom frontmatter is safe — nobody strips metadata with Dream disabled
6. Graduation pipeline works — staging > score > promote to memory/insights/ with full frontmatter

**Risk:** Auto Memory may fight our MEMORY.md writes (Claude appends during sessions). Mitigation: PostToolUse hook on Write to detect memory path writes and reconcile.
