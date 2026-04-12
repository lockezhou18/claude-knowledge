---
name: "ApplicationProcessor race condition — stage mapping missing on CREATE"
description: "When ATS applicants stuck in sourcing stage, check HPC→ApplicationStage mapping. Race: CREATE event processed before stage exists in IP."
type: project
originSessionId: 0e9b0eb1-5032-446a-81a7-04633c37b4ea
---
**When** new ATS applicants are stuck in HP sourcing stage ("potential candidate") instead of ATS stage, **check** if the HPC→ApplicationStage mapping exists **because** the IntegrationApplication CREATE event can be processed before the IntegrationApplicationStage exists in IP.

## Symptoms
- Candidates show "Save to pipeline" instead of "Change stage" in Recruiter UI
- ApplicationStageResolutionService logs "No resolved stage for HPC, skipping sync"
- HPC→ApplicationStage entity mapping is empty for the candidate

## Root Cause
ApplicationProcessor.getAllStages() returns empty when the stage hasn't been synced to IP yet (race condition, ~4 seconds). connect(null) short-circuits → no mapping. When the stage event arrives later, processPhase2() can't find the mapping → skips sync.

## Fix
PR #526: ensureApplicationStageMappingExists() before resolveAndSyncCurrentState() in processPhase2(). Zero overhead when mapping exists, creates it on the recovery path.

## Prevention
When processing Kafka events that depend on other entities, always verify the dependency exists before proceeding. Don't assume event ordering guarantees entity availability.

**Graduated from:** `~/.claude/learnings/staging/bug-002.md` (use_count=3, score=3)
