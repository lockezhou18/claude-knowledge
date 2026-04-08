---
id: know-041
track: knowledge
type: semantic
repos: ["*"]
tags: ["publication", "paper", "patent", "plan", "research", "conference"]
severity: high
rot_rate: slow
created: "2026-04-04"
last_verified: "2026-04-04"
use_count: 0
outcome_score: 0
status: active
---

## Context
Plan to publish a research paper on the compound learning system. Patent filed (ID 93827). Need to follow go/engpublications process and strengthen the paper with multi-user data.

## The Plan

### Phase 1: Foundation (Week 1)
- Talk to manager — get initial support for publication
- Identify Eng Lead (Sr Director+) for sign-off
- Pick target venue: CHASE workshop first (40-50% acceptance, N=1 sufficient), then CHI/ASE with multi-user data
- Get 2-3 teammates to install the system

### Phase 2: Data Collection (Week 2-3)
- Teammates use the system for real work with /checkpoint + /compound
- Run /insights on each teammate's data — compare before/after
- 15-min interview with each: "What worked? What didn't?"
- Collect metrics: wrong-approach count, time saved, insights generated, skills used

### Phase 3: Paper Writing (Week 4)
- Frame as insight paper, not tool paper: "We discovered that AI agents can adapt behavior from implicit signals and that DIKW-structured knowledge lifecycle produces measurably better outcomes"
- Write one-pager (Google Doc) for Initial Review
- Run Eagle Eye (go/EagleEyeAgent) for hot topic detection
- Create JIRA ticket #1 in Peer-Review Requests (PR) project (SLA 15 days)

### Phase 4: Review + Submission (Week 5-8)
- Address Initial Review feedback
- Write full paper with multi-user data
- Create JIRA ticket #2 for Final Review (SLA 15 days, needs 2 Staff+ peer reviewers)
- Submit to venue

### What Increases Acceptance (ranked)

| Factor | Impact | Effort |
|--------|--------|--------|
| Get 2-3 teammates using system | Very high | Medium (2 weeks) |
| Before/after /insights comparison | High | Low (baseline exists) |
| Ablation study (disable components → measure) | High for full papers | Medium |
| Strong framing (discovery, not tool) | High | Low |
| Right venue selection | High | Low |
| Qualitative interviews | Medium | Low (15 min each) |
| Open-source (if approved) | Medium | Medium |

### Venue Strategy

| Venue | Acceptance | What to emphasize | N needed |
|-------|-----------|-------------------|----------|
| CHASE (workshop at ICSE) | 40-50% | Complete system + real data | N=1 ok |
| ASE Industry Track | 30-40% | Productivity gains + LinkedIn deployment | N≥3 |
| CHI Late-Breaking Work | ~35% | Behavioral RL + implicit feedback | N≥3 |
| CHI Full Paper | 20-25% | User study + interaction analysis | N≥5 |

### Strong vs Weak Framing

Weak: "We built a productivity system with 20 skills and 348 tests."
Strong: "We discovered that AI coding agents can adapt behavior from implicit conversational signals without model training, and that a DIKW-structured knowledge lifecycle with outcome-based graduation produces measurably better engineering outcomes."

### References
- Patent: ID 93827, https://linkedin-patent.anaqua.com/Details.aspx?ID=93827
- Process: go/engpublications (see know-040)
- Recipe: /recipe patent-publication-tracker

## When to Apply
When moving from patent filing to paper publication for any technical innovation.
