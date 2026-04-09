# Agent Briefing
<!-- Last updated: 2026-04-07 23:30 -->

## Active Work

### Connected Projects Phase 2 — Bidirectional Sync
- **Status:** in-progress
- **Repo:** hp-ats-integration-mt
- **Recent:** Self-healing pipeline creation PR, V1/V2 identity mismatch fix
- **Active PRs:** #541 (resilience), #530 (history mapping), self-healing pipeline, V1/V2 identity fix
- **Blockers:** ESPENG-57173

### Developer Productivity Tooling
- **Status:** watering phase — stop adding, let data prove what works
- **Latest (2026-04-07):** Built portable knowledge architecture
  - `~/claude-knowledge/` git repo (144 files, ~1MB) pushed to bizhou_LinkedIn/claude-knowledge
  - `install.sh` symlinks into `~/.claude/`, `sync.sh` auto push/pull
  - SessionEnd + UserPromptSubmit hooks for auto-sync
  - VM routing rule, vm-setup recipe, vm-bootstrap.sh
  - All ~/.claude knowledge dirs now symlinked to git repo
- **Next:** Bootstrap VM (run vm-bootstrap.sh on bizhou-ld2.linkedin.biz), set up mutagen, verify sync cycle

### AI Usage Intelligence
- **Status:** proof-of-concept complete
- **Next:** Consider /recipe ai-usage-report parameterized by crew_id

## Last Session (2026-04-07)
Designed and built VM-primary Claude Code architecture with durable knowledge sync. User got a new dev VM (bizhou-ld2.linkedin.biz) — session evolved from "what to use VM for" into full portable knowledge system. Key: separate durable knowledge from ephemeral state, auto-sync via git hooks, VM as 24/7 primary workstation with laptop as thin client. VM bootstrap deferred to next session (SSH permissions need restart).

## Hot Insights

1. **[bug-001] GRADUATED** — Never findFirst() on V2 identity streams
2. **[bug-002] race condition** — ApplicationProcessor stage not in IP (close to graduation)
3. **[know-043] NEW** — Portable knowledge architecture: symlink + auto-sync + GitHub backup
4. **[know-044] NEW** — Permission changes require session restart
5. **[bug-006] NEW** — install.sh must not overwrite settings.json
6. **[know-031] #1 friction: wrong-approach** — Hypothesis-first not optional
7. **[aha-003] Tier 1.5** — capability tools (browser eyes, production eyes, production hands)
8. **[eureka-003] multi-source synthesis** — graduation candidate

## Recent Patterns
- User drives architecture through gentle redirects ("what do you think", "meanwhile", "I feel like")
- Scored -0.2 (GENTLE_REDIRECT) 4 times this session — user had to steer toward VM-primary, IDE offloading, knowledge portability, and simplification
- User sees system evolution as holistic — connects VM provisioning to knowledge durability to session continuity
- research_depth still strong (+0.9 avg) but solution_simplicity needs attention — tendency to propose complex multi-option architectures before user simplifies

## Stale Alerts
- None flagged (all recent)

## Behavioral Reminders
- **Present hypotheses before deep-diving** (14+ signals)
- **Prefer simple solutions from codebase** (5+ signals)
- **Don't overwrite — add alongside** (3 signals)
- **Listen for gentle redirects** — "how do you feel", "meanwhile", "I feel like" = soft instruction, not question
- **Start simple, let user escalate complexity** — propose Option A first, not A/B/C matrix
- **Cross-validate data against SoT** before presenting
- **Cite code references** (file:line for every claim)
- **NEW (eval 2026-04-08):** "Compare with our system" = lead with mapping, not standalone description
- **NEW (eval 2026-04-08):** "Check/monitor/verify" = read-only, do NOT initiate actions
- **NEW (eval 2026-04-08):** 3-strike rule — same tool, same error, 3x → switch strategy or ask
- **NEW (eval 2026-04-08):** curli/grpcurli = try LOCAL first, VM only if local auth fails
- **NEW (eval 2026-04-08):** Use built-in tools (Read for PDF, Playwright for rich pages, observe-agent for logs)
- **NEW (eval 2026-04-08):** COMPOUND: Every 3+ task session must generate >= 1 insight. Log outcomes in real-time. Suggest /compound proactively.

## Quick Stats
- Skills: 22 commands + 15 skills + 8 recipes
- Insights: 58 total (3 new this session), 1 graduated, 0 pruned, 0 stale
- Feedback signals: 63 total (13 new this session)
- Knowledge repo: bizhou_LinkedIn/claude-knowledge (144 files, ~1MB)
- VM bootstrap: pending (next session)
