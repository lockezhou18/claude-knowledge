---
id: eureka-008
track: knowledge
type: semantic
repos: [*]
tags: [eureka, goal-driven, paradigm, context-repo, execution, design-driven, cross-boundary, workflow, figma, playwright, worktree]
severity: critical
created: '2026-04-05'
last_verified: '2026-04-05'
use_count: 12
outcome_score: 0.0
rot_rate: permanent
status: active
origin_skill: eureka
emerged_from: 'eureka-006,eureka-007'
graduation_candidate: True
visibility: team
---

## Breakthrough

Reframe engineering work from **task-driven** ("fix file X line Y") to **goal-driven** ("recruiter sees Failed badge when ATS rejects a stage move"). The deliverable isn't a PR — it's a **completed goal verified end-to-end across all layers**.

## The Old Way (Task-Driven)

```
Jira ticket: "Add failureReasonType to ExportStatusEventProcessor"
  → Engineer opens one repo
  → Makes change in one file
  → Tests in isolation
  → PR merged
  → Hope it works with other services
  → Hope it looks right in the UI
  → Hope Greenhouse sees it correctly
```

Each task is a disconnected unit of work. The engineer must hold the full picture in their head. Cross-service features require multiple tickets, multiple engineers, manual coordination.

## The New Way (Goal-Driven)

```
Goal: "Recruiter sees Failed badge when ATS rejects a stage move"
  │
  ├── Design (Figma): red badge, failure reason copy, conflict banner
  │     → extracted from figma/screens/failed.png
  │
  ├── Frontend (ts-web): ProfilePipelineStatus reads latestRequest.status
  │     → identified from design-to-code-traceability.md
  │     → selectors: [data-test-pipeline-state], failureReasonType display
  │
  ├── API (ts-api): failureReasonType in hiringProjectRecruitingProfile
  │     → identified from frontend-scope.md
  │
  ├── Backend (hp-ats): ExportStatusEventProcessor sets FAILED + reason
  │     → identified from three-pipelines.md (Pipeline 3)
  │     → worktree: hp-ats/bizhou/add-failure-reason
  │
  ├── Backend (mcm-mt): surface failure reason to HPC decorator
  │     → worktree: mcm-mt/bizhou/surface-failure-reason
  │
  ├── Verification:
  │     → Playwright: sees red badge with correct failure text
  │     → Greenhouse API: confirms application move was rejected
  │     → grpcurli: HireEntityRequest status=FAILED, failureReasonType=BLOCKED
  │
  └── Goal COMPLETE ✓ when all layers agree
```

## How It Works (Architecture)

```
connected-projects-shared          hp-dev-agents
(Context: what + why)              (Execution: how)
                    \              /
                     \            /
                   Bridge Skills
                   /implement (goal → worktrees → PRs)
                   /fix (bug → trace → worktrees → PRs)
                   /adapt (dep change → worktrees → PRs)
```

- **Context repo** provides: Figma designs, architecture (3 pipelines), file paths (traceability), test data, verification commands, patterns, glossary
- **Execution repo** provides: git worktrees for parallel multi-service branches, build/test per service, PR creation, deployment
- **Bridge skills** connect them: take a goal, use context to determine what to change, use execution to make and verify the changes

## Impact

- **Quality**: Goals are verified end-to-end, not in isolation. "It works in my service" → "it works across all layers"
- **Speed**: Parallel worktrees + pre-identified file paths = no time wasted searching for what to change
- **Alignment**: Design → implementation → verification all traced. No "it works but doesn't match the spec"
- **Onboarding**: New engineer gets a goal, not a list of files. The system guides them through the full chain
- **Coordination**: Cross-service features don't need separate tickets per service. One goal, one flow, multiple worktrees

## The Knowledge Chain

```
/learn (individual facts) → /aha (3 pipelines) → /eureka (cross-boundary view)
  → /eureka (context repo = force multiplier) → /eureka (goal-driven development)
```

Each level:
- Facts → one person, one session
- Pattern → one person, across sessions
- Unified view → one person, across boundaries
- Context repo → entire team, permanently
- Goal-driven → entire team, paradigm shift in how work is done
