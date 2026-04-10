# Connected Projects Phase 2 — Project Memory

## Active Reference (use daily)
- [CLAUDE.md](../../CLAUDE.md) — Service routing table, architecture, data flow, command reference, working style
- [REFERENCE.md](../../sublime-tabs-organized/REFERENCE.md) — Verified curli/grpcurli/kafka commands (auto-updated)
- [EI_DATA_SUMMARY.md](../../EI_DATA_SUMMARY.md) — EI environment test entity IDs, stage mappings, grpcurli commands
- [HIRE_IDENTITY_INVESTIGATION.md](../../hp-ats-integration-mt/HIRE_IDENTITY_INVESTIGATION.md) — V2 identity resolution rules, V1/V2 mapping strategy

## Design Docs
- [Eng Design](../../Connected%20Projects%20Phase%202%20-%20Job%20Requisition%20Stage%20Sync%20Eng%20Design.md) — Full Phase 2 eng design (Yufei Wang)
- [IP Interface](../../IP%20Interface%20App%20Stage%20Sync%20.md) — IP upsert/export API design (Sanjana Vohra)
- [Entitlements](../../entitlement_investigation.md) — CAN_ACCESS/CAN_USE_CONNECTED_PROJECT_FEATURES grant conditions
- [Espresso KEY_TOO_LONG](../../espresso_schema_maxsize_fix.md) — History URN exceeds 150-char key limit, shortened URN workaround

## Test Data & Procedures
- [EI E2E Reference](../../EI_E2E_TESTING_REFERENCE.md) — EI entity IDs, application/candidate test data, grpcurli commands
- [ATS Reporting](../../ATS_APPLICATIONS_REPORTING_SUMMARY.md) — ATS_APPLICATIONS sourcing channel in analytics reporting
- [HP Reporting Testing](../../HP_REPORTING_USAGE_TESTING.md) — hp_reporting_usage Spark job testing process

## Tracking
- [Phase 2 TODOs](../../phase2_todo_notes.md) — Automation settings, ramp strategy, failure list, notifications

## Feedback
- [Check knowledge BEFORE trial-and-error](feedback_check_knowledge_first.md) — Search learnings/memory files before attempting unfamiliar operations
- [Parallel debugging agents](feedback_parallel_debugging.md) — Spawn parallel agents for cross-service debugging (HP/IP/mcm-mt)
- [Plugin auto-trigger rules](feedback_plugin_triggers.md) — When to proactively invoke LinkedIn plugin skills

## Dev Process
- [Dev Process](dev_process.md) — PR descriptions, rdev deployment, Avro schema forward-compatibility
- [Espresso Schema Workflow](espresso_schema_workflow.md) — Schema change workflow for talent-partner-integrations-mt
- [InLogs](inlogs.md) — Kusto query patterns for hp-ats-integration-mt
- [Greenhouse API](greenhouse_api.md) — Full Harvest API reference, sandbox credentials, webhook events
- [Oncall Knowledge](oncall_knowledge.md) — Deployment commands, EKG, ACLs, dashboards, shell hosts

## Reference
- [IP Sync Cadence](ip_sync_cadence_throttle.md) — IP throttled GH sync: stages 1hr, apps 15min, webhooks disabled
- [Sandbox 2 LiX](sandbox2_lix_config.md) — TReX experiment IDs for Greenhouse Sandbox 2 (contract 2043270072)

## Worklogs (historical)
- [ExportStatus E2E](../../worklog_export_status_processor_e2e_2026-03-13.md) — ExportStatusEventProcessor prod testing (Mar 13, done)
- [Phase 2 Processor E2E](../../worklog_phase2_processor_testing_2026-03-15.md) — ApplicationStageProcessor SUCCESS path testing (Mar 15-19, done)
- [PR #584 E2E](pr584_e2e_testing.md) — IP schema change E2E testing for HiringProjectCandidateHistoryUrn

## Insights (from this session, 2026-04-09)
- [Insights Report](insights_april_2026.md) — Top friction patterns from 32-session analysis
- **Identity group pagination**: `findByRelatedHireIdentity` default page size (~15) truncates member identity → PR #557
- **Search index delay**: HireCandidateProfile CDC only fires on Espresso write — if profile unchanged during re-sync, no CDC → no search update
- **hire-identity-service errors**: `fetchPrimaryHireIdentityMap` errors on 15+ member groups (5,419 errors/day for contract 2011455851)
- **curli for associations**: RestLiAssociation finders need v1 protocol (no v2 header) — see know-050
