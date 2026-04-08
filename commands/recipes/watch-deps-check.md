---
name: watch-deps-check
description: Check deployed versions of watched dependencies and surface changes since last validated
inputs: []
chain_to: investigate
chain_when: "unexpected breaking change detected in watched paths"
project: connected-project-phase2
---

## Steps

1. **Read dependency list:**
   Read `~/.claude/projects/-Users-bizhou-workspace-connected-project-phase2/watchers/dependencies.jsonl`
   Parse each entry for: `app`, `relationship`, `watch_paths`, `last_validated_version`, `notes`

2. **Check deployed version for each service dependency:**
   For each entry where `app` is not null:
   ```
   go-status -f prod-ltx1 -a {{app}}
   ```
   Extract the currently deployed version/tag.

3. **Compare against last validated version:**
   For each dependency:
   - If `last_validated_version` is null → this is the first check, record current version as baseline
   - If version unchanged → mark as "no change"
   - If version changed → proceed to step 4 for this dependency

4. **Diff changes in watched paths:**
   For changed dependencies, use `jarvis_codesearch` to search the repo for recent changes in the `watch_paths`:
   - Search for recent commits/PRs touching those paths
   - Focus on: proto changes, topic renames, API signature changes, config changes
   - Flag anything that looks like a contract change

5. **For shared-lib dependencies (no app):**
   Check if the model version in our `build.gradle` / `product-spec.json` matches what's currently available:
   ```
   grep 'model-HireEntityRequest' product-spec.json
   ```
   Compare with latest published version via version set.

6. **Write results and enforce 14-day retention:**
   Append findings to `~/.claude/projects/-Users-bizhou-workspace-connected-project-phase2/watchers/dep-changes.jsonl`:
   ```json
   {"timestamp": "ISO8601", "app": "service-name", "prev_version": "v1", "curr_version": "v2", "changes_in_watched_paths": ["summary"], "risk": "none|low|high"}
   ```
   Then trim `dep-changes.jsonl` to entries from the last 14 days only. Remove older entries.

7. **Update dependency file:**
   Update `last_validated_version` and `last_checked` in `dependencies.jsonl` for each checked dependency.

8. **Update alerts summary:**
   Rewrite `~/.claude/projects/-Users-bizhou-workspace-connected-project-phase2/watchers/alerts.md` with:
   - Last check timestamp
   - Table of all deps with current version and status
   - Any action-required items at the top

## Expected Output

```
Dependency Check — Connected Projects Phase 2

  talent-partner-integrations-mt  v2.3.45 (was v2.3.40) — 3 changes in watched paths ⚠️
    - PR #612: renamed ExportStatusEvent field
    - PR #608: new IntegrationApplication field
    - PR #605: kafka config update
  mcm-mt                          v5.1.2 (unchanged) ✅
  talent-solutions-api-frontend   v8.0.1 (was v7.9.8) — 0 changes in watched paths ✅
  hire-access-control             v3.2.0 (unchanged) ✅
  model-HireEntityRequest         v1.0.5 (unchanged) ✅
  talent-copilot-service          v1.2.0 (unchanged) ✅
```

## On Failure

- If `go-status` fails for a service → note as "unreachable", don't block other checks
- If `jarvis_codesearch` fails → fall back to noting version changed but paths not diffed
- If changes look like breaking contract changes → chain to `/investigate` with the specific change details
- If a dependency shows "BURNED BEFORE" in notes and has changes in those paths → flag as HIGH RISK
