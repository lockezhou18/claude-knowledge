---
id: know-013
track: knowledge
type: semantic
repos: [hp-ats-integration-mt]
tags: [lix, feature-flag, phase2, connected-projects, ramp]
severity: medium
created: 2026-03-31
last_verified: 2026-03-31
use_count: 0
outcome_score: 0
status: active
rot_rate: fast
---

**When** testing or debugging Phase 2 features, **verify the correct LIX is enabled for the target entity** because different features are gated by different LIX keys with different scoping (per-dataProvider vs per-contract).

## Context

### Backend LIX Keys
| LIX Key | Scope | Controls | Ramped For |
|---------|-------|----------|------------|
| `talent.connected.project.phase2.enabled` | per-dataProvider | Phase 2 branch in all processors (ApplicationStageProcessor, ExportStatusEventProcessor, etc.) | `225950754`, `223878556` |
| `talent.shortened.history.urn.mapping.key.enabled` | per-dataProvider | Shortened URN workaround for Espresso KEY_TOO_LONG | Same as above |

### Frontend LIX Keys
| LIX Key | Scope | Controls |
|---------|-------|----------|
| `talent-solutions-api.hire.entity.request.real.data.enabled` | per-request (cookie override) | Real data in `talentHireEntityRequests` API (vs mock data) |

### LIX Override Methods
- **Local service (mint deploy)**: `--ic 'Lror-<lix.key>:enabled'` in curli/grpcurli
- **Browser (frontend)**: Add `key=enabled` to `lror` cookie
- **Prod service**: LIX must be ramped via LIX dashboard (no override)

## Guidance

- Phase 2 processors check LIX at the **event processing level** using the `dataProvider` from the event. If the dataProvider isn't in the ramp list, the event falls through to Phase 1 processing (or is skipped).
- ATS notification LIX is separate — logs show "ATS stage change notification disabled by Lix" even when Phase 2 processing succeeds.
- When adding a new data provider to testing, it must be added to the LIX ramp list first.

## When to Apply

When Phase 2 code paths aren't executing despite correct events being published, or when testing with a new data provider / contract.
