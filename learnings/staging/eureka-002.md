---
id: eureka-002
track: knowledge
type: semantic
repos: ["*"]
tags: ["eureka", "compound-learning", "meta", "productivity", "architecture", "self-improving", "reward-system"]
severity: critical
rot_rate: permanent
created: "2026-04-02"
last_verified: "2026-04-02"
use_count: 0
outcome_score: 0
status: active
visibility: "team"
---

## Breakthrough
An AI coding agent can be made self-improving — not through model training, but through a file-based compound learning ecosystem that captures knowledge, scores it, decays stale information, graduates proven insights, and adapts behavior from implicit user feedback. All with zero infrastructure beyond markdown, JSONL, and Python scripts.

## The Old Way
AI coding assistants were stateless — each session started from scratch. Knowledge lived in the user's head or in static CLAUDE.md files. The agent made the same mistakes across sessions. No learning loop, no behavioral adaptation, no knowledge lifecycle.

## The New Way
A complete self-improving ecosystem built on 5 interconnected systems:

1. **Engineering Pipeline** (Research → Clarify → Plan → Execute → Review → Compound) with quality gates at each phase. Grounded in Faith of God → Engineering Principles → Process.

2. **Knowledge Base** with agent-optimized retrieval: YAML frontmatter on insights, JSONL manifests for search, three-signal scoring (recency × relevance × importance), episodic/semantic memory types, rot-rate based decay, tiered loading (briefing → hot manifest → full manifest → files), and graduation lifecycle (create → score → graduate to memory or prune).

3. **19 Custom Skills** organized in tiers: Tier 1 universal (/kickoff, /scope, /research, /find, /verify, /investigate, /learn, /aha, /eureka, /compound, /worklog, /watch-deps), Tier 2 project-specific, Tier 3 recipes. Skills chain to each other via soft orchestration, not rigid rails.

4. **Automated Hooks**: Knowledge scout (Python, 50ms, reads briefing + manifests + preference profile), commit/PR loggers, multi-persona PR reviewer (7 conditional personas, confidence-gated), SessionEnd compound agent (feedback classification, insight generation, briefing rebuild, worklog, skill proposals, watch list).

5. **Behavioral RL System**: Implicit feedback classification from user responses (+2 to -2), preference profile that evolves from accumulated signals, behavioral dimension tracking (hypothesis_first, solution_simplicity, tool_choice, etc.), skill invocations as strong positive signals (/eureka = +2.0 retroactive on preceding behaviors). No model training needed — behaviors change through rules and knowledge adjustments.

## Impact
- Estimated 1.5-2 days/week saved now, growing to 3+ as insights accumulate
- 143/143 deterministic tests passing across 4 test suites
- First insight (bug-001) already graduated to permanent memory
- #1 friction point (wrong approach, 14/18 sessions) addressed with behavioral gate + preference profile
- System that no commercial product or known open-source framework fully replicates

## Risks & Caveats
- Untested at scale (25 insights works, 1000+ is designed but unproven)
- Behavioral RL hasn't run a full cycle yet — preference profile seeded from /insights data, not yet from actual compound feedback classification
- Single-user — team scaling designed but not implemented
- The compound loop needs to actually spin in production work sessions to prove it compounds

## Next Steps
1. Use the system for real work — let the flywheel spin
2. Run /compound after each substantial session — this is how the system learns
3. After 5+ sessions of feedback data, review preference-profile.md — does it reflect reality?
4. Share the system (/share system) — others can adopt and contribute
5. Implement per-repo CLAUDE.md with architecture insights (know-010 to know-016)
