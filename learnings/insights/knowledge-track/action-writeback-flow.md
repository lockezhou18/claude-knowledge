---
id: know-015
track: knowledge
type: semantic
repos: [hp-ats-integration-mt]
tags: [writeback, action, phase2, connected-projects, greenhouse, grpc]
severity: high
created: 2026-03-31
last_verified: 2026-03-31
use_count: 0
outcome_score: 0
status: active
rot_rate: slow
paths: ["**/ConnectedProjectCandidateService*", "**/ConnectedProjectCandidateApi*"]
---

**When** debugging ActionWriteBack failures, **trace through the full chain step by step** because the flow spans 5+ services and failures at any link produce different error patterns.

## Context

### Full ActionWriteBack Chain
```
1. ConnectedProjectCandidateApi/ActionWriteBack (hp-ats-integration-mt)
   - Resolves V2 identity (V1→V2 if needed)
   - Looks up HPC→IntegrationApplicationStage mapping
   - Looks up target CandidateHiringState→IntegrationJobRequisitionStage mapping
   - Creates HireEntityRequest in Euler (status=PENDING)
   - Calls IP actionUpsert

2. IP IntegrationApplicationStageApi/actionUpsert (talent-partner-integrations-mt)
   - Creates IntegrationApplicationStageExportRequest
   - Routes to nexor-backend

3. nexor-backend → Greenhouse Harvest API
   - POST /applications/{id}/move (moves candidate to stage)

4. IP confirmation loop
   - Greenhouse data re-ingested
   - IntegrationExportRequestStatusEvent published (tracking cluster)

5. ExportStatusEventProcessor (hp-ats-integration-mt)
   - Updates HireEntityRequest: PENDING → SUCCESS/FAILURE
   - Publishes realtime event for UI refresh
```

### Common Failure Patterns

| Error | Location | Cause |
|-------|----------|-------|
| "No IntegrationApplicationStage mapping found" | Step 1 | Wrong V2 identity (bug-001) or race condition (bug-002) |
| FAILED_PRECONDITION | Step 2 | Integration disabled for this data provider |
| PERMISSION_DENIED | Step 1/2 | ACL not deployed for prod (EI ACLs don't cover prod) |
| Greenhouse 422 | Step 3 | Invalid stage transition or candidate already on target stage |
| HireEntityRequest stuck PENDING | Step 4-5 | ExportStatusEvent not published, or consumer on wrong topic (know-001) |

### Export Request Status Fields
| Field | Values | Meaning |
|-------|--------|---------|
| writeStatus | REQUEST_RECEIVED → REQUEST_AT_GATEWAY → PARTNER_API_SUCCESS/FAILURE | Outbound write progress |
| readStatus | DATA_READ_PENDING → DATA_READ_CONFIRMED/CONFLICT/EXPIRED | Confirmation read progress |
| recommendedStatus | INTERMEDIATE → SUCCESS/FAILURE | Overall recommendation |

## Guidance

Debug checklist:
1. Check HireEntityRequest status in Euler: `ManagedEntityCrudHireEntityRequest/get`
2. Check IP export request: `IntegrationApplicationStageExportRequestApi/Get` with requestId
3. Check hp-ats-integration-mt logs by treeId
4. If PARTNER_API_SUCCESS but HireEntityRequest still PENDING → ExportStatusEvent not consumed (check topic, consumer lag)

## When to Apply

When an ActionWriteBack call returns a requestId but the request stays PENDING, or when investigating write-back failures for any candidate.
