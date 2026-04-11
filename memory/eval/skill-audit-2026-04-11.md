---
name: Skill Audit — Native Tool Replacements
description: Audit of 42 skills against Claude Code native tools (CronCreate, Monitor, Agent). 4 to replace, 6 to simplify, 32 to keep.
type: eval
---

## Audit Date: 2026-04-11

### Replace with Native Tools (4)
- **wait-for** → CronCreate (durable) + condition check. Same pattern, native scheduling.
- **loop** → CronCreate with recurring=true. Direct equivalent.
- **checkpoint** → Just sync.sh push + read last-session-summary.txt. Too thin for a skill.
- **standup** → Read commit-log + pr-log + active-work.md inline. Simplify to one-liner.

### Simplify with Native Tools (6)
- **ship** → Replace chained /wait-for with CronCreate + Monitor. Simpler.
- **watch-deps** → CronCreate (daily) + diff script + Monitor.
- **session-handoff** → Redundant with memory system (last-session-summary.txt + active-work.md).
- **recipe vm-login** → One command: `ssh -t vm 'tmux attach'`.
- **recipe vm-setup** → Duplicate of vm-bootstrap.sh.
- **recipe auth-preflight** → Already in scout hook.

### Keep Custom (32)
Core: compound, dream, research, investigate, implement, explore, scope, find, verify, think
Capture: learn, aha, eureka, worklog (auto-run)
Meta: improve-agent, integrate, kickoff, recipe, share, export-session, scout
LinkedIn: oncall, triage-alert, hp-pipeline-pem, hp-contract-chooser-pem, hiring-platform,
  search-inlogs, deploy-check, validate-qprod, pr-fix, lix, oncall-daily-digest, oncall-trunk-health
Tools: delegate, markitdown, playwright-cli

### Decision
- worklog: KEEP + auto-run (user decision)
- All others per audit above
