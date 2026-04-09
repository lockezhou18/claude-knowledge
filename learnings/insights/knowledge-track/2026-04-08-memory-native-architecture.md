---
id: know-049
track: knowledge
type: semantic
repos: ["*"]
tags: [architecture, memory, auto-dream, migration, compound-learning, meta]
severity: high
rot_rate: slow
status: active
created: 2026-04-08
last_verified: 2026-04-08
use_count: 0
outcome_score: 0
summary: "Memory-native architecture: Claude's Auto Memory/Dream as single knowledge store, custom systems as engines (eval, compound, behavior) that read/write memory."
file: "insights/knowledge-track/2026-04-08-memory-native-architecture.md"
---

When designing the knowledge architecture, make Claude's native memory the foundation — not a parallel store.

**Principle:** We generate + evaluate → Claude stores + maintains → we retrieve.

**Three layers:**
1. Auto Memory (native) = the WHAT (facts, preferences, findings)
2. Compound Engine (custom) = the HOW (scoring, lifecycle, search)
3. Eval Engine (custom) = the WHY (measurement, classification, improvement)

**Key insight:** Auto Dream handles memory hygiene (prune stale, merge overlaps, fix dates) for free. Our custom systems should generate knowledge and measure quality — not maintain the store.

**Migration plan:** ~/projects/compound-learning-ecosystem/memory-migration/plan.md
**Risk gate:** Phase 0 — test if Auto Dream preserves custom frontmatter fields.

**How to apply:** When writing new knowledge, write to memory/ (for Auto Dream) AND staging/ (for scoring). When graduating insights, move to memory/. Stop maintaining parallel stores.
