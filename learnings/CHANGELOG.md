# Compound Learning System — Changelog

## v2.4 — 2026-04-03 (late)
**Theme: Adopt, enrich, water**
- Evaluated hp-dev-agents/tee-dev-agent repos (27 skills each)
- Adopted 5 system-deep-dive principles as Engineering Principles: substance over plumbing, negative space, self-verification, naming disambiguation, cite code references
- Built `/implement` (Phase 4 Execute — was the missing pipeline piece)
- Built `/think` (open-ended conversational stance, inspired by OpenSpec explore)
- Built `/checkpoint` (lightweight 30s knowledge sync, feeds DIKW data layer)
- Created anti-pattern track in SCHEMA + directory
- Added plan-verify step to Phase 5 Review
- Added artifact archiving to /compound
- Wired 14 unused LinkedIn/Captain tools into question-first search guides
- Added playwright-cli as Tier 1.5 capability tool + 3 browser recipes
- DIKW pyramid analysis → fixed data layer gaps (outcome-log, synthesis, anti-patterns)
- Diminishing returns insight → entered "watering phase"
- Saved system evolution backlog to active-work.md

## v2.3 — 2026-04-03 (mid)
**Theme: Reward system + LinkedIn integration + /insights adoption**
- Implemented behavioral RL: feedback classification in /compound + /checkpoint
- Immediate feedback logging in /learn (+1.0), /aha (+1.5), /eureka (+2.0), /share (+1.5), /export-session (+1.5)
- Recalibrated signal scale: soft clarifications = -0.1 (not -1.0)
- Preference profile created with 6 behavioral dimensions
- Knowledge scout reads + surfaces STRONG behavioral reminders every prompt
- SessionEnd hook: fixed Read-before-Write error + timeout 180s → 600s
- Applied all /insights suggestions: pre-commit build hook, test-first-fix recipe, stronger behavioral gate
- Wired LinkedIn plugin gaps: map-infrastructure in /scope, infra-specs-expert in /investigate, library-specs auto-download
- captain.md referenced as SoT for LinkedIn tool usage (not hardcoded lists)
- PR review hook timeout 180s → 600s
- 67/67 session2 tests + 53/53 reward tests + 51/51 DIKW tests

## v2.2 — 2026-04-02
**Theme: Research guide optimization + search tool wiring**
- Question-first authority-sources.md (search by question, not by tool)
- 5 search guides: code-search (Jarvis syntax), logs-metrics (treeId + PEM strategies), slack (exception-first), jira (JQL + resolved), wiki (CQL modes)
- LinkedIn codebase as Source of Truth + logs as Runtime SoT in Research phase
- Code search guide from Confluence (Jarvis User Guide + your personal tips)
- `jarvis_codesearch` MCP-not-CLI warning added
- All search guides split into subfolder with links from authority-sources.md

## v2.1 — 2026-04-01 (late)
**Theme: Compound learning system v2 buildout**
- Built 19 custom skills: /kickoff, /scope, /research, /find, /verify, /investigate, /learn, /aha, /eureka, /compound, /scout, /share, /integrate, /export-session, /recipe, /worklog, /watch-deps, /pr-fix, /validate-qprod
- 7 automated hooks: UserPromptSubmit scout, commit logger, PR logger, multi-persona PR reviewer, insight scanner, SessionEnd compound agent
- Agent-optimized knowledge base: YAML frontmatter, JSONL manifests, three-signal scoring, episodic/semantic memory, rot-rate decay
- Score engine (score-insights.py): task-type routing, tag matching, decay calculation
- Knowledge scout (knowledge-scout.py): 50ms, keyword matching on hot manifest
- Tiered skill system: Tier 1 (universal) → Tier 2 (project) → Tier 3 (recipes)
- Recipe system with chain-up (recipe → skill) and chain-down (skill → recipe)
- E2E test suite: 143/143 deterministic tests across 4 suites
- /insights data integrated: behavioral gate for wrong-approach friction

## v2.0 — 2026-04-01 (early)
**Theme: Engineering pipeline + principles from Amazon SDE Guide**
- 6-phase engineering pipeline: Research → Clarify → Plan → Execute → Review → Compound
- Quality gates at each phase (GATE: verify before proceeding)
- 13 engineering principles from Amazon SDE Insider's Guide
- Principle 0: Faith of God (humility, integrity, stewardship, purpose, patience, gratitude)
- Evaluated Compound Engineering + Superpowers repos → adopted compound loop, multi-persona review, knowledge lifecycle
- Research on knowledge base design: three-signal scoring, episodic/semantic memory, rot-rate decay, task-type routing
- Research on scaling: DIKW pyramid, hub-and-spoke model, team sharing

## v1.0 — 2026-03-30
**Theme: Initial rules and memory**
- Investigation-First Rule from Amazon SDE Guide
- Engineering Principles extracted from SDE Insider's Guide PDF
- Compound Learning Rule (Search → Do → Document → Refresh)
- Self-Improvement Rule
- Memory files: engineering-principles, workflow-rules, tricks, build-troubleshooting
- 16 e2e tests for rules behavior

## v0.1 — 2026-03-04
**Theme: Foundation**
- Initial workflow rules: explore-then-implement, config editing, build & test
- First memory files created
