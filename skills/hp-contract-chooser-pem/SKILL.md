---
name: hp-contract-chooser-pem
description: Investigates Hiring Platform - Contract Chooser PEM availability alerts. Analyzes session count dips and availability drops starting from talent-solutions-web through talent-solutions-api-frontend, hire-access-control, hp-ep-mt, and eis-backend. Includes caller quantification, fan-out analysis, dark traffic verification, and DYCO/settings-mt failure patterns.
version: 3.0.0
triggers:
  - contract chooser pem
  - hiring platform contract chooser pem
  - contract chooser pem dip
  - contract chooser availability drop
  - contract chooser pem alert
  - investigate contract chooser pem
  - why did contract chooser availability drop
  - cap-pem-count-deviation contract chooser
  - contract chooser session count dip
  - hp contract chooser pem
---

# HP Contract Chooser PEM Investigation Skill

Execute phases in order. **Checkpoint after each phase** — present findings, wait for user confirmation.

> **Product:** Hiring Platform - Contract Chooser (Web)
> **Fabrics:** prod-lor1, prod-ltx1, prod-lva1
> **PEM Debug Dashboard:** go/pem/inlogs
> **Service Topology:** See `references/service-topology.md`

---

## PHASE 0: LOAD MCP TOOLS

Load these MCP tools using **ToolSearch**:
1. `select:mcp__captain__fetch_alert_inputs`
2. `select:mcp__captain__fetch_pem_errors`
3. `select:mcp__captain__get_server_side_top_contributors`
4. `select:mcp__captain__fetch_application_events`
5. `select:mcp__captain__fetch_incidents`
6. `select:mcp__captain__fetch_metrics_by_rrd`
7. `select:mcp__captain__kql_fetch_logs`
8. `select:mcp__captain__analyze_single_trace`
9. `select:mcp__captain__execute_kusto_query`

Verify Azure CLI token for PEM Kusto:
```bash
az account get-access-token --resource "https://inlogsprodplatform.westus2.kusto.windows.net" --query "expiresOn" -o tsv 2>/dev/null
```

---

## PHASE 1: RESOLVE INPUT AND EXTRACT PARAMETERS

### Step 1.1: Detect Input Type

| Input Pattern | Action |
|---|---|
| Observe PEM Alert URL | Call `fetch_alert_inputs` → extract start/end/fabrics/product |
| Observe Service Alert URL | Call `fetch_alert_inputs` |
| Time range / description | Parse time, default product = "Hiring Platform - Contract Chooser" |
| Incident number | Call `get_incidents` to fetch details |

### Step 1.2: Classify Alert Type

| Signal | Category |
|---|---|
| "session count", "count-deviation" | `count_deviation` |
| "availability", "< 9X%" | `availability` |
| "NPE", "NullPointerException", "global outage" | `service_failure` (see Phase 5B) |

---

## PHASE 2: SESSION COUNT CHECK [FAST PATH]

Call `fetch_metrics_by_rrd` with:
- `application` = `"samza-pem-degradation-tracking"`
- `rrd_names` = `["samza-pem-degradation-tracking/Hiring_Platform_-_Contract_Chooser-Web-totalSessionCount.rrd"]`
- 6-hour window centered on alert

**IF session count < 50 AND no 500s in FeatureDegradeEvent → LOW-TRAFFIC AMPLIFICATION (benign). Skip to Phase 9.**

---

## PHASE 3: PEM ERROR CATEGORIZATION

### Step 3.1: Query FeatureDegradeEvent

```kql
FeatureDegradeEvent
| where timestamp between (datetime({start_time}) .. datetime({end_time}))
| where productName == 'Hiring Platform - Contract Chooser'
| summarize count(), dcount(memberId), take_any(downstreamApiTreeId, 2)
    by downstreamApiEndpointPath, downstreamApiResponseCode, responseErrorType, fabric, bin(timestamp, 5m)
| order by count_ desc
| take 30
```

### Step 3.2: Query DebuggableOopsPageEvent

```kql
DebuggableOopsPageEvent
| where timestamp between (datetime({start_time}) .. datetime({end_time}))
| where productName == 'Hiring Platform - Contract Chooser'
| summarize count(), dcount(memberId), take_any(downstreamCallTreeId, 2)
    by pageKey, responseErrorType, header__auditHeader__fabricUrn, responseTraceHeaders__fabric, bin(timestamp, 5m)
| order by count_ desc
```

> **CRITICAL:** `header__auditHeader__fabricUrn` = client POP. `responseTraceHeaders__fabric` = actual serving fabric. Always check serving fabric.

### Step 3.3: Classify as Spike vs Baseline

**Baseline (always present, not incident-related):**
- `talentContractOptions` 401 (60-80/5min) — expired sessions
- `talentAuthentication` 403/307/401 — auth redirects, session expiry

**Spike (investigate):**
- Any endpoint with 500 status
- Counts significantly above baseline
- Concentrated in a single time bucket

---

## PHASE 4: CONTEXTUAL EVENTS

### Step 4.1: Fetch Events (run in parallel)

Call `fetch_application_events` for each service:
1. `talent-solutions-api-frontend`
2. `hire-access-control`
3. `hp-ep-mt`
4. `settings-mt` ← **NEW: DYCO changes here caused incident-11041 SEV0**
5. `mcm-mt`
6. `hp-mt`

Check 2 hours before alert start for:
- Deployments
- LiX ramps
- D2 config changes
- Fabric shifts (CM tickets)
- **DYCO config changes in settings-mt** ← can cause NPEs in hire-access-control

### Step 4.2: Check for Concurrent Incidents

Call `fetch_incidents` for the time window. Look for SEV incidents on overlapping services.

---

## PHASE 5: TRACE-DOWN — FOLLOW THE ERROR CHAIN

### Step 5.1: Get treeIds

Use observe-agent:
```
Search ERROR logs for talent-solutions-api-frontend in <fabric> during <dip-window>.
Filter for talentContractOptions OR talentAuthentication OR talentMe with 500 status.
Show 5 treeIds.
```

### Step 5.2: Trace Each treeId

Use `analyze_single_trace` or observe-agent to trace 2-3 treeIds through the call chain.

**Path A: talentContractOptions → hp-ep-mt → eis-backend**
```
ts-api-frontend /talentContractOptions
  → hp-ep-mt /contractsV2 (finder:activeUser)
    → ep-apps-connector-mt /epContracts
      → eis-backend /memberContractSeats ← Root cause: 503/429
```

**Path B: talentAuthentication → hp-ep-mt → eis-backend**
```
ts-api-frontend /talentAuthentication
  → hp-ep-mt /seatsV2
    → ep-apps-connector-mt /epSeats
      → eis-backend /memberContractSeats ← Same downstream
```

**Path C: talentSeats → hire-access-control → Espresso**
```
ts-api-frontend /talentSeats
  → hire-access-control /seatEntitlements
    → eis-backend (MemberContractSeatLookup) ← 429s
    → ats-middleware → Espresso (OwnerToAtsIntegrationContext) ← timeouts
```

**Trace Explorer URL:** `https://observe.prod.linkedin.com/trace-explorer/visualize?traceId=<url-encoded-treeId>&environment=prod&viewType=Tree`
(URL-encode: `+` → `%2B`, `=` → `%3D`, `/` → `%2F`. Retention ~7 days.)

---

## PHASE 5B: SETTINGS-MT / ESPRESSO SCHEMA FAILURE PATTERN [from incident-11041 SEV0]

> **When to use:** Global outage (availability < 30%), NullPointerException in hire-access-control, or `service_failure` alert category.

### Pattern: Espresso Schema Missing → settings-mt NPE → hire-access-control 500 → Global HP Outage

```
Espresso schema registry: schema version N for SettingsDB table becomes unresolvable
  → Espresso returns 400 DOCUMENT_SCHEMA_MISSING
    → settings-mt NPE in BaseStrongSchemaEspressoDataAccessor.createSettingField():1060
      → settings-mt /simpleSettings returns 500
        → hire-access-control gets 500, logs NPE (~4M errors in incident-11041)
          → ALL HP services fail (hire-access-control is universal dependency)
            → Global availability < 30%
```

### Investigation Steps:
1. **Search hire-access-control** for NPE count and stack trace:
   ```
   observe-agent: Search hire-access-control logs in <fabric> for NullPointerException during <window>. Show count per minute and stack trace.
   ```
2. **Search settings-mt** for the root cause — look for `DOCUMENT_SCHEMA_MISSING`:
   ```
   observe-agent: Search settings-mt logs in <fabric> for DOCUMENT_SCHEMA_MISSING or NullPointerException during <window>. Show which Espresso table and schema version is missing.
   ```
3. **Verify it's NOT a code deploy or DYCO change** — check settings-mt version was unchanged:
   ```
   go-status -f <fabric> -a settings-mt
   ```
4. **Identify the missing schema** — look for: `DOCUMENT_SCHEMA_MISSING, /schemata/document/<DB>/<Table>/<version>`
5. **Mitigation options:**
   - Re-register the missing schema version in Espresso
   - Rollback the Espresso groot deployment that removed/evolved the schema
   - As temporary workaround: rollback hire-access-control to reduce error volume

### Real Data from incident-11041 (2026-04-06):
- **Trigger:** Espresso schema version 9 for `SettingsDB/UserContractHiringDataControlSettings` became unresolvable at 23:27 UTC
- **Peak:** ~121K NPE-containing errors/min at 23:32 UTC
- **Total impact:** ~4M hire-access-control errors, ~607K Espresso 400s
- **NOT a DYCO change** — Rootly summary was wrong. Logs proved no code deploy, no DYCO push. It was Espresso schema registry.
- **Lesson:** Always verify incident summaries with actual log evidence.

### Why this is critical:
- hire-access-control is a **universal dependency** — it's in the call path for Contract Chooser, Pipeline, Project Home, and every other HP surface
- settings-mt → hire-access-control is a hidden dependency not in most call chain diagrams
- A single Espresso schema issue can take down ALL of Hiring Platform globally
- This is NOT a fabric-specific issue — it affects all fabrics simultaneously
- **Severity is always SEV0/SEV1** due to global impact
- `BaseStrongSchemaEspressoDataAccessor.createSettingField():1060` has no null guard — defensive coding gap

---

## PHASE 6: QUANTIFY BY CALLER [KEY PHASE — from incident-10781]

> **This phase prevents the #1 investigation mistake: assuming the PEM endpoint is the top caller.**

### Step 6.1: Group hp-ep-mt Inbound by Caller

Use observe-agent:
```
During <dip-window>, search hp-ep-mt logs in <fabric> for ALL seatsV2 and contractsV2 requests.
Group by the originating service and endpoint from the rpc-trace.
Show concrete counts per caller, sorted by volume.
```

### Step 6.2: Compare Caller Distribution

Expected top callers to hp-ep-mt during overload (from incident-10781):

| Rank | Caller | Expected % | Notes |
|------|--------|-----------|-------|
| 1 | `/talentMe` | ~53% | Every Recruiter page load — dominant amplifier |
| 2 | `voyager-api-messaging-dash` | ~22% | Non-Recruiter messaging traffic |
| 3 | `job-posting-flow-mt` | ~5% | Job posting eligibility |
| 4-N | Various endpoints | ~20% | Spread across 10+ endpoints |

**If the PEM endpoint (talentContractOptions) is < 5% of hp-ep-mt traffic, the overload is NOT caused by Contract Chooser itself — it's a victim of broader hp-ep-mt saturation.**

### Step 6.3: Identify the Real Load Source

The top caller reveals where mitigation effort should focus:
- `/talentMe` dominant → needs circuit breaker or caching at ts-api-frontend level
- `voyager-api-messaging-dash` dominant → non-HP traffic overloading HP infra, engage messaging team
- Single large contract → Espresso hot key, engage EP team

---

## PHASE 7: VERIFY DUPLICATE CALLS [from incident-10781]

> **When to use:** If you suspect call amplification (same seat/contract called multiple times per treeId).

### Step 7.1: Pick a High-Fan-Out treeId

Use observe-agent:
```
For treeId <id>, search hp-ep-mt logs during <window>.
Show ALL log lines with timestamps, hosts, seat IDs, and rpc-trace.
```

### Step 7.2: Distinguish Three Patterns

| Pattern | How to Identify | Real Duplicate? |
|---|---|---|
| **Duplicate log lines** | Same host, same nanosecond timestamp, byte-identical message | No — logging artifact |
| **Dark traffic** | rpc-trace contains "Dispatching dark request", different ts-api-frontend host | No — shadow copy |
| **Real fan-out** | Different intermediate services (mcm-mt, recruiter-search-mt, etc.) each calling seatsV2 for the same seat | Yes — architectural amplification |

### Step 7.3: Quantify Fan-Out

For notification treeIds, expect 25-49 seatsV2 calls per page load via 6+ intermediate paths. This is architectural, not a bug.

---

## PHASE 8: FABRIC VERIFICATION

### Step 8.1: Verify Serving Fabric

From Phase 3 DebuggableOopsPageEvent, compare:
- `header__auditHeader__fabricUrn` (client POP)
- `responseTraceHeaders__fabric` (actual serving fabric)

If these differ, 100% of errors may originate from a single fabric despite appearing in multiple.

### Step 8.2: Verify Canary vs Stable

```bash
go-status -f <fabric> -a <service>
```

Cross-reference error log hostnames against canary pods. **NEVER assume errors are canary-only.**

---

## PHASE 9: ROOT CAUSE DECISION TREE

```
Global outage (availability < 30%)?
  YES → Check settings-mt for DYCO changes → Phase 5B
  YES → Check hire-access-control for NPE → Phase 5B

Session count < 50?
  YES → 500 errors in FeatureDegradeEvent?
         NO  → LOW-TRAFFIC AMPLIFICATION (benign)
         YES → Proceed to full trace-down

Phase 6 shows single dominant caller?
  /talentMe (>40%) → hp-ep-mt saturation from page loads, not Contract Chooser specific
  voyager-api-messaging → Non-HP traffic overloading shared infra
  Single contract → Espresso hot key

Phase 5 trace-down shows:
  eis-backend 503 → Fabric shift overloaded lva1/ltx1 → Self-recovers
  eis-backend 429 → Espresso quota exceeded → Engage EP team
  ats-middleware timeout → Espresso timeout on OwnerToAtsIntegrationContext
  hire-access-control NPE → DYCO/settings-mt change → Phase 5B
  Errors on specific hosts only → Deployment rolling restart → Auto-recovers
```

### Root Cause Categories (by frequency)

| Category | Frequency | Key Indicator |
|----------|-----------|--------------|
| **Low-traffic amplification** | Very High | Session count < 50, only baseline errors |
| **eis-backend 503/overload** | Very High | 503 from memberContractSeats, often from fabric shift |
| **DYCO/settings-mt → NPE in hire-access-control** | Rare but SEV0 | Global outage, NPE stack trace, settings-mt change |
| **Espresso MemberContractSeatLookup 429** | High | 429 in eis-backend-war |
| **ats-middleware Espresso timeout** | High | TimeoutException on OwnerToAtsIntegrationContext |
| **ts-api deployment restart** | Medium | Errors on specific hosts, deployment event |
| **Fabric shift / maintenance** | Medium | CM ticket, traffic redistribution |
| **Espresso hot key** | Medium | SEV-level 429s, specific contract ID |

---

## PHASE 10: GENERATE REPORT

### Step 10.1: Get On-Call Contacts

Call `get_current_oncall` for the root cause service:
- **ep-foundation** — eis-backend / MemberContractSeatLookup (Crew 1035)
- **hp-backend** — mcm-mt / hp-mt (Crew 394)
- **signal-platforms** — settings-mt / DYCO (check incident-11041 for contact)

### Step 10.2: Generate Report

```markdown
## Contract Chooser PEM Investigation Report

**Time:** {time_window} | **Fabric:** {actual_serving_fabric}
**Session count:** max {max}, min {min}
**Alert category:** {availability / count_deviation / service_failure}

### Root Cause
{one-line root cause}

### Error Chain
{service call chain with error codes}

### Top Callers to hp-ep-mt (Phase 6)
| Caller | Endpoint | Error Count | % of Total |
|---|---|---|---|

### PEM Error Breakdown
| Endpoint | Status | Count | Members | Spike/Baseline |
|---|---|---|---|---|

### Traces Verified
| treeId | Path | Error | Trace Explorer |
|---|---|---|---|

### Contextual Events
{deployments, fabric shifts, lix ramps, DYCO changes, incidents}

### Impact
{oops events, unique members, duration, self-recovered?}

### Actions
- [ ] {immediate}
- [ ] {follow-up}
```

### Step 10.3: Annotate

- Annotate on `go/hp-pem`
- Update oncall worklog

---

## REFERENCE: Incident Patterns

### incident-10781 (2026-03-26) — Fabric Shift → eis-backend Overload
- Fabric shift at 1:44 PM PDT marked prod-lor1 buckets offline
- Traffic redirected to prod-lva1, overloading eis-backend/memberContractSeats
- 293 oops events, ~109 affected members, 10 min duration, self-recovered
- Key learning: `/talentMe` was 53% of hp-ep-mt load, not `talentContractOptions`
- Key learning: All 153 ltx1-labeled oops were actually served by lva1 (fabric mismatch)

### incident-11041 (2026-04-06) — Espresso Schema Missing → Global HP Outage (SEV0)
- Espresso schema version 9 for `SettingsDB/UserContractHiringDataControlSettings` became unresolvable at 23:27 UTC
- settings-mt NPE in `BaseStrongSchemaEspressoDataAccessor.createSettingField():1060` → 500 on `/simpleSettings`
- hire-access-control received 500s → ~4M NPE-containing errors, peak ~121K/min
- Global availability dropped below 30%, all 3 fabrics affected simultaneously
- **Rootly summary was wrong** — said "DYCO-related change" but logs proved: no code deploy (version 9.0.1161 unchanged), no DYCO push. Root cause was Espresso schema registry.
- Key learning: Always verify incident summaries with actual log evidence
- Key learning: `DOCUMENT_SCHEMA_MISSING` in settings-mt = immediate SEV0 risk for all HP

---

## CHANGELOG

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2026-04-07 | Added Phase 5B (DYCO/settings-mt pattern from incident-11041 SEV0), Phase 6 (quantify by caller from incident-10781), Phase 7 (duplicate call verification), fan-out analysis, dark cluster config, trace explorer URL format, `/talentMe` as top caller, incident pattern references |
| 2.0.0 | 2026-03-28 | PEM Kusto primary data source, low-traffic fast path, category-driven trace-down |
| 1.0.0 | 2026-03-20 | Initial version |
