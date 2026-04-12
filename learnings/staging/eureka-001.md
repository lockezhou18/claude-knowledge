---
id: eureka-001
track: knowledge
type: semantic
repos: [*]
tags: [eureka, workflow, cron, async, cross-session, polling, automation]
severity: critical
created: "2026-04-02"
last_verified: "2026-04-02"
use_count: 14
outcome_score: 0
rot_rate: permanent
status: active
---

## Breakthrough

Durable cron jobs enable **cross-session async workflows** — start a long-running external wait in one session, and the next session picks up automatically when the condition is met.

## The Old Way

When waiting on an external process (IP sync, deployment, PR merge, Kafka lag clearing):
- Set up a poll, wait in the current session
- If the session ends, manually remember to re-check next time
- Or: tell the user "check back in an hour" and hope they remember
- Context is lost between sessions — the next session doesn't know what was being waited on

## The New Way

```
Session 1:
  → Create Greenhouse job
  → IP hasn't synced yet (1hr+ cadence, Kafka lag)
  → CronCreate(durable=true, cron="*/10 * * * *", prompt="check if IP synced job X")
  → Continue working on other things

Session 2 (hours/days later):
  → Cron fires automatically on session start
  → "IP synced! IntJobReqId=12345"
  → Continue E2E testing from where Session 1 left off
```

The durable cron persists to `.claude/scheduled_tasks.json` and survives session restarts. The prompt contains all the context needed — the next session doesn't need to know the backstory.

## Impact

- **Eliminates "remember to check" cognitive load** — the system tracks it for you
- **Enables parallel async workflows** — wait for IP sync + wait for deployment + wait for PR review, all as separate cron jobs
- **Cross-session continuity** — the hardest problem in multi-session work (losing context) is solved by encoding the check into the prompt itself
- **Scope: all projects** — any workflow involving external waits benefits

### Use cases discovered:
1. **Dependency sync polling** (IP sync from Greenhouse) — `/watch-deps` pattern
2. **Deployment monitoring** — poll `go-status` until new version appears
3. **PR status tracking** — poll until CI passes or reviewer approves
4. **Kafka lag clearing** — poll until consumer catches up
5. **Entity indexing** — poll GLAI find until entity becomes queryable

## Risks & Caveats

- **7-day auto-expiry** on recurring cron jobs — need to re-create for longer waits
- **Only fires when REPL is idle** — won't fire mid-query
- **Prompt must be self-contained** — next session has no memory of why the cron was created, so the prompt must encode all context (entity IDs, expected values, what to do on success)
- **Don't over-poll** — `*/5` for urgent, `*/30` for background, don't spam external APIs

## Next Steps

1. Use this pattern in `/watch-deps` recipe — durable nightly cron checking upstream versions
2. Add to E2E testing skill — automatic poll for IP sync after Greenhouse job creation
3. Consider a `/wait-for` skill that wraps the pattern: `/wait-for "IP syncs job 4120265009" --check-every 10m`
