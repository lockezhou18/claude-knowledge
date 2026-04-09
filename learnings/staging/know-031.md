---
id: know-031
track: knowledge
type: semantic
repos: ["*"]
tags: ["meta", "friction", "wrong-approach", "compound-learning", "behavior", "self-improvement"]
severity: high
rot_rate: slow
created: "2026-04-02"
last_verified: "2026-04-02"
use_count: 0
outcome_score: 0
status: active
---

## Context
Claude Code /insights report (18 sessions, 467 messages) revealed that the #1 friction source is "wrong initial approach" — 14 instances across 18 sessions where the agent pursued the wrong root cause, wrong processor, or over-engineered solutions requiring user interruption and redirect.

## Guidance
The compound learning system captures knowledge effectively (insights accumulate), but doesn't yet prevent wrong-approach behavior at the start of work. Three things need strengthening:

1. **Hypothesis-first is not optional**: Before any code search or log reading, present 2-3 candidate hypotheses and wait for user confirmation. This is already in /investigate but the agent sometimes skips it.
2. **Pre-work context check matters**: The knowledge scout surfaces relevant insights, but the agent doesn't always use them to narrow the investigation before starting.
3. **Simpler = better**: When the codebase already has a pattern for the problem (e.g., in master), use it. Don't invent a new approach when an existing one works.

## When to Apply
Every debugging session, every investigation, every time the agent is about to "deep dive" into code. The cost of asking one question first ("which processor should I look at?") is 10 seconds. The cost of going down the wrong path is 20+ minutes.
