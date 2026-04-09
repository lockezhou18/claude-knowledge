---
name: Phase 0 — Auto Dream frontmatter compatibility test
description: Test whether Auto Dream preserves custom frontmatter fields during consolidation. This determines the entire migration scope.
type: feedback
use_count: 3
outcome_score: 2.5
tags: [test, eval, migration]
last_verified: 2026-04-09
status: active
---

This is a test memory file with custom frontmatter fields that our compound learning system uses.

**If Auto Dream preserves use_count, outcome_score, tags, last_verified, and status** → we can put scored insights directly in memory/ and Auto Dream will maintain them.

**If Auto Dream strips these fields** → insights must stay in learnings/staging/ and only summaries (native frontmatter only) go to memory/.

## How to Verify

1. Copy this file to `~/.claude/projects/-Users-bizhou/memory/test-frontmatter.md`
2. Wait for Auto Dream cycle (24hrs + 5 sessions, or trigger manually with "dream")
3. Read the file back — check if custom fields survived
4. Record result in this project's `tests/phase0-results.md`

## Expected Fields to Check
- `use_count: 3` — numeric custom field
- `outcome_score: 2.5` — float custom field
- `tags: [test, eval, migration]` — array custom field
- `last_verified: 2026-04-09` — date custom field
- `status: active` — string custom field
