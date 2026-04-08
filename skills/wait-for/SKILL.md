---
description: "Wait for an external condition to be met, polling across sessions. Sets up a durable cron that fires until the condition is satisfied, then auto-cancels."
user-invocable: true
allowed-tools:
  - Bash
  - CronCreate
  - CronDelete
  - Read
  - Write
inputs:
  - condition:
      description: "What to wait for — a natural language description or a specific command to run"
      example_value: "IP syncs Greenhouse job 4120265009"
  - interval:
      description: "How often to check (default: 10m). Supports: 5m, 10m, 30m, 1h"
      example_value: "10m"
---

# Wait For — Poll Until a Condition is Met

Set up a durable cron job that checks an external condition on a recurring interval, persists across sessions, and reports when the condition is satisfied.

## Usage

```
/wait-for IP syncs Greenhouse job 4120265009
/wait-for go-status shows v2.3.45 deployed on prod-ltx1 --every 30m
/wait-for PR #28 CI passes --every 5m
/wait-for HireEntityRequest 10513 status changes from PENDING --every 2m
/wait-for Kafka consumer lag clears for ApplicationStageProcessor --every 15m
```

## Step 1: Parse the Condition

From the user's input, determine:

1. **What to check** — the bash command or API call that tests the condition
2. **What success looks like** — how to detect the condition is met
3. **Interval** — extract from `--every Nm` suffix, or default to `10m`
4. **Context IDs** — extract entity IDs, service names, version numbers to embed in the prompt

### Common Patterns

| Condition | Check Command | Success Signal |
|-----------|--------------|----------------|
| IP syncs Greenhouse job `X` | `grpcurli FindByCriteria keyword=X` | `elements` array non-empty |
| Service deploys version `V` | `go-status -f FABRIC -a APP` | Output contains version `V` |
| PR CI passes | `gh pr checks PR_NUM` | All checks pass |
| HireEntityRequest status change | `grpcurli EulerEntityTestApi/get requestId=X` | Status != PENDING |
| Kafka consumer lag clears | `observe agent "check consumer lag for TOPIC"` | Lag below threshold |
| Entity appears in GLAI | `grpcurli find query` | Results non-empty |

## Step 2: Build a Self-Contained Prompt

The prompt must contain ALL context — the next session won't know why this cron exists.

Template:
```
Check if [CONDITION]. Run: [EXACT COMMAND]. 
If [SUCCESS_SIGNAL], report: "[FRIENDLY_MESSAGE]" and cancel this cron job (CronDelete job ID [JOB_ID]).
If not met, just say "[SHORT_STATUS]".
```

**Critical:** Include the cron job ID in the prompt so it can self-cancel on success.
Since CronCreate returns the job ID AFTER creation, use a two-step approach:
1. Create the cron with a placeholder
2. Update the stored prompt with the actual job ID

## Step 3: Convert Interval to Cron

| Input | Cron Expression |
|-------|----------------|
| `1m` | `* * * * *` |
| `2m` | `*/2 * * * *` |
| `5m` | `*/5 * * * *` |
| `10m` | `*/10 * * * *` |
| `15m` | `*/15 * * * *` |
| `30m` | `*/30 * * * *` |
| `1h` | `7 * * * *` |
| `2h` | `7 */2 * * *` |
| `6h` | `7 */6 * * *` |

Use off-minute values for hourly+ to avoid fleet congestion.

## Step 4: Create the Durable Cron

```
CronCreate(
  cron: "<expression>",
  prompt: "<self-contained prompt>",
  recurring: true,
  durable: true
)
```

**Always use `durable: true`** — this is the whole point. The job survives session restarts.

## Step 5: Track in Waitlist

Append to `/tmp/.claude-wait-for.jsonl` for local tracking:
```json
{"job_id": "abc123", "condition": "IP syncs job 4120265009", "created": "2026-04-02T01:00:00Z", "interval": "10m", "status": "waiting"}
```

## Step 6: Confirm to User

Report:
- What's being waited for
- Check interval
- Job ID (for manual cancel: `CronDelete <job_id>`)
- That it persists across sessions
- 7-day auto-expiry reminder

## Step 7: Run First Check Immediately

Don't wait for the first cron fire — run the check now and report the current status.

## On Success (when the cron fires and condition is met)

1. Report the result clearly
2. Cancel the cron: `CronDelete <job_id>`
3. Update `/tmp/.claude-wait-for.jsonl` status to "completed"
4. Suggest next action if obvious (e.g., "IP synced — want me to create the Connected Project?")

## On Expiry (7-day limit hit)

The cron auto-expires. If the condition was never met:
- Log it to `/tmp/.claude-wait-for.jsonl` as "expired"
- Next session should surface this: "A wait-for condition was never met: [condition]. Still relevant?"

## Managing Active Waits

```
/wait-for list    → show all active wait-for jobs
/wait-for cancel  → cancel a specific job
```

### List
Read `.claude/scheduled_tasks.json` and `/tmp/.claude-wait-for.jsonl`, show active waits:
```
Active waits:
  [abc123] IP syncs job 4120265009 (every 10m, since 2h ago)
  [def456] PR #28 CI passes (every 5m, since 30m ago)
```

### Cancel
```
CronDelete <job_id>
```
