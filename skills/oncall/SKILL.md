---
name: oncall
description: Master oncall workflow for HP Backend. Orchestrates the full oncall loop from ticket/alert intake through investigation, fix, deployment, worklog, and handoff. Delegates to specialized skills (/triage-alert, /hp-pipeline-pem, /deploy-check, /session-handoff) as needed.
version: 1.0.0
triggers:
  - oncall
  - oncall task
  - oncall workflow
  - start oncall
  - oncall help
---

# HP Backend Oncall Master Workflow

This skill orchestrates the full oncall loop. It dispatches to specialized skills based on the task type.

> **Oncall Guide:** go/hp-oncall
> **Primary Confluence:** https://linkedin.atlassian.net/wiki/spaces/PRT/pages/552233793
> **Worklog:** `/Users/bizhou/workspace/oncall/oncall_week_<date>_worklog.md`

---

## STEP 1: CLASSIFY THE TASK

Ask the user what they need, or detect from context:

| Input Pattern | Task Type | Dispatch To |
|---------------|-----------|-------------|
| Alert URL (observe.prod.linkedin.com) | Alert triage | **STEP 2A** |
| PEM dip / availability drop | PEM investigation | **STEP 2B** |
| CSE ticket / JIRA link | CSE investigation | **STEP 2C** |
| Deploy / release | Deployment | **STEP 2D** |
| Incident channel (#incident-XXXXX) | Incident response | **STEP 2E** |
| Samza job failed / nearline lag | Nearline fix | **STEP 2F** |
| CMON / compliance ticket | Data compliance | **STEP 2G** |
| "what's going on" / status check | Daily status | **STEP 2H** |
| End of shift | Handoff | **STEP 2I** |

---

## STEP 2A: ALERT TRIAGE

Invoke `/triage-alert <alert-url>`. The skill will:
1. Identify service, fabric, alert type
2. Check recent deployments
3. Search error logs via observe-agent
4. Check downstream dependencies
5. Compare with baseline
6. Summarize findings

After triage, proceed to **STEP 3** (Fix or Escalate).

---

## STEP 2B: PEM INVESTIGATION

Determine which PEM surface:
- **Contract Chooser** → invoke `/hp-contract-chooser-pem`
- **Pipeline** → invoke `/hp-pipeline-pem`
- **Project Create / Project Home / Project Overview / Project List** → use `/triage-alert` with PEM-specific context

After investigation, annotate on `go/hp-pem` and proceed to **STEP 3**.

---

## STEP 2C: CSE TICKET INVESTIGATION

### Standard CSE Flow (48-hour SLA from Open to Triage)

1. **Fetch the ticket**: Use `mcp__captain__get_jira_issue` with the ticket key
2. **Update status**: Set to "In Progress" via `mcp__captain__update_jira_issue`
3. **Identify the issue type**:

| Category | Common Fix | Reference |
|----------|-----------|-----------|
| Seat transfer (most frequent) | Undo script at `go/seat-transfer-script` | Google Drive folder |
| Duplicate sourcing channels | Run JMX `jobApplicationsToHiringPlatformEntitiesCreator` | — |
| Duplicate OJ contracts | Deactivate contract via curli | — |
| Project stuck in DRAFT | curli partial update project status to ACTIVE | — |
| Missing candidates after transfer | Expected — POTENTIAL_CANDIDATE/ARCHIVED states don't transfer | — |
| Data deletion (DSR) | JMX delete + GDPR exclusion list | CLAUDE.md DSR section |

4. **Investigate**: Use logs (observe-agent / inlogs), curli calls, DB queries
5. **Check master for existing fix**: `git log --grep="<keyword>" --since="30 days ago"` in relevant repos
6. **Fix or escalate**: Apply data fix or redirect to owning team
7. **Document**: Comment on ticket with findings

After resolution, proceed to **STEP 4** (Worklog).

---

## STEP 2D: DEPLOYMENT

Invoke `/deploy-check <service>` to check current state, then follow deployment process:

### Pre-Deploy Checklist
- [ ] Check `go-status -f <fabric> -a <service>` for current version
- [ ] Check EKG status — no active rollbacks
- [ ] Check CRT pauses
- [ ] For talent-agent-service: verify staging regression tests pass (#liha-quality-e2e-staging-regression-testing)
- [ ] For talent-copilot-service: run gRPC curli call in EI first

### Deploy Commands
Refer to CLAUDE.md "Deployment Process" and "D2 Update Commands" sections.

### Post-Deploy
- Monitor for 30 min (canary window 9am-2pm)
- Check EKG for rollback signals
- If first colo (prod-ltx1), nominate "All_Prod" separately for remaining colos

---

## STEP 2E: INCIDENT RESPONSE

1. **Join the incident channel** (#incident-XXXXX)
2. **Read latest messages**: Use `mcp__captain__read_slack_message` with channel permalink
3. **Assess HP impact**:
   - Are any HP services listed as impacted?
   - Check our Espresso DBs: MultichannelManagement, HireAccessControlDB, HiringPlatformActivityDB, ResumesSearchDB
   - Run Trino queries to verify data impact if needed
4. **Check deployment correlation**: Were any HP services deployed around incident start time?
5. **Communicate**: Post findings in incident channel and #hp-oncall
6. **Follow incident lifecycle**: Detect → Triage → Mitigate → Communicate → Document → Follow-up
7. **GCN procedures**: Follow `go/enterprise-gcn-guidelines` if needed

---

## STEP 2F: NEARLINE / SAMZA FIX

1. **Check job status**: `sp job status -p <product> -a <app> -f <fabric>`
2. **Check for lag**: Use observe-agent or Grafana dashboards
3. **Restart if needed**:
```bash
sp job deploy -p <product> -a <app> -v <version> -f <fabric> -i i001 \
  --job-startpoint UPCOMING --moratorium-override="Restart failed jobs" \
  --nomination-check-skipped
```
4. **For talent-agent-nearline**: Must SSH to prod shell first (`ltx1-shell07.prod.linkedin.com`)
5. **Monitor**: Check lag decreases after restart

---

## STEP 2G: DATA COMPLIANCE (CMON)

1. **Read the ticket**: Identify the dataset and purge failure type
2. **Common fixes**:
   - Annotation schema mismatch → Update DataHub annotations (see wiki)
   - Non-nullable field with non-purge key → Mark as purge key or make column nullable
   - HDFS cleanup needed → SSH to grid gateway, ksudo, hdfs dfs commands
3. **Permission issues**: Files owned by `metrics` user need metrics team help
4. **Reference**: CLAUDE.md "HDFS Access Steps" section

---

## STEP 2H: DAILY STATUS CHECK

Run in parallel:
1. **SRD availability**: Check `go/srd` / `go/hs-observe` for any surface below 99.90%
2. **Active alerts**: Use observe-agent to check alerts for all owned services
3. **Pending CSE tickets**: `mcp__captain__search_jira_issues` for open CSE tickets assigned to HP
4. **Deployment status**: `/deploy-check mcm-mt` and other services due for deploy
5. **Samza jobs**: Check for failed/lagging nearline jobs

Summarize findings for daily update.

---

## STEP 2I: HANDOFF

Invoke `/session-handoff` to generate:
- What was done
- What's pending
- Key decisions made
- Blockers
- Next steps

---

## STEP 3: FIX OR ESCALATE

### If Code Fix Needed:
1. **Check master first**: `git log --grep="<keyword>"` for existing patterns
2. **Propose minimal change**: Show diff before editing
3. **Write test first**: Ensure test fails before fix, passes after
4. **Build locally**: `mint build` or `./gradlew build`
5. **Create PR**: Include Testing Done, Curli Calls sections
6. **Monitor CI**: Fix any failures before requesting review

### If Escalation Needed:

| Team | When to Engage |
|------|----------------|
| EP team | Seat/contract/entitlement issues |
| Recruiter Experience | UI/permission/EIAM issues |
| Recruiter Search | Search-related issues |
| Jobs/EJ team | Job posting/application flow |
| Messaging team | Messaging deletion requests |
| Media infra | Attachment/resume processing |
| Samza oncall | Stream processing issues |
| Fuse team | Rate limiting issues |
| Espresso team | DB quota/hot key issues |

---

## STEP 4: UPDATE WORKLOG

After every completed task, append to the worklog:
```
### <Title>
- **Ticket/Alert**: <link>
- **Issue**: <one-line summary>
- **Root cause**: <what happened>
- **Fix**: <what was done>
- **PR**: <link if applicable>
- **Status**: <current state>
```

File: `/Users/bizhou/workspace/oncall/oncall_week_<date>_worklog.md`

---

## REFERENCE: Oncall Responsibilities Quick Reference

### Primary Oncall
- CSE ticket triage (48hr SLA)
- Mitigate GCNs
- Investigate & mitigate prod issues
- Monitor auto alert emails
- Restart failed Samza jobs

### Secondary Oncall
- Monitor daily HP Availabilities (< 99.90% → investigate)
- Deploy MPs 9am-5pm Mon-Fri (canary 9am-2pm)
- Dependency Freshness
- Daily deployment updates
- LiX Approval for mcm-mt and ts-api
- Attend HP Availability meeting THURSDAY
