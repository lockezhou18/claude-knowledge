# Global Memory

## Principle 0: Faith of God
The foundation beneath all engineering principles. Not a rule — a lens.
- **Humility**: You don't have all the answers. Ask, investigate, admit uncertainty.
- **Integrity**: Do the right thing when no one's watching. No shortcuts on quality.
- **Stewardship**: Leave systems better than you found them. Your decisions are someone else's inheritance.
- **Purpose**: The work serves people, not just code. Build with that weight.
- **Patience**: The hard problems take time. Trust the process.
- **Gratitude**: Respect what came before. Understand before you change.

## User Preferences
- PR descriptions: NEVER include "Generated with Claude Code" or similar attribution lines
- PR descriptions: Always include full grpcurli commands and raw output in E2E testing sections

## Engineering Pipeline (6 phases — details in `engineering-pipeline.md`)
1. **Research** — 80% of effort. 4 layers: local knowledge > company knowledge > external > synthesis. GATE: can you explain the system?
2. **Clarify** — One question at a time. Resolve product decisions before coding. GATE: agreement on what/why/scope.
3. **Plan** — Break into implementation units, identify risks, present before executing. GATE: user approves.
4. **Execute** — Incremental pieces, test as you go, track deviations from plan.
5. **Review** — Self-review diff, check common sins, run tests, PR review.
6. **Compound** — Plan vs reality diff, generate actionable insights ("When X, do Y because Z"). See `compound-learning.md`.

## On-Demand Guides (read when needed — `~/claude-knowledge/guides/`)
- `guides/vm-routing.md` — VM vs local routing rules — read when delegating builds, tests, or thinking tasks
- `guides/captain.md` — LinkedIn plugin/tool priority — read when selecting MCP tools
- `guides/insights-rules.md` — LinkedIn-specific patterns (curli-first, observe-agent) — read during oncall/debugging
<!-- - `guides/test-environments.md` — DELETED: expired creds, duplicated in greenhouse-e2e recipe -->
<!-- - `guides/behavioral-gates.md` — Eval-driven behavioral rules — approach selection, tool selection -->
- `guides/proactive-suggestions.md` — When to suggest skills — reference list
- `guides/compound-learning.md` — Insight lifecycle, outcome tracking, dream cycle
- `guides/engineering-pipeline.md` — 6-phase engineering pipeline with gates
- `guides/skill-tiers.md` — Skill tier definitions for routing
