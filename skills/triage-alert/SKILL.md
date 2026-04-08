# Triage Alert

Quickly triage a production alert for HP services.

## Usage
`/triage-alert <alert-url-or-description>`

## Steps

1. **Identify the alert** — parse the alert URL or description to determine:
   - Service name
   - Fabric
   - Alert type (error rate, latency, availability)
   - Time window

2. **Check for global outage first** — if availability < 30% or errors across ALL HP surfaces:
   - Check `settings-mt` for DYCO changes (within 30 min before outage)
   - Check `hire-access-control` for NullPointerException
   - If NPE from DYCO → **SEV0, revert settings-mt change immediately**
   - hire-access-control is universal dependency — one NPE takes down ALL of HP
   - See `/hp-contract-chooser-pem` Phase 5B for full pattern

3. **Check recent deployments** — look for deployments to this service in the affected time window:
   ```bash
   go-status -f <fabric> -a <service>
   ```
   Use `mcp__captain__fetch_application_events` for deployment history.
   **Also check `settings-mt`** — DYCO config changes here can cascade to HP services.

4. **Search error logs** — use observe-agent:
   "Search ERROR logs for <service> in <fabric> in the last <timewindow>. Show error breakdown by type/exception with counts."

5. **Check downstream dependencies** — use observe-agent:
   "Show me dependency errors for <service> in <fabric>"

6. **Quantify by caller** — if the bottleneck is a shared service (hp-ep-mt, eis-backend):
   Use observe-agent to group inbound traffic by originating service/endpoint.
   The PEM-triggering endpoint is often NOT the top caller. In incident-10781, `/talentMe` was 53% of hp-ep-mt load while the PEM endpoint was only 0.4%.

7. **Check if errors are from dark cluster traffic** — look for `pageKey: DarkCluster-null` or `"Dispatching dark request"` in rpc-trace.
   - Dark cluster config: `config/public/lps-d2-<ClusterName>.src` in the MP repo
   - Deploy changes: `lps d2 update -f <fabric> -c <ClusterName> --bypass-canary`

8. **Verify serving fabric** — `responseTraceHeaders__fabric` (actual serving fabric) may differ from `header__auditHeader__fabricUrn` (client POP). Always check serving fabric.

9. **Compare with baseline** — use observe-agent to compare error rates before vs after the alert started.

10. **Get trace evidence** — for key treeIds:
    - Trace Explorer: `https://observe.prod.linkedin.com/trace-explorer/visualize?traceId=<url-encoded-treeId>&environment=prod&viewType=Tree`
    - URL-encode: `+` → `%2B`, `=` → `%3D`, `/` → `%2F`
    - Retention ~7 days — get evidence early

11. **Summarize findings**:
    - Root cause (or top candidates)
    - Whether it's a real issue vs dark traffic / client errors / low-traffic amplification
    - Top caller distribution (from step 6)
    - Recommended action (rollback, escalate, monitor, annotate)
    - Relevant treeIds and Trace Explorer links
