---
name: hp-pipeline-pem
description: Investigates Hiring Platform - Pipeline PEM availability alerts. Analyzes availability dips and session count deviations for the Pipeline surface (change-candidate-stage, pipeline-profile-list), tracing through talent-solutions-api-frontend, mcm-mt, hp-mt, hire-access-control, and Espresso DBs to pinpoint root causes.
version: 1.0.0
triggers:
  - pipeline pem
  - hiring platform pipeline pem
  - pipeline pem dip
  - pipeline availability drop
  - pipeline pem alert
  - investigate pipeline pem
  - why did pipeline availability drop
  - pipeline session count dip
  - hp pipeline pem
  - change candidate stage errors
  - pipeline profile list errors
---

# HP Pipeline PEM Investigation Skill

This skill investigates **Hiring Platform - Pipeline** PEM availability alerts. Execute phases in order.

> **Product:** Hiring Platform - Pipeline (Web)
> **Affected Page:** `d_talent_projectsHome`
> **Key Features:** `change-candidate-stage` (61% of errors historically), `pipeline-profile-list` (37.5%)
> **Fabrics:** prod-lor1, prod-ltx1, prod-lva1
> **SLA Target:** 95% availability
> **PEM Debug Dashboard:** go/pem/inlogs

---

## PHASE 0: LOAD MCP TOOLS

Load these MCP tools using **ToolSearch**:
1. `select:mcp__captain__fetch_alert_inputs`
2. `select:mcp__captain__search_product_names`
3. `select:mcp__captain__fetch_pem_errors`
4. `select:mcp__captain__get_server_side_top_contributors`
5. `select:mcp__captain__fetch_application_events`
6. `select:mcp__captain__fetch_incidents`
7. `select:mcp__captain__fetch_metrics_by_rrd`
8. `select:mcp__captain__kql_fetch_logs`
9. `select:mcp__captain__analyze_single_trace`
10. `select:mcp__captain__execute_trino_query` (if Kusto queries needed)

---

## PHASE 1: RESOLVE INPUT AND EXTRACT PARAMETERS

### Step 1.1: Detect Input Type

**INPUT TYPE A — Observe PEM Alert URL:**
- Pattern: `observe.prod.linkedin.com/curated/application/triage/pem` or `observe.prod.linkedin.com/pem-triage`
- Action: Call **mcp__captain__fetch_alert_inputs** with the URL
- Extract: `start_time`, `end_time`, `fabrics`, `product`, `platform`

**INPUT TYPE B — Observe Service Alert URL:**
- Pattern: `observe.prod.linkedin.com/alert/{id}`
- Action: Call **mcp__captain__fetch_alert_inputs** with the URL

**INPUT TYPE C — Time Range / Description:**
- Keywords: `last`, `past`, `since`, `ago`, `pipeline dip`
- Action: Parse time, ask for fabric if not specified
- Defaults: `product = "Hiring Platform - Pipeline"`, `platform = "Web"`

---

## PHASE 2: PEM OVERVIEW — QUANTIFY THE DIP

### Step 2.1: Fetch PEM Error Summary
Call **mcp__captain__fetch_pem_errors** with:
- `product_name`: "Hiring Platform - Pipeline"
- `start_time` / `end_time` from Phase 1
- `fabrics`: all 3 prod fabrics

### Step 2.2: Produce Dip Summary Table

| Metric | Value |
|--------|-------|
| Uptime % | |
| SLA Target | 95% |
| Failure Minutes | |
| Incident Windows | |
| Members Impacted | |
| Sessions Impacted | |
| Dominant Error Type | SERVER_ERROR vs CLIENT_ERROR |

### Step 2.3: Low-Traffic Fast Path
If session count < 50 AND only baseline errors (no 500s):
- **STOP** — this is low-traffic amplification (benign)
- Report: "Low-traffic amplification. No real impact."
- Skip remaining phases

---

## PHASE 3: ERROR CATEGORIZATION

### Step 3.1: Break Down by Feature

Expected feature distribution for Pipeline:
| Feature | Typical Error Share | Service Path |
|---------|-------------------|-------------|
| **change-candidate-stage** | ~60% | tsapi → mcm-mt → hp-mt → Espresso |
| **pipeline-profile-list** | ~35% | tsapi → mcm-mt → hire-access-control → Espresso |
| **save-to-csv** | ~1% | tsapi → mcm-mt |
| **add-a-candidate** | ~1% | tsapi → mcm-mt → hp-mt |

### Step 3.2: Break Down by Error Group
- SERVER_ERROR (5xx) — backend/downstream issues
- CLIENT_ERROR (4xx) — client-side issues
- APPLICATION_ERROR — application logic failures
- UNCLASSIFIED_ERROR — unknown

### Step 3.3: Get Top Contributors
Call **mcp__captain__get_server_side_top_contributors** for the affected time window.

---

## PHASE 4: DEPLOYMENT & EVENT CORRELATION

### Step 4.1: Check Deployments (run in parallel for all services)
Call **mcp__captain__fetch_application_events** for each service in the call chain:
- `talent-solutions-api` (frontend)
- `mcm-mt` (core MCM)
- `hp-mt` (hiring platform core)
- `hire-access-control` (ACL)
- `hp-ep-mt` (entitlements)

Check for:
- Deployments within 2 hours before the dip started
- LiX ramps in the same window
- D2 config changes
- Fabric shifts

### Step 4.2: Check for Concurrent Incidents
Call **mcp__captain__fetch_incidents** for the time window to see if any related incidents were filed.

### Step 4.3: Produce Timeline
Align deployments, LiX ramps, and the PEM dip start time to identify the trigger.

---

## PHASE 4B: QUANTIFY BY CALLER [KEY PHASE — from incident-10781]

> **This phase prevents the #1 investigation mistake: assuming the PEM endpoint is the top caller of a bottleneck service.**

### Step 4B.1: Group Bottleneck Service Inbound by Caller

Use observe-agent:
```
During <dip-window>, search <bottleneck-service> logs in <fabric> for ALL inbound requests.
Group by the originating service and endpoint from the rpc-trace.
Show concrete counts per caller, sorted by volume.
```

For Pipeline, the bottleneck is typically mcm-mt or hp-mt. For seatsV2/contractsV2 issues, check hp-ep-mt.

### Step 4B.2: Identify the Real Load Source

If the PEM-triggering endpoint (e.g., change-candidate-stage) is < 10% of the bottleneck's inbound traffic, the overload is NOT Pipeline-specific — it's a broader service saturation issue.

From incident-10781 (Contract Chooser, but pattern applies):
- `/talentMe` was 53% of hp-ep-mt load (every Recruiter page load)
- `voyager-api-messaging-dash` was 22% (non-Recruiter traffic)
- The actual PEM endpoint was only 0.4%

---

## PHASE 4C: DYCO / SETTINGS-MT FAILURE PATTERN [from incident-11041 SEV0]

> **When to use:** Global outage (availability < 30%), NullPointerException in hire-access-control, or errors across ALL PEM surfaces simultaneously.

### Pattern: settings-mt DYCO Change → NPE in hire-access-control → Global HP Outage

```
settings-mt (DYCO config change)
  → hire-access-control (reads config)
    → NullPointerException (missing/null config value)
      → ALL HP services fail (hire-access-control is universal dependency)
```

### Steps:
1. Check `fetch_application_events` for `settings-mt` — look for DYCO changes within 30 min before outage
2. Search hire-access-control logs for NullPointerException via observe-agent
3. If NPE confirmed → **Mitigation:** Revert settings-mt DYCO change or rollback hire-access-control
4. **Severity is always SEV0/SEV1** — hire-access-control is in every HP call path

---

## PHASE 5: TRACE-DOWN — FOLLOW THE ERROR CHAIN

### Step 5.1: Get treeIds from Logs
Use **observe-agent** skill to search error logs:
```
Search ERROR logs for <top-contributing-service> in <fabric> during <dip-window>.
Show error breakdown by type and give me 5 treeIds.
```

### Step 5.2: Trace Each treeId
Use **mcp__captain__analyze_single_trace** or **observe-agent** to trace 2-3 treeIds through the full call chain:

**Pipeline Call Chain (change-candidate-stage):**
```
talent-solutions-web (Ember)
  → talent-solutions-api-frontend (/talentHiringProjects, /talentCandidateHiringStates)
    → mcm-mt (hiringProjectCandidates, candidateHiringStates)
      → hp-mt (hiringProjectCandidates gRPC)
        → Espresso (MultichannelManagement DB)
```

**Pipeline Call Chain (pipeline-profile-list):**
```
talent-solutions-web (Ember)
  → talent-solutions-api-frontend (/talentHiringProjects)
    → mcm-mt (hiringProjectCandidates)
      → hire-access-control (roleAssignments)
        → Espresso (HireAccessControlDB)
```

### Step 5.3: Identify Where the Error Originates
For each trace, identify:
- Which service returns the first error
- What HTTP/gRPC status code
- Whether it's a real error or a wrapped downstream error (like 400→500)

**Trace Explorer URL:** `https://observe.prod.linkedin.com/trace-explorer/visualize?traceId=<url-encoded-treeId>&environment=prod&viewType=Tree`
(URL-encode: `+` → `%2B`, `=` → `%3D`, `/` → `%2F`. Retention ~7 days.)

### Step 5.4: Verify Duplicate vs Legitimate Calls [if amplification suspected]

When you see the same resource called multiple times per treeId, distinguish three patterns:

| Pattern | How to Identify | Real Duplicate? |
|---|---|---|
| **Duplicate log lines** | Same host, same nanosecond timestamp, byte-identical | No — logging artifact |
| **Dark traffic** | rpc-trace contains "Dispatching dark request", different host | No — shadow copy |
| **Real fan-out** | Different intermediate services each calling the same downstream | Yes — architectural amplification |

D2 dark cluster config location: `config/public/lps-d2-<ClusterName>.src` in the MP repo.

---

## PHASE 6: ROOT CAUSE DECISION TREE

Based on findings from Phases 2-5:

| Pattern | Root Cause | Action |
|---------|-----------|--------|
| Deployment correlates with dip start | Bad deploy | Rollback the deployment |
| LiX ramp correlates | Feature flag issue | Revert the LiX |
| Espresso errors (quota, hot key) | DB pressure | Check WCU/RCU, engage Espresso oncall |
| Downstream service unavailable | Dependency outage | Engage dependency oncall |
| 400s wrapped as 500s | Error handling bug | Fix error propagation code |
| Dark cluster traffic | Not real impact | Annotate as dark cluster, no action |
| Fabric shift correlates | Planned maintenance | Annotate on SRD |
| Low session count + no 500s | Low-traffic amplification | No action, annotate |

---

## PHASE 7: REPORT AND ANNOTATE

### Step 7.1: Generate Report
```
## Pipeline PEM Investigation Report
- **Time Window:** <start> to <end>
- **Uptime:** X% (SLA target: 95%)
- **Members Impacted:** X / Y (Z%)
- **Sessions Impacted:** X / Y (Z%)
- **Dominant Feature:** change-candidate-stage / pipeline-profile-list
- **Root Cause:** <description>
- **Trigger:** <deployment / LiX / dependency / etc>
- **treeIds:** <list>

### Error Breakdown
| Error Type | Count | % |
|---|---|---|

### Timeline
| Time | Event |
|---|---|

### Action Items
- [ ] <immediate action>
- [ ] <follow-up action>
```

### Step 7.2: Annotate on SRD
Remind user to annotate on `go/hp-pem` with:
- Root cause
- Whether it's actionable or expected
- Link to any JIRA ticket created

### Step 7.3: Update Oncall Worklog
Append findings to `/Users/bizhou/workspace/oncall/oncall_week_<date>_worklog.md`

---

## REFERENCE: Week of 2026-03-23 Pipeline Dip (Real Investigation)

### Dip Summary
- **Uptime:** 82.37% (SLA target 95%) — FAILING
- **Duration:** 36-hour sustained degradation from 2026-03-23 08:23 UTC to 2026-03-24 20:33 UTC
- **Failure minutes:** 1,777 total (1,268 from the major window = 71%)
- **Members impacted:** 1,278 / 225,597 (0.57%)
- **Sessions impacted:** 8,265 / 2,836,891 (0.29%)
- **Total incident windows in the week:** 59

### Error Breakdown
| Error Type | Count | % |
|---|---|---|
| SERVER_ERROR | 7,292 | 74.9% |
| CLIENT_ERROR | 2,382 | 24.5% |
| UNCLASSIFIED_ERROR | 44 | 0.5% |
| APPLICATION_ERROR | 20 | 0.2% |

### Feature Breakdown
| Feature | Error Count | % |
|---|---|---|
| change-candidate-stage | 1,969 | 61.0% |
| pipeline-profile-list | 1,210 | 37.5% |
| save-to-csv | 37 | 1.1% |
| add-a-candidate | 10 | 0.3% |

### Correlated Events (2026-03-23 to 2026-03-24)
- mcm-mt deployments: 3/23 ~02:00 UTC and ~10:00 UTC
- LiX ramp: `talent.connected.project.phase2.enabled` at 3/23 10:55 UTC
- LiX ramp: `mcm.seat.transfer.sourcing.channel.copy.association.enabled` at 3/23 23:47 UTC
- talent-agent-mt deployment failed 3/23 17:17 UTC (retried successfully 3/24 01:04 UTC)

### Key Observations
- Server errors dominated (75%) — backend/downstream issue, not client-side
- `change-candidate-stage` was the primary impacted feature (61%)
- Page `d_talent_projectsHome` was the sole affected page (6,512 oops pages)
- Despite 59 incident windows, user impact was low (0.57% members) suggesting degradation hit low-traffic periods
- Ongoing instability persisted throughout the week even after the major 36hr window resolved

---

## REFERENCE: Known Pipeline Error Patterns

| Pattern | Root Cause | Frequency |
|---------|-----------|-----------|
| `change-candidate-stage` 500s spike after mcm-mt deploy | Warm-up latency or code regression | Common |
| `pipeline-profile-list` errors from hire-access-control | ACL/permission check failures | Occasional |
| Espresso WCU quota exceeded on MultichannelManagement | Large contract bulk operations | Occasional |
| GRPC migration ACL issues | D2 config changes | Rare |
| Downstream EP service unavailable | hp-ep-mt deployment or outage | Occasional |
| `responseTraceHeaders__fabric` != `header__auditHeader__fabricUrn` | PEM attributes to client POP, not serving fabric | Always verify |

## REFERENCE: Key Dashboards & Links

| Link | Purpose |
|------|---------|
| go/hp-pem | PEM dip follow-up and annotations |
| go/pem/inlogs | PEM debug dashboard (ADX) |
| go/srd | SRD availability monitoring |
| go/hs-observe | Observability dashboard |
| go/ekg | Exception information |
| go/kusto | Log investigation |
