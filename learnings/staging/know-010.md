---
id: know-010
track: knowledge
type: semantic
repos: ["*"]
tags: ["debugging", "retry", "logs", "exception", "stacked-bugs"]
severity: medium
rot_rate: permanent
status: active
created: "2026-04-01"
last_verified: "2026-04-01"
use_count: 0
outcome_score: 0
---

## When retries exhaust without visible errors, check exception chains — and expect stacked bugs

### Context
During hp-ats-integration-mt history item E2E testing, 3 bugs were stacked — each only visible after fixing the previous one. The retry logs showed "max retry attempt 5 reached" but no ERROR in the `message` field between the action and the retry.

### Guidance
1. **Check `exceptionChain`/`exceptionStackTrace` fields**, not just `message` — InLogs/Kusto stores them separately. Use `observe agent` to ask for "full exception chain" for a treeId.
2. **After fixing one failure, re-test immediately** — there may be another bug hiding behind it. Don't assume the flow works just because the first error is gone.
3. **Trace the treeId across services** — the caller (hp-ats) may log a generic gRPC error, but the server (mcm-mt) logs the actual root cause (e.g., "ProjectCandidateHistoryV3 not found").
4. **When a workaround changes data format** (e.g., shortened URNs with placeholder zeros), audit every consumer of that data — some need the real values, not the placeholders.

### When to Apply
- Debugging Kafka consumer retry loops with no visible errors
- After deploying a fix, re-testing shows the same retry count
- When a temp workaround (lix-gated) changes data shape
