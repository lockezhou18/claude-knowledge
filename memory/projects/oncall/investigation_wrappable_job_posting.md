---
name: CSE WRAPPABLE_JOB_POSTING Investigation
description: Edit Job greyed out because hiring project stuck in WRAPPABLE_JOB_POSTING type — traced through mcm-mt entitlements and mcm-jobs-integration-mt CLAIM workflow
type: project
---

## CSE-22355 / CSE-22266: Edit Job Button Greyed Out

**Root cause chain:**
1. mcm-mt `HiringProjectViewerEntitlementsFacadeImpl.getViewerEntitlementForHiringProject()` — if project type is `WRAPPABLE_JOB_POSTING`, returns only `CAN_VIEW_HIRING_PROJECT` (no edit)
2. ts-web `job-action-entitlements.js` `canEditJob()` checks `jobPosting.jobActions.includes('EDIT')` — without `CAN_EDIT_HIRING_PROJECT`, EDIT action missing → button greyed out

**Write flow (type conversion):**
- `mcm-jobs-integration-mt` creates project as `WRAPPABLE_JOB_POSTING` for enterprise wrappable jobs
- `JobClaimStatusValidator` checks if job is no longer wrappable → adds `WorkFlow.CLAIM`
- `HiringProjectClaimProcessor` does `setType(HiringProjectType.RECRUITER)` via partial update to mcm-mt
- But `PurchasedHiringPlatformFeatureHelper` gates ALL workflows — if contract missing features, `_workFlows=[]` and CLAIM never triggers

**Key finding for contract 282130:**
- `purchasedHiringPlatformFeatures` returns 404 → all workflows skipped → CLAIM never runs → project stays WRAPPABLE_JOB_POSTING permanently
- Other contracts (228994176, 2006173180) self-resolved because they have features and CLAIM eventually ran

**Verification commands:**
```bash
curli --dv-auth self -f prod-ltx1 "d2://hiringProjects?ids=List((hiringContext:urn%3Ali%3Acontract%3A<contractId>,id:<projectId>))" -H Accept:application/json -H X-RestLi-Protocol-Version:2.0.0
curli --dv-auth self -f prod-ltx1 "d2://purchasedHiringPlatformFeatures?ids=List(urn%3Ali%3Acontract%3A<contractId>)" -H Accept:application/json -H X-RestLi-Protocol-Version:2.0.0
```

**Why:** This pattern recurs — CSE-22266 was the same issue in Feb 2026. Escalate to EJ oncall for mcm-jobs-integration-mt flow issues.

**How to apply:** When seeing "Edit Job greyed out" CSEs, first check project type via curli. If WRAPPABLE_JOB_POSTING, check purchasedHiringPlatformFeatures for the contract.
