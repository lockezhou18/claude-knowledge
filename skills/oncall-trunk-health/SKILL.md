---
name: oncall-trunk-health
description: Check trunk build health across HP Backend services — CI status, post-merge failures, flaky tests, and blocked merges.
version: 1.0.0
triggers:
  - trunk health
  - build health
  - master broken
  - CI status
  - post-merge failure
  - trunk check
---

# HP Backend Trunk Health Check

Monitor trunk (master) build health across team services. Surface failures before they block development.

> **Invoked by**: `/oncall-daily-digest` STEP 5, or directly via `/oncall-trunk-health`
> **Services**: hp-ats-integration-mt, mcm-mt, hire-access-control, mcm-jobs-integration-mt, talent-solutions-api-frontend

---

## STEP 1: CHECK DEPLOYED vs TRUNK

For each service, check the deployed version and compare to trunk HEAD:

```bash
# Deployed version (run all in parallel via VM)
bash -c "ssh vm 'go-status -f prod-ltx1 -a hp-ats-integration-mt'"
bash -c "ssh vm 'go-status -f prod-ltx1 -a mcm-mt'"
bash -c "ssh vm 'go-status -f prod-ltx1 -a hire-access-control'"
bash -c "ssh vm 'go-status -f prod-ltx1 -a mcm-jobs-integration-mt'"
bash -c "ssh vm 'go-status -f prod-ltx1 -a talent-solutions-api-frontend'"
```

If deployed version is significantly behind trunk (>5 commits), post-merge build may be broken or deployment is paused.

---

## STEP 2: IDENTIFY POST-MERGE FAILURES

For services with a version gap:

1. **Check recent trunk commits**:
   ```bash
   bash -c "ssh vm 'cd ~/workspace/<service> && git log --oneline -20 origin/master'"
   ```

2. **Look for fix indicators** in commit messages:
   - `PROTOVALIDATIONOVERRIDE` — proto backward-compat fix attempt
   - `PCVALIDATIONOVERRIDE` — PDL/Rest.li backward-compat fix attempt
   - `trigger-build` — someone manually retriggered the post-merge build
   - These indicate the trunk was recently broken and someone attempted a fix

3. **Check build status** via observe-agent:
   "Show CI build status for [service] master branch in the last 24 hours"

4. **Check for open Jira tickets** about the break:
   Use `search_jira_issues`: `project = HP AND summary ~ "post-merge" AND status != Done`

---

## STEP 3: CHECK FLAKY TESTS

### Known Flaky Tests (keep updated)

| Service | Test | Notes |
|---------|------|-------|
| talent-solutions-api-frontend | `SkillServiceTest.testBatchGet` | Known flaky, not related to team changes |
| talent-solutions-api-frontend | `StrongSkillsMatchNotificationFormatterTest.testNotificationFormatterSuccess` | Known flaky |

### Detect New Flaky Tests

Use observe-agent: "Show test failure rates for [service] in the last 7 days"

Classify:
- **Flaky** (intermittent, <50% failure rate) — note but don't escalate
- **Broken** (consistent, >50% failure rate) — escalate immediately
- **New** (first seen in last 7 days) — investigate the introducing commit

---

## STEP 4: CHECK MERGE BLOCKERS

For each service, check if PRs are blocked:

1. **Blocked by trunk failure**: If post-merge is red, all PRs queue behind it
2. **Blocked by dependency conflicts**: Check for version set issues in recent PR CI failures
3. **Blocked by EKG**: If EKG evaluation is running, deploys pause

Use observe-agent or GitHub: "Show open PRs for [service] with failing CI checks"

---

## STEP 5: COMPILE HEALTH REPORT

```
# Trunk Health Report — {YYYY-MM-DD}

## Overall: [GREEN] Healthy / [YELLOW] Degraded / [RED] Broken

## Build Status
| Service | Trunk | Deployed | Gap (commits) | Status |
|---------|-------|----------|---------------|--------|

## Failures
### {service} — [RED/YELLOW]
- **Breaking commit**: {hash} by {author} — {message}
- **Impact**: {what's blocked — deploys, PRs, etc.}
- **Fix attempts**: {trigger-build? override commit? open ticket?}
- **Recommended action**: {specific command or step}

## Flaky Tests
| Service | Test | Failure Rate (7d) | Known? | New? |
|---------|------|--------------------|--------|------|

## Blocked PRs
| Service | PR | Author | Blocked By | Age |
|---------|-----|--------|------------|-----|

## Recommended Actions
1. [prioritized — broken builds first, then flaky tests, then blocked PRs]
```

---

## FIX RECIPES

### Post-merge proto validation failure
```bash
# Use trigger-build CLI (requires interactive tmux for password)
# invoke linkedin-cli-tools:launch-tmux first
trigger-build -b master -m "PROTOVALIDATIONOVERRIDE <description>"
```
Note: PROTOVALIDATIONOVERRIDE must be in the commit message (which becomes PR title in squash merge).

### Post-merge PDL validation failure
```bash
trigger-build -b master -m "PCVALIDATIONOVERRIDE <description>"
```

### ts-api GraphQL schema failure after version bump
```bash
bash -c "cd <ts-api-dir> && vm-run ./gradlew -PgraphQLSchemaGenCompatMode=IGNORE build"
```

---

## NOTES

- **Tools**: `ssh vm` for go-status/git. observe-agent for CI/test metrics. Jira MCP for tickets.
- **Parallelism**: Run all go-status checks in parallel. Run git log checks in parallel for flagged services.
- **Escalation**: If trunk is RED for >4 hours with no fix attempts, flag in team Slack channel.
- **Cross-reference with deploys**: A trunk break + recent deploy = possible rollback needed.
