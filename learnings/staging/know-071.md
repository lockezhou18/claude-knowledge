---
id: know-071
track: knowledge
type: semantic
repos: [compound-learning-ecosystem]
tags: [compound-learning, scoring, outcome, decay, ebbinghaus, dream]
severity: critical
rot_rate: permanent
status: active
created: 2026-04-14
last_verified: 2026-04-14
use_count: 0
outcome_score: 0
origin_skill: compound
---

When insights accumulate retrieval counts but outcome_score stays at 0, the problem is the scoring pipeline — not the decay math. The dream engine's Ebbinghaus decay only touches insights with score > 0. If outcome-log.jsonl only contains "retrieved" events (delta=0), scores never move, nothing graduates, nothing gets pruned. The fix: /compound must explicitly judge each retrieved insight as helped (+1.0), irrelevant (0), or wrong (-1.0) and log "scored" events with real deltas. This is the pump that keeps the lifecycle alive.
