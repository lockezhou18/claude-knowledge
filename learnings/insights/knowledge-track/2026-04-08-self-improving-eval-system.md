---
id: know-048
track: knowledge
type: semantic
repos: ["*"]
tags: [eval, self-improving, oracle, compound-learning, meta, architecture]
severity: critical
rot_rate: permanent
status: active
created: 2026-04-08
last_verified: 2026-04-08
use_count: 0
outcome_score: 0
summary: "Self-improving eval system: LLM judge classifies session failures into 7 types, simulates fix impact, applies highest-priority fix, re-measures. Oracle pattern adapted for AI Partner quality."
file: "insights/knowledge-track/2026-04-08-self-improving-eval-system.md"
---

When building a quality improvement system for an AI agent, use the Oracle eval pattern: structured failure taxonomy + LLM-as-judge + improvement simulation + closed loop.

**Architecture:**
- Judge evaluates sessions across 5 dimensions: agreement rate, behavioral awareness, compound learning, collaboration, principle adherence
- 7 failure types: wrong_approach, tool_misuse, over_engineering, skill_deficiency, skill_gap, context_miss, user_ambiguity
- Simulation: "if we fix all X failures, agreement improves by Y%" → prioritize fixes
- Closed loop: fix → re-measure → accept/revert

**Key numbers (baseline, 35 sessions):**
- Agreement rate: 76.2% (94.5/124 correct first approach)
- Principle adherence: 85.1% (349/410)
- Foundation score: 0.84
- Loop closure: 10% (worst metric)

**Why:** Modeled after candidate-quality-oracle (PRs #265, #300). Their system drove industry_match agreement from 25% → 70%. Ours identified wrong_approach as #1 friction (+9.7% if fixed) and verify_own_understanding as #1 principle violation (14x).

**How to apply:** Run `/improve-agent` periodically. It reads session transcripts, judges them, classifies failures, simulates improvements, and proposes fixes to behavioral gates. Each iteration should target one failure type.
