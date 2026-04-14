---
id: eureka-007
track: knowledge
type: semantic
repos: [*]
tags: [eureka, context-repo, team-sharing, knowledge-management, claude-code, onboarding, productivity, force-multiplier]
severity: critical
created: '2026-04-04'
last_verified: '2026-04-04'
use_count: 28
outcome_score: 0.0
rot_rate: permanent
status: active
origin_skill: eureka
emerged_from: 'eureka-006'
graduation_candidate: True
visibility: team
---

## Breakthrough

A **context repo** (git repo with `.claude/CLAUDE.md` + skills + docs + test data + runbooks) turns one person's deep investigation into the entire team's starting point. Anyone who `git clone`s and opens with Claude Code instantly inherits weeks of accumulated knowledge — architecture mental models, debugging skills, verified commands, design doc references — without reading a single doc.

## The Old Way

Knowledge sharing was lossy and slow:
- **Confluence pages**: Written once, stale in weeks, nobody reads the 30-page design doc
- **Slack threads**: Context buried in scrollback, unsearchable after 90 days
- **Onboarding docs**: "Read these 15 pages" → new engineer is productive in 2-3 weeks
- **Tribal knowledge**: "Ask Sarah, she knows how the writeback works"
- **Personal notes**: Each engineer accumulates their own debugging recipes, never shared

When someone leaves or switches projects, their knowledge evaporates.

## The New Way

Package everything into a **context repo** with this structure:
```
.claude/CLAUDE.md          ← Auto-loaded: instant project context
.claude/commands/*.md      ← Skills: team capabilities
docs/                      ← Design docs: why things are the way they are
docs/architecture/         ← Mental models: how to think about the system
docs/onboarding/           ← 10-minute guide: minimum viable understanding
test-data/                 ← Verified commands: copy-paste-ready
figma/                     ← Design screenshots: what the user sees
runbooks/                  ← Debugging: when things break
bug-bash/                  ← Testing: how to verify
```

**What makes it different from a wiki:**
1. **`.claude/CLAUDE.md` auto-loads** — Claude Code reads it on every session. No "did you check the wiki?"
2. **Skills are executable** — `/action-writeback` isn't a doc, it's a capability. New engineer can debug writeback on day 1.
3. **Git-native** — PRs for updates, blame for history, branches for experiments. No wiki permission dance.
4. **Portable** — works offline, works in any Claude Code session, works across IDEs
5. **Composable** — skills from the context repo compose with personal skills and global skills

## Impact

- **Onboarding**: 2-3 weeks → 10 minutes (clone repo, open with Claude Code, ask questions)
- **Debugging**: "Ask Sarah" → `/action-writeback` or `runbooks/debugging.md` (Sarah's knowledge encoded)
- **Bug bash**: Manual test case writing → design-driven test matrix ready to go
- **Knowledge retention**: Engineer leaves → knowledge stays in the repo
- **Cross-team collaboration**: FE engineer sees backend architecture, backend sees Figma designs

## The Pattern (Reusable)

Any team can create a context repo for any major initiative:
1. **Investigate deeply** (one person does the research)
2. **Encode as skills** (turn debugging recipes into executable `/commands`)
3. **Structure as docs** (architecture, design, onboarding, runbooks)
4. **Package in git** (`.claude/CLAUDE.md` as the entry point)
5. **Share with team** (`linkedin-context` org, internal visibility)

Cost: ~2 hours to package (mostly automated by the agent).
Value: Every team member saves days of ramp-up, permanently.

## Proof of Concept

`linkedin-context/connected-projects-shared` — created 2026-04-04:
- 25 files, 3451 lines
- 5 executable skills
- 3 design docs (backend, IP, frontend)
- 3 architecture docs (system map, 3 pipelines, frontend components)
- Full test data reference + Greenhouse sandbox setup
- 6 Figma prototype screenshots
- 6 E2E test cases
- 2 runbooks (debugging + common failures)
- 1 onboarding guide ("Phase 2 in 10 minutes")

## The Knowledge Chain

```
/learn (50+ individual facts over 3 weeks)
  → /aha (3 pipelines pattern)
    → /eureka (cross-boundary unified view)
      → /eureka (context repo = force multiplier)
```

Each level amplified the value:
- Individual facts → useful to one person in one session
- Pattern → useful to one person across sessions
- Unified view → useful to one person across boundaries
- Context repo → **useful to the entire team, permanently**
