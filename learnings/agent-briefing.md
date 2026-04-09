# Agent Briefing
<!-- Last updated: 2026-04-09 01:45 -->

## Active Work

### Connected Projects Phase 2 — Bidirectional Sync
- **Status:** in-progress
- **Repo:** hp-ats-integration-mt
- **Active PRs:** #541 (resilience), #530 (history mapping)
- **Blockers:** ESPENG-57173

### Developer Productivity Tooling
- **Status:** watering phase — stop adding, let data prove what works
- **Latest (2026-04-09):** VM at near-full parity with local
  - code-server running on port 8080 (auto-tunneled via SSH config)
  - mutagen bidirectional sync for ~/workspace
  - tmux clipboard working via OSC 52 yank script + iTerm2
  - Claude hooks, settings, plugins, git config all deployed
  - Only remaining: `gh auth login` on VM
- **System state:** 23+ skills, 8 recipes, portable knowledge repo, VM near-parity
- **Next:** gh auth login, verify code-server workflow, test mutagen under real dev workload

### AI Usage Intelligence
- **Status:** proof-of-concept complete
- **Next:** Consider /recipe ai-usage-report parameterized by crew_id

## Last Session (2026-04-09)
VM infrastructure hardening session. Started from "how to better leverage VM" → health check → gap analysis → fixed 4 of 5 gaps (clipboard, git config, hooks, settings). Key discovery: Terminal.app doesn't support OSC 52, so installed iTerm2. Clipboard fix required 3 iterations (yank script /dev/tty → tmux client TTY → iTerm2). Also started code-server, set up mutagen sync, added SSH LocalForward. Clean session, no code changes — all infrastructure.

## Hot Insights

1. **[bug-001] GRADUATED** — Never findFirst() on V2 identity streams
2. **[bug-002] race condition** — ApplicationProcessor stage not in IP (close to graduation)
3. **[know-046] NEW** — OSC 52 clipboard: check terminal first, yank uses tmux client TTY, DCS passthrough for nested tmux
4. **[know-047] NEW** — VM parity checklist: 7 items to sync, what NOT to copy
5. **[know-045]** — vm-run: sync-and-build from any local repo, PreToolUse hook auto-intercepts
6. **[know-031] #1 friction: wrong-approach** — Hypothesis-first not optional
7. **[aha-003] Tier 1.5** — capability tools (browser eyes, production eyes, production hands)
8. **[eureka-003] multi-source synthesis** — graduation candidate

## Recent Patterns
- User drives architecture through gentle redirects — 4 instances last 2 sessions
- VM setup sessions are iterative: fix → test → discover new issue → fix. Budget 3 iterations for any SSH/terminal fix.
- solution_simplicity improving — this session had clean single-option proposals accepted without redirects
- research_depth strong — comprehensive gap analysis well-received

## Stale Alerts
- None flagged (all recent)

## Behavioral Reminders
- **Present hypotheses before deep-diving** (14+ signals)
- **Prefer simple solutions from codebase** (5+ signals)
- **Don't overwrite — add alongside** (3 signals)
- **Listen for gentle redirects** — "how do you feel", "meanwhile", "I feel like" = soft instruction
- **Start simple, let user escalate complexity**
- **Cross-validate data against SoT** before presenting
- **Cite code references** (file:line for every claim)
- **"Check/monitor/verify" = read-only, do NOT initiate actions**
- **3-strike rule** — same tool, same error, 3x → switch strategy or ask
- **curli/grpcurli = try LOCAL first**, VM only if local auth fails
- **COMPOUND: Every 3+ task session → generate >= 1 insight**
- **PRINCIPLES: Verify before asserting. Never guess values. Assume complex until proven simple. Cite file:line.**

## Quick Stats
- Skills: 22 commands + 15 skills + 8 recipes
- Insights: 63 total (2 new this session), 1 graduated, 0 pruned, 0 stale
- Feedback signals: 72 total (9 new this session)
- Knowledge repo: bizhou_LinkedIn/claude-knowledge
- VM parity: 6/7 items complete (gh auth pending)
