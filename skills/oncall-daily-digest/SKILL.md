---
name: oncall-daily-digest
description: Generate overnight oncall digest — alerts, deploys, open tickets, PEM status, and trunk health for HP Backend services. Internal skill invoked by /oncall STEP 2H, not a standalone command.
version: 1.0.0
invocable: false
---

# HP Backend Oncall Daily Digest

Generate a consolidated overnight digest so the oncall engineer starts the day with full context.

> **Invoked by**: `/oncall` STEP 2H ("what's going on" / status check), or directly via `/oncall-daily-digest`
> **Worklog**: `/Users/bizhou/workspace/oncall/oncall_week_<date>_worklog.md`

---

## STEP 1: ALERTS (last 12 hours)

Query observe-agent for each service **in parallel**:

| Service | Query |
|---------|-------|
| hp-ats-integration-mt | "Show alerts for hp-ats-integration-mt in the last 12 hours" |
| mcm-mt | "Show alerts for mcm-mt in the last 12 hours" |
| hire-access-control | "Show alerts for hire-access-control in the last 12 hours" |
| mcm-jobs-integration-mt | "Show alerts for mcm-jobs-integration-mt in the last 12 hours" |
| talent-solutions-api-frontend | "Show alerts for talent-solutions-api-frontend in the last 12 hours" |

Categorize each alert:
- **Firing** — still active, needs attention
- **Resolved** — auto-resolved or manually acked
- **Pattern** — flag if same alert fired >2 times (indicates flapping or recurring issue)

---

## STEP 2: DEPLOYMENTS (last 24 hours)

Check deployed versions for each service via VM:
```bash
bash -c "ssh vm 'go-status -f prod-ltx1 -a <service>'"
```
Run all 5 in parallel.

Then use observe-agent: "Show recent deployments for [service] in the last 24 hours"

Note:
- Version changes (old → new)
- Who deployed
- Any EKG evaluations or rollbacks

---

## STEP 3: OPEN TICKETS

Search Jira for oncall-relevant tickets:
- Use `search_jira_issues` with query: `project = ENGSUP AND assignee = currentUser() AND status in (Open, "In Progress", Triaging) ORDER BY priority DESC`
- Also check: `project = HP AND type = Bug AND status in (Open, "In Progress") AND labels = oncall`

Flag SLA breaches:
- CSE tickets in Open/Triaging > 48 hours → **SLA BREACH**
- Include ticket key, summary, age, and SLA status

---

## STEP 4: PEM STATUS

Check PEM availability for key surfaces via observe-agent:
- "Show PEM availability for hp-ats-integration-mt surfaces in the last 12 hours"
- "Show PEM availability for mcm-mt surfaces in the last 12 hours"

Key surfaces to check:
| Surface | Service | Threshold |
|---------|---------|-----------|
| Contract Chooser | mcm-mt | 99.5% |
| Pipeline | mcm-mt | 99.5% |
| Project Create | mcm-mt | 99.5% |
| Project Home | mcm-mt | 99.5% |
| Project List | mcm-mt | 99.5% |

Flag any surface below 99.5% availability.

---

## STEP 5: TRUNK HEALTH (quick check)

If `/oncall-trunk-health` skill is available, invoke it for a quick summary.
Otherwise, check deployed version vs trunk for each service — a large gap indicates possible post-merge failures.

---

## STEP 6: COMPILE DIGEST

Output format:

```
# HP Backend Oncall Digest — {YYYY-MM-DD}

## Action Required
- [items needing immediate attention, sorted by severity]

## Alerts (last 12h)
| Service | Firing | Resolved | Pattern? |
|---------|--------|----------|----------|

## Deployments (last 24h)
| Service | Fabric | Old → New | Who | When |
|---------|--------|-----------|-----|------|

## Open Tickets ({count})
| Ticket | Summary | Status | Age | SLA |
|--------|---------|--------|-----|-----|

## PEM Status
| Surface | Availability | Trend | Alert? |
|---------|-------------|-------|--------|

## Trunk Health
[summary from STEP 5]

## Recommended Actions
1. [prioritized list of what to do first]
```

---

## NOTES

- **Tools**: observe-agent for alerts/PEM/deploys. `ssh vm` for go-status. Jira MCP for tickets.
- **Parallelism**: Run STEP 1-4 in parallel where possible (all 5 service queries at once).
- **Append to worklog**: After generating, offer to append the digest summary to the oncall worklog.
- **Standup ready**: The "Action Required" + "Recommended Actions" sections are directly usable for standup.
