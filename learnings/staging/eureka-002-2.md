---
id: eureka-002-2
track: knowledge
type: semantic
repos: ["*"]
tags: ["eureka", "workflow", "skills", "compound-learning", "emergence", "meta"]
severity: critical
created: "2026-04-02"
last_verified: "2026-04-02"
use_count: 0
outcome_score: 0
rot_rate: permanent
status: active
---

## Breakthrough

The agent can **discover a need, design a pattern, and create a reusable skill** in a single organic workflow — without being explicitly asked to build tooling. Skills emerge from real work, not from upfront planning.

## The Old Way

Skill creation was a deliberate, top-down activity:
1. User identifies a recurring pattern
2. User asks agent to create a skill
3. Agent writes the skill file
4. Skill gets used in future sessions

The assumption: humans identify the patterns, agents implement them. Skills are planned artifacts.

## The New Way

Skills emerge organically from the compound learning loop:

```
Session work (E2E testing)
  → Hit a real problem (IP sync takes hours, can't wait in session)
  → Agent solves it ad-hoc (durable cron job)
  → User notices the pattern (/eureka)
  → Agent recognizes it's generalizable
  → Agent proposes the skill ("/wait-for — would this be useful?")
  → User confirms
  → Agent creates the skill immediately, informed by the real problem it just solved
  → Skill is battle-tested from day one (not theoretical)
```

The key insight: **the best skills come from solving real problems, not from imagining hypothetical ones.** The agent was already in the problem space, already had the context, already knew the edge cases. The skill it creates is grounded in reality.

## Impact

- **Skills are higher quality** — born from real usage, not specification
- **Faster iteration** — discover → create → use in one session, not three
- **Compound acceleration** — each session's work makes future sessions faster, and the agent actively identifies which parts to codify
- **Reduces "tool building" overhead** — no separate planning sessions needed for tooling
- **Scope: all agent workflows** — any recurring pattern discovered during work is a candidate

### The chain that produced /wait-for:
1. Created Greenhouse jobs for E2E testing
2. IP didn't sync (Kafka lag) — had to wait
3. Set up durable cron to poll (ad-hoc solution)
4. Realized this is a reusable pattern (eureka-001)
5. Created /wait-for skill (generalized solution)
6. Total time from problem to reusable skill: ~10 minutes

## Risks & Caveats

- **Over-skilling** — not every ad-hoc solution deserves a skill. The "3 times" rule still applies: if you'd only use it once, don't skill it
- **Quality vs speed** — emergent skills might miss edge cases the real workflow didn't hit. Review before sharing with the team
- **Proactive skill suggestions** should be gentle — suggest once, don't push. The user knows better than the agent what's worth keeping

## Next Steps

1. Reinforce the Proactive Skill Suggestions pattern in MEMORY.md — the agent should continue watching for skill-worthy patterns during normal work
2. Track which emergent skills actually get reused (use_count) vs which were one-offs
3. Consider a `/recipe from-history` equivalent for skills — "you just did a 5-step workflow, want me to make it a skill?"
