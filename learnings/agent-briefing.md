# Agent Briefing
<!-- Last updated: 2026-04-15 23:30 -->

## Active Work

### Connected Projects Phase 2 — Bidirectional Sync
- **Status:** in-progress
- **Repo:** hp-ats-integration-mt
- **Active PRs:** #541 (resilience), #530 (history mapping)
- **Blockers:** ESPENG-57173
- **Open investigation:** CSE-22440 (Admin unable to edit jobs) — backend entitlements correct, root cause unclear

### Memory Migration — Single SoT
- **Status:** Phase 6 complete, Phase 7-10 remaining
- **Architecture:** ~/claude-knowledge/memory/ is THE SoT. autoMemoryDirectory + per-project symlinks
- **Next:** Phase 2 (rewrite scout for better relevance), compound scoring validation

### AgentBus — VM Agent Communication
- **Status:** v0.3.0 — A2A + task lifecycle complete, QA verified (24/24 pass)
- **Repo:** ~/workspace/.agentbus
- **Last (2026-04-15):** Compared AgentBus vs Claude Agent Teams/subagents. Agent Teams = single-machine only, no cross-machine coordination. Created 3-layer bridge plan (docs/agent-teams-bridge-plan.md).
- **Next:** Layer 1 (vm-operator agent def), Layer 2 (--agent flag in adapter), FileTaskStore

### Developer Productivity Tooling
- **Status:** watering phase — stop adding, let data prove what works
- **System state:** 23+ skills, 8 recipes, portable knowledge repo, VM near-parity
- **Dream Agent:** Running at 10:57 UTC via cron on laptop

### Cybernetics Research
- **Status:** in-progress — session recovered after accidental tmux close
- **Location:** ~/projects/compound-learning-ecosystem
- **Session:** f0ba1463-8a19-4c92-979e-342faaa05cc9

## Last Session (2026-04-15)
Research/planning session in agentbus repo. Deep comparison of AgentBus vs Claude Code's native agent systems (subagents + Agent Teams). Key finding: Agent Teams are strictly single-machine/single-process — AgentBus is the only cross-machine coordination layer. Created 3-layer integration plan (vm-operator teammate -> agent-aware listener -> cross-machine bridge). Enriched docs/comparison-cutting-edge.md, created docs/agent-teams-bridge-plan.md, saved project memory.

## Hot Insights

1. **[know-032] GRADUATED** — Knowledge loop works, behavior loop is the gap
2. **[bug-002] race condition** — ApplicationProcessor stage not in IP
3. **[know-068] Assert-Before-Verify** — 3-gate check before any conclusion
4. **[know-072]** — Claude Code session recovery via JSONL files
5. **[know-045]** — vm-run: sync-and-build from any local repo
6. **[know-031] #1 friction: wrong-approach** — Hypothesis-first not optional
7. **[aha-007]** — 7-layer production agent platform model + AgentBus gap analysis
8. **[eureka-006]** — AI agent as connective tissue between silos

## Recent Patterns
- AgentBus positioning: complementary to Claude native agents, not competing
- User exploring how to bridge single-machine Agent Teams with cross-machine AgentBus
- Research sessions producing documentation artifacts rather than code changes

## Behavioral Reminders
- **Present hypotheses before deep-diving** (14+ signals)
- **Prefer simple solutions from codebase** (5+ signals)
- **Don't overwrite — add alongside** (3 signals)
- **Listen for gentle redirects** — "how do you feel", "meanwhile", "I feel like" = soft instruction
- **Start simple, let user escalate complexity**
- **NEVER assert — only hypothesize with likelihood**
- **curli/grpcurli = try LOCAL first**, VM only if local auth fails
- **COMPOUND: Every 3+ task session -> generate >= 1 insight**

## Quick Stats
- Skills: 22 commands + 15 skills + 8 recipes
- Insights: 83 total, 3 graduated, 0 pruned, 0 stale
- Feedback signals: 190 total
- Knowledge repo: bizhou_LinkedIn/claude-knowledge
