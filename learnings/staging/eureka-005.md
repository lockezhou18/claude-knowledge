---
id: eureka-005
track: knowledge
type: semantic
repos: [hp-ats-integration-mt, mcm-mt, talent-solutions-api, talent-solutions-web, talent-partner-integrations-mt]
tags: [eureka, phase2, connected-projects, architecture, pattern, pipeline-sync, writeback, realtime, entity-mapping, mental-model]
severity: critical
created: '2026-04-03'
last_verified: '2026-04-03'
use_count: 11
outcome_score: 0.0
rot_rate: permanent
status: active
origin_skill: eureka
emerged_from: aha-004
graduation_candidate: True
visibility: team
synthesized_from: [know-010, know-011, know-014, know-015, know-016, know-035, know-040]
---

## Breakthrough

50+ tasks, 9 workstreams, 7 services — but Phase 2 is actually **3 pipelines sharing one entity mapping layer**. This single mental model replaces the need to understand each task individually. Every bug, test, debugging session, onboarding explanation, and bug bash test case maps to one of these 3 + the shared layer.

## The Old Way
Reason about Phase 2 as a flat list of 50+ tasks across 7 services. Each service "does stuff." Debugging means tracing through arbitrary code paths. Explaining to someone new means walking through each service.

## The New Way
Phase 2 = 3 pipelines + 1 shared layer. Period.

## The Pattern

```
                    ┌──────────────────────┐
                    │   Entity Mapping      │
                    │   (shared layer)      │
                    │                       │
                    │  HP entity ↔ IP entity│
                    │  HPC ↔ IntApp         │
                    │  CHS ↔ IntAppStage    │
                    │  History ↔ IntAppStageHistory │
                    └───┬──────┬───────┬───┘
                        │      │       │
            ┌───────────┘      │       └───────────┐
            ▼                  ▼                   ▼
   ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
   │ Pipeline 1:  │   │ Pipeline 2:   │   │ Pipeline 3:   │
   │ INBOUND SYNC │   │ OUTBOUND      │   │ REALTIME      │
   │              │   │ WRITEBACK     │   │ FEEDBACK      │
   │ IP → HP      │   │ HP → ATS      │   │ Status → UI   │
   │              │   │               │   │               │
   │ Kafka:       │   │ gRPC chain:   │   │ Kafka:        │
   │ queuing      │   │ mcm→hp-ats→IP │   │ tracking      │
   │ cluster      │   │ →Greenhouse   │   │ cluster       │
   │              │   │               │   │               │
   │ Processors:  │   │ Services:     │   │ Services:     │
   │ JobReqStage  │   │ ActionWrite   │   │ ExportStatus  │
   │ Application  │   │ BackApi       │   │ EventProcessor│
   │ AppStage     │   │               │   │ → HireEntity  │
   │              │   │               │   │   Request     │
   │ Creates:     │   │ Creates:      │   │ → Realtime    │
   │ CHS, HPC,    │   │ IP action,    │   │   push event  │
   │ pipeline     │   │ HireEntity    │   │ → Notification│
   │ stages       │   │ Request       │   │               │
   └─────────────┘   └──────────────┘   └──────────────┘
```

## Why This Matters

**For debugging**: Every issue is either "data didn't come in" (Pipeline 1), "action didn't go out" (Pipeline 2), "status didn't come back" (Pipeline 3), or "mapping is wrong/missing" (shared layer). Start by identifying which pipeline, then trace within it.

**For testing**: Each pipeline can be tested independently:
- Pipeline 1: Produce IntegrationEntityReadyEvent → verify CHS/HPC created
- Pipeline 2: Move candidate in UI → verify Greenhouse stage changed
- Pipeline 3: Produce ExportStatusEvent → verify HireEntityRequest updated → verify UI refreshes

**For the bug bash**: The 3-state machine (Pending/Confirmed/Failed) maps directly:
- PENDING = Pipeline 2 fired (outbound)
- CONFIRMED = Pipeline 3 received success (feedback)
- FAILED = Pipeline 3 received failure (feedback)

**For frontend**: All 9 FE tasks map to Pipeline 3 output:
- Tasks 1-4: Subscribe to realtime events from Pipeline 3
- Tasks 5-6: Display aggregated Pipeline 3 failures
- Tasks 7-8: Banners + notifications from Pipeline 3 status changes

**For the mapping layer**: Most subtle bugs live here (V1/V2 identity mismatch, KEY_TOO_LONG, race conditions). If any pipeline misbehaves, check mappings first.

## When to Apply

- When debugging any Phase 2 issue: first ask "which of the 3 pipelines?"
- When planning tests: test each pipeline independently, then integration
- When explaining Phase 2 to someone new: "it's 3 pipelines + shared mappings"
- When a bug spans services: trace through the specific pipeline path, not randomly
