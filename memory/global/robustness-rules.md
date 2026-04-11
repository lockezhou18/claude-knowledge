---
name: System robustness rules from agentbus bugs
description: Rules derived from 8 bugs found during agentbus/eval session. Three patterns — silent failures, fragile chains, misleading signals.
type: feedback
---

## Pattern 1: Silent Failures → Add Health Checks

Things that fail silently are the worst — they look healthy but aren't working.

**Rules:**
- Every daemon/cron MUST write a heartbeat or log entry on each run — absence of log = failure
- Every `claude -p` dispatch MUST check the exit code AND stderr — rc=1 with empty stderr means auth issue
- Every cron job MUST redirect stderr to a log file (`2>&1 >> logfile`) — never discard errors
- After deploying a new service, verify it works with a health check within the same session — don't assume

**Anti-pattern:** "It's set up, it should work." Verify.

**Example:** Dream cron was "set up" but never actually ran for 3 days because git pull failed silently.

## Pattern 2: Fragile Chains → Use Semicolons, Not &&

Sequential commands where one failure kills the rest.

**Rules:**
- Cron jobs: use `;` between independent steps, not `&&` — git pull failing shouldn't stop dream.py
- Multi-step scripts: each step should fail independently unless there's a TRUE dependency
- If step B genuinely depends on step A: use `&&`. If they're just sequential: use `;`
- Add explicit error handling for known failure modes (git conflicts, auth expiry, network timeout)

**Anti-pattern:** `git pull && process && push` — if pull fails (conflict, network), nothing runs.

**Better:** `git pull 2>/dev/null; process >> log 2>&1; push 2>/dev/null`

## Pattern 3: Misleading Signals → Label Output Clearly

Output that looks like errors but isn't, or looks fine but is broken.

**Rules:**
- "NATS disconnected" is a normal close, not an error — label it: `[info] Connection closed` not just the raw message
- SSH "Address already in use" is informational when the tunnel exists — suppress or label
- `claude auth status` showing "logged in" doesn't mean `claude -p` works — test the actual command
- When health checking, test the ACTUAL operation, not a proxy. `auth status = OK` is not the same as `claude -p "test" = OK`

**Anti-pattern:** Seeing "connected" in auth status and assuming headless mode works.

## How to Apply

When building any new infrastructure (services, crons, daemons):
1. Add a `--health` command that tests the ACTUAL operation end-to-end
2. Every cron writes to a log file — check the log, not the crontab
3. Use `;` not `&&` for independent steps in cron
4. After setup, run the health check in the same session — don't leave and hope
5. Label all output clearly — `[error]`, `[info]`, `[warning]` — not raw messages
