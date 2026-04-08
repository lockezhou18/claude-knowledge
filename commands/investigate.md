# Investigate — Find Root Cause

Structured investigation workflow for debugging, incident response, and "why is this broken" scenarios. Follows the hypothesis-first approach with 5 Whys until root cause is found.

**Usage:** `/investigate [symptom or problem description]`

If no argument, ask: "What's the symptom or problem you're seeing?"

## Parallel Mode (for complex incidents)

When the symptom spans multiple services or the root cause is unclear, use parallel sub-agents to test hypotheses simultaneously instead of one linear investigation:

```
Spawn 3 parallel Agent calls:

Agent 1 — Code Regression Hunt:
  Search for recent code changes in the affected service path (git log, grep for recent PRs).
  Check: did anything deploy in the last 24h that touches this code path?

Agent 2 — Log & Trace Analysis:
  Use observe-agent to search logs for error patterns, duplicate calls, or upstream failures.
  Quantify: how many errors? Which callers? What's the blast radius?

Agent 3 — Config & Deploy Correlation:
  Check LiX ramps, config changes, deployment history.
  Correlate: did any change happen at the same time as the symptom?
```

Each agent reports: (1) evidence found/not found, (2) confidence 1-5, (3) specific trace/log links.
Synthesize into a ranked root cause analysis before presenting to the user.

**When to use parallel mode:** User says "investigate" with no clear direction, or symptom involves 2+ services, or initial hypothesis was wrong.
**When to skip:** User already pointed to a specific file/service — go there directly (trust user direction).

## Step 0: Check Past Knowledge

Before investigating from scratch:
1. Read `~/.claude/learnings/agent-briefing.md` — has this been seen before?
2. Search `~/.claude/learnings/manifest.jsonl` filtering by `track: bug` + matching tags/repo/error patterns.
3. If a matching episodic insight exists, present it: "This looks similar to [bug-XXX]. Last time the root cause was X. Want to verify if it's the same issue?"
4. If no match, proceed with fresh investigation.

## Step 1: Establish the Facts

Gather concrete data before forming any hypothesis:
- **What is the exact symptom?** Error messages, log lines, metrics, user reports. Copy exact text.
- **When did it start?** Check metrics/logs for the transition point. `git log --since="X days ago"` for recent deployments.
- **What changed?** Recent PRs, deploys, config changes, upstream dependency changes.
- **What's the blast radius?** One user? One fabric? All traffic? Check canary vs stable.
- **What's the severity?** Does this need immediate action or can it be investigated methodically?

Present facts to the user before hypothesizing.

## Step 2: Form Hypotheses (at least 2-3)

Based on the facts, generate multiple hypotheses — not just the first one that comes to mind:

**Hypothesis format:**
```
H1: [what you think is happening] because [evidence that supports it]
    Disproves if: [what would prove this wrong]
    
H2: [alternative explanation] because [evidence]
    Disproves if: [what would prove this wrong]

H3: [less likely but possible] because [evidence]
    Disproves if: [what would prove this wrong]
```

**Common root cause categories** (check each):
- Recent deploy introduced a bug (check `git log`, `go-status`)
- Upstream dependency changed behavior (check dependency logs, PEM)
- Configuration drift (check config files, LiX ramps)
- Data issue (bad input, schema mismatch, null where not expected)
- Infrastructure issue (capacity, network, Espresso, Kafka lag)
- Race condition / timing issue (ordering, eventual consistency)

## Step 3: Test Hypotheses (most likely first)

For each hypothesis, define the **one check** that would confirm or disprove it:

Use available tools:
- **Logs**: Use `observe-agent` skill with pre-loaded context: include the service name, the symptom/error, and any relevant insights from the knowledge base. **Always reuse the session ID** (`--session <id>`) for multi-step investigations — the agent accumulates context across queries.
- **Metrics**: Use `fetch_metrics_by_rrd` or Grafana dashboards
- **Traces**: Use `analyze_single_trace` for specific request traces (treeId). For visual inspection: `https://observe.prod.linkedin.com/trace-explorer/visualize?traceId=<url-encoded-treeId>&environment=prod&viewType=Tree` (URL-encode: `+` → `%2B`, `=` → `%3D`). Retention ~7 days — get evidence early. See search-guides/logs-metrics.md for top-down + bottom-up strategies.
- **Code**: Read the code path — look for the business logic. Use `jarvis_codesearch` for cross-repo tracing.
- **Data**: Query Espresso/Trino for data state. Use `linkedin-framework:infra-specs-expert` for Espresso/Kafka questions — it has deep knowledge about Espresso key constraints, Kafka topic configs, D2 routing that we don't.
- **Deploys**: `go-status` for current versions (via `linkedin-cli-tools:cli-tools`), `git log` for recent changes
- **API verification**: Use `grpcurli` / `curli` (via `linkedin-cli-tools:cli-tools`) to test endpoints directly
- **UI verification**: Use `playwright-cli` to reproduce UI issues in a real browser. Open headed (`playwright-cli open --headed URL`), take snapshots/screenshots as evidence. For Greenhouse/LinkedIn, load saved auth (`playwright-cli state-load`). Chain to `/recipe ui-smoke-test` for structured checks or `/recipe capture-ui-state` for before/after evidence.
- **PEM**: Check PEM dashboards for availability dips. See search-guides/logs-metrics.md for PEM Kusto queries.
- **Broad search**: Use `unified_context_search` to search code + wiki + Slack + Jira simultaneously when unsure where to look

### Proven Investigation Techniques (from incident-10781 and incident-11041)

**Technique A: "Quantify by Caller" — run BEFORE tracing individual requests**
When a shared service is the bottleneck (hp-ep-mt, eis-backend, settings-mt), group its inbound traffic by caller before deep-diving:
```
observe-agent: During <window>, search <bottleneck-service> logs in <fabric>.
Group ALL inbound requests by originating service and endpoint from rpc-trace.
Show counts sorted by volume.
```
This prevents the #1 investigation mistake: assuming the symptom endpoint is the top caller. In incident-10781, `/talentMe` was 53% of hp-ep-mt traffic while the PEM endpoint was 0.4%.

**Technique B: "Cascading Root Cause Trace" — never stop at the first exception**
When Service A shows an NPE or 500, always ask: "What's returning the error TO this service?"
- incident-11041: hire-access-control NPE → settings-mt 500 → Espresso `DOCUMENT_SCHEMA_MISSING` → schema version 9 missing. Three levels deep.
- The Rootly summary was wrong ("DYCO-related change"). Logs proved it was an Espresso schema registry issue.
- **Rule: Always verify incident summaries with actual log evidence.**

**Technique C: "Cross-Service Single-TreeId Trace"**
Search the bottleneck service filtered by a single treeId and count how many calls it received:
```
observe-agent: For treeId <id>, search <service> logs during <window>.
Show ALL log lines with timestamps, hosts, and URIs.
```
In incident-10781, one treeId generated 49 seatsV2 calls to hp-ep-mt — evidence of architectural fan-out invisible from any single-service view.

**Technique D: "Duplicate vs Legitimate Call Verification"**
When the same resource is called multiple times per treeId, distinguish three patterns:
| Pattern | Identifier | Real duplicate? |
|---|---|---|
| Duplicate log line | Same host, same nanosecond, byte-identical | No — logging artifact |
| Dark traffic | rpc-trace contains "Dispatching dark request" | No — shadow copy |
| Real fan-out | Different intermediate services calling same downstream | Yes — architectural |

**Technique E: "Espresso Schema Missing = SEV0 Alert"**
`DOCUMENT_SCHEMA_MISSING` in a service that feeds hire-access-control or settings-mt → immediate global HP outage risk. Check: was a schema evolved, a groot deployment done, or a schema registry cache invalidated?

**Technique F: "Fabric Attribution Verification"**
`responseTraceHeaders__fabric` = actual serving fabric. `header__auditHeader__fabricUrn` = client POP. These can differ. Always check serving fabric. In incident-10781, 100% of errors labeled ltx1 were actually served by lva1.

**After each check**, update the hypothesis:
- Confirmed → proceed to Step 4
- Disproved → move to next hypothesis
- Inconclusive → refine the check, gather more data

## Step 4: Apply 5 Whys

Once you have the proximate cause, dig deeper:

```
Why 1: Why did [symptom] happen?
  → Because [proximate cause]

Why 2: Why did [proximate cause] happen?
  → Because [deeper cause]

Why 3: Why did [deeper cause] happen?
  → Because [root cause]

Why 4: Why did [root cause] exist?
  → Because [systemic issue]

Why 5: Why wasn't [systemic issue] caught?
  → Because [process gap]
```

Stop when you reach something actionable. Not every investigation needs all 5 whys.

## Step 5: Present Findings

```
## Investigation: [symptom]

### Root Cause
[What's actually wrong and why]

### Evidence
- [Log line / metric / code path that confirms]

### 5 Whys Chain
1. → 2. → 3. → ... → root cause

### Fix
- **Immediate**: [what to do right now to stop the bleeding]
- **Proper fix**: [the real fix, with PR plan]
- **Prevention**: [how to prevent recurrence — test, monitor, guard]

### Impact
- Duration: [how long was this broken]
- Scope: [who/what was affected]
- Severity: [actual customer impact]
```

## Step 6: Auto-Learn

After investigation completes, automatically run the equivalent of `/learn`:
- Save as a `bug-track` episodic insight with:
  - `situation.error_pattern`: the exact error/symptom
  - `situation.context`: what was happening
  - `resolution.steps`: the fix steps
  - `resolution.outcome`: what resolved it
- This ensures the next time someone sees the same symptom, Step 0 catches it immediately.

Tell the user: "Saved as [bug-XXX]. Next time this symptom appears, I'll recognize it."
