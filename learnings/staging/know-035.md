---
id: know-035
track: knowledge
type: semantic
repos:
  - mcm-mt
  - hp-ats-integration-mt
tags:
  - mcm-mt
  - architecture
  - hiring-platform
  - writeback
  - automation
  - phase2
  - connected-projects
  - mental-model
severity: high
rot_rate: slow
status: active
created: "2026-04-03"
last_verified: "2026-04-03"
use_count: 0
outcome_score: 0
---

# mcm-mt Mental Model — Multi-Channel Management

## What It Is
Core HP backend owning hiring projects, candidate pipelines, and candidate state. "MCM" = Multi-Channel Management.

## Core Entities
- **HiringProject**: recruiter's hiring effort. Owns `atsPipelineUrn` (Phase 2).
- **CandidateHiringPipeline**: ordered stage list. ATS stages are non-global.
- **CandidateHiringState**: single stage, has `source` (ATS/HP) and `isGlobalState`.
- **HiringProjectCandidate**: candidate↔project association + current stage. Key: `(hiringContext, candidate, hiringProject)`.
- **HiringProjectPreference**: project-level settings incl. `atsPipelineAutomationSettings`.

## Write-Back Flow
```
Recruiter UI → ts-web BATCH_PARTIAL_UPDATE → ts-api → mcm-mt partialUpdate
  → ConnectedProjectCandidateGrpcClient.actionWriteBack() [D2: connectedProjectCandidateApi]
    → hp-ats-integration-mt → IP actionUpsert → Greenhouse
```

## ATS Automation Flow
```
InMail sent/replied → HireMessageHistory event
  → AutomatedPipelineStageTask (Brooklin consumer)
    → LiX: MCM_ATS_AUTOMATED_PIPELINE_STAGE_TASK_ENABLED (per contract)
    → If source==ATS → AtsAutomationPipelineSettingsHandler
      → Reads automation prefs → checks target AHEAD of current → moveCandidatesInProject()
    → Else → legacy HP automation (SHORTLISTED→CONTACTED→REPLIED)
```

## Key Packages
| Package | Purpose |
|---------|---------|
| `impl/resource-impl` | REST.li resources (API entry) |
| `impl/service` | Business logic (HiringProjectCandidatesServiceImpl, AtsAutomationPipelineSettingsHandler) |
| `impl/ds/client` | Downstream gRPC clients (→ hp-ats-integration-mt) |
| `impl/event-processors` | Brooklin consumers (AutomatedPipelineStageTask) |

## Architecture
- REST.li + gRPC, Espresso (`multichannelmanagement`, table `candidatehiringstatesv2`)
- Upstream: talent-solutions-api (20+ endpoints), talent-solutions-web
- Downstream: hp-ats-integration-mt (writeback), hire-identity-service
- Siblings: mcm-jobs-integration-mt, mcm-offline (reconciliation), hire-access-control

## Gotchas
1. **Silent writeback fallback**: needs LiX + source=ATS + entity mapping. Any missing = no error, no call.
2. **Error propagation**: 401/404 from mcm-mt → 500 upstream (known pain point).
3. **HPC composite key**: hiringContext = contract URN (not integration context).
4. **Automation blocks backward moves**: target must be AHEAD of current by pipeline index.
5. **Shortened URN breaks partialUpdate**: placeholder zeros fail Espresso composite key lookup.
