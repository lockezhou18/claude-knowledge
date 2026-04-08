# Watch Deps — Track Upstream/Downstream Changes

Monitor changes in your dependencies and consumers. Know when the world around your code shifts.

**Usage:**
- `/watch-deps` — check what changed since last session
- `/watch-deps [service-name]` — check a specific dependency
- `/watch-deps add [repo/service]` — add a dependency to watch
- `/watch-deps list` — show all watched dependencies

## Where Dependency Config Lives

```
~/.claude/learnings/dependencies.jsonl
```

Each entry:
```json
{
  "repo": "talent-solutions-api",
  "relationship": "upstream|downstream|shared-lib|infra",
  "what_we_use": "GetCandidateHiringState gRPC endpoint",
  "what_to_watch": ["proto changes", "API contract", "deployment"],
  "last_checked": "2026-04-01",
  "contact": "ts-api-oncall@",
  "notes": "V2 migration in progress — watch for breaking changes"
}
```

## Auto-Detection

When working in a repo for the first time, scan for dependencies:
- **gRPC clients**: grep for `GrpcClient`, `@ServiceClient` → upstream services
- **Kafka consumers/producers**: grep for topic names → upstream/downstream data flows
- **Espresso tables**: grep for `@EspressoTable`, table names → data dependencies
- **REST.li clients**: grep for `@RestClient` → upstream services
- **Shared libraries**: check `product-spec.json` or `build.gradle` dependencies
- **LiX checks**: grep for `LixManager`, lix key names → feature flag dependencies

Present findings and ask user which to watch.

## Check What Changed

### For upstream services (services I call):
1. `jarvis_codesearch` or `gh api` — check recent commits to their proto/API files
2. `search_jira_issues` — any migration or breaking change tickets?
3. `search_slack` — any deployment announcements or incident threads?
4. `go-status` — what version are they running? Did they deploy recently?

### For downstream consumers (services that call me):
1. `jarvis_codesearch` — who imports my proto/client? Have they changed their usage?
2. `search_jira_issues` — any tickets about my service from other teams?
3. PEM/metrics — any change in call patterns from downstream?

### For shared libraries:
1. Check version in `product-spec.json` vs latest available
2. `search_jira_issues` — any known issues with current version?
3. Check library changelog for breaking changes between versions
4. Use `library-specs` plugin for dependency documentation

### For infra/config:
1. LiX dashboard — any ramp changes for flags I depend on?
2. Espresso schema — any pending migrations?
3. Kafka topics — any config changes, retention policy updates?

## Report

```
## Dependency Changes Since [last_checked]

### ⚠️ Action Required
- [upstream-service] deployed v2.3.1 — proto field `foo` deprecated, affects our client
- [shared-lib] released v5.0 — breaking change in retry API we use

### ℹ️ Awareness
- [downstream-service] started calling our new endpoint (first traffic seen)
- [espresso] cluster maintenance scheduled for [date]

### ✅ No Changes
- [service-a] — same version, no proto changes
- [service-b] — stable

### Suggested Actions
- "Update client for deprecated proto?" → /kickoff the migration
- "Verify our code handles the new behavior?" → /verify
- "Find how others adapted?" → /find
```

## Auto-Learn

When a dependency change causes an issue:
- Save as `/learn` with tags including the dependency name
- Link to the upstream change that caused it
- Future `/watch-deps` checks will flag similar patterns

When a dependency change is benign:
- Note it to calibrate — avoid alert fatigue on non-issues

## Integration

### At session start (via briefing):
The compound agent should check `dependencies.jsonl` and add a "Dependency Changes" section to `agent-briefing.md` if any watched deps have updates.

### Before PR creation:
If your changes affect a downstream API contract, the multi-persona reviewer should flag:
"This changes a public interface — downstream consumers should be notified."

### During /scope:
When mapping a system, auto-detect dependencies and offer to add them to the watchlist.

### During /investigate:
When debugging, check if a dependency recently changed:
"Upstream [service] deployed 2 hours ago — could be related?"
