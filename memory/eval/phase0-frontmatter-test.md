---
name: Phase 0 Frontmatter Survival Test
description: Test file to verify Auto Dream preserves custom frontmatter fields. If these fields survive consolidation, the full migration is safe.
type: eval
outcome_score: 0
use_count: 3
tags: ["phase0", "test", "frontmatter", "migration"]
test_created: "2026-04-11"
custom_nested:
  graduation_threshold: 2.0
  prune_threshold: -2.0
originSessionId: f33377f6-2c2a-446f-b37b-f40474d6b4c4
---
This is a test memory file for Phase 0 of the memory-native migration.

**Purpose:** Verify that Auto Dream preserves custom frontmatter fields that our compound learning system depends on.

**Fields to check after next Auto Dream cycle:**
- `outcome_score: 0` — must survive as-is
- `use_count: 3` — must survive as-is
- `tags: ["phase0", "test", "frontmatter", "migration"]` — must survive as array
- `test_created: "2026-04-11"` — must survive as string
- `custom_nested` object — must survive with children

**How to verify:** Compare this file's frontmatter before and after Auto Dream runs. If any custom field is stripped, modified, or moved, the migration plan must adjust (insights stay in staging, only summaries graduate to memory).

**Original checksum fields (for diff):**
```
outcome_score=0 use_count=3 tags=4items test_created=2026-04-11 custom_nested=2keys
```
