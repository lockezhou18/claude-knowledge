# CSE Entitlement Check

Check seat entitlements, role assignments, project entitlements, and job posting details for a CSE ticket about permission issues (edit greyed out, missing entitlements, etc.).

## Input
- Contract ID, Seat ID, Job ID (optional), Project ID (optional)

## Steps

### 1. Seat Entitlements
```bash
curli --dv-auth SELF -f prod-ltx1 \
  "d2://seatEntitlements/(hiringContext:urn%3Ali%3Acontract%3A{{contract}},seat:urn%3Ali%3Aseat%3A{{seat}})" \
  -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0'
```
Check for: CAN_CREATE_HIRING_PROJECT, CAN_POST_JOB, CAN_PERFORM_JOB_POSTING_ACTIONS

### 2. Role Assignments
```bash
curli --dv-auth SELF -f prod-ltx1 \
  "d2://hireRoleAssignments?q=assignee&hiringContext=urn%3Ali%3Acontract%3A{{contract}}&assignee=urn%3Ali%3Aseat%3A{{seat}}&state=ACTIVE" \
  -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0'
```
Check for: HIRING_PROJECT_OWNER or HIRING_PROJECT_SOURCER on relevant projects

### 3. Project Viewer Entitlements (if project ID known)
```bash
curli --dv-auth SELF -f prod-ltx1 \
  "d2://hiringProjects?ids=List((hiringContext:urn%3Ali%3Acontract%3A{{contract}},id:{{project}}))&fields=id,state,type,viewerEntitlements&viewer=urn%3Ali%3Aseat%3A{{seat}}" \
  -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0'
```
Check for: CAN_EDIT_HIRING_PROJECT, project type (RECRUITER vs WRAPPABLE_JOB_POSTING)

### 4. Job Posting Details (if job ID known)
```bash
curli --dv-auth SELF -f prod-ltx1 \
  "d2://jobPostings/{{jobId}}?fields=jobState,listingType,limitedListing,source,subListingType,owner" \
  -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0'
```
Check for: jobState (LISTED/SUSPENDED/CLOSED), source (JobWrappingSource vs direct), limitedListing

### 5. Contract Type
```bash
curli --dv-auth SELF -f prod-ltx1 \
  "d2://contractsV2/{{contract}}?fields=type,onlineJobPosting" \
  -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0'
```
RECRUITER contract type grants CAN_CREATE_HIRING_PROJECT without PurchasedHiringPlatformFeatures.

### 6. PurchasedHiringPlatformFeatures (if entitlements missing)
```bash
curli --dv-auth SELF -f prod-ltx1 \
  "d2://purchasedHiringPlatformFeatures/urn%3Ali%3Acontract%3A{{contract}}" \
  -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0'
```
404 = not provisioned. But RECRUITER type should still grant base entitlements.

### 7. Role Assignment on Specific Project (if needed)
```bash
curli --dv-auth SELF -f prod-ltx1 \
  "d2://hireRoleAssignments?q=target&hiringContext=urn%3Ali%3Acontract%3A{{contract}}&target=urn%3Ali%3AhiringProject%3A%28urn%3Ali%3Acontract%3A{{contract}}%2C{{project}}%29&assignees=List(urn%3Ali%3Aseat%3A{{seat}})&state=ACTIVE" \
  -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0'
```

## Important
- **NEVER assert root cause** — present hypotheses with likelihood after running these checks
- **Compare working vs non-working** — always find a seat/project that WORKS on the same contract and diff
- Role assignments use `roleassignmentsv3` (NOT legacy `roleassignment` Espresso table)
- The `canEdit` logic in talent-jobs-api has additional conditions beyond entitlements (JobAdminSettings, lix flags, allowEditAtsJobsBackendEnabled)
