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
