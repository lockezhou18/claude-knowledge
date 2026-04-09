---
name: Plan — Migrate ecosystem to Claude-native memory architecture
description: Restructure the entire Claude ecosystem so Auto Memory/Dream is the knowledge foundation. Custom systems become engines (eval, compound, behavior) that read/write memory, not parallel stores.
type: project
originSessionId: 27db5d4c-f39d-4ca8-b029-b22a12079f15
---
## Problem

We're maintaining two parallel knowledge systems:
- **Claude Native** (memory/MEMORY.md + 13 files, Auto Dream consolidates) — simple, maintained by Anthropic
- **Our Custom** (rules/MEMORY.md 26KB + learnings/ 63 insights + evals/ + hooks/) — complex, WE maintain

This happened because Claude didn't have good memory when we started. Now it does. We're fighting a maintenance battle Anthropic is already solving.

**Why:** Our job shifts from STORING knowledge to GENERATING and EVALUATING it. Let Claude's native system handle storage and maintenance.

```
OLD: We store + maintain + retrieve + evaluate
NEW: We generate + evaluate → Claude stores + maintains → we retrieve
```

## Target Architecture

```
┌──────────────────────────────────────────────────────────┐
│              CLAUDE MEMORY (Single Knowledge Store)        │
│                                                          │
│  memory/MEMORY.md — index (Auto Dream keeps < 200 lines) │
│                                                          │
│  memory/                                                  │
│  ├── user/                                               │
│  │   ├── role.md              (SDE, HP backend team)     │
│  │   └── preferences.md       (terse, no emoji, etc.)    │
│  ├── feedback/                                           │
│  │   ├── approach-rules.md    (hypothesis-first, etc.)   │
│  │   ├── tool-rules.md        (curli-first, observe-agent)│
│  │   ├── principle-scores.md  (eval-driven, 85.1%)       │
│  │   └── frontload-context.md (28 instances)             │
│  ├── project/                                            │
│  │   ├── connected-projects.md (phase 2, active PRs)     │
│  │   ├── dev-tooling.md       (VM parity, skills status)  │
│  │   └── active-work.md       (current initiatives)       │
│  ├── reference/                                          │
│  │   ├── espresso-metrics.md  (MD-2 cluster)             │
│  │   ├── test-environments.md (Greenhouse sandbox)        │
│  │   └── authority-sources.md (research sources)          │
│  ├── insights/                (graduated knowledge)       │
│  │   ├── v2-identity.md       (never findFirst)          │
│  │   ├── research-pipeline.md (5-step pattern)           │
│  │   └── ... (promoted from staging via compound engine)  │
│  └── eval/                    (system health)             │
│      ├── behavioral-gates.md  (latest eval findings)      │
│      ├── principle-adherence.md                          │
│      └── system-scorecard.md  (last eval summary)         │
│                                                          │
│  Auto Dream consolidates ALL of these.                   │
│  Auto Memory writes new ones during sessions.            │
└──────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────────┐
│ EVAL ENGINE  │   │ COMPOUND     │   │ BEHAVIOR ENGINE   │
│              │   │ ENGINE       │   │                   │
│ pipeline.py  │   │ scout hook   │   │ skills/*.md       │
│ judge_prompt │   │ outcome      │   │ recipes/*.md      │
│ verdicts/    │   │   tracking   │   │ hooks/*.py        │
│ sessions/    │   │ graduation   │   │ settings.json     │
│              │   │   pipeline   │   │                   │
│ Reads memory │   │ Reads+writes │   │ Reads memory      │
│ Writes to    │   │ memory files │   │ for context       │
│ memory/eval/ │   │              │   │                   │
└──────────────┘   └──────────────┘   └──────────────────┘
   (custom)           (hybrid)            (custom)
```

**Key principle:**
- Auto Memory = the WHAT (facts, preferences, findings)
- Compound Learning = the HOW (scoring, lifecycle, search)
- Eval = the WHY (measurement, classification, improvement)
- Behavior = the DO (skills, hooks, rules)
- Auto Dream consolidates the WHAT. Our systems manage HOW/WHY/DO.

## What Changes

### 1. Memory Structure: Flat → Organized by Type
Now: 13 memory files flat, mixed types.
Target: Organized by Claude's native types + our extensions (insights/eval).

### 2. Insights: Separate Store → Memory Files
Now: 63 insights in learnings/insights/ with JSONL manifest.
Target: Staging area → score → graduate to memory/ → Auto Dream maintains.

```
Lifecycle:
  Created → learnings/staging/{id}.md (custom frontmatter with scoring)
  Scored  → outcome tracking updates use_count, outcome_score
  Graduated (score >= 2.0) → MOVED to memory/insights/{name}.md (native frontmatter)
  Pruned (score < -2) → deleted from staging
  Stale (>90 days) → flagged for review
```

### 3. Rules/MEMORY.md: 269 lines → ~50 lines
Keep: Principle 0, phase routing table (one-liner per phase), behavioral gate summary.
Move: Engineering principles, compound learning spec, proactive suggestions, skill tiers.

### 4. Agent Briefing: Static → Dynamic
Now: agent-briefing.md compiled by SessionEnd hook.
Target: Scout hook reads memory files and compiles context dynamically. No static file.

### 5. Eval Findings → Memory Files
/improve-agent writes to memory/eval/ (already started). Auto Dream consolidates.

### 6. Outcome Tracking → Memory Metadata
Staging insight frontmatter tracks use_count + outcome_score.
Summary written to memory/eval/insight-outcomes.md for Auto Dream.

## What We Stop Maintaining

| Component | Now | After |
|-----------|-----|-------|
| agent-briefing.md | SessionEnd recompiles | Scout reads memory dynamically |
| Graduated insights | We maintain in learnings/ | Auto Dream maintains in memory/ |
| Stale cleanup | Manual (0 pruned ever) | Auto Dream prunes stale |
| Memory merging | Never happens | Auto Dream merges overlaps |
| Date fixing | Never happens | Auto Dream fixes relative → absolute |
| Index maintenance | Manual MEMORY.md edits | Auto Dream keeps < 200 lines |

## What We Keep Custom

| Component | Why |
|-----------|-----|
| Staging insights (learnings/staging/) | Scoring metadata Auto Dream doesn't understand |
| Manifest.jsonl | Search index — JSONL, not markdown |
| Eval pipeline (pipeline.py, verdicts) | Python + structured JSON |
| Hooks | Code, not memory |
| Skills | Behavior definitions, not memory |
| Logs (commit, PR, feedback) | Append-only structured data |

## Migration Phases

### Phase 0: Risk Gate — Test Auto Dream Frontmatter Behavior ⚠️
**Must do first.** Write a test memory file with custom frontmatter fields (outcome_score, use_count, tags). Wait for Auto Dream cycle. Check if fields survive consolidation.
- If preserved → full migration is safe
- If stripped → insights must stay in staging, only summaries go to memory
- **Effort:** Small | **Risk:** HIGH — determines entire migration scope

### Phase 1: Slim rules/MEMORY.md to ~50 lines
Extract pipeline phase details, compound spec, proactive suggestions, skill tiers into separate files loaded on demand. Keep Principle 0 + routing table + gate summary.
- **Effort:** Small | **Risk:** Low
- **Unblocks:** Context window savings (~18KB)

### Phase 2: Restructure memory/ with type organization
Create subdirs (user/, feedback/, project/, reference/, insights/, eval/). Move existing files. Update MEMORY.md index.
- **Effort:** Small | **Risk:** Low (verify Auto Dream scans subdirs)
- **Unblocks:** Clean organization for all subsequent phases

### Phase 3: Create outcome-log + staging area
Create learnings/staging/ for pre-graduation insights. Create outcome-log.jsonl for real-time scoring. Wire into hooks.
- **Effort:** Medium | **Risk:** Low
- **Unblocks:** Graduation pipeline, pruning, eval accuracy

### Phase 4: Graduation pipeline — staging → memory
Script that checks staging insights, graduates to memory/insights/ when threshold met, prunes when score negative. Run during /compound.
- **Effort:** Medium | **Risk:** Medium (depends on Phase 0 results)
- **Unblocks:** Auto Dream maintaining graduated insights

### Phase 5: Migrate existing insights
Move the 1-2 already-graduated insights from learnings/ to memory/insights/. Keep 62 active insights in staging. Update manifest.
- **Effort:** Medium | **Risk:** Medium
- **Unblocks:** Single source of truth for graduated knowledge

### Phase 6: Rewrite scout hook to read memory/
Scout currently reads learnings/manifest.jsonl + agent-briefing.md. Rewrite to read memory/ files directly (MEMORY.md index → relevant files by type).
- **Effort:** Medium | **Risk:** Medium
- **Unblocks:** Memory-native retrieval

### Phase 7: Deprecate agent-briefing.md
Scout compiles context dynamically from memory files. SessionEnd hook no longer needs to compile briefing. Remove static file.
- **Effort:** Medium | **Risk:** Medium (verify scout produces equivalent context)
- **Unblocks:** Auto Dream is sole maintainer of knowledge summaries

### Phase 8: Slim compound learning spec
Move SCHEMA.md, compound system description, search/write/maintain specs to a reference file loaded on demand. Only the routing rules stay in rules/MEMORY.md.
- **Effort:** Small | **Risk:** Low
- **Unblocks:** rules/MEMORY.md reaches target ~50 lines

## Success Criteria

- rules/MEMORY.md < 50 lines (from 269)
- All graduated insights in memory/ (Auto Dream maintained)
- Outcome tracking operational (outcome-log.jsonl exists, scores accumulating)
- Scout reads memory/ natively (no agent-briefing.md dependency)
- /improve-agent writes findings to memory/eval/ (already done ✓)
- Auto Dream consolidation verified working with our files

## Dependencies

- Phase 0 gates Phases 4, 5 (frontmatter survival)
- Phase 3 gates Phase 4 (staging + scoring needed before graduation)
- Phase 2 gates Phase 6 (structure needed before scout rewrite)
- Phases 1, 8 are independent (can do anytime)
