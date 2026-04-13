---
id: know-067
track: knowledge
type: semantic
repos: ["oncall", "hire-access-control"]
tags: ["entitlements", "seat-entitlements", "contract-type", "PurchasedHiringPlatformFeatures", "hire-access-control", "curli"]
severity: high
rot_rate: slow
status: active
created: "2026-04-13"
last_verified: "2026-04-13"
use_count: 0
outcome_score: 0
---

## HP Seat Entitlement Resolution — Full Code Path

**When investigating missing entitlements, trace the full evaluation chain before proposing fixes.**

### How seat entitlements are resolved (HiringPlatformEntitlementsServiceImpl):

1. Fetch seat from seatsV2 → get `seatRoles` (HP_ADMIN_SEAT, etc.)
2. Fetch contract from contractsV2 → get `contractType` (RECRUITER, RECRUITER_PLUS, etc.)
3. Fetch PurchasedHiringPlatformFeatures → if 404, returns **empty set** (doesn't fail)
4. Build `contractKeys` = {each feature name} + {contractType name}
5. Look up `SeatRoleAndContractEntitlements.json`:
   - For "ALL" seat role section: match contractKeys against inner keys → collect entitlements
   - For each seatRole: match contractKeys against inner keys → collect more entitlements
   - Add "ALL" contract type entitlements (always present)
6. Post-processors may add/remove entitlements

### Key implication:
RECRUITER contract type ALREADY grants CAN_CREATE_HIRING_PROJECT in the JSON config. PurchasedHiringPlatformFeatures is NOT required for this entitlement on RECRUITER contracts.

### Curli reference:
```bash
# Seat entitlements
d2://seatEntitlements/(hiringContext:urn%3Ali%3Acontract%3A{contract},seat:urn%3Ali%3Aseat%3A{seat})

# PurchasedHiringPlatformFeatures
d2://purchasedHiringPlatformFeatures/urn%3Ali%3Acontract%3A{contract}

# Contract type
d2://contractsV2/{contractId}?fields=type,onlineJobPosting

# Role assignments by assignee
d2://hireRoleAssignments?q=assignee&hiringContext=urn%3Ali%3Acontract%3A{contract}&assignee=urn%3Ali%3Aseat%3A{seat}&state=ACTIVE

# Role assignments by target project
d2://hireRoleAssignments?q=target&hiringContext=urn%3Ali%3Acontract%3A{contract}&target=urn%3Ali%3AhiringProject%3A%28urn%3Ali%3Acontract%3A{contract}%2C{projectId}%29&assignees=List(urn%3Ali%3Aseat%3A{seat})&state=ACTIVE

# Project viewer entitlements
d2://hiringProjects?ids=List((hiringContext:urn%3Ali%3Acontract%3A{contract},id:{projectId}))&fields=id,state,type,viewerEntitlements&viewer=urn%3Ali%3Aseat%3A{seat}

# Job posting details
d2://jobPostings/{jobId}?fields=jobState,listingType,limitedListing,source,subListingType,owner
```
All curlis use: `--dv-auth SELF -f prod-ltx1 -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0'`
