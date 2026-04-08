# Agent Briefing
<!-- Last updated: 2026-04-03 23:15 -->

## Active Work

### Connected Projects Phase 2 — Bidirectional Sync
- **Status:** in-progress
- **Active PRs:** #541 (resilience), #530 (history mapping), mcm-mt #3848
- **Next:** Merge PRs. E2E testing. Test FAILURE path.
- **Blockers:** ESPENG-57173

### Developer Productivity Tooling
- **Status:** watering phase — stop adding, let data prove what works
- **Latest:** playwright-cli adopted as Tier 1.5, 3 browser recipes, /investigate + auth-preflight updated
- **Next:** Use system for 10 real work sessions with /checkpoint + /compound

### AI Usage Intelligence (new)
- **Status:** proof-of-concept complete
- **Context:** crew 393 AI usage report built from multi-source synthesis
- **Next:** Consider /recipe ai-usage-report parameterized by crew_id

## Hot Insights

1. **[bug-001] GRADUATED** → Never findFirst() on V2 identity streams
2. **[bug-002] race condition** — ApplicationProcessor stage not in IP (close to graduation)
3. **[know-031] #1 friction: wrong-approach** — 14 instances. Hypothesis-first not optional.
4. **[know-041] cost table units** — claude_code amounts in cents (÷100 for USD), enterprise pricing
5. **[aha-003] Tier 1.5** — capability tools (browser eyes, production eyes, production hands)
6. **[eureka-003] multi-source synthesis** — combine Trino + Console + Confluence + crew API for exec-level intelligence. Graduation candidate.

## Recent Patterns
- research_depth is the strongest positive dimension (+1.2 avg from 10+ signals this session alone)
- Multi-source cross-validation caught a unit error — always verify against SoT
- User values comprehensive analysis over quick answers — "even my director doesn't have such full picture"
- User corrects tier/categorization assumptions (soft signal -0.1) — ask before placing

## Behavioral Reminders
- **Present hypotheses before deep-diving** (14+ signals)
- **Prefer simple solutions from codebase** (5+ signals)
- **Don't overwrite — add alongside** (3 signals)
- **Cite code references** (file:line for every claim)
- **Substance over plumbing** (WHAT before HOW)
- **Cross-validate data against SoT** before presenting (new — cost unit lesson)
- **Ask classification before assuming** — user prefers to name tiers, categories (soft signal)

## System Status
- Skills: 20 commands + 13 skills + 6 recipes
- Tier taxonomy: 1 (skills) / 1.5 (capabilities) / 2 (project) / 3 (recipes)
- Hooks: 8 (incl. pre-commit build, knowledge scout)
- Feedback signals: 41 (13 new this session)
- Insights: 42 total, 3 hot (aha-003, know-041, eureka-003)
- Graduation candidates: eureka-003 (multi-source synthesis)
- Entering watering phase — backlog items tracked in active-work.md
