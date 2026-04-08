---
id: know-037
track: knowledge
type: semantic
repos: ["*"]
tags: [meta, skills, learn, aha, eureka, compound-learning, automation, hooks]
severity: high
created: "2026-04-03"
last_verified: "2026-04-03"
use_count: 0
outcome_score: 0
rot_rate: permanent
status: active
---

# Metadata Skill Evolution Plan: /learn, /aha, /eureka

## Context
The three knowledge capture skills form a graduated taxonomy: fact → connection → breakthrough. Each has a different signal weight (+1.0, +1.5, +2.0). The taxonomy is worth preserving — the evolution should be in how they interact, not what they are.

## Evolution Directions

### 1. Smarter Auto-Detection
When [/investigate finds a root cause matching a previous incident], suggest `/aha` with the connection pre-filled.
When [a proposed approach is fundamentally different from codebase patterns], suggest `/eureka`.
When [debugging reveals a non-obvious fact], suggest `/learn`.
**How to apply:** Update proactive suggestion triggers in MEMORY.md to be more specific about WHEN each skill is suggested, based on what just happened in the session.

### 2. Bidirectional Linking
When [3+ related /learn insights accumulate on the same topic], auto-suggest `/aha` to synthesize them.
/learn insights should link forward to the /aha they eventually feed (add `feeds_into` field).
/aha already links back to source episodes via `synthesized_from`.
**How to apply:** During /compound phase, scan manifest for clusters of related /learn insights and prompt for /aha synthesis.

### 3. Graduated Graduation
- `/learn` → standard path (use_count >= 3, outcome_score >= 2.0)
- `/aha` → fast-track (use_count >= 2, outcome_score >= 1.5 — patterns are inherently higher value)
- `/eureka` → immediate candidate for memory/rules promotion (ask user at capture time)
**How to apply:** Update graduation logic in compound phase to check insight origin skill.

### 4. Phase-Mapped Surfacing
- Phase 1 (Research): surface relevant `/learn` + `/aha` insights for the area being researched
- Phase 4 (Execute): flag contradictions between current work and existing `/learn` insights
- Phase 6 (Compound): explicitly prompt "Any `/aha` connections? Any `/eureka` moments?"
**How to apply:** UserPromptSubmit hook already does tiered retrieval — add phase-awareness to boost aha/eureka in relevant phases.

## Key Principle
The three skills stay simple — the intelligence goes into the hooks and compound phase, not the skills themselves.
