# Worklog — Track What You Did

View, edit, and export your work log. Auto-populated by hooks, manually adjustable.

**Usage:**
- `/worklog` — show today's work log
- `/worklog week` — show this week's summary
- `/worklog standup` — generate standup update (yesterday + today's plan)
- `/worklog add [what you did]` — manually add an entry
- `/worklog export [range]` — export for perf review or handoff

## Where Worklogs Live

```
~/.claude/learnings/logs/worklog.jsonl
```

Each entry:
```json
{
  "timestamp": "2026-04-01T14:30:00Z",
  "type": "commit|pr|investigation|review|oncall|meeting|other",
  "repo": "hp-ats-integration-mt",
  "summary": "Fixed V2 identity mismatch in stage sync",
  "details": "PR #530 — updated TransformerContext with V1/V2 helpers",
  "duration_min": 45,
  "jira": "HPCP-1234",
  "tags": ["phase2", "identity", "bug-fix"],
  "source": "auto|manual"
}
```

## Auto-Capture (via hooks)

The SessionEnd compound agent should append worklog entries for:
- **Every commit** this session (from commit-log.jsonl)
- **Every PR** created or updated (from pr-log.jsonl)
- **Every investigation** run (from conversation context)
- **Key decisions** made
- **Time estimates** — session start to end

## Manual Entry

`/worklog add` for things hooks can't capture:
- Meetings, design discussions, code reviews of others' PRs
- Offline work (whiteboarding, reading docs, pair programming)
- Context-switching overhead

## Views

### `/worklog` (today)
```
## Work Log — 2026-04-01

### Commits (3)
- [14:30] hp-ats-integration-mt: Fixed V2 identity mismatch (PR #530)
- [15:45] hp-ats-integration-mt: Added regression tests for V1/V2
- [16:20] hp-ats-integration-mt: Updated stage sync to use V2 for mappings

### Investigations (1)
- [10:00-11:30] Investigated PEM availability dip on pipeline surface — root cause: canary deploy with config regression

### PRs (1)
- [16:30] Created PR #530: Fix V1/V2 HireIdentity mismatch in stage sync

### Insights Captured (2)
- [learn] V2 identity required for all mapping operations
- [aha] Same V1/V2 mismatch pattern in 3 services — shared utility needed

### Time: ~6h active work
```

### `/worklog standup`
```
## Standup — 2026-04-01

### Yesterday
- Fixed V1/V2 identity mismatch in stage sync and history operations (PR #530)
- Investigated PEM dip — canary config regression, self-resolved
- Captured 2 insights (V2 mapping rule, cross-service V1/V2 pattern)

### Today
- [from active-work.md] Deploy PR #526 and #529 to fix stuck candidates
- [from active-work.md] Complete E2E test with new job 4117765009

### Blockers
- [from active-work.md] ESPENG-57173 (Espresso key maxsize increase)
```

### `/worklog week`
```
## Week Summary — 2026-03-25 to 2026-03-31

### By Category
- Bug fixes: 3 PRs (V2 identity, race condition, export event)
- Features: 1 PR (shortened history URN)
- Investigations: 5 (PEM dips, GDPR incident, various oncall)
- Code reviews: 2

### By Repo
- hp-ats-integration-mt: 4 PRs, 3 investigations
- cap-services: 1 investigation

### Insights: 18 new, 2 graduated to memory
### Total active hours: ~32h

### Key Accomplishments
1. Phase 2 bidirectional sync E2E tested with 17 applicants
2. Resolved V1/V2 identity mismatch across 3 services
3. Built compound learning system (14 skills, 7 hooks, knowledge base)
```

### `/worklog export [range]`
Export as markdown for:
- **Perf review**: grouped by impact, with PR links and metrics
- **Oncall handoff**: grouped chronologically with resolution status
- **Manager 1:1**: highlights + blockers + what I need help with
