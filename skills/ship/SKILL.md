---
description: "Automated PR → prod pipeline. Submit code and walk away — CI, review, merge, deploy, PEM via native CronCreate."
user-invocable: true
allowed-tools:
  - Bash
  - CronCreate
  - CronDelete
  - Read
  - Write
inputs:
  - pr:
      description: "PR number or URL to ship"
      example_value: "123"
  - fabric:
      description: "Target fabric (default: prod-ltx1)"
      example_value: "prod-ltx1"
  - skip:
      description: "Steps to skip: ci, review, deploy, pem"
      example_value: "pem"
---

# Ship — PR to Prod Pipeline

Chain CronCreate jobs to monitor CI → review → deploy → PEM. Each step's cron self-cancels on success and reports.

## Usage

```
/ship 123
/ship 123 --skip pem
```

## Pipeline

```
Step 1: CI      → CronCreate(*/5, "gh pr checks PR passes?", durable=true)
Step 2: Review  → CronCreate(*/15, "gh pr view PR shows APPROVED?", durable=true)
Step 3: Merge   → PAUSE — ask user before merging. Never auto-merge.
Step 4: Deploy  → CronCreate(*/10, "go-status shows new version?", durable=true)
Step 5: PEM     → CronCreate(*/5, "PEM stable 15min post-deploy?", durable=true)
```

Each cron prompt must be self-contained (include PR number, repo, app name, fabric, cron job ID for self-cancel).

## Steps

1. **Parse input**: Extract PR number, repo (from URL/git remote), app name, fabric, skip set.
2. **Check current state**: `gh pr view PR --json state,checks,reviews,mergeable` — skip completed steps.
3. **Start pipeline**: Create first applicable CronCreate. Each cron's success prompt creates the next cron.
4. **Track state**: Write to `/tmp/.claude-ship-{PR}.json` for resume across sessions.

## CI Auto-Fix (before escalating)

| Failure | Auto-Fix |
|---------|----------|
| LI-Policy description | Add `## Summary` + `## Testing Done` via `gh pr edit --body` |
| Proto/PDL validation | Add `PROTOVALIDATIONOVERRIDE`/`PCVALIDATIONOVERRIDE` to title |
| Known flaky test | `gh pr checks --rerun-failed` |

Non-fixable (compilation, real test failure) → report to user, suggest `/pr-fix`.

## Completion

Report: PR title, CI time, reviewer, merge time, deploy version, PEM status, total elapsed.
