---
description: "Automated PR → prod pipeline. Submit code and walk away — the system handles CI, review, merge, deploy, and PEM verification via chained /wait-for steps."
user-invocable: true
allowed-tools:
  - Bash
  - CronCreate
  - CronDelete
  - Read
  - Write
  - Skill
inputs:
  - pr:
      description: "PR number or URL to ship"
      example_value: "123"
  - repo:
      description: "Repository (default: current repo)"
      example_value: "hp-ats-integration-mt"
  - fabric:
      description: "Target fabric to verify deployment (default: prod-ltx1)"
      example_value: "prod-ltx1"
  - app:
      description: "App name for go-status (default: inferred from repo)"
      example_value: "hp-ats-integration-mt"
  - skip:
      description: "Steps to skip: ci, review, deploy, pem (comma-separated)"
      example_value: "pem"
---

# Ship — Automated PR to Prod Pipeline

Submit a PR and walk away. The system chains `/wait-for` steps to monitor CI, review, deployment, and post-deploy health — all persisting across sessions.

## Usage

```
/ship 123                              # ship PR #123 in current repo
/ship 123 --skip pem                   # skip PEM verification
/ship 123 --fabric prod-lva1           # verify deploy on specific fabric
/ship https://github.com/.../pull/123  # from URL
```

## Pipeline Steps

```
Step 1: CI Check
  → /wait-for "PR CI passes" --every 5m
  → on success → Step 2
  → on failure → report which check failed, suggest /pr-fix

Step 2: Review Check
  → /wait-for "PR approved" --every 15m
  → on success → Step 3 (pause for human confirmation before merge)
  → on timeout (7 days) → remind user

Step 3: Merge (REQUIRES HUMAN CONFIRMATION)
  → Ask user: "CI passed, review approved. Merge PR #X?"
  → on confirm → merge, proceed to Step 4
  → on decline → stop pipeline

Step 4: Deploy Check
  → /wait-for "new version deployed to FABRIC" --every 10m
  → on success → Step 5
  → on timeout → suggest checking deploy queue

Step 5: PEM Verification (optional, skip with --skip pem)
  → /wait-for "PEM stable for 15min after deploy" --every 5m
  → on success → "Ship complete!"
  → on failure → "PEM dip detected — investigate?"
```

## Step 1: Parse Input

Extract from user input:
- **PR number** — from number, URL, or current branch
- **Repo** — from URL, flag, or current git remote
- **App name** — inferred from repo name (e.g., `hp-ats-integration-mt`)
- **Fabric** — default `prod-ltx1`, override with `--fabric`
- **Skip steps** — parse `--skip ci,pem` into skip set

## Step 2: Validate PR State

```bash
gh pr view {{PR_NUM}} --repo {{REPO}} --json state,title,headRefName,checks,reviews,mergeable
```

Check current state and skip already-completed steps:
- CI already passing? → skip to Step 2
- Already approved? → skip to Step 3
- Already merged? → skip to Step 4
- Already deployed? → skip to Step 5

Report starting state to user.

## Step 3: Start the Pipeline

### CI Check

```bash
gh pr checks {{PR_NUM}} --repo {{REPO}}
```

If any check is pending/failing, set up wait:
```
/wait-for "gh pr checks {{PR_NUM}} --repo {{REPO}} shows all passing" --every 5m
```

On success prompt:
```
PR #{{PR_NUM}} CI passed! All checks green.
Next: waiting for review approval. (polling every 15m)
```

On failure (check failed, not just pending): attempt auto-fix before escalating.

### CI Auto-Fix (attempt before escalating to user)

When CI fails, detect the failure type and auto-fix if possible. Only escalate to user for real code issues.

```
gh pr checks {{PR_NUM}} --repo {{REPO}} --json name,state,description,link
```

**Auto-fixable failures (fix → push → re-check, no user intervention):**

| Failure | Detection | Auto-Fix |
|---------|-----------|----------|
| **LI-Policy description check** | Check name contains `LI-Policy` or `description` | Ensure PR body has `## Summary` and `## Testing Done` headers. Read current body via `gh pr view --json body`, add missing sections, update via `gh pr edit --body` |
| **PROTOVALIDATIONOVERRIDE needed** | Error mentions "proto validation" or "backward incompatible proto" | Add `PROTOVALIDATIONOVERRIDE` to PR title: `gh pr edit --title "PROTOVALIDATIONOVERRIDE: {{ORIGINAL_TITLE}}"` |
| **PCVALIDATIONOVERRIDE needed** | Error mentions "PDL validation" or "backward incompatible" or "rest.li compatibility" | Add `PCVALIDATIONOVERRIDE` to PR title: `gh pr edit --title "PCVALIDATIONOVERRIDE: {{ORIGINAL_TITLE}}"` |
| **Known flaky test** | Test name matches known flaky list (e.g., `SkillServiceTest.testBatchGet`, `StrongSkillsMatchNotificationFormatterTest`) | Re-run failed checks: `gh pr checks {{PR_NUM}} --repo {{REPO}} --rerun-failed` or `trigger-build` |
| **REST model snapshot stale** | Error mentions "snapshot" or "idl" mismatch | Run `mint gen-idl-ignore` or manual snapshot edit, commit, push |
| **GraphQL schema stale** | Error mentions "federated schema" or "graphql" | Run `./gradlew -PgraphQLSchemaGenCompatMode=IGNORE build`, commit schema changes, push |

**Auto-fix flow:**
```bash
# 1. Get failed checks
FAILED=$(gh pr checks {{PR_NUM}} --repo {{REPO}} --json name,state | python3 -c "
import json,sys
checks = json.load(sys.stdin)
for c in checks:
    if c['state'] == 'FAILURE':
        print(c['name'])
")

# 2. For each failure, attempt auto-fix
for CHECK in $FAILED; do
  case "$CHECK" in
    *LI-Policy*|*description*)
      # Fix PR description
      BODY=$(gh pr view {{PR_NUM}} --repo {{REPO}} --json body -q .body)
      if ! echo "$BODY" | grep -q "## Summary"; then
        NEW_BODY="## Summary\n\n$BODY"
      fi
      if ! echo "$BODY" | grep -q "## Testing Done"; then
        NEW_BODY="$NEW_BODY\n\n## Testing Done\n\n- Unit tests passing\n- Manual verification"
      fi
      gh pr edit {{PR_NUM}} --repo {{REPO}} --body "$NEW_BODY"
      ;;
    *proto*validation*|*PROTO*)
      TITLE=$(gh pr view {{PR_NUM}} --repo {{REPO}} --json title -q .title)
      if ! echo "$TITLE" | grep -q "PROTOVALIDATIONOVERRIDE"; then
        gh pr edit {{PR_NUM}} --repo {{REPO}} --title "PROTOVALIDATIONOVERRIDE $TITLE"
      fi
      ;;
    *PDL*|*rest.li*compat*|*PCVALIDATION*)
      TITLE=$(gh pr view {{PR_NUM}} --repo {{REPO}} --json title -q .title)
      if ! echo "$TITLE" | grep -q "PCVALIDATIONOVERRIDE"; then
        gh pr edit {{PR_NUM}} --repo {{REPO}} --title "PCVALIDATIONOVERRIDE $TITLE"
      fi
      ;;
  esac
done

# 3. Re-run failed checks after fix
gh pr checks {{PR_NUM}} --repo {{REPO}} --rerun-failed
```

**After auto-fix:** Wait 2 min, then re-check CI. If still failing, report to user:
```
PR #{{PR_NUM}} CI failed after auto-fix attempt:
  - check-name: FAILED (link)
  Auto-fix attempted: [what was tried]
  Suggest: /pr-fix {{PR_NUM}} for manual investigation
```

**Non-auto-fixable failures (escalate immediately):**

| Failure | Action |
|---------|--------|
| Compilation error | `/pr-fix` — needs code change |
| Unit test failure (not flaky) | `/pr-fix` — needs code fix or test update |
| Coverage below threshold | Suggest adding tests for changed files |
| Merge conflict | `git pull origin master && resolve` |
| Unknown check failure | Report to user with link to check details |

### Review Check

```
/wait-for "gh pr view {{PR_NUM}} --repo {{REPO}} --json reviews shows APPROVED" --every 15m
```

On success prompt:
```
PR #{{PR_NUM}} approved by @reviewer!
CI: passed. Review: approved. Ready to merge.
⚠️ Waiting for your confirmation to merge. Reply "merge" or run: gh pr merge {{PR_NUM}}
```

**CRITICAL: Do NOT auto-merge.** Always pause and ask the user.

### Deploy Check

After merge, determine the expected version:
```bash
# Get merge commit
gh pr view {{PR_NUM}} --repo {{REPO}} --json mergeCommit

# Poll go-status for new version
/wait-for "go-status -f {{FABRIC}} -a {{APP}} shows version after merge" --every 10m
```

On success prompt:
```
PR #{{PR_NUM}} deployed to {{FABRIC}}!
Version: v2.3.45 (merged at 14:30, deployed at 15:10)
Monitoring PEM for 15 minutes...
```

### PEM Verification

```
/wait-for "PEM availability stable (>99%) for {{APP}} for 15min after deploy" --every 5m
```

This step uses observe-agent or PEM metrics to check post-deploy health.

On success:
```
🚀 Ship complete!

PR #{{PR_NUM}}: {{PR_TITLE}}
  CI:      passed
  Review:  approved by @reviewer
  Merged:  2026-04-02 14:30 UTC
  Deploy:  v2.3.45 on {{FABRIC}} at 15:10 UTC
  PEM:     stable (99.8% for 15min post-deploy)
  
Total time: 1h 23m (45m CI, 20m review, 15m deploy, 15m PEM)
```

On PEM failure:
```
⚠️ PEM dip detected after deploying PR #{{PR_NUM}}!

Availability dropped to 97.2% at 15:25 UTC (15min after deploy)
Previous baseline: 99.5%

Suggest: /investigate PEM dip for {{APP}} after deploy v2.3.45
```

## Step 4: Track Pipeline State

Write pipeline state to `/tmp/.claude-ship-{{PR_NUM}}.json`:
```json
{
  "pr": 123,
  "repo": "linkedin-multiproduct/hp-ats-integration-mt",
  "app": "hp-ats-integration-mt",
  "fabric": "prod-ltx1",
  "started": "2026-04-02T14:00:00Z",
  "steps": {
    "ci": {"status": "completed", "at": "2026-04-02T14:45:00Z"},
    "review": {"status": "completed", "at": "2026-04-02T15:05:00Z", "by": "@reviewer"},
    "merge": {"status": "completed", "at": "2026-04-02T15:10:00Z", "commit": "abc123"},
    "deploy": {"status": "waiting", "cron_id": "xyz789"},
    "pem": {"status": "pending"}
  }
}
```

### List active pipelines
```
/ship list
```
Reads all `/tmp/.claude-ship-*.json` files and shows status.

### Cancel a pipeline
```
/ship cancel 123
```
Cancels all cron jobs for the pipeline and removes the state file.

## Logging

On completion (success or failure), append to worklog:
```json
{"type": "ship", "pr": 123, "repo": "...", "result": "success|failed", "duration_min": 83, "steps": {...}, "timestamp": "..."}
```

## Error Recovery

- **CI flaky failure** → suggest re-running: `gh pr checks {{PR_NUM}} --repo {{REPO}} --rerun-failed`
- **Review stale** → suggest pinging reviewer
- **Deploy stuck** → suggest checking deploy queue / release train
- **PEM unrelated dip** → compare with baseline, suggest ignoring if pre-existing
- **Session ends mid-pipeline** → durable crons continue, next session picks up from state file
