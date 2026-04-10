---
name: Seat Transfer MOVE_APPLICATION_DATA Failure Pattern
description: Seat transfer fails at MOVE_APPLICATION_DATA due to legacy hireIdentity records missing referenceEntityUrn — trace through mcm-mt → hire-identity-service → Espresso
type: project
---

When seat transfers fail at MOVE_APPLICATION_DATA step, the root cause is often in hire-identity-service, not mcm-mt.

**Error chain:**
```
EP orchestrator (enterpriseProfileMoveJobs) → MOVE_APPLICATION_DATA FAILED
  → mcm-mt SeatTransferNearlineEntityActionEventHandler → McmException: Unable to fetch all entities
    → hire-identity-service HireIdentityV2CopyServiceImpl.copyReference() → "HireIdentityV2 cannot miss reference"
      → Espresso HireIdentity record has null referenceEntityUrn (legacy V1 record from 2018)
```

**Investigation workflow:**
1. Check EP's enterpriseProfileMoveJobs for the error (errorsV2 → MOVE_APPLICATION_DATA FAILED)
2. Search mcm-mt logs for SeatTransferNearlineEntityActionEventHandler errors with the source contract
3. Search hire-identity-service logs for "Failed to copy reference" or "cannot miss reference" — this reveals the blocking hireIdentity ID
4. Verify the hireIdentity via: `curli -f prod-lor1 --dv-auth SELF -H 'X-RestLi-Protocol-Version:2.0.0' -H 'Accept:application/json' "d2://hireIdentitiesV2/{id}?contract=urn%3Ali%3Acontract%3A{contractId}"`
5. If referenceEntityUrn is null → data fix needed

**Data fix (direct Espresso write):**
- SSH to prod shell (ltx1-shell07.prod.linkedin.com)
- `id-tool grestin -f prod-lor1 sign` (needs Yubikey)
- D2 service: `EDB-HireIdentity`, path: `/HireIdentity/HireIdentity/{id}`
- Espresso schema version: 6
- Set referenceEntityUrn to `urn:li:member:{memberId}` and hiringContextUrn to `urn:li:contract:{contractId}`

**Why:** Legacy V1 hireIdentity records (pre-2018) were created before referenceEntityUrn was mandatory. The copyReference() method hard-fails on these. Retries never succeed — persistent data issue.

**How to apply:** Any CSE ticket about failed seat transfers with MOVE_APPLICATION_DATA error. Check hire-identity-service logs first for the specific hireIdentity ID.
