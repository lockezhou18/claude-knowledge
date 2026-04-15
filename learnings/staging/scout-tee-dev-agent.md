---
id: scout-tee-dev-agent
track: knowledge-track
repos: [linkedin-context/tee-dev-agent]
tags: [scout, agent-systems, ralph-loop, convention-audit, autonomous-coding, pr-review]
severity: info
created: "2026-04-07"
last_verified: "2026-04-07"
use_count: 6
outcome_score: 0
status: active
rot_rate: slow
---

# Scout: tee-dev-agent (Hiring Platform TEE Team)

## What They Have That We Don't

### 1. Ralph Loop — Fresh-Session-Per-Task Execution
When implementing a multi-task plan, generate a bash script that spawns a fresh Claude CLI session per task. Each task gets full context without cumulative degradation. `[HUMAN]` gates stop the loop for manual intervention. Inter-iteration context via structured `progress-summary.md`.
**Why it matters:** Prevents the #1 problem with long implementation sessions — context window exhaustion and hallucination creep.
**Adopted:** Yes — added to `/implement` as ralph-loop generator.

### 2. Codebase Convention Audit (Pre-Design Step)
Before creating any design artifacts, formally audit the target codebase: (1) find 2-3 similar examples, (2) trace naming conventions end-to-end (proto → stubs → API → service → client → factory → wiring → test), (3) verify upstream/downstream contract fields field-by-field, (4) document conventions in the plan.
**Why it matters:** Prevents expensive "wrong naming/wrong pattern" mistakes that require full rework.
**Adopted:** Yes — added as Phase 3 sub-step.

### 3. Auto PR Batch Reviewer with Risk Classification
Batch-review all open PRs in a repo, classify each as LOW-RISK (6 criteria: auto-deps, approval count, line count, prior review status) or HIGH-RISK, review LOW-RISK ones, produce summary.
**Why it matters:** Useful for oncall PR review duty.
**Status:** Watching — not yet adopted.

### 4. JIRA-to-PR Autonomous Orchestrator
MongoDB-backed system: polls JIRA → auto-detects target repo → creates worktrees → spawns 3-5 parallel workers → handles full PR lifecycle. Dashboard at localhost:5000.
**Status:** Watching — too heavy to adopt directly, but architecture patterns worth studying.

### 5. Centauri — Multi-Machine Agent Dashboard
Electron app connecting to agents on multiple machines via HTTP+WebSocket. Session monitoring, live streaming, permission handling, cost tracking.
**Status:** Watching.

### 6. Design Doc → JIRA Task Breakdown
Read design doc → deep codebase research → JIRA-ready tasks with agent-assisted estimation (50% reduction for pattern-based work).
**Status:** Watching.

## Our Competitive Advantages Over Them
- **Memory/Learning system**: Compound learning with tiered retrieval, manifest, graduation/pruning — far more sophisticated.
- **Hook ecosystem**: Automated scout, compound, commit-log, PR review hooks.
- **Skill taxonomy**: Layered Tier 1-3 system with capability tools vs their flat directory.
- **Cross-domain breadth**: Oncall, PEM, deployment, research skills vs their JIRA-to-PR focus.
