---
id: know-011
track: knowledge
type: semantic
repos: [hp-ats-integration-mt]
tags: [entity-mapping, identity, v2, phase2, connected-projects, integration]
severity: high
created: 2026-03-31
last_verified: 2026-03-31
use_count: 0
outcome_score: 0
status: active
rot_rate: slow
paths: ["**/HpIntegrationEntityMapping*", "**/EntityMappingTransformer*", "**/HireIdentityV2Service*"]
---

**When** working with entity mappings in Connected Projects Phase 2, **understand the two mapping systems and V2 identity resolution** because mapping lookup failures are the most common source of sync issues.

## Context

Two separate mapping systems exist:

### 1. HP Entity Mapping (hp-ats-integration-mt Espresso)
- API: `HpIntegrationEntityMappingApi`
- Maps: HP entity URN ↔ IP entity URN
- Written by: hp-ats-integration-mt processors during inbound sync
- Key mappings:
  - HiringProject ↔ IntegrationJobRequisition
  - SourcingChannelCandidate ↔ IntegrationApplication
  - CandidateHiringState ↔ IntegrationJobRequisitionStage
  - HiringProjectCandidate ↔ IntegrationApplicationStage (the one that races)

### 2. IP URN Mapping (talent-partner-integrations-mt Espresso)
- API: `IntegrationEntityUrnToClientEntityUrnMappingApi`
- Maps: IP entity URN ↔ client (HP) entity URN
- Written by: hp-ats-integration-mt via IP API calls
- Subject to Espresso 150-char key limit (know-002)

### V2 Identity Resolution
- HP stores candidates by V2 identity (`hireIdentityId`)
- V1 member candidates: resolved via `HireIdentitiesV2Service` → find candidate-profile V2 in group
- Multiple V2s per member possible (one per IntegrationCandidate)
- Bug-001: `findFirst()` picks wrong V2 → PR #524 added fallback to try all V2s

### TransformerContext Requirements
- `EntityMappingTransformer.toIntegrationEntity()` requires `hiringProjectUrn` in `TransformerContext`
- Without it, IP mapping metadata lacks `hiringProjectUrn` → `getMappingStatus()` returns INACTIVE
- INACTIVE mappings are filtered out → processor takes CREATE path instead of UPDATE

## Guidance

- Always verify both HP and IP mappings when debugging sync failures
- For HP mappings: `FindByHiringEntity` (HP→IP direction) or `FindByIntegrationEntity` (IP→HP direction)
- For IP mappings: `FindUrnMappingByClientEntityUrn` (HP→IP) or `FindUrnMappingByIntegrationEntityUrn` (IP→HP)
- Mapping status `ACTIVE` requires both `isActive=true` AND `hiringProjectUrn` present in metadata (for types in `TYPES_NEED_FILTER_BY_HIRING_PROJECT`)

## When to Apply

When a processor takes the CREATE path unexpectedly, or when ActionWriteBack can't find a mapping, check both mapping systems and verify V2 identity resolution.
