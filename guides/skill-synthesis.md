# Skill Synthesis — Claude-Knowledge × Gstack × Custom

How to layer three skill systems without collision. Captured 2026-04-18 after comparing our commands against Garry Tan's gstack and our own custom skills.

## Three Systems, Different Strengths

| Source | Strength | Weakness |
|---|---|---|
| **claude-knowledge** (this repo) | Tier/chain capture (`/learn` → `/aha` → `/eureka` → `/compound`), differentiated pre-work (`/explore` / `/scope` / `/find`), smart orchestrator (`/kickoff`) | Some commands (`/investigate`, `/ship`, oncall skills) are LinkedIn-specific |
| **gstack** (`github.com/garrytan/gstack`) | YC-flavored design (`/office-hours`), safety guardrails (`/careful`/`/freeze`/`/guard`), review roles (plan-ceo-review, plan-eng-review) | Heavy telemetry preamble, 34 commands creates cognitive load, `/retro` + `/learn` bloated vs ours |
| **Custom** (per-machine) | Project-specific (`/intel`, `/go-review`, `/lfg` pipeline, `/debug-api`) | Not globally portable — shape around the project, not the generic workflow |

## Synthesis Recommendations

### Cluster 1: Root-cause debugging

**Winner**: claude-knowledge's `/investigate` — parallel sub-agents mode (code / logs / config) + Step 0 past-knowledge check + 5 Whys + evidence-first.

Gstack's `/investigate` is linear 4-phase with bloated preamble. Our `/debug-api` is narrower (API-only).

**Caveat for non-LinkedIn users:** claude-knowledge's `/investigate` references LinkedIn tools (Espresso, observe-agent, fabric). Generalize by replacing with equivalents for your stack (e.g., Postgres for Espresso, Grafana for observe-agent).

### Cluster 2: Learning capture (the big unlock)

**Keep** `/compound` as end-of-session batch.
**Adopt** `/learn` / `/aha` / `/eureka` as **mid-session real-time capture** (portable, no LinkedIn refs).

The tier chain:
```
/learn (fact, +1.0)
  → /aha (connection, +1.5) when 3+ learns cluster
    → /eureka (breakthrough, +2.0) when approach changes
      → /compound (batch, end-of-session) reads staging/ files
```

`/compound` Step 0 now explicitly consumes `~/.claude/learnings/staging/{learn,aha,eureka}-*.md` — no captures lost if `/compound` fires late.

### Cluster 3: Pre-work differentiation

Use the right skill for the right intent:

| Intent | Skill | Source priority |
|---|---|---|
| "I don't know this domain" | `/explore` | External-first |
| "Map this codebase for a feature" | `/scope` | Local-first |
| "Find the root cause of this bug" | `/investigate` | Local-first |
| "Answer this with evidence" | `/research` | Mixed |
| "Has someone done this?" | `/find` | External-first |
| "Route me to the right skill" | `/kickoff` | Orchestrator |
| "Brainstorm a product idea" | `/office-hours` (gstack) | YC-style 6 Qs |

**Adopt from claude-knowledge**: `/explore`, `/scope`, `/find`, `/kickoff`
**Adopt from gstack**: `/office-hours`
**Keep**: `/research`

### Safety trio (gstack-only)

Neither claude-knowledge nor the custom stack has these. Install from gstack:

- `/careful` — warns before `rm -rf`, `DROP TABLE`, force-push, `git reset --hard`, `kubectl delete`
- `/freeze` — locks edits to a specific directory (prevents scope creep during debugging)
- `/guard` — combines `/careful` + `/freeze` for prod work

## What NOT to Install

- **gstack `/checkpoint`** — deprecated (Auto Memory handles it natively per this repo's `session-handoff` note)
- **gstack `/document-release`** — only install if you ship often and need auto-updated README/CHANGELOG
- **gstack `/retro` + `/learn`** — our `/compound` + `/learn` chain covers this better
- **gstack `/autoplan`** — depends on `/plan-*-review` family; only install if you adopt gstack's full review pipeline
- **gstack `/browse`** — overrides your existing Chrome integration; only adopt if you want to replace

## Install Script

See `install-skills.sh` in this repo for the selective install pattern (symlinks only portable commands, skips LinkedIn-specific ones when not on LinkedIn infra).
