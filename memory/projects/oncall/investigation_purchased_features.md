---
name: PurchasedHiringPlatformFeatures Creation Flow
description: How purchasedHiringPlatformFeatures records are created, read, and why they go missing — affects job posting and CLAIM workflow
type: project
---

## PurchasedHiringPlatformFeatures — Creation and Lookup

### Creation Flow
```
Fulfillment Orchestrator (license allocation change)
  → hp-ep-mt: HireFulfillmentConfigurationServiceImpl.preFulfillmentChange()
    → modifyHiringPlatformFeatures(contractId, productUrn, isNewAllocation, isFullRevoke)
      → PurchasedHiringPlatformFeaturesClient.createOrUpdatePurchasedHiringPlatformFeatures()
        → hire-access-control: PurchasedHiringPlatformFeaturesResource (PUT)
          → Espresso DB: HireAccessControlDB
```

**When created:** On new license allocation (existingTotalAmount=0, proposedTotalAmount>0) for products in `ALLOWED_PRODUCTS_FOR_PURCHASED_HIRING_PLATFORM_FEATURES`
**When deleted:** On full revoke (existingTotalAmount>0, proposedTotalAmount=0) — removes ATS_FEATURES

### Read Flow (hire-access-control)
`PurchasedHiringPlatformFeaturesServiceImpl.get()`:
1. If `contract.onlineJobPosting == true` → returns `JOB_POSTING_FEATURES` directly (no DB hit)
2. Otherwise → reads from Espresso DB
3. If not found → throws 404

### MINI (RLite/OJ) Contract Special Case
- MINI contracts should have `onlineJobPosting=true`, which bypasses the DB entirely
- If `onlineJobPosting=false` on a MINI contract, it falls through to DB → 404 if no record exists
- PORT-199994: Contract 13002001 is type MINI but `onlineJobPosting=false` → 404

### Impact of Missing Record
- **mcm-jobs-integration-mt:** `PurchasedHiringPlatformFeatureHelper` gates all workflows → `_workFlows=[]` → CLAIM never triggers → WRAPPABLE_JOB_POSTING stuck
- **talent-jobs-api / jobposting-relevance:** Can't fetch features → job posting/promotion fails with "NO_RECORD_FOUND"

**Why:** This is a recurring pattern — missing features blocks multiple flows. Understanding the creation path helps determine if it's a provisioning gap vs accidental deletion.

**How to apply:** When purchasedHiringPlatformFeatures returns 404, check: (1) contract type, (2) onlineJobPosting flag, (3) whether Fulfillment Orchestrator ever provisioned it. For MINI contracts, the onlineJobPosting flag is the key.
