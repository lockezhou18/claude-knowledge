---
id: bug-007
track: bug
type: episodic
repos: ["hp-ats-integration-mt", "mcm-mt"]
tags: ["history", "mapping", "espresso", "validation", "partialUpdate", "dedup", "shortened-urn"]
severity: high
rot_rate: slow
status: active
created: "2026-04-01"
last_verified: "2026-04-01"
use_count: 0
outcome_score: 0
related_to: ["know-002"]
paths: ["hp-ats-integration-mt/src/main/java/com/linkedin/hire/ats/integration/service/ApplicationStageHistoryService.java", "hp-ats-integration-mt/src/main/java/com/linkedin/hire/ats/integration/service/HpIntegrationEntityMappingService.java"]
---

## When debugging history item duplicate creation, check all 3 layers because bugs stack

### Symptoms
- 5 duplicate `HiringProjectCandidateHistoryItem` created per Kafka event (retry loop)
- `INVALID_ARGUMENT` errors in `IntegrationEntityUrnMappingGrpcClient`
- `partialUpdate` failures with `hiringProjectId:0` in mcm-mt logs

### Root Cause — 3 stacked bugs

**Bug 1 (PR #529):** Shortened URN lix not ramped → full URN (~175 chars) exceeds IP Espresso 150-char key limit → `KEY_TOO_LONG` → mapping never saved → no dedup possible.

**Bug 2 (PR #537):** `validateMappingUpdate()` rejects history mapping because HPC mapping already exists for the same `integrationApplicationStageUrn`. The validation doesn't differentiate by entity type. Fix: skip validation for `INTEGRATION_APPLICATION_STAGE_HISTORY` (same pattern as `INTEGRATION_CANDIDATE`).

**Bug 3 (PR #538):** `getHistoryByApplicationStage()` returns shortened URN (zeros) from IP mapping → `partialUpdate` sends zeroed URN to mcm-mt → mcm-mt Espresso DAO uses 4-part composite key `(candidate, hiringContext, hiringProjectId, historyId)` → `[hireIdentity:0, contract:0, 0, historyId]` not found. Fix: reconstruct real URN from `hpcUrn` (in scope, has real V1 identity) + `historyId` from mapping, gated behind same lix.

### Fix
- PR #529: Shortened URN workaround (ESPENG-57173)
- PR #537: Skip validation for `INTEGRATION_APPLICATION_STAGE_HISTORY`
- PR #538: Reconstruct real URN for mcm-mt `partialUpdate`, lix-gated

### Prevention
- **When IP entity mapping uses shortened/placeholder URNs as keys, never pass those URNs to downstream service APIs.** The shortened URN is only valid as a storage key — downstream services (mcm-mt) use the full URN for Espresso composite key lookups.
- **When adding new entity types that share integration entity keys with existing types**, check `validateMappingUpdate()` — it may reject the new mapping. Add the new type to the skip list.
- **When retries happen without visible errors in the `message` field**, always check `exceptionChain`/`exceptionStackTrace` — the real error may only be in the exception details.
