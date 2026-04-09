---
id: know-020
track: knowledge
repos: [hp-ats-integration-mt, mcm-mt, talent-solutions-api, hire-access-control]
tags: [architecture, design, phase2, prd, rfc, decisions]
severity: high
created: 2026-03-31
last_verified: 2026-03-31
use_count: 0
outcome_score: 0
status: active
rot_rate: slow
---

**When** making architectural decisions or extending Phase 2, **check** these design-to-implementation mappings **because** each implementation choice was driven by a specific business requirement, and changing one requires understanding the chain.

## Business → Tech Mapping

### 1. "Surface ATS requisition stages in Connected Project pipeline"
- **PRD**: Recruiter sees ATS stages alongside HP sourcing stages
- **RFC Decision**: Create a separate `candidateHiringPipeline` (atsPipeline) with **non-global states** for ATS stages
- **Why non-global**: ATS stages are project-specific (each job has different stages). Global states are contract-level and shared across all projects. Using non-global prevents one project's ATS stages from polluting another.
- **Why separate pipeline**: HP sourcing stages (uncontacted, contacted, replied) are shared across contract. ATS stages are per-job-requisition. Separate pipeline preserves this boundary.
- **Implementation**: `hiringProject.atsPipelineUrn` → `candidateHiringPipeline` with one `candidateHiringState` per `integrationJobRequisitionStage`

### 2. "Move candidate in Recruiter, reflects in ATS"
- **PRD**: Recruiter initiates stage change → ATS updates
- **RFC Decision**: Write-back goes through **hp-ats-integration-mt → IP → ATS** (not direct to ATS)
- **Why through IP**: IP handles partner-specific API implementations (Greenhouse, Lever, etc.). HP doesn't know ATS partner details. IP provides the `actionUpsert` abstraction.
- **Why hp-ats-integration-mt is orchestrator**: It already hosts the entity mapping (IntegrationApplicationStage ↔ HPC) and knows how to translate HP URNs to IP URNs. mcm-mt is the caller (detects Connected Project context), hp-ats-integration-mt is the executor.
- **Implementation**: mcm-mt `hiringProjectCandidates/partialUpdate` → detects Connected Project → calls `ConnectedProjectCandidateApi/ActionWriteBack` → resolves V2 identity → finds entity mapping → calls IP `actionUpsert`

### 3. "ATS confirms change, reflected back in HP"
- **PRD**: After write-back, ATS confirmation syncs back
- **RFC Decision**: Two confirmation paths — SUCCESS via `IntegrationEntityReadyEvent` (queuing), FAILURE via `IntegrationExportRequestStatusEvent` (tracking)
- **Why two paths**: SUCCESS path is the normal ATS sync (same event as initial sync). FAILURE path is a nearline status update specific to export requests.
- **Why ATS is source of truth**: Even when HP initiates a stage change, we don't sync it directly. We send the request to ATS via IP. Only when ATS sends back an update (via BI/BO) do we actually sync it. The ExportRequestDB tracks this lifecycle.
- **Implementation**: `ApplicationStageProcessor.processPhase2()` handles SUCCESS. `IntegrationApplicationStageExportStatusEventProcessor` handles FAILURE.

### 4. "ATS applicants can only be moved to ATS stages"
- **PRD**: Prevent stage going out of sync between HP and ATS
- **RFC Decision**: ATS applicants restricted to ATS stages in UI. Sourced candidates can move to any stage.
- **Why**: Most major ATS partners (including Greenhouse) don't support creating new stages via API. If an ATS applicant is moved to an HP-only stage, there's no way to sync that back to ATS. This would break the bidirectional promise.
- **Implementation**: Frontend enforces this in ts-web. Backend validates in mcm-mt before calling write-back.

### 5. "Synchronize new ATS stages automatically"
- **PRD**: When stages are added/updated/reordered in ATS, HP pipeline updates
- **RFC Decision**: Consume `IntegrationEntityReadyEvent` for `IntegrationJobRequisitionStage` entity type
- **Why Kafka events (not polling)**: IP already publishes events for all entity changes via BI/BO. Polling would be wasteful and add latency.
- **Implementation**: `JobRequisitionStageProcessor` handles CREATE (add state), UPDATE (rename, reorder), and DELETE (deactivate mapping) via `syncPipeline()`

### 6. "Complete stage movement history across systems"
- **PRD**: Recruiter sees full candidate history regardless of which system initiated the move
- **RFC Decision**: Create `HiringProjectCandidateHistoryItem` for each stage change, with entity mapping to `IntegrationApplicationStage`
- **Why entity mapping for history**: Enables idempotency (don't create duplicate history items on event retry) and enables reverse lookup (which ATS stage corresponds to which history entry)
- **Blocker**: Espresso KEY_TOO_LONG — `HiringProjectCandidateHistoryUrn` exceeds 150-char key limit. Workaround: shortened URN with placeholder zeros (PR #529). Permanent fix: ESPENG-57173.

### 7. "ATS pipeline automation (InMail → auto-move to stage)"
- **PRD**: When recruiter sends InMail to ATS applicant, auto-move to configured stage
- **RFC Decision**: Store automation settings in `HiringProjectPreference` (hire-access-control), project-level setting independent of contract-level autoPipeline
- **Why project-level**: Each Connected Project connects to a different job requisition with different stages. The automation target stage must be per-project.
- **Why LLM suggestions**: Uses `talent-copilot-service/processStageMappingApi` to map ATS stage names to HP `candidateHiringStateUrn`. Reduces recruiter clicks during setup.

### 8. "Export sourced candidates to ATS"
- **PRD**: Candidates sourced in Recruiter can be exported to ATS pipeline
- **RFC Decision**: One-click export with credit enforcement, stage information included
- **Greenhouse limitation**: Greenhouse doesn't support creating new stages via API. Export sends the candidate to ATS with the selected stage, but ATS must already have that stage.
- **Not yet fully implemented** as of Phase 2 testing.

## Key Architectural Principles (from RFC)

1. **hp-ats-integration-mt is the orchestrator** — all HP↔IP coordination goes through it
2. **Entity mappings are the source of truth** for cross-system URN translation
3. **V2 identity for mappings, V1 for gRPC entities** — consistent separation
4. **ATS is source of truth for applicant stages** — HP doesn't override ATS state
5. **Non-global states for ATS stages** — prevents cross-project contamination
6. **Kafka events for inbound, gRPC for outbound** — natural for async (inbound) vs sync (outbound)
7. **Lix-gated per dataProvider** — enables gradual rollout per ATS partner
