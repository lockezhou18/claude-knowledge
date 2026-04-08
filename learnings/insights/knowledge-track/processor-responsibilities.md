---
id: know-016
track: knowledge
type: semantic
repos: [hp-ats-integration-mt]
tags: [processor, kafka, phase2, connected-projects, architecture, nearline]
severity: high
created: 2026-03-31
last_verified: 2026-03-31
use_count: 0
outcome_score: 0
status: active
rot_rate: slow
paths: ["**/processors/**", "**/IntegrationEntityReadyEventProcessor*"]
---

**When** working on Phase 2 event processing, **understand which processor handles which entity type and what each one does** because the routing is implicit (based on entity URN prefix) and each processor has distinct Phase 2 behavior.

## Context

All inbound events arrive as `IntegrationEntityReadyEvent` and are routed by `IntegrationEntityReadyEventProcessor` based on the `integrationEntityUrn` prefix.

### ApplicationProcessor
- **Entity**: `integrationApplication:*`
- **Phase 2**: Creates HiringProjectCandidate (HPC) + SourcingChannelCandidate, resolves V2 identity, creates HPC→IntegrationApplication mapping
- **Known issue**: Race condition — `getAllStages()` can return empty if IntegrationApplicationStage not yet in IP (bug-002, fixed by PR #526)
- **Key method**: `processPhase2()` → `getOrCreateCandidate()` → `connect(currentStage)`

### ApplicationStageProcessor
- **Entity**: `integrationApplicationStage:*`
- **Phase 2**:
  1. Look up mapped HP stage via CandidateHiringState ↔ IntegrationJobRequisitionStage mapping
  2. Find PENDING HireEntityRequests matching the target state → update to SUCCESS
  3. Publish realtime SUCCESS event
  4. `resolveAndSyncCurrentState()` — move HPC to correct ATS stage if mismatched
  5. `createOrUpdateHistoryForStage()` — create history item in mcm-mt + IP mapping
- **Depends on**: HPC→ApplicationStage mapping (created by ApplicationProcessor)
- **ACL required**: `HiringProjectCandidateHistoryItemApi/create` and `partialUpdate` on mcm-mt

### JobRequisitionStageProcessor
- **Entity**: `integrationJobRequisitionStage:*`
- **Phase 2**:
  1. Fetch all stages from `IntegrationJobRequisitionStageApi/FindByCriteria`
  2. For each stage: check if CandidateHiringState mapping exists → CREATE or UPDATE path
  3. CREATE: create new CandidateHiringState (source=ATS) + IP entity mapping
  4. UPDATE: compare stage name → partialUpdate with `setMask` + `deleteMask`
  5. Sync pipeline: add/remove/reorder items in CandidateHiringPipeline
- **Fixed bugs**: Missing `setMask` (PR #518), missing `hiringProjectUrn` in TransformerContext (PR #518)
- **Key detail**: Processes ALL stages for the job requisition on every event (not just the changed one)

### ExportStatusEventProcessor
- **Event**: `IntegrationExportRequestStatusEvent` (tracking cluster, NOT queuing)
- **Phase 2**:
  1. Extract requestId + requestStatus from event
  2. Look up HireEntityRequest by requestId
  3. On FAILURE: update to FAILURE/FAILURE_WITH_TIMEOUT, publish realtime FAILURE event
  4. Idempotency: skip if already terminal (FAILURE/FAILURE_WITH_TIMEOUT)
- **Does NOT handle SUCCESS** — SUCCESS is handled by ApplicationStageProcessor when the confirmed stage event arrives
- **Topic**: `IntegrationExportRequestStatusEvent` (know-001: was wrong topic name before PR #528)

## Guidance

- When a new event type needs handling, add routing in `IntegrationEntityReadyEventProcessor`
- Each processor factory must be registered in `HpAtsIntegrationMtBootListener` with `@Import` + `generator.getBean()` (+ `provider.registerBean()` for gRPC services)
- Missing any registration piece = silent failure (zero events consumed, no errors logged)

## When to Apply

When adding new processing logic, debugging why events aren't handled, or understanding the Phase 2 event processing architecture.
