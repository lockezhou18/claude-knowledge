---
id: eureka-003
track: knowledge
type: semantic
repos: [*]
tags: [eureka, workflow, ship, ci-cd, wait-for, automation, cross-session]
severity: critical
created: "2026-04-02"
last_verified: "2026-04-02"
use_count: 1
outcome_score: 0
rot_rate: permanent
status: active
---

## Breakthrough

Chain `/wait-for` steps into a **fully automated PR → prod pipeline** — submit code, walk away, come back to "deployed and verified" or "failed at step X with reason Y."

## The Old Way

The PR → prod loop is a series of manual waits:
1. Push code, wait for CI (tab-switch, check back in 10min)
2. CI passes, wait for review (check Slack, ping reviewer)
3. Review approved, merge, wait for deploy (check go-status every few minutes)
4. Deployed, watch PEM/metrics for 30min (forget, come back tomorrow hoping nothing broke)

Each wait is a context switch. Each context switch is lost momentum. The whole cycle takes hours of wall-clock time but only minutes of actual work — the rest is waiting and remembering to check.

## The New Way

```
/ship PR #123
  → /wait-for "PR #123 CI passes" --every 5m
    → on success: notify "CI passed, waiting for review"
    → /wait-for "PR #123 approved" --every 15m
      → on success: merge, then
      → /wait-for "go-status shows new version on prod-ltx1" --every 10m
        → on success: 
        → /wait-for "PEM availability >99% for 30min" --every 5m
          → on success: "Ship complete. PR #123 live on prod. PEM stable."
          → on failure: "PEM dip after deploy — investigate?"
```

Each step is a durable cron. Each self-cancels on success and kicks off the next. The whole chain persists across sessions. You submit the PR and the system does the rest.

## Impact

- **Eliminates the #1 developer time sink** — waiting for CI/CD with manual polling
- **Zero context switches** — the chain handles all the waiting
- **Catches regressions immediately** — PEM check is built into the pipeline, not an afterthought
- **Full audit trail** — each step logs its result, creating a deployment worklog automatically
- **Scope: every engineer on the team** — anyone who ships code benefits

### The eureka chain that led here:
```
eureka-001: durable crons enable cross-session async workflows
eureka-002: skills emerge from real work (agent discovers → proposes → creates)
eureka-003: chain wait-fors into automated PR → prod pipeline
```

Each eureka built on the previous one. Compound learning compounding.

## Risks & Caveats

- **Auto-merge risk** — the chain should NOT auto-merge without human confirmation. Pause and notify before merge step.
- **PEM flakiness** — PEM dips might be unrelated to the deploy. Need a baseline comparison, not just absolute threshold.
- **7-day cron expiry** — if review takes >7 days, the chain breaks. Need to handle re-creation.
- **Multiple PRs** — if you ship 2 PRs in parallel, the chains shouldn't interfere.

## Next Steps

1. Build `/ship` skill that orchestrates the chain
2. Start simple: CI wait → notify. Add review/deploy/PEM steps incrementally.
3. Use `/wait-for list` to show all active ship pipelines
4. Log each completed ship to worklog automatically
