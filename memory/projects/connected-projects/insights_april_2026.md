---
name: Insights Report Findings (April 2026)
description: Key friction patterns and improvements from 32-session analysis — wrong approaches, environment blockers, and what works best
type: feedback
---

## Top Friction: Wrong Investigation Paths (28 instances)

Claude frequently starts down the wrong technical approach. **Mitigation applied:**
- CLAUDE.md now has "Trust user domain knowledge" rule
- Service Routing Table + "Use curli not Trino" + "Use observe-agent for logs" already existed
- **How to apply:** When user names a specific class/processor/ticket, start there. Don't second-guess.

## What Works Best

User satisfaction highest when Claude:
1. **Traces bugs end-to-end** across multi-service pipelines (13 debugging successes)
2. **Makes multi-file changes** that compile and pass tests first try (8 successes)
3. **Delivers fast accurate search** across codebases (5 successes)

**Why:** User is an active supervisor with tight feedback loop — delegates broad goals, watches approach, corrects early. High tolerance for iteration, low tolerance for wrong direction.

## Applied Improvements (2026-04-07)

1. **CLAUDE.md additions:** Java compatibility (no Set.of), bias toward action, trust user domain knowledge, project-level saves
2. **Headless scripts:** `~/.claude/scripts/daily-standup.sh`, `~/.claude/scripts/weekly-ai-report.sh`
3. **Already existed:** investigate skill, pre-commit hooks, REST/observe-agent rules

## Session Stats (2 weeks)
- 32 sessions, 134h total, 373 messages, 6 commits
- Tool usage: Bash(449) > Read(140) > Grep(66) > Edit(65) — investigation-heavy
- 84% positive satisfaction signals
