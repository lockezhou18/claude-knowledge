---
id: know-012
track: knowledge
type: semantic
repos: [talent-solutions-web, talent-solutions-api, mcm-mt, hp-ats-integration-mt]
tags: [phase2, writeback, frontend, e2e, connected-projects, rest-li, ui-flow]
severity: high
created: "2026-04-01"
last_verified: "2026-04-01"
use_count: 1
outcome_score: 0
rot_rate: slow
status: active
paths: [**/HiringProjectCandidatesServiceImpl.java, **/talentHiringProjectCandidates/**]
---

## Frontend → mcm-mt → ActionWriteBack: Full UI Write-Back Chain

**When** tracing or testing the write-back flow from the Recruiter UI, **understand the full call chain** so you can debug at each layer.

### Full Chain (verified 2026-04-01)

```
1. Recruiter UI (talent-solutions-web)
   → BATCH_PARTIAL_UPDATE to /talentHiringProjectCandidates
   
2. talent-solutions-api-frontend
   → REST.li resource receives the patch
   → Forwards to mcm-mt
   
3. mcm-mt HiringProjectCandidates.batchPartialUpdate
   → Checks 3 prerequisites (LiX, ATS source, entity mapping)
   → If all pass: batchUpsertWithHistoryIds → triggerWriteBack
   → Calls hp-ats-integration-mt ActionWriteBack
   
4. hp-ats-integration-mt
   → V1→V2 identity resolution
   → IntegrationApplicationStage mapping lookup
   → IP actionUpsert → Greenhouse
```

### Frontend curl format (from browser Network tab)

```
URL: /talent/api/talentHiringProjectCandidates/?ids=List(urn:li:ts_hiring_project_candidate:(urn:li:ts_contract:CONTRACT,urn:li:ts_hire_identity:HI_ID,urn:li:ts_hiring_project:(urn:li:ts_contract:CONTRACT,PROJECT_ID)))&altkey=urn
Method: BATCH_PARTIAL_UPDATE (X-RestLi-Method header)
Body: {"entities":{"urn:li:ts_hiring_project_candidate:(...)":{"patch":{"$set":{"candidateHiringState":"urn:li:ts_hiring_state:(urn:li:ts_contract:CONTRACT,TARGET_STATE_ID)"}}}}}
```

**Key differences from direct mcm-mt curli:**
- Uses `ts_` prefixed URN types (frontend format): `ts_hiring_project_candidate`, `ts_contract`, `ts_hire_identity`, `ts_hiring_state`
- Goes through `talentHiringProjectCandidates` (ts-api resource), NOT `hiringProjectCandidates` (mcm-mt) directly
- Uses BATCH_PARTIAL_UPDATE (not single partial_update)
- Actor is the authenticated recruiter session (from cookies), not a query param

### Verified E2E (2026-04-01)

- Project: `1447054345`, candidate: `738455478` (Haiwei Liu)
- Move: Reference Check (13035948183) → Face to Face (13035952104)
- Frontend response: `{"results":{"urn:...":{"status":204}},"errors":{}}`
- This triggered mcm-mt → ActionWriteBack downstream
