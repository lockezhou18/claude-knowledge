---
id: know-032
track: knowledge
type: semantic
repos: [*]
tags: [meta, compound-learning, behavior, reward-system, aha]
severity: high
rot_rate: permanent
created: "2026-04-02"
last_verified: "2026-04-02"
use_count: 22
outcome_score: 0
status: active
synthesized_into: "aha-005"
---

## Context
/aha moment from comparing insights report data with compound system capabilities: the system captures knowledge well (23 insights, 1 graduated) but doesn't yet prevent behavioral mistakes (14 wrong-approach instances).

## Guidance
Knowledge and behavior are different feedback loops:
- **Knowledge loop** (working): experience → insight → manifest → scout surfaces it → next session benefits
- **Behavior loop** (gap): agent does wrong thing → user corrects → but no mechanism prevents the same type of mistake next time

The reward/feedback system (researched, Option A ready) would close the behavior loop:
- Detect when user redirects the agent → classify as correction
- Track which behavioral dimensions get corrected (e.g., "guesses root cause without evidence")
- After 3+ corrections on same dimension → generate a behavioral rule
- Behavioral rules are stronger than insights — they directly change how the agent acts

## When to Apply
When building self-improving agent systems: knowledge capture alone is insufficient. You also need behavior correction that persists across sessions. The reward system is the missing piece.
