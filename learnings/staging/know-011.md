---
id: know-011
track: knowledge
type: semantic
repos: [mcm-mt, hp-ats-integration-mt]
tags: [phase2, writeback, mcm-mt, e2e, connected-projects, lix, entity-mapping]
severity: high
created: "2026-04-01"
last_verified: "2026-04-01"
use_count: 4
outcome_score: 0
rot_rate: slow
status: active
paths: [**/HiringProjectCandidatesServiceImpl.java, **/ConnectedProjectCandidateService.java]
---

## mcm-mt → ActionWriteBack: 3 Prerequisites for Write-Back to Trigger

**When** testing the mcm-mt partialUpdate → ActionWriteBack E2E flow (either via curli or UI), **check all 3 conditions** because any one missing causes silent fallback to regular batchUpsert with no error.

### Prerequisites

1. **LiX `talent.connected.project.phase2.enabled`** must be ramped for the contract
   - mcm-mt checks: `_lixUtil.isEnabled(CONNECTED_PROJECT_PHASE2_ENABLED, contractUrn)` (HiringProjectCandidatesServiceImpl:683)
   - Currently ramped for contracts: `2011455851`, `237044161`

2. **Target CandidateHiringState must have `source: ATS`**
   - mcm-mt checks: `newState.hasSource() && newState.getSource() == "ATS"` (line 733)
   - Only non-global ATS stages have this — HP sourcing stages don't trigger write-back
   - Verify: `curli d2://candidateHiringStates/(hiringContext:...,id:STATE_ID)` → check `source` field

3. **Project must have active entity mapping in hpIntegrationEntityMappingApi**
   - mcm-mt checks: `FindByHiringEntity(hiringProjectUrn)` returns mapping with `status: ACTIVE` (line 784-801)
   - This mapping is created during Connected Project creation via `connectedProjectsApi/Create`
   - Verify: `grpcurli d2://hpIntegrationEntityMappingApi FindByHiringEntity -d '{"hiringEntityUrn":{"hiringProjectUrn":{...}}}'`
   - **Note**: Response uses `values` array not `elements` — parser must check both

### curli Command (requires seat URN as actor)

```bash
curli -X POST --dv-auth SELF -f prod-lva1 \
  -H "X-RestLi-Method:partial_update" \
  -H "Accept:application/json" -H "Content-Type:application/json" \
  -H "X-RestLi-Protocol-Version:2.0.0" \
  -d '{"patch":{"$set":{"candidateHiringState":"urn:li:candidateHiringState:(urn:li:contract:CONTRACT,TARGET_STATE_ID)"}}}' \
  "d2://hiringProjectCandidates/(candidate:urn%3Ali%3AhireIdentity%3AHI_ID,hiringContext:urn%3Ali%3Acontract%3ACONTRACT,hiringProject:urn%3Ali%3AhiringProject%3A%28urn%3Ali%3Acontract%3ACONTRACT%2CPROJECT_ID%29)?actor=urn%3Ali%3Aseat%3ASEAT_ID"
```

- `actor` query param is optional for curli but **must be seat URN** for write-back (line 691/816: `isActorSeat` check)
- Without seat actor, mcm-mt uses `DEFAULT_SEAT_URN`

### Verified E2E (2026-04-01)

- Project: `1447054345`, candidate: `69902986467`, seat: `1532862756`
- Move: Application Review (13035946218) → Preliminary Phone Screen (13035965517)
- Result: ActionWriteBack succeeded, requestId=9108
- Logs confirmed full chain: pre-filter → batchUpsertWithHistoryIds → entity mapping check → triggerWriteBack → actionWriteBack succeeded

### Silent Failure Mode

If any of the 3 conditions fails, mcm-mt silently falls back to `batchUpsert` — the candidate stage moves in HP but NO write-back happens to ATS. No error logged, just INFO: "LIX disabled, falling back to regular batchUpsert" or "no eligible candidates after pre-filter".
