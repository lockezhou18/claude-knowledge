---
description: "Compound learning quick reference — insight lifecycle, outcome tracking, dream cycle"
---

# Compound Learning — Quick Reference

## Insight Format
"When [situation], do [action] because [reason]"
- Bug-track: Symptoms → Root Cause → Fix → Prevention
- Knowledge-track: Context → Guidance → When to Apply

## Outcome Tracking
```bash
~/.claude/learnings/log-outcome.sh <insight_id> <+1|-1> "<note>"
```
Log DURING work, not at session end. +1 = helped, -1 = misled.

## Lifecycle
```
New insight → staging/{id}.md → score via outcomes → graduate or prune
  Graduate: use_count >= 3 AND outcome_score >= 2.0 → memory/insights/
  Prune: outcome_score < -2 → deleted
  Stale: last_verified > 90 days → flagged for review
```

## Dream Cycle (overnight on VM, or /dream manually)
NREM: score staging insights from outcome-log
REM: graduate/prune/stale
SORT: classify flat files into subdirs
REBUILD: all MEMORY.md indexes
PROJECTS: per-project maintenance
SYNTHESIZE: cross-project patterns → new insights

## Key Paths
- `~/claude-knowledge/learnings/staging/` — pre-graduation insights
- `~/claude-knowledge/learnings/manifest.jsonl` — search index
- `~/claude-knowledge/learnings/logs/outcome-log.jsonl` — outcome tracking
- `~/claude-knowledge/memory/insights/` — graduated (permanent)
- See `~/.claude/learnings/SCHEMA.md` for full frontmatter spec
