---
id: know-001
track: knowledge
repos: [hp-ats-integration-mt]
tags: [kafka, export-event, topic, ip, phase2]
severity: medium
created: 2026-03-25
last_verified: 2026-03-25
use_count: 1
outcome_score: 2
status: active
rot_rate: medium
---

**When** investigating why export status events aren't being consumed, **check** the topic name **because** IP silently migrated from `IntegrationApplicationStageExportStatusEvent` to `IntegrationExportRequestStatusEvent`.

## Context
The new topic is generic (has `requestType` field: APPLICATION_STAGE, APPLICATION_DISPOSITION). The `clientEntityUrn` moved from top-level to `requestMetadata.clientEntityUrn`. Uses standard `EventHeader` instead of `KafkaAuditHeader`.

## Key Details
- Tracking cluster with colo rerouting — each fabric's consumer uses `kafka.tracking-local`
- No cross-fabric duplicates — colo rerouting routes to one fabric
- Multiple status transitions per request (REQUEST_RECEIVED → REQUEST_AT_GATEWAY → SUCCESS/FAILURE)
- Add idempotency check: skip if HireEntityRequest already in terminal FAILURE state
