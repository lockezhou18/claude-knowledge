# Logs & Metrics Search Guide

Code tells you what SHOULD happen. Logs tell you what ACTUALLY happened.

## Tools

| Tool | What | When |
|------|------|------|
| **observe-agent** | Natural language queries for any service | First stop for quick checks |
| **kql_fetch_logs** | Direct KQL against app logs | When you need specific log queries |
| **fetch_metrics_by_rrd** | InGraphs metrics by RRD path | Session counts, availability scores |
| **analyze_single_trace** | Trace a request end-to-end by treeId | Following one request across services |
| **pb_investigate_trace_id** | Captain's trace playbook (more guided) | When analyze_single_trace needs more structure |
| **fetch_pem_errors** | PEM availability and error data | User-facing error breakdown |
| **pb_investigate_pem_alert** | Captain's PEM playbook (may be more current) | PEM alerts — try alongside our /hp-pipeline-pem |
| **get_server_side_top_contributors** | PEM top error contributors by endpoint | Which endpoint/service is causing the dip |
| **analyze_iris_alerts** | Iris alert analysis (pass the alert link) | When you have an Iris alert URL |
| **fetch_grafana_dashboard_panels** | Read Grafana dashboard panels | Service-specific metrics visualization |
| **read_grafana_dashboard** | Read full Grafana dashboard | When you need the complete dashboard |
| **fetch_slo_data** | SLO status | Checking if SLOs are breached |
| **fetch_call_graph** | Service dependency graph | Understanding which services call which |
| **fetch_application_events** | Deploys, LiX ramps, config changes | Correlating changes with errors |
| **fetch_incidents** | SEV incidents | Checking if a known incident overlaps |
| **execute_trino_query** | Trino SQL against Holdem cluster | Querying Espresso CDC tables, HDFS data, GDPR impact |
| **get_table_mapping_for_application** | Espresso table mappings for a service | Which tables a service reads/writes |

## Two Debugging Strategies

### Strategy A: Top-Down (PEM → TreeId → Root Cause)
Start from what the USER sees, trace down to the failing service.

```
PEM availability dip (user-facing ground truth)
  → Query PEM Kusto: FeatureDegradeEvent (categorize ALL errors)
  → Classify: spike vs chronic baseline
  → Extract treeIds per spike category
  → analyze_single_trace(treeId) per category
  → Follow error chain downstream service by service
  → Find the service that ORIGINATED the error
```

**When to use:** Oncall alerts, availability dips, "users are seeing errors."

**PEM is the ground truth** for user-facing issues. The Kusto `FeatureDegradeEvent` table shows every degradation by endpoint, status code, and fabric. Categorize first, then trace — don't trace random treeIds.

**Key queries:**
```kql
// Categorize all errors for a product/time window
FeatureDegradeEvent
| where timestamp between (datetime({start}) .. datetime({end}))
| where productName == '{product}'
| summarize count(), dcount(memberId), take_any(downstreamApiTreeId, 2)
    by downstreamApiEndpointPath, downstreamApiResponseCode, responseErrorType, fabric
| order by count_ desc

// Oops page events (user saw an error page)
DebuggableOopsPageEvent
| where timestamp between (datetime({start}) .. datetime({end}))
| where productName == '{product}'
| summarize count(), take_any(downstreamCallTreeId, 2)
    by pageKey, responseErrorType, responseTraceHeaders__fabric
| order by count_ desc
```

### Strategy B: Bottom-Up (Error → TreeId → Trace Across Services)
Start from a specific error, trace the request across service boundaries.

```
Exception/error in logs
  → Extract the treeId from the log line
  → analyze_single_trace(treeId) to see the full request path
  → Follow treeId upstream: who called this service?
  → Follow treeId downstream: what service did this call that failed?
  → Find where the error ORIGINATED in the chain
```

**When to use:** Specific errors in logs, debugging a code path, "why did this request fail?"

**TreeId is the key.** Every request gets a unique treeId that follows it across all services. One treeId = one request's complete journey.

**How to trace with treeId:**
1. **Try `analyze_single_trace` first** — gives the full span tree
2. **If trace not sampled**, fall back to KQL across service logs:
```kql
// Search for a treeId in a specific service's logs
{service}_logs
| where timestamp between (datetime({start}) .. datetime({end}))
| where treeId == '{tree_id}'
| project timestamp, level, message, exception, treeId
| order by timestamp asc
```
3. **If no logs for this treeId**, broaden to endpoint + time:
```kql
{service}_logs
| where timestamp between (datetime({start}) .. datetime({end}))
| where level == 'ERROR'
| where message contains '{endpoint_or_error_class}'
| take 20
```

### Combining Both Strategies

Most effective approach: **top-down to categorize, bottom-up to trace**
```
PEM shows availability dip
  → Categorize errors (Strategy A, Step 1)
  → Pick 1-2 treeIds per spike category
  → Trace each treeId across services (Strategy B)
  → Root cause found at the service that originated the error
```

## Critical Gotchas

### Fabric Attribution
- `header__auditHeader__fabricUrn` = **client POP** (where user connected), NOT serving fabric
- `responseTraceHeaders__fabric` = **actual backend** that served the request
- These CAN differ — user connects via ltx1 POP but served by lva1 backend
- **Always check `responseTraceHeaders__fabric`** for the real serving fabric

### Low-Traffic Amplification
- Session count < 50 + only baseline errors = low-traffic amplification (benign)
- Check session count FIRST — this is the #1 most common false alert
- No deep investigation needed for low-traffic benign alerts

### Canary vs Stable
- NEVER assume errors are canary-only
- `go-status` to check which pods have which version
- Cross-reference error hosts with deploy version

## What Logs Tell You That Code Can't
- **Actual runtime behavior**: Is this code path actually being hit? How often?
- **Error patterns**: What errors are occurring in prod right now? Spike vs baseline?
- **Timing**: When did behavior change? Correlate with deploys via `go-status` + `git log`.
- **Data flow**: What data is actually flowing through Kafka topics? What volume?
- **Dependencies**: Which services are being called? With what latency?

## When to Check Logs
```
Debugging/Incidents:  Logs → Code → Docs
Architecture:         Code → Logs (verify) → Docs
New features:         Code → Docs → Logs (baseline metrics)
Performance:          Metrics → Logs → Code
```

## Tips
- PEM data has ~28 day retention. For older alerts, use the PEM Debug Dashboard.
- `fetch_pem_errors` MCP tool uses partial data. For ground truth, use PEM Kusto directly.
- `analyze_single_trace` may return only client-side spans if server didn't sample the trace — fall back to KQL.
- When searching for an error in Slack, copy the first line of the exception — others likely pasted the same text (see slack.md).
- If you find a root cause via treeId tracing, `/learn` it with the error pattern so future incidents match immediately.
