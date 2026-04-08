---
id: bug-001
track: bug
repos: [hp-ats-integration-mt]
tags: [identity, v2, mapping, writeback, phase2]
severity: high
created: 2026-03-23
last_verified: 2026-03-25
use_count: 3
outcome_score: 3
status: active
rot_rate: slow
paths: ["**/HireIdentityV2Service.java", "**/ConnectedProjectCandidateService.java"]
---

**When** ActionWriteBack fails with "No IntegrationApplicationStage mapping found" for V1 member candidates, **check** if the identity group has multiple candidate-profile V2s **because** `findCandidateProfileV2InGroup().findFirst()` picks an arbitrary V2 which may not be the one used when the entity mapping was written.

## Symptoms
- ActionWriteBack returns NOT_FOUND for V1 candidates that definitely have mappings
- Logs show "Resolved hire identity for mapping: V1=X converted to member-referenced V2=Y" but the mapping was written with a different V2

## Root Cause
`createHireIdentityV2WithHireCandidateProfile` creates a NEW candidate-profile V2 per IntegrationCandidate (not idempotent per member+contract). Same person with multiple Greenhouse candidate records → multiple V2s in one identity group → `findFirst()` picks wrong one.

## Fix
PR #524: Fast path (single V2) + fallback (try all V2s in group, skip already-tried). Filter out already-tried V2 to avoid redundant lookups.

## Prevention
When resolving identity for entity mapping lookups, never rely on `findFirst()` from an identity group. Always consider that groups can have multiple candidate-profile V2s.
