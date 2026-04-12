---
id: know-013
track: knowledge
type: semantic
repos: [hp-ats-integration-mt, talent-partner-integrations-mt]
tags: [ei, testing, e2e, local-dev, grpcurli, kafka, espresso, connected-projects]
severity: high
created: "2026-04-02"
last_verified: "2026-04-02"
use_count: 4
outcome_score: 0
rot_rate: slow
status: active
paths: [**/ApplicationProcessor.java, **/CandidateProcessor.java, **/ApplicationStageProcessor.java]
---

## EI Testing Patterns for hp-ats-integration-mt (Application + Candidate Sync)

**When** testing locally or in EI, use these patterns to set up test data, produce events, and verify the sync pipeline end-to-end.

### EI Test Environment

| Field | Value |
|-------|-------|
| Contract | `93003909` |
| Data Provider | `urn:li:developerApplication:1592055` |
| Integration Context | `urn:li:company:1000` (REST) / `organizationId: "1000"` (gRPC) / `urn:li:organization:1000` (Kafka) |
| Fabric | `ei-ltx1` |
| Local hp-ats-integration-mt port | `28465` |
| Local talent-partner-integrations-mt port | `28288` |

### Key Entity Mappings (EI)

| Entity | ID | Notes |
|--------|----|-------|
| IntegrationApplication | `2522` | atsJobApplicationId: `yfwang-fake-application-04091600` |
| IntegrationCandidate | `8` | atsCandidateId: `yfwang-test-1` |
| HireIdentity (candidateProfile) | `30255999532` | SCC references this |
| SourcingChannel | `348946` | Contract 93003909 |
| IntegrationCandidate (simple) | `7` | atsCandidateId: `C23339` |

### Mapping Lookup Commands

```bash
# Find HP mapping by IntegrationApplication
grpcurli --dv-auth SELF -f ei-ltx1 d2://hpIntegrationEntityMappingApi \
  proto.com.linkedin.hire.integration.HpIntegrationEntityMappingApi/FindByIntegrationEntity \
  -d '{"integrationEntityUrn":{"integrationApplicationUrn":{"integrationApplicationId":"{{INT_APP_ID}}"}}}'

# Find HP mapping by IntegrationCandidate
grpcurli --dv-auth SELF -f ei-ltx1 d2://hpIntegrationEntityMappingApi \
  proto.com.linkedin.hire.integration.HpIntegrationEntityMappingApi/FindByIntegrationEntity \
  -d '{"integrationEntityUrn":{"integrationCandidateUrn":{"integrationCandidateId":"{{INT_CAND_ID}}"}}}'

# Deactivate a mapping (reset for re-testing)
grpcurli --dv-auth SELF -f ei-ltx1 d2://hpIntegrationEntityMappingApi \
  proto.com.linkedin.hire.integration.HpIntegrationEntityMappingApi/Update \
  -d '{"integrationEntityUrn":{"integrationApplicationUrn":{"integrationApplicationId":"{{INT_APP_ID}}"}},"status":"MappingStatus_INACTIVE"}'

# IP-side mapping lookup
grpcurli --dv-auth SELF -f ei-ltx1 d2://integrationEntityUrnToClientEntityUrnMappingApi \
  proto.com.linkedin.talent.partner.integrations.IntegrationEntityUrnToClientEntityUrnMappingApi/FindUrnMappingByIntegrationEntityUrn \
  -d '{"integrationEntityUrn":{"candidateUrn":{"integrationCandidateId":"{{INT_CAND_ID}}"}}}'
```

### Kafka Event Production (EI)

```bash
# Produce IntegrationEntityReadyEvent for application sync
echo '{"header":{"com.linkedin.events.EventHeader":{"memberId":0,"time":{{TIMESTAMP_MS}},"server":"","service":"kafka-tool","environment":{"string":"ei-ltx1"},"guid":"abcdefghijklmnop","treeId":null,"requestId":null,"auditHeader":{"com.linkedin.events.KafkaAuditHeader":{"time":{{TIMESTAMP_MS}},"server":"test","instance":{"string":"test"},"appName":"kafka-tool","messageId":"0123456789abcdef","auditVersion":{"int":1},"fabricUrn":{"string":"urn:li:fabric:ei-ltx1"},"clusterConnectionString":null}}}},"integrationEntityUrn":{"string":"urn:li:integrationApplication:{{INT_APP_ID}}"},"operationType":{"avro.com.linkedin.events.unifiedintegration.IntegrationEntityOperationType":"CREATE"},"integrationContext":{"string":"urn:li:organization:1000"},"dataProvider":{"string":"urn:li:developerApplication:1592055"}}' \
| kafka-tool topic produce -f ei-ltx1 -t IntegrationEntityReadyEvent -c queuing
```

**Important:** guid, treeId (if set), messageId must be exactly 16 bytes.

### Verification Commands

```bash
# Verify HPC created after application sync
curli --dv-auth SELF -f ei-ltx1 -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0' \
  "d2://hiringProjectCandidates?q=candidate&candidate=urn%3Ali%3AhireIdentity%3A{{HI_ID}}&hiringContext=urn%3Ali%3Acontract%3A93003909"

# Verify activity history items
curli --dv-auth SELF -f ei-ltx1 -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0' \
  "d2://recruitingActivityHistoryItems?q=criteria&hiringContext=urn%3Ali%3Acontract%3A93003909&candidate=urn%3Ali%3AhireIdentity%3A{{HI_ID}}&start=0&count=20"

# Verify V2 identity group associations
curli --dv-auth SELF -f ei-ltx1 -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0' \
  "d2://hireIdentitiesV2?q=relatedHireIdentity&hireIdentity=urn%3Ali%3AhireIdentity%3A{{V2_ID}}&contract=urn%3Ali%3Acontract%3A93003909"

# Verify candidate profile
grpcurli --dv-auth SELF -f ei-ltx1 d2://hireCandidateProfilesApi \
  proto.com.linkedin.hireidentityv2.HireCandidateProfilesApi/get \
  -d '{"id":"{{PROFILE_ID}}","contract":{"contractId":"93003909"}}'
```

### Espresso Data Setup (via Sceptre/REST)

```bash
# Create SCC via REST
curli --dv-auth SELF -f ei-ltx1 -X PUT -H 'Content-Type:application/json' -H 'X-RestLi-Protocol-Version:2.0.0' \
  "d2://sourcingChannelCandidateCreations/(candidate:urn%3Ali%3AhireIdentity%3A{{HI_ID}},hiringContext:urn%3Ali%3Acontract%3A93003909,sourcingChannel:urn%3Ali%3AsourcingChannel%3A(urn%3Ali%3Acontract%3A93003909%2C{{SC_ID}}))" \
  -d '{"created":{"actor":"urn:li:developerApplication:1592055","time":0},"addedToPipeline":{"actor":"urn:li:developerApplication:1592055","time":0}}'

# Partial update atsCandidates (add member match)
curli --dv-auth SELF -f ei-ltx1 -X POST -H 'X-RestLi-Method:partial_update' \
  -H 'Content-Type:application/json' -H 'X-RestLi-Protocol-Version:2.0.0' \
  "d2://atsCandidates/(atsCandidateId:{{ATS_CAND_ID}},dataProvider:urn%3Ali%3AdeveloperApplication%3A1592055,integrationContext:urn%3Ali%3Acompany%3A1000)" \
  -d '{"patch":{"$set":{"manualMatchedMember":"urn:li:member:{{MEMBER_ID}}"}}}'

# Remove member match
curli --dv-auth SELF -f ei-ltx1 -X POST -H 'X-RestLi-Method:partial_update' \
  -H 'Content-Type:application/json' -H 'X-RestLi-Protocol-Version:2.0.0' \
  "d2://atsCandidates/(atsCandidateId:{{ATS_CAND_ID}},dataProvider:urn%3Ali%3AdeveloperApplication%3A1592055,integrationContext:urn%3Ali%3Acompany%3A1000)" \
  -d '{"patch":{"$delete":["manualMatchedMember"]}}'
```

### Local Dev Testing

```bash
# Deploy to EI locally
mint deploy -f ei-ltx1

# Local grpcurli (hp-ats-integration-mt)
grpcurli --dv-auth SELF -d '...' localhost:28465 proto.com.linkedin.hire.integration.ConnectedProjectCandidateApi/ActionWriteBack

# Local grpcurli (talent-partner-integrations-mt)
grpcurli --dv-auth SELF -d '...' localhost:28288 proto.com.linkedin.talent.partner.integrations.IntegrationCandidateApi/Get
```

### Gotchas

1. **Integration context URN format differs by protocol:**
   - REST: `urn:li:company:1000`
   - gRPC: `organizationId: "1000"`
   - Kafka Avro: `urn:li:organization:1000`

2. **SCC NOT_FOUND with V1 identity** — SCC uses `candidateProfileIdentityUrn` (V2), not member V1. Use the V2 ID from the hireIdentitiesV2 group.

3. **CandidateProfile identity persists across member add/delete** — deleting `manualMatchedMember` removes member from group but the candidateProfile V2 stays.

4. **Each resync creates fresh hireIdentity IDs** — test data accumulates in EI. Deactivate mappings to reset.

5. **Avro fixed-length fields** — guid, treeId, messageId must be exactly 16 bytes (e.g., `abcdefghijklmnop`).
