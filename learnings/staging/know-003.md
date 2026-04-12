---
id: know-003
track: knowledge
repos: [hp-ats-integration-mt]
tags: [ip, job-requisition, greenhouse, api, testing]
severity: low
created: 2026-03-25
last_verified: 2026-03-25
use_count: 3
outcome_score: 1.94
status: active
rot_rate: slow
---

**When** you need to find the IntegrationJobRequisitionId for a Greenhouse job, **use** `IntegrationJobRequisitionApi/FindByCriteria` with keyword search + seatUrn viewer **because** IP's Get API requires the IntJobReqId which you don't have, and atsJobPostings API doesn't work for Greenhouse sandbox data.

## Command
```bash
grpcurli --dv-auth SELF -f prod-lva1 d2://integrationJobRequisitionApi \
  proto.com.linkedin.talent.partner.integrations.IntegrationJobRequisitionApi/FindByCriteria \
  -d '{"criteria":{"keyword":"JOB_TITLE","integrationContext":{"organizationUrn":{"organizationId":"107201551"}},"hasConnectedHiringProjects":false,"requestType":"RequestType_CONNECTED_PROJECTS"},"seatUrn":{"seatId":"SEAT_ID"},"paging":{"start":0,"count":5}}'
```
This is the same API the requisitions page uses.
