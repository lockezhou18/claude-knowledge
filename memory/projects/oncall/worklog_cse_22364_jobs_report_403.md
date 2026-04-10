# Worklog: CSE-22364 — Unable to access Jobs report (403 FORBIDDEN)

**Date:** 2026-03-24
**Author:** bizhou
**CSE Ticket:** [CSE-22364](https://linkedin.atlassian.net/browse/CSE-22364)
**Fix PR:** [talent-reporting-api #2971](https://github.com/linkedin-multiproduct/talent-reporting-api/pull/2971)

---

## Summary

Non-admin users hitting 403 FORBIDDEN when accessing the Jobs report. Root cause: a LIX ramp in mcm-mt started returning cancelled projects from `findByOwner`, which broke a set-match validation in talent-reporting-api.

---

## Root Cause Analysis

### The Trigger: mcm-mt LIX Ramp

- **LIX:** `mcm.hiring.project.finder.refactor.enabled` (constant: `LixUtil.MCM_HIRING_PROJECT_FINDER_REFACTOR`)
- **JIRA:** [HPLT-16014](https://linkedin.atlassian.net/browse/HPLT-16014) — "Refactor the hiring projects finders to use findByCriteria"
- **PR:** [mcm-mt #3667](https://github.com/linkedin-multiproduct/mcm-mt/pull/3667) — merged **2026-03-11** by `pjohn_LinkedIn`, approved by `rading_LinkedIn`
- **Parent PR:** [mcm-mt #3617](https://github.com/linkedin-multiproduct/mcm-mt/pull/3617) — merged 2026-02-24 (Step 1+2 of multi-step refactor)

### What Changed in mcm-mt

In [`HiringProjectsServiceImpl.java`](https://github.com/linkedin-multiproduct/mcm-mt/blob/master/impl/service/src/main/java/com/linkedin/hire/impl/HiringProjectsServiceImpl.java):

**Line 978-981** — `findByOwner()` LIX gate:
```java
if (_lixUtil.isEnabled(LixUtil.MCM_HIRING_PROJECT_FINDER_REFACTOR, hiringContext)) {
    return findProjectsUsingFindByCriteria(hiringContext, hiringProjectState, start, count, config, owner, viewer);
}
```

**Line 1052-1078** — `findProjectsUsingFindByCriteria()` bug:
```java
if (hiringProjectState != null) {
    query.setHiringProjectStates(new HiringProjectStateArray(...));
}
// When hiringProjectState == null → NO state filter → returns ALL projects including CANCELLED
```

**Old path** (`findProjectsUsingGaleneSearch`, line 995-1047): Used Galene/SEAS search which **implicitly excluded** cancelled/closed projects via search indexing.

**New path** (`findProjectsUsingFindByCriteria`): Direct DB query with **no state filter** when `hiringProjectState=null` → returns all projects including cancelled.

### The Failure Point: talent-reporting-api

In [`JobAnalyticV2QueryValidatorService.java`](https://github.com/linkedin-multiproduct/talent-reporting-api/blob/master/talent-reporting-api-frontend/src/main/java/com/linkedin/talent/reporting/services/JobAnalyticV2QueryValidatorService.java):

`getHiringProjectValidationTask` (non-admin path):
1. Calls `findByOwner` → gets N projects (including cancelled)
2. Calls `batchGet` → gets N-X projects (cancelled silently dropped by auth check)
3. Set difference = X → throws **403 FORBIDDEN**

**Example:** Seat 293623736 → `findByCriteria` returns 401 projects (7 cancelled), `batchGet` returns 394 → 7 missing → 403.

### Why Some Seats Work Fine

Seat 1580388725 has **no cancelled/closed projects** → set difference is empty → 403 never triggered.

---

## Evidence: Error Timeline from Kusto

| Date | Error Count |
|------|-------------|
| Before Mar 9 | 0 |
| Mar 9 | 19 |
| Mar 10 | 98 |
| Mar 11+ | 100-165/day |

Zero errors before the LIX ramp. Exact correlation with the ramp date.

---

## Fix Applied

**PR:** [talent-reporting-api #2971](https://github.com/linkedin-multiproduct/talent-reporting-api/pull/2971)

**Change:** Added `HiringProjectState.ACTIVE` filter to `HiringProjectClient.findByOwner()` in talent-reporting-api:

```java
// Before (no state filter — returns all projects including cancelled)
HiringProjectSearchQuery searchQuery = new HiringProjectSearchQuery()
    .setHiringContext(hiringContext)
    .setOwners(new SeatUrnArray(ownerSeatUrns));

// After (only active projects returned)
HiringProjectSearchQuery searchQuery = new HiringProjectSearchQuery()
    .setHiringContext(hiringContext)
    .setOwners(new SeatUrnArray(ownerSeatUrns))
    .setHiringProjectStates(new HiringProjectStateArray(
        Collections.singletonList(HiringProjectState.ACTIVE)));
```

**Why this approach:**
- Cleanest fix — prevents cancelled projects from ever entering the validation pipeline
- Correct behavior — no reason to report on cancelled projects
- In our team's code (talent-reporting-api) — no dependency on mcm-mt team for deployment

**Files changed:**
- `HiringProjectClient.java` — added ACTIVE state filter (1 line)
- `HiringProjectClientTest.java` — added `testFindByOwnerFiltersActiveProjectsOnly`

**Build:** `mint build` passes (BUILD SUCCESSFUL)

---

## Key Links

| Resource | Link |
|----------|------|
| CSE Ticket | [CSE-22364](https://linkedin.atlassian.net/browse/CSE-22364) |
| Fix PR | [talent-reporting-api #2971](https://github.com/linkedin-multiproduct/talent-reporting-api/pull/2971) |
| Root Cause PR | [mcm-mt #3667](https://github.com/linkedin-multiproduct/mcm-mt/pull/3667) |
| Root Cause JIRA | [HPLT-16014](https://linkedin.atlassian.net/browse/HPLT-16014) |
| Validator Code | [JobAnalyticV2QueryValidatorService.java](https://github.com/linkedin-multiproduct/talent-reporting-api/blob/master/talent-reporting-api-frontend/src/main/java/com/linkedin/talent/reporting/services/JobAnalyticV2QueryValidatorService.java) |
| mcm-mt Finder Code | [HiringProjectsServiceImpl.java](https://github.com/linkedin-multiproduct/mcm-mt/blob/master/impl/service/src/main/java/com/linkedin/hire/impl/HiringProjectsServiceImpl.java) |

---

## Follow-up Considerations

1. **mcm-mt should also fix**: `findProjectsUsingFindByCriteria` should default to `ACTIVE` when `hiringProjectState=null` to match old Galene behavior (Option C from analysis). This would prevent similar issues in other downstream consumers.
2. **Monitor after deploy**: Confirm error count drops to 0 in Kusto after talent-reporting-api deployment.
