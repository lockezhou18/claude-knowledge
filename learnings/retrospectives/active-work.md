# Active Work Context

## Current Initiatives

### Connected Projects Phase 2 — Bidirectional Sync
- **Started:** 2026-03-15
- **Status:** in-progress
- **Repo:** hp-ats-integration-mt
- **Context:** E2E testing and bug fixes for bidirectional sync between HP and Greenhouse
- **Last session (2026-04-03):**
  - Reviewed + cleaned up PR #541 (ActionWriteBack fire-and-forget HireEntityRequest write)
  - Removed unused LixUtil dep, fixed trailing newline, reverted unrelated config, tightened tests
  - Verified HireEntityRequest write uses full URN (not shortened workaround from PR #529)
  - Enhanced PR #3848 (mcm-mt AtsAutomationPipelineSettingsHandler null viewer fix)
- **Active PRs:**
  - PR #541: ActionWriteBack resilience (fire-and-forget Euler write) — review fixes pushed
  - PR #530: Skip history mapping validation + reconstruct real history URN
  - PR #3848 (mcm-mt): AtsAutomationPipelineSettingsHandler null viewer fix
- **Next:**
  - Get PR #541 and #530 merged
  - Continue E2E testing with new test projects
  - Test export status event FAILURE path
- **Blockers:** ESPENG-57173 (Espresso key maxsize increase) — Espresso team analyzing

### Memory Migration — Single SoT
- **Started:** 2026-04-09
- **Status:** Phase 6 complete, Phases 7-10 remaining (improvements)
- **Repo:** memory-migration (git@github.com:bizhou_LinkedIn/memory-migration.git)
- **Context:** Migrate from dual knowledge stores to single SoT via autoMemoryDirectory
- **Last session (2026-04-11):**
  - /dream skill created and tested
  - VM dream cron deployed (3:47am on bizhou-ld2)
  - Push notifications: scout hook shows overnight dream results automatically
  - markitdown skill created, 3 design docs converted to memory
  - cmux evaluated — skip for now (existing infra covers the use cases)
  - AgentBus bugs fixed: command extraction + NATS auth retry
- **Architecture:** ~/claude-knowledge/memory/ is THE SoT. autoMemoryDirectory + per-project symlinks. dream.py maintains overnight on VM. Scout hook = notification center.
- **Next:** Phase 7 (rewrite scout to read memory/ natively), Phase 8 (deprecate agent-briefing.md), intelligent dreaming via /delegate
- **Key files:** plan.md, scripts/dream.py, scripts/probe_features.py

### AgentBus — VM Agent Communication
- **Started:** 2026-04-10
- **Status:** operational, QA + test suite complete
- **Repo:** ~/workspace/.agentbus (laptop), /home/bizhou/workspace/.agentbus (VM, not git)
- **Context:** NATS-backed messaging between laptop Claude and VM Claude agent
- **What's working:**
  - Shell commands via AgentBus: tested ✓
  - Thinking tasks (claude -p on VM): tested ✓ (14s round-trip)
  - Session resume (multi-turn): tested ✓ (3-turn demo)
  - Async with Monitor (watch_result.py): tested ✓
  - Auto mode (multi-round): implemented, outcome detection fixed (word-boundary regex)
  - NATS server + listener auto-start on VM login
  - SSH tunnel on port 14222 (not 4222)
- **Skill:** `/delegate` (merged from vm-remote + vm-agent)
- **Last session (2026-04-12):**
  - Validated external QA assessment (Architecture 8/10, Code 6/10, Tests 3/10, Docs 8/10, Idea 9/10)
  - Wrote 109 new tests (143 total): ClaudeAdapter 77 tests, CLI 29 tests, e2e 22 tests
  - Fixed fragile dispatch_auto success detection (word-boundary regex, _detect_outcome)
  - Fixed _extract_shell_command (known-tool-first, removed brittle "in repo" regex)
  - Fixed blocking subprocess.run in listener.py (asyncio.to_thread)
  - Removed hardcoded NATS credentials from 4 files
  - Removed sys.path hacks from 8 files
  - Deduped send.py CLI (redirect to unified CLI)
  - Deployed to VM via ssh cat pipe + systemd restart
  - Commit: 1e59470, pushed to origin/main
- **Next:**
  - A2A HTTP transport adapter (strategic priority — see strategy-a2a-alignment.md)
  - Formal task lifecycle (create/get/cancel/status)
  - Explore teammate access (agent cards for team members)
  - Level 2 (streaming daemon) when needed

### Developer Productivity Tooling
- **Started:** 2026-03-25
- **Status:** watering phase (stop adding, let data prove what works)
- **Context:** Skills, hooks, and rules for team sharing
- **Last session (2026-04-09):**
  - VM parity gap analysis: found 5 gaps (clipboard, gh auth, git config, hooks, settings)
  - Fixed tmux clipboard: OSC 52 yank script using tmux client TTY (not /dev/tty)
  - Discovered Terminal.app doesn't support OSC 52 → installed iTerm2
  - Created git config on VM (user.name, email, LFS, credential helper)
  - Copied 7 Claude hooks to VM (skipped vm-route-builds — not needed on VM)
  - Updated VM settings.json with hooks, permissions, plugins (paths adapted for /home/bizhou)
  - Started code-server on port 8080, added SSH LocalForward to config.custom
  - Set up mutagen bidirectional sync for ~/workspace
  - Cleaned up stale mutagen sessions
- **System state:** 23+ skills, 8 recipes, Tier 1/1.5/2/3 taxonomy, portable knowledge repo, VM at near-full parity
- **Next:** gh auth login on VM, verify code-server workflow, test mutagen sync under real dev workload

### AI Usage Intelligence (new — potential recipe)
- **Started:** 2026-04-03
- **Status:** proof-of-concept complete
- **Context:** Querying developer_supertable + claude_code + cursor_usage_events + crew API for team AI usage reports
- **Key tables:** `openhouse.u_svc_pr_deitools.developer_supertable`, `claude_code`, `cursor_usage_events`
- **Key finding:** estimated_cost.amount in cents, enterprise pricing (Opus ~40% of public)
- **Next:** Consider creating /recipe ai-usage-report parameterized by crew_id

### Self-Improving Eval System
- **Started:** 2026-04-08
- **Status:** operational, first eval complete
- **Context:** Oracle eval pattern adapted for AI Partner quality measurement
- **Location:** ~/claude-knowledge/evals/ (pipeline, judge, taxonomy, verdicts)
- **Baseline (2026-04-08, 35 sessions):** 76.2% agreement, 85.1% principle adherence, P0=0.84, loop closure 10%
- **Fixes applied:** 4 iterations (wrong_approach, tool_misuse, compound gate, principle gate)
- **Report:** ~/claude-knowledge/evals/results/agent-quality/agent_quality_report_2026-04-08.html
- **Next:** Re-run /improve-agent in 1 week to measure if fixes moved the numbers

### Claude-Native Memory Migration
- **Started:** 2026-04-09
- **Status:** planning complete, Phase 0 test deployed
- **Context:** Restructure ecosystem so Auto Memory/Dream is the knowledge foundation
- **Location:** ~/projects/compound-learning-ecosystem/memory-migration/
- **Risk gate:** Phase 0 — test-frontmatter.md deployed to memory/, waiting for Auto Dream cycle
- **Next:** Check Phase 0 results, then Phase 1 (slim MEMORY.md to 50 lines)

### Backlog — System Evolution (do when data supports it)
- [ ] Merge overlapping skills (identify via usage data — which pairs are always invoked together?)
- [ ] Split /compound (8 steps → separate /compound-quick already done as /checkpoint)
- [ ] Prune rules the agent follows without being told (measure with reward system — if dimension score is +1.0 consistently, the rule may be internalized)
- [ ] Periodic system health review (after 10 real work sessions: dead skills? stale guides? outdated rules?)
- [x] Version tracking for changes — DONE: ~/claude-knowledge/ is a git repo with full history
- [ ] Explore how to use Figma from Claude — Figma MCP setup, REST API with personal token, rate limit workarounds (View seat limit), design-to-test-case pipeline, prototype flow extraction. Reference: eureka-004, eureka-006, session 2026-04-03
- [ ] `/synthesize` skill — combine multiple data sources into a new output none could produce alone. Emerged from eureka-003 (AI usage report). Build when pattern recurs.
- [ ] **Goal-driven development**: Integrate `connected-projects-shared` (context) with `hp-dev-agents` (execution) via bridge skills. Reframe from task-driven ("fix file X") to goal-driven ("recruiter sees Failed badge when ATS rejects"). The deliverable = a completed goal verified end-to-end, not a PR. Flow: Goal → design (Figma) → architecture (which services) → worktrees (parallel branches) → implementation (guided by patterns) → verification (Playwright + Greenhouse API + grpcurli) → goal COMPLETE when all layers agree. Option B: loose coupling, bridge skills connect repos. Reference: eureka-006, eureka-007, session 2026-04-04/05
- [ ] Paper publication plan — patent filed (ID 93827). Next: talk to manager, get 2-3 teammates on the system for 2 weeks, run /insights before/after, 15-min interviews. Target CHASE workshop first (N=1 sufficient), then CHI/ASE with multi-user data. See know-040 and recipe patent-publication-tracker.
- [ ] **SWE-bench benchmark run** — Measure raw coding ability against industry standard. Setup: install mini-swe-agent, generate patches locally with Claude Opus 4.6, submit to sb-cli cloud evaluation (ARM64 Mac can't run SWE-bench Docker containers natively). Start with 10-instance sample (~$30), then full Verified (500 instances, ~$1,500). Current SOTA: Claude 4.5 Opus 76.8%. Also design a system-level benchmark for dimensions SWE-bench doesn't cover (knowledge reuse, investigation quality, skill routing, compound learning).
