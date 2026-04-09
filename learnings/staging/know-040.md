---
id: know-040
track: knowledge
type: semantic
repos: ['hp-ats-integration-mt', 'mcm-mt', 'talent-solutions-api', 'talent-solutions-web', 'hire-access-control', 'talent-partner-integrations-mt']
tags: ['phase2', 'connected-projects', 'system-map', 'architecture', 'frontend', 'backend', 'bug-bash', 'pipeline-sync', 'realtime', 'hireEntityRequest']
severity: critical
created: '2026-04-03'
last_verified: '2026-04-03'
use_count: 0
outcome_score: 0.0
rot_rate: medium
status: active
origin_skill: learn
---

## Context

Complete system map of Connected Projects Phase 2 combining: backend task list (50+ P0/P1 tasks across 7 services), frontend scope doc ("ATS Pipeline Sync States Scope" — 55 days, 9 tasks), ts-web component exploration, and Figma design analysis.

## Key Facts

### 9 Feature Workstreams
1. Stage Sync (inbound) — IP → hp-ats → mcm-mt CHS creation
2. Stage Move (outbound) — ts-web → ts-api → mcm-mt → hp-ats → IP → Greenhouse
3. Automation Settings — Connected Project creation + HiringProjectPreference
4. Request Tracking (HireEntityRequest) — NEW table/resource, status: PENDING→CONFIRMED/FAILED
5. Realtime + UI Updates — RequestStatusUpdateEvent → ts-web subscription → refresh
6. Notifications + Banners — Global notification (success/failed), stage banners (pending/failed count)
7. Offline Reconciliation — mcm-offline job req + app stage consistency
8. Export Sourced Candidates — HP sourced → ATS with stage info
9. Entitlements — Phase 2 feature gate in hire-access-control

### Frontend Pipeline Sync States (ts-web, 55 days)
- Task 1: Realtime subscription (15d) — IN PROGRESS, unblocks everything
- Task 2: Stage tooltip (2d) — pending icon from connectedProjectAtsApplicationInfo.latestRequest
- Task 3: Recruiter activities (5d) — Pending/Confirmed/Failed in activity feed, actor = ATS data provider
- Task 4: Profile card updates (5d) — realtime refresh on stage change
- Task 5: Review sync conflicts modal (10d) — list failed requests, retry/dismiss, batch actions
- Task 6: ATS pipeline sync CTA (3d) — failed count badge in project header → opens modal
- Task 7: ATS stage banner (5d) — pending + failed banners per stage, dismiss = update lastAccessTime
- Task 8: Global notification (5d) — success/failed notifications, batch within 15min, link to applicants or ?showAtsSyncConflicts=true
- Task 9: Import applicants banner (3d) — importing status + count

### ts-web Key Components
- `lib/pipeline-engine/addon/components/connected-project-pipeline.js` — main pipeline
- `packages/ember-ts-hp-core/addon/utils/profile-actions/move-profiles-to-state.js` — stage move function
- `test-packages/e2e-tests/specs/pipeline/profile-actions/stages.spec.js` — existing E2E test
- Key selectors: `[data-test-connected-project-pipeline]`, `[data-test-pipeline-state="<vanityName>"]`, `[data-test-pipeline-profile-count]`

### URL Patterns
- Pipeline: `/talent/hire/<projectId>/manage/<stageVanityName>`
- Applicants: `/talent/hire/<projectId>/discover/applicants`
- Sync conflicts: `/talent/hire/<projectId>/manage/all?showAtsSyncConflicts=true`

### State Machine (3 states only)
Stage move start → PENDING → CONFIRMED (success) or FAILED (error)
No Mismatch/Expired/Rejected in current scope (those are future iterations in Figma).

### Critical Path for Bug Bash
1. BE: HireEntityRequest table + resource + realtime event must be live
2. FE: Realtime subscription (Task 1) unblocks Tasks 2-8
3. Integration: ActionWriteBack → IP → Greenhouse → ExportStatusEvent → HireEntityRequest update

### Frontend Doc
"Phase 2: ATS Pipeline Sync States Scope" — Google Doc 1GwcSECwPkokrt8z_4N-rp5PF34QkWLSHNNY126RFzjQ

## When to Apply

When planning bug bash testing, debugging sync issues, understanding which service owns what, or onboarding someone to Phase 2 scope. This is the single reference for how all 7 services connect.
