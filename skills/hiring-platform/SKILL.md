---
description: |-
  Check Hiring Platform (HP) Connected Project data for Phase 2.
  Use when the user wants to query HP entities like ConnectedProjects, HpIntegrationEntityMappings,
  HpIntegrationStageMappings, HiringProjects, CandidateHiringStates, CandidateHiringPipelines,
  HiringProjectCandidates, or trigger write-back operations.
  Covers hp-ats-integration-mt, mcm-mt, and hire-access-control services.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - execute_kusto_query
inputs:
  - action:
      description: "Action: connected-project, create-connected-project, trigger-sync, rsc-connections, default-owner, writeback, entity-mapping-by-integration, entity-mapping-by-hiring, stage-mapping, hiring-project, candidate-hiring-state, create-ats-state, pipeline, project-candidates, sourcing-candidates, euler-request"
      example_value: "connected-project"
  - id:
      description: "The entity ID to query"
      example_value: "1386691241"
  - contract:
      description: "Contract ID"
      example_value: "2011455851"
  - fabric:
      description: "Fabric (default: prod-lva1)"
      example_value: "prod-lva1"
---

# Hiring Platform (HP) - Connected Projects APIs

Query HP services for Connected Projects Phase 2 debugging and testing.

**Services**:
- `hp-ats-integration-mt` — Connected Project orchestration, entity mappings, write-back
- `mcm-mt` — HiringProject, CandidateHiringState, CandidateHiringPipeline, HiringProjectCandidate
- `hire-access-control` — HiringProjectPreference, entitlements

**Proto package**: `proto.com.linkedin.hire.integration` (hp-ats-integration-mt)
**Source repo**: `linkedin-multiproduct/hp-ats-integration-mt`

---

## 1. ConnectedProjectsApi (hp-ats-integration-mt)

D2 URI: `d2://connectedProjectsApi`

Methods: **Create**, **BatchCreate**, **Get**, **ActionTriggerSync**, **ActionGetRscConnections**, **ActionGetDefaultOwner**, **ActionBootstrapForAutoSync**

### connected-project — Get by HiringProject + IntegrationJobRequisition
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://connectedProjectsApi \
  proto.com.linkedin.hire.integration.ConnectedProjectsApi/Get \
  -d '{"key":{"hiringContext":"urn:li:contract:{{contract}}","id":{{id}}},"integrationJobRequisitionUrn":{"integrationJobRequisitionId":"JOB_REQ_ID"},"viewerSeatUrn":{"seatId":"SEAT_ID"}}'
```

### create-connected-project — Create a connection
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://connectedProjectsApi \
  proto.com.linkedin.hire.integration.ConnectedProjectsApi/Create \
  -d '{"value":{"hiringProjectUrn":{"hiringContext":"urn:li:contract:{{contract}}","id":{{id}}},"integrationJobRequisitionUrn":{"integrationJobRequisitionId":"JOB_REQ_ID"},"ownerSeatUrn":{"seatId":"SEAT_ID"},"contractUrn":{"contractId":"{{contract}}"},"integrationJobRequisitionStageUrns":[{"integrationJobRequisitionStageId":"STAGE_ID"}],"atsPipelineAutomationSettings":{"inmailSentAutomation":{"isEnabled":true,"integrationJobRequisitionStageUrns":[{"integrationJobRequisitionStageId":"TARGET_STAGE"}]}}},"actorSeatUrn":{"seatId":"SEAT_ID"}}'
```

### trigger-sync — Trigger entity sync for a connected project
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://connectedProjectsApi \
  proto.com.linkedin.hire.integration.ConnectedProjectsApi/ActionTriggerSync \
  -d '{"hiringProjectUrn":{"hiringContext":"urn:li:contract:{{contract}}","id":{{id}}},"actorSeatUrn":{"seatId":"SEAT_ID"}}'
```

### rsc-connections — Get RSC connections (data providers) for a contract
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://connectedProjectsApi \
  proto.com.linkedin.hire.integration.ConnectedProjectsApi/ActionGetRscConnections \
  -d '{"contractUrn":{"contractId":"{{contract}}"},"viewerSeatUrn":{"seatId":"SEAT_ID"}}'
```

### default-owner — Get default owner seat for a job requisition
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://connectedProjectsApi \
  proto.com.linkedin.hire.integration.ConnectedProjectsApi/ActionGetDefaultOwner \
  -d '{"integrationJobRequisitionUrn":{"integrationJobRequisitionId":"JOB_REQ_ID"},"viewerSeatUrn":{"seatId":"SEAT_ID"},"contractUrn":{"contractId":"{{contract}}"}}'
```

### ConnectedProject Data Model

| Field | Type | Description |
|---|---|---|
| `hiringProjectUrn` | HiringProjectUrn | HP project (primary key) |
| `integrationJobRequisitionUrn` | IntegrationJobRequisitionUrn | Linked ATS job req |
| `ownerSeatUrn` | SeatUrn | Connection owner |
| `contractUrn` | ContractUrn | Associated contract |
| `useExistingProjectMetadata` | bool | Reuse existing project metadata |
| `syncProjectWithRequisitionEnabled` | bool | Auto-sync with ATS req changes |
| `atsPipelineAutomationSettings` | AtsPipelineAutomationSettings | Automation rules |
| `integrationJobRequisitionStageUrns` | repeated IntegrationJobRequisitionStageUrn | Selected ATS stages |

### AtsPipelineAutomationSettings

| Field | Type | Description |
|---|---|---|
| `inmailSentAutomation` | AtsPipelineAutomationRule | Move candidate when InMail sent |
| `inmailReplyAutomation` | AtsPipelineAutomationRule | Move candidate when InMail replied |
| `lihaEvalAutomationExclusion` | AtsPipelineAutomationRule | Exclude stages from LiHA evaluation |

Each `AtsPipelineAutomationRule` has:
- `isEnabled` (bool)
- `integrationJobRequisitionStageUrns` (repeated) — target stages

### Connected Project Creation Flow (10 Steps)

1. ts-web calls middleware `/talentIntegrationJobRequisitionStages` to fetch ATS stages (populates dropdown)
2. ts-web calls ts-api `/talentConnectedProjects getAtsPipelineAutomationSuggestions(HiringProjectUrn, IntegrationJobRequisitionUrn)`
3. ts-api calls hp-ats-integration-mt `/hpIntegrationStageMappingApi findOrCreateByJobRequisition(IntegrationJobRequisitionUrn, ContractUrn)`
4. hp-ats-integration-mt checks HiringPlatformIntegrationDB; if no mappings → calls talent-copilot-service `/processStageMappingApi` for LLM-based mapping → stores result
5. Returns suggestions to frontend
6. User selects automation settings, ts-web calls `/talentConnectedProjects create`
7. ts-api calls hp-ats-integration-mt `/connectedProjectsApi create`
8. **NEW**: hp-ats-integration-mt gets all stages from IP, creates entity mappings (CandidateHiringStateUrn ↔ IntegrationJobRequisitionStageUrn) in IP
9. **NEW**: Creates CandidateHiringPipeline with one **non-global** CandidateHiringState per ATS stage; stores as `atsPipelineUrn` on HiringProject
10. **NEW**: Stores `atsPipelineAutomationSettings` in HiringProjectPreference (hire-access-control)

---

## 2. ConnectedProjectCandidateApi (hp-ats-integration-mt)

D2 URI: `d2://connectedProjectCandidateApi`

Methods: **ActionWriteBack**

### writeback — Move candidate between ATS stages
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://connectedProjectCandidateApi \
  proto.com.linkedin.hire.integration.ConnectedProjectCandidateApi/ActionWriteBack \
  -d '{"actorSeat":{"seatId":"SEAT_ID"},"hiringProjectCandidateUrn":{"hiringProjectUrn":{"hiringContext":"urn:li:contract:{{contract}}","hiringProjectId":"{{id}}"},"hireIdentityUrn":{"hireIdentityId":"HI_ID"}},"previousState":{"hiringContext":"urn:li:contract:{{contract}}","candidateHiringStateId":"PREV_STATE"},"targetState":{"hiringContext":"urn:li:contract:{{contract}}","candidateHiringStateId":"TARGET_STATE"},"historyItemId":0}'
```

Response includes `status` (google.rpc.Status) and `requestId` (int64) for tracking.

---

## 3. HpIntegrationEntityMappingApi (hp-ats-integration-mt)

D2 URI: `d2://hpIntegrationEntityMappingApi`

Methods: **FindByIntegrationEntity**, **FindByHiringEntity**, **Update**

HP's own entity mapping store (separate from IP's URN mapping). Maps HP entities ↔ IP entities with contract, data provider, and status.

### entity-mapping-by-integration — Find by IP entity
```bash
# By IntegrationJobRequisition
grpcurli --dv-auth SELF -f {{fabric}} d2://hpIntegrationEntityMappingApi \
  proto.com.linkedin.hire.integration.HpIntegrationEntityMappingApi/FindByIntegrationEntity \
  -d '{"integrationEntityUrn":{"integrationJobRequisitionUrn":{"integrationJobRequisitionId":"{{id}}"}},"status":"MappingStatus_ACTIVE"}'

# By IntegrationApplication
grpcurli --dv-auth SELF -f {{fabric}} d2://hpIntegrationEntityMappingApi \
  proto.com.linkedin.hire.integration.HpIntegrationEntityMappingApi/FindByIntegrationEntity \
  -d '{"integrationEntityUrn":{"integrationApplicationUrn":{"integrationApplicationId":"{{id}}"}},"status":"MappingStatus_ACTIVE"}'

# By IntegrationJobRequisitionStage
grpcurli --dv-auth SELF -f {{fabric}} d2://hpIntegrationEntityMappingApi \
  proto.com.linkedin.hire.integration.HpIntegrationEntityMappingApi/FindByIntegrationEntity \
  -d '{"integrationEntityUrn":{"integrationJobRequisitionStageUrn":{"integrationJobRequisitionStageId":"{{id}}"}},"status":"MappingStatus_ACTIVE"}'

# By IntegrationApplicationStage
grpcurli --dv-auth SELF -f {{fabric}} d2://hpIntegrationEntityMappingApi \
  proto.com.linkedin.hire.integration.HpIntegrationEntityMappingApi/FindByIntegrationEntity \
  -d '{"integrationEntityUrn":{"integrationApplicationStageUrn":{"integrationApplicationStageId":"{{id}}"}},"status":"MappingStatus_ACTIVE"}'
```

### entity-mapping-by-hiring — Find by HP entity
```bash
# By HiringProject
grpcurli --dv-auth SELF -f {{fabric}} d2://hpIntegrationEntityMappingApi \
  proto.com.linkedin.hire.integration.HpIntegrationEntityMappingApi/FindByHiringEntity \
  -d '{"hiringEntityUrn":{"hiringProjectUrn":{"hiringContext":"urn:li:contract:{{contract}}","id":{{id}}}}}'

# By SourcingChannelCandidate
grpcurli --dv-auth SELF -f {{fabric}} d2://hpIntegrationEntityMappingApi \
  proto.com.linkedin.hire.integration.HpIntegrationEntityMappingApi/FindByHiringEntity \
  -d '{"hiringEntityUrn":{"sourcingChannelCandidateUrn":{"sourcingChannelUrn":{"hiringContext":"urn:li:contract:{{contract}}","sourcingChannelId":SC_ID},"hireIdentityUrn":{"hireIdentityId":HI_ID}}},"status":"MappingStatus_ACTIVE"}'

# By CandidateHiringState
grpcurli --dv-auth SELF -f {{fabric}} d2://hpIntegrationEntityMappingApi \
  proto.com.linkedin.hire.integration.HpIntegrationEntityMappingApi/FindByHiringEntity \
  -d '{"hiringEntityUrn":{"candidateHiringStateUrn":{"hiringContext":"urn:li:contract:{{contract}}","candidateHiringStateId":"STATE_ID"}}}'
```

### HpIntegrationEntityMapping Data Model

| Field | Type | Description |
|---|---|---|
| `integrationEntityUrn` | IntegrationEntityUrn (oneof) | IP side entity |
| `dataProvider` | DeveloperApplicationUrn | ATS data provider |
| `integrationContext` | OrganizationUrn | ATS org |
| `hiringEntityUrn` | HiringEntityUrn (oneof) | HP side entity |
| `contractUrn` | ContractUrn | Contract |
| `integrationEntityType` | IntegrationEntityType | Entity type enum |
| `status` | MappingStatus | `MappingStatus_ACTIVE`, `MappingStatus_INACTIVE` |

---

## 4. HpIntegrationStageMappingApi (hp-ats-integration-mt)

D2 URI: `d2://hpIntegrationStageMappingApi`

Methods: **findByContract**, **update**

Maps raw ATS stage names → CandidateHiringState URNs (used for LLM-backed stage mapping suggestions).

### stage-mapping — Find stage mappings for a contract
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://hpIntegrationStageMappingApi \
  proto.com.linkedin.hire.integration.HpIntegrationStageMappingApi/findByContract \
  -d '{"contractUrn":{"contractId":"{{contract}}"}}'
```

### HpIntegrationStageMapping Data Model

| Field | Type | Description |
|---|---|---|
| `contractUrn` | ContractUrn | Contract |
| `candidateHiringStateUrn` | CandidateHiringStateUrn | HP stage |
| `rawStage` | string | Raw ATS stage name |

---

## 5. MCM-MT APIs (Hiring Platform Core)

### hiring-project — Get HiringProject with fields (REST)
```bash
curli --dv-auth SELF -f {{fabric}} \
  "d2://hiringProjects?ids=List((hiringContext:urn%3Ali%3Acontract%3A{{contract}},id:{{id}}))&fields=id,name,atsPipelineUrn,owner,sourcingChannels" \
  -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0'
```

### Set atsPipelineUrn on HiringProject (gRPC)
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://hiringProjectsGrpc \
  proto.com.linkedin.hire.HiringProjectsService/partialUpdate \
  -d '{"id":{"key":{"hiringContext":"urn:li:contract:{{contract}}","id":{{id}}}},"input":{"atsPipelineUrn":{"hiringContext":"urn:li:contract:{{contract}}","candidateHiringPipelineId":PIPELINE_ID}},"actor":"urn:li:seat:0"}'
```

### candidate-hiring-state — Get CandidateHiringState (REST)
```bash
curli -X GET --dv-auth SELF -f {{fabric}} \
  "d2://candidateHiringStates/(hiringContext:urn%3Ali%3Acontract%3A{{contract}},id:STATE_ID)" \
  -H 'X-RestLi-Protocol-Version:2.0.0'
```

### create-ats-state — Create ATS CandidateHiringState (gRPC)
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://localCandidateHiringStatesApi \
  proto.com.linkedin.hire.LocalCandidateHiringStatesApi/create \
  -d '{"value":{"hiringContext":"urn:li:contract:{{contract}}","statusType":"HireStatusType_SHORTLISTED","customName":"Stage Name","nameCustomized":true,"source":"CandidateHiringStateSource_ATS","sortOrder":1,"hidden":false,"associatedRules":[],"created":{"actor":"urn:li:seat:SEAT","time":"0"},"lastModified":{"actor":"urn:li:seat:SEAT","time":"0"}},"actorSeatUrn":{"seatId":0}}'
```

### pipeline — Get CandidateHiringPipeline (REST)
```bash
curli --dv-auth SELF -f {{fabric}} \
  "d2://candidateHiringPipelines/(hiringContext:urn%3Ali%3Acontract%3A{{contract}},id:PIPELINE_ID)" \
  -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0'
```

### Move HPC to a specific stage (REST partial_update)
```bash
curli "d2://hiringProjectCandidates/(hiringContext:urn%3Ali%3Acontract%3A{{contract}},hiringProject:urn%3Ali%3AhiringProject%3A%28urn%3Ali%3Acontract%3A{{contract}}%2C{{id}}%29,candidate:urn%3Ali%3AhireIdentity%3AHI_ID)" \
  -X POST -H 'Accept:application/json' -H 'Content-Type:application/json' \
  -H 'X-RestLi-Protocol-Version:2.0.0' -H 'X-RestLi-Method:partial_update' \
  -d '{"patch":{"$set":{"candidateHiringState":"urn:li:candidateHiringState:(urn:li:contract:{{contract}},STATE_ID)"}}}' \
  -f {{fabric}} --dv-auth SELF
```

### project-candidates — List HiringProjectCandidates (REST)
```bash
curli --dv-auth SELF -f {{fabric}} \
  "d2://hiringProjectCandidates?q=hiringProject&hiringContext=urn%3Ali%3Acontract%3A{{contract}}&hiringProject=urn%3Ali%3AhiringProject%3A%28urn%3Ali%3Acontract%3A{{contract}}%2C{{id}}%29&count=100" \
  -H 'Accept:application/json' -H 'X-RestLi-Protocol-Version:2.0.0'
```

### sourcing-candidates — List SourcingChannelCandidates (REST)
```bash
curli --dv-auth SELF -f {{fabric}} --pretty-print \
  "d2://sourcingChannelCandidates?q=candidateSourcingChannel&sourcingChannel=urn%3Ali%3AsourcingChannel%3A%28urn%3Ali%3Acontract%3A{{contract}}%2CSC_ID%29&viewer=urn%3Ali%3Aseat%3ASEAT_ID"
```

---

## 6. Euler HireEntityRequest Store

### euler-request — Get write-back request from Euler store
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://ManagedEntityCrudHireEntityRequest \
  proto.com.linkedin.euler.managed.EulerEntityTestApi/get \
  -d '{"key":{"entityType":"HireEntityRequest","urn":"{\"requestId\": {{id}}}"},"actor":{"member":{"memberId":12345}}}'
```

### euler-request-create — Create HireEntityRequest directly (for testing)
```bash
grpcurli --dv-auth SELF --fabric {{fabric}} -d '{
  "entityType": "HireEntityRequest",
  "actor": {"member": {"memberId": 12345}},
  "value": {
    "value": "{\"requestId\":{\"requestId\":REQUEST_ID},\"hiringProjectUrn\":{\"hiringContext\":\"urn:li:contract:CONTRACT\",\"hiringProjectId\":PROJECT_ID},\"candidate\":{\"hireIdentityId\":HI_ID},\"status\":\"HireEntityRequestStatus_PENDING\",\"type\":\"HireEntityRequestType_HIRING_PROJECT_CANDIDATE\",\"hiringProjectCandidateRequestDetails\":{\"candidate\":{\"hireIdentityId\":HI_ID},\"targetPipelineStateValue\":{\"hiringContext\":\"urn:li:contract:CONTRACT\",\"candidateHiringStateId\":TARGET_STATE},\"previousPipelineStateValue\":{\"hiringContext\":\"urn:li:contract:CONTRACT\",\"candidateHiringStateId\":PREV_STATE}},\"isDismissed\":false,\"createdBy\":{\"seatId\":SEAT_ID}}"
  }
}' d2://ManagedEntityCrudHireEntityRequest proto.com.linkedin.euler.managed.EulerEntityTestApi/create
```

**Notes:**
- The `value.value` field is a **JSON string** (escaped JSON inside JSON)
- `requestId` must be unique — use a large number to avoid collisions
- `status` options: `HireEntityRequestStatus_PENDING`, `HireEntityRequestStatus_FAILURE`, `HireEntityRequestStatus_FAILURE_WITH_TIMEOUT`, `HireEntityRequestStatus_COMPLETED`
- Useful for E2E testing: create a PENDING request, then fire a Kafka event to test the processor

---

## Entity Relationships (HP Side)

```
HiringProject (mcm-mt)
  ├── atsPipelineUrn → CandidateHiringPipeline (ATS stages pipeline)
  │                      └── has states → CandidateHiringState (source=ATS, non-global)
  ├── has many → HiringProjectCandidate
  │                └── has history → HiringProjectCandidateHistory
  └── has many → SourcingChannelCandidate

ConnectedProject (hp-ats-integration-mt)
  ├── hiringProjectUrn → HiringProject
  ├── integrationJobRequisitionUrn → IntegrationJobRequisition (IP)
  ├── atsPipelineAutomationSettings → automation rules
  └── integrationJobRequisitionStageUrns → selected ATS stages

HpIntegrationEntityMapping (hp-ats-integration-mt)
  ├── integrationEntityUrn (IP) ↔ hiringEntityUrn (HP)
  ├── Maps: IntegrationJobRequisition ↔ HiringProject
  ├── Maps: IntegrationApplication ↔ SourcingChannelCandidate
  ├── Maps: IntegrationCandidate ↔ HireIdentity
  ├── Maps: IntegrationJobRequisitionStage ↔ CandidateHiringState
  └── Maps: IntegrationApplicationStage ↔ HiringProjectCandidateHistory

HpIntegrationStageMapping (hp-ats-integration-mt)
  └── rawStage (ATS stage name) → candidateHiringStateUrn (HP stage)
```

## Data Sync Pipeline (Inbound: ATS → HP)

### Kafka Event: IntegrationEntityReadyEvent

Published by IP, consumed by hp-ats-integration-mt. Drives all inbound data sync.

| Field | Description |
|---|---|
| `integrationUrn` | e.g., `urn:li:integrationRequisition:123` |
| `entityType` | `JOB_REQUISITION`, `APPLICATION`, `CANDIDATE`, `APPLICATION_STAGE`, etc. |
| `operationType` | `SYNC` (bootstrap) or `UPDATE` (continued sync) |
| `integrationContext` | `urn:li:organization:ORG_ID` |
| `dataProvider` | `urn:li:developerApplication:APP_ID` |

**Partition key**: `[integrationContext + dataProvider]` — ensures ordered processing per org+ATS.

```bash
# Produce IntegrationEntityReadyEvent (EI)
cat EVENT_FILE | kafka-tool topic produce -f ei-ltx1 -t IntegrationEntityReadyEvent -c tracking

# Produce IntegrationEntityReadyEvent (Prod)
kafka-tool topic produce -f prod-ltx1 -t IntegrationEntityReadyEvent -c queuing

# Check consumer offset
kafka-tool offset get -g hpAtsIntegrationMt-integrationEntityReadyEvent-consumer --cluster queuing -t IntegrationEntityReadyEvent -f prod-lor1
```

### Sync Flows

**Manual Connect** (user-initiated):
1. ts-web → ts-api `/talentConnectedProjects create()`
2. ts-api → hp-ats-integration-mt `ConnectedProjectsApi/Create`
3. hp-ats-integration-mt: get requisition from IP, transform, create/update HiringProject in mcm-mt, store entity mapping, trigger child sync
4. IP enqueues IntegrationEntityReadyEvent per child entity (parent→child order)
5. hp-ats-integration-mt consumer processes each event: look up mapping → get IP entity → transform → create/update HP entity

**Continued Sync** (ATS-initiated updates):
1. ATS change → IP persists → IP publishes IntegrationEntityReadyEvent (operationType=UPDATE)
2. hp-ats-integration-mt consumer: look up mapping → check RSC enabled → transform → update HP entity

**Auto Connect** (auto-sync enabled):
1. ts-api → hire-access-control `/hiringAccountPreferences partialUpdate()` (persist prefs)
2. ts-api → hp-ats-integration-mt `ConnectedProjectsApi/ActionBootstrapForAutoSync`
3. IP finds unconnected requisitions → enqueues events
4. Consumer: check pref → find similar project → create/update → store mapping → trigger child sync

**Offline Reconciliation** (mcm-offline):
1. Compare HP vs IP data offline
2. Push IntegrationEntityReadyEvent for inconsistencies
3. Consumer re-checks with online data and fixes

### Entity Dependency Order

Parent entities must be created before children. IP triggers in order:
```
IntegrationJobRequisition → IntegrationApplication → IntegrationCandidate
                          → IntegrationApplicationStage
                          → IntegrationEntityAcl (RoleAssignment)
                          → IntegrationAttachment (HiringDocument)
```

## Write-Back Flow (Outbound: HP → ATS)

1. User moves candidate to ATS stage in Recruiter (ts-web)
2. ts-api `/talentHiringProjectCandidates partialUpdate` → mcm-mt `/hiringProjectCandidates partialUpdate`
3. mcm-mt detects Connected Project → calls hp-ats-integration-mt `ConnectedProjectCandidateApi/ActionWriteBack`
4. hp-ats-integration-mt resolves HP entities → IP entities via entity mappings
5. Calls IP `IntegrationApplicationStageApi/ActionUpsert` → gets `requestId`
6. IP forwards to gateway → ATS partner API
7. Status updates via `IntegrationApplicationStageExportStatusEvent` Kafka event
8. HP can poll status via `IntegrationApplicationStageExportRequestApi/Get`

### Write-Back Rules

| Candidate Type | Can move to HP sourcing stages? | Can move to ATS stages? | Write-back triggered? |
|---|---|---|---|
| **ATS applicant** (synced from ATS) | NO (prevents out-of-sync) | YES | YES |
| **Sourced candidate** (HP-sourced) | YES | YES | YES (+ export to ATS if enabled) |

- **On write-back failure**: The state update on hiringProjectCandidate is **FAILED** — the stage change is rolled back / not recorded
- **Sourced → ATS stage**: Also triggers one-click export to ATS if setting is enabled and credits are available
- **ATS limitation**: Greenhouse does NOT support creating new stages via API

## ACL Management

### Check if caller has access to a target service resource
```bash
# Check TARGET service's ACLs and grep for CALLER
acl-tool app viewAcls {{TARGET_APP}} 2>&1 | python3 -c "
import json,sys
data = json.load(sys.stdin)
for el in data.get('elements',[]):
    text = json.dumps(el)
    if '{{CALLER_APP}}' in text:
        resource = el.get('aclDataKey',{}).get('resource','')
        scope = el.get('aclDataKey',{}).get('accessControlScopeValue','')
        print(f'  scope={scope}  resource={resource}')
"

# Example: check hp-ats-integration-mt → mcm-mt access
acl-tool app viewAcls mcm-mt 2>&1 | grep -B 5 'hp-ats-integration-mt'
```

### ACL UI (recommended for visual inspection)
```
https://aclin.nuage.prod.linkedin.com/deployments/urn%3Ali%3AdataPlatform%3AGRPC/{{TARGET_APP}}%2F{{PROTO_SERVICE_NAME}}/urn%3A...
```

### Key ACL pattern
- **Resource URN**: `urn:li:grpc:({{TARGET_APP}},{{PROTO_PACKAGE}}.{{SERVICE_NAME}})` (for gRPC)
- **Resource URN**: `urn:li:restli:{{TARGET_APP}}/{{RESOURCE_NAME}}` (for REST)
- **EI ACLs don't cover prod** — must deploy to each fabric group separately
- **Propagation**: ~15-30 min after deploy

### Phase 2 Required ACLs (hp-ats-integration-mt → mcm-mt)
| Resource | Methods | Status |
|----------|---------|--------|
| `urn:li:grpc:(mcm-mt,proto.com.linkedin.hire.HiringProjectCandidateHistoryItemApi)` | create, partialUpdate | Deployed to EI + Prod (2026-03-15) |
| `urn:li:grpc:(mcm-mt,proto.com.linkedin.hire.HiringProjectCandidatesService)` | ALL | Existing |
| `urn:li:grpc:(mcm-mt,proto.com.linkedin.hire.LocalCandidateHiringStatesApi)` | ALL | Existing |
| `urn:li:grpc:(mcm-mt,proto.com.linkedin.hire.HiringProjectsService)` | ALL | Existing |

## ATS Middleware — jobRequisitionStagesApi

### Get stage by key
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://jobRequisitionStagesApi \
  proto.com.linkedin.atsmiddleware.JobRequisitionStagesApi/get \
  -d '{"key":{"jobRequisitionId":"EXTERNAL_JOB_ID","integrationContext":{"organizationUrn":{"organizationId":"ORG_ID"}},"dataProvider":{"developerApplicationUrn":{"applicationId":"APP_ID"}},"stageId":"GH_STAGE_ID"}}'
```

### Update stage (full upsert, RequestSource_MERGED writes to DB)
```bash
grpcurli --dv-auth SELF -f {{fabric}} d2://jobRequisitionStagesApi \
  proto.com.linkedin.atsmiddleware.JobRequisitionStagesApi/update \
  -d '{"key":{"jobRequisitionId":"EXTERNAL_JOB_ID","integrationContext":{"organizationUrn":{"organizationId":"ORG_ID"}},"dataProvider":{"developerApplicationUrn":{"applicationId":"APP_ID"}},"stageId":"GH_STAGE_ID"},"value":{"stageName":"NAME","stageType":"StageType_OFFER","stageOrder":ORDER,"stageStatus":"StageStatus_ACTIVE","externalCreatedAt":"TIMESTAMP","externalLastModifiedAt":"TIMESTAMP"},"requestSource":"RequestSource_MERGED"}'
```

**RequestSource behavior (DualWritePreProcessor):**
- `RequestSource_MERGED` or LIX=CONTROL → writes to **DB only**
- `RequestSource_RAW` + LIX=ENABLED → writes to **Kafka only** (DB not touched)
- `RequestSource_RAW` + LIX=BACKFILL → writes to **DB + Kafka**

**Key fields:** `JobRequisitionStageKey` = {jobRequisitionId, integrationContext, dataProvider, stageId}. Value fields: stageName(6), stageType(7), stageOrder(8), stageStatus(9), integrationJobRequisitionStageUrn(12, auto-generated).

### Produce IntegrationEntityReadyEvent for JobRequisitionStage
```bash
# On shell host or EI (queuing cluster needs auth)
echo '{"header":{...},"integrationEntityUrn":{"string":"urn:li:integrationJobRequisitionStage:IP_STAGE_ID"},"operationType":{"avro.com.linkedin.events.unifiedintegration.IntegrationEntityOperationType":"UPDATE"},"integrationContext":{"string":"urn:li:organization:ORG_ID"},"dataProvider":{"string":"urn:li:developerApplication:APP_ID"}}' | kafka-tool topic produce -f FABRIC -c queuing -t IntegrationEntityReadyEvent
```

## Local QEI Deployment

### Full deploy sequence
```bash
mint undeploy && mint clean && mint build && mint build-cfg -f qei-ltx1 && mint deploy -f qei-ltx1 --debug-app
```

### Quick redeploy (code already built)
```bash
mint undeploy && mint build-cfg -f qei-ltx1 && mint deploy -f qei-ltx1 --debug-app
```

### Service endpoints
- gRPC: `localhost:28465`
- HTTPS admin: `localhost:28466/hp-ats-integration-mt/admin`

### Check local logs
```bash
grep "PATTERN" /export/content/lid/logs/hp-ats-integration-mt/i001/hp-ats-integration-mt.log | tail -20
```

### Verify compiled config
```bash
# After mint build-cfg, check the compiled config:
grep "PROPERTY" build/hp-ats-integration-mt/qei-ltx1/application.cfg
```

### Config property pattern (Offspring @Config)
- Factory scope: `Scope.ROOT.child("ClassName")` → config key = `ClassName.fieldName`
- Set in `config/app/hp-ats-integration-mt/groups/qei.src`
- `view.fill(Cfg.class)` reads from factory's scope prefix

## Logs

hp-ats-integration-mt logs: use `/search-inlogs` skill or Kusto directly:
- Cluster: `lilogsusprod05`
- Database: `hp-ats-integration-mt`
- Table: `hp_ats_integration_mt_logs`

## Default Fabric

Default to `prod-lva1` for hp-ats-integration-mt APIs. Use `prod-ltx1` for mcm-mt REST APIs.
