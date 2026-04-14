---
id: know-069
track: knowledge
type: semantic
repos: ["*"]
tags: [compound-learning, outcome-tracking, graduation, dream, scout, meta]
severity: critical
rot_rate: slow
status: active
created: 2026-04-13
last_verified: 2026-04-13
use_count: 0
outcome_score: 0
origin_skill: learn
related_to: ["know-032"]
---

# Outcome Scoring Gap: 97 Retrievals, 0 Judgments

## Context
Scout hook logs "retrieved" events (bumps use_count) but nobody logs "helped" or "wrong" — outcome_score stays at 0 for all insights. Dream can't graduate (needs score >= 2.0) because scores never move.

Evidence: eureka-006 has 97 uses but score=0. bug-002 only graduated because we manually seeded its score.

## Guidance
When fixing the outcome scoring gap, the missing piece is a **judgment step** — something must decide whether a retrieved insight actually helped during the session.

**Three options (pick one):**
1. **SessionEnd compound agent** — at session end, review which insights were retrieved and judge each as "helped" / "wrong" / "irrelevant"
2. **PostToolUse hook** — after certain tools, check if action was influenced by a retrieved insight and auto-score
3. **Inline in /compound** — during manual /compound, review retrieved insights and score them

Option 1 is the most automatic. Option 3 is the most accurate.

## When to Apply
- When fixing the compound learning graduation pipeline
- When insights accumulate high use_count but score stays 0
- When dream.py reports 0 graduations despite active usage
