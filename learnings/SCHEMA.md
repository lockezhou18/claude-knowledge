# Knowledge Base Schema — Agent Reference
# Version: 2.0

This file defines how the agent reads, writes, scores, and maintains the knowledge base.
The human never needs to touch this — the agent manages everything.

## Agent Retrieval (READ PATH)

### Session start: Read ONE file
```
~/.claude/learnings/agent-briefing.md    ← 1 tool call. Pre-compiled. Has everything.
```

### Need more: Tiered escalation
```
Tier 1: agent-briefing.md                ← always (1 call)
Tier 2: manifest-hot.jsonl               ← if briefing doesn't cover topic (1 call)
Tier 3: manifest.jsonl                   ← if hot doesn't match (1 call)
Tier 4: Individual insight files          ← top 3-5 matches only
Tier 5: Memory files                     ← graduated permanent knowledge
Tier 6: Company knowledge                ← Jira/Confluence/Slack/GitHub Pages
Tier 7: External knowledge               ← docs/papers/blogs (see authority-sources.md)
```

### Task-Type Router
Classify user prompt first, then load the right knowledge subset:

| Task Type | Trigger Words | Load Which Tracks | Boost Tags |
|-----------|--------------|-------------------|------------|
| `debug` | fix, bug, error, crash, exception, broken | bug, knowledge | error, fix, workaround |
| `implement` | add, create, build, new, feature, endpoint | knowledge, review | pattern, api, architecture |
| `refactor` | refactor, clean up, simplify, extract, rename | knowledge | pattern, style, structure |
| `configure` | config, setup, deploy, ci, build, docker | knowledge, bug | config, deploy, build |
| `investigate` | how, what, where, explain, understand | knowledge, bug | (broad) |
| `review` | review, check, audit, test, quality | review, bug | pattern, testing, style |
| `migrate` | upgrade, migrate, deprecate, version | knowledge | migration, version, upgrade |
| `oncall` | alert, pager, incident, outage, PEM | bug, knowledge | oncall, monitoring, debugging |

Default to `investigate` if uncertain (broadest retrieval).

## Retrieval Scoring

### Three-Signal Score (for ranking insights)
```
score = (1.0 × recency) + (2.5 × relevance) + (1.5 × importance)
```

**Recency** (exponential decay):
```
recency = decay_rate ^ days_since_last_verified
```

Decay rates by content type:
| rot_rate | decay_rate | Half-life | Use for |
|----------|-----------|-----------|---------|
| permanent | 0.9999 | ~19 years | Fundamental principles, architecture decisions |
| slow | 0.999 | ~693 days | Stable patterns, design rationale |
| medium | 0.995 | ~138 days | General knowledge (DEFAULT) |
| fast | 0.990 | ~69 days | API specifics, library versions, config values |
| volatile | 0.980 | ~34 days | Workarounds, sprint context, temp fixes |

**Relevance** (without embeddings):
```
relevance = 0.4 × tag_jaccard + 0.35 × keyword_overlap + 0.25 × repo_match
```
- `tag_jaccard` = |insight_tags ∩ query_tags| / |insight_tags ∪ query_tags|
- `keyword_overlap` = shared meaningful tokens / query tokens
- `repo_match` = 1.0 if repo matches, 0.0 if not

**Importance:**
```
importance = outcome_score / 10.0    (normalized 0-1)
```
For bug-track insights during debug tasks, boost importance weight to 2.5.

### Episodic Boost (for debug/oncall tasks)
When task type is `debug` or `oncall`, apply situation matching for episodic insights:
- Error pattern match: +5.0 (exact), +2.0 (same error class)
- Repo match: +1.5
- File path overlap: +0.3 per matching path segment
- Context word overlap: up to +2.0

## Memory Types

### Episodic Memory (type: episodic)
Records of specific past incidents — what happened, what was tried, what worked.
Retrieved by **situation similarity** (error patterns, file paths, repo context).
```yaml
type: episodic
situation:
  error_pattern: "java.lang.OutOfMemoryError"
  context: "gradle build with >50 subprojects"
resolution:
  steps: ["Add -Xmx4g to gradle.properties", "Enable parallel builds"]
  outcome: "Build dropped from 45min to 12min"
```

### Semantic Memory (type: semantic)
Distilled patterns, rules, architecture facts — generalized from experience.
Retrieved by **topic matching** (tags, keywords, repo).
```yaml
type: semantic
# Standard knowledge-track body (Context, Guidance, When to Apply)
```

### Reflection: Episodic → Semantic Synthesis
When 3+ episodic memories share a pattern (same tags, same repo area):
1. Identify the common thread across incidents
2. Generate a semantic insight that captures the generalized pattern
3. Mark episodic sources as `synthesized_into: "new-semantic-id"`
4. The semantic insight is more valuable (higher signal-to-noise) than individual episodes

## Insight File Format

### YAML Frontmatter (required fields)
```yaml
---
id: "unique-short-id"
track: "bug" | "knowledge" | "review" | "decision" | "anti-pattern"
type: "episodic" | "semantic"
repos: ["repo-name"] or ["*"]
tags: ["tag1", "tag2", ...]         # 3-7 tags, from taxonomy when possible
paths: ["src/api/**/*.java"]        # optional: glob patterns for path-scoped loading
severity: "critical" | "high" | "medium" | "low"
rot_rate: "permanent" | "slow" | "medium" | "fast" | "volatile"
created: "YYYY-MM-DD"
last_verified: "YYYY-MM-DD"
use_count: 0
outcome_score: 0.0                  # +1 when helped, -1 when wrong
status: "active" | "stale" | "graduated" | "superseded" | "pruned"
# Lifecycle fields
graduated_to: ""                    # path in memory/ if promoted
superseded_by: ""                   # id of newer insight that replaces this
contradicts: ""                     # id of insight this contradicts
synthesized_from: []                # ids of episodic insights this was synthesized from
# Scaling fields (for future use)
visibility: "personal"              # "personal" | "team" | "org" — default personal
schema_version: 2                   # for future schema migrations
---
```

### Additional fields for episodic insights (bug-track)
```yaml
situation:
  error_pattern: "string"           # regex or exact error text
  context: "string"                 # what was happening when this occurred
resolution:
  steps: ["step1", "step2"]
  outcome: "string"
```

### Additional fields for review-track (future: Tech Lead)
```yaml
trigger: "reviewing PR that modifies X"  # when to apply this review heuristic
checklist: ["item1", "item2"]
```

### Additional fields for decision-track (future: Architect)
```yaml
decision_status: "proposed" | "accepted" | "deprecated"
supersedes: ""                      # id of previous decision this replaces
```

## Body Format

### Bug-track (episodic):
```markdown
## Symptoms
What you observe. Include error messages, log patterns, behavior.

## Root Cause
Why it happens (5 Whys applied). Be specific.

## Fix
Exact steps to resolve.

## Prevention
"When [situation], do [action] because [reason]."
```

### Knowledge-track (semantic):
```markdown
## Context
When this applies and why it matters.

## Guidance
What to do. Concrete, actionable, with code examples if relevant.

## When to Apply
Specific triggers: "When you see X" or "When working on Y."
```

### Anti-pattern track:
```markdown
## Do NOT
"When [situation], do NOT [action]."

## Why Not
What happened when this was tried. Specific failure with evidence.

## Instead
What to do instead. The correct approach.

## Source
Which feedback signals or past failures generated this anti-pattern.
```

### Review-track (future):
```markdown
## Trigger
When to apply this review heuristic.

## Checklist
- [ ] Item 1 with rationale
- [ ] Item 2 with rationale

## Rationale
Why each item matters. Common failures when missed.
```

### Decision-track (future, ADR format):
```markdown
## Context
What situation prompted this decision.

## Decision
What we decided and why.

## Consequences
What follows. Trade-offs accepted.

## Alternatives Considered
What else was evaluated and why it was rejected.
```

## Manifest (manifest.jsonl)

One-line JSON per insight. Pre-computed fields for fast scoring without reading files:

```json
{
  "id": "config-cache-gotcha",
  "track": "knowledge",
  "type": "semantic",
  "repos": ["hp-ats-integration-mt"],
  "tags": ["config", "cache", "ats-provider"],
  "paths": ["**/application.src"],
  "severity": "medium",
  "rot_rate": "medium",
  "created": "2026-03-31",
  "last_verified": "2026-03-31",
  "use_count": 0,
  "outcome_score": 0.0,
  "status": "active",
  "summary_tokens": ["config", "cache", "ats", "provider", "override", "gotcha"],
  "error_pattern": "",
  "file": "insights/knowledge-track/2026-03-31-config-cache-gotcha.md"
}
```

`summary_tokens` and `error_pattern` in the manifest enable scoring without reading full files.

## Tag Taxonomy

Use standardized tags. Freeform allowed but prefer these for reliable search.

### Domain tags
`api`, `auth`, `build`, `cache`, `ci-cd`, `config`, `data-model`, `database`, `debugging`, `deploy`, `grpc`, `integration`, `logging`, `metrics`, `migration`, `monitoring`, `networking`, `oncall`, `performance`, `proto`, `rest-li`, `security`, `serialization`, `testing`

### System tags (LinkedIn-specific, will grow)
`connected-projects`, `hiring-platform`, `talent-solutions`, `hp-ats-integration`, `mcm`, `d2`, `espresso`, `kafka`, `samza`, `venice`, `rest-li`, `parseq`

### Problem type tags
`null-pointer`, `race-condition`, `timeout`, `memory-leak`, `config-error`, `dependency-conflict`, `schema-mismatch`, `auth-failure`, `data-loss`, `retry-storm`, `n-plus-one`, `deadlock`

### Pattern tags
`retry-pattern`, `circuit-breaker`, `cache-invalidation`, `idempotency`, `graceful-degradation`, `feature-flag`, `migration-pattern`, `rollback-strategy`, `bulk-processing`, `pagination`

Tags are lowercase, hyphenated. 3-7 per insight. New tags allowed when no existing tag fits.

## Agent Maintenance Duties

### After each session (SessionEnd hook):
1. Write new insights with full frontmatter + manifest entry
2. Increment `use_count` and update `outcome_score` for insights used this session
3. Reflection: if 3+ episodic insights share tags/repo, synthesize a semantic insight
4. Staleness: flag insights past their rot_rate threshold as `status: stale`
5. Pruning: set `status: pruned` for insights with `outcome_score < -2`
6. Graduation: promote insights with `use_count >= 3 AND outcome_score >= 2.0` to memory/
7. Contradiction check: if new insight contradicts existing, set `contradicts` field and resolve
8. Rebuild `agent-briefing.md` and `manifest-hot.jsonl`
9. Update `retrospectives/active-work.md`
10. Trim JSONL logs to last 50 entries

### Scaling milestones (auto-triggered):
- At ~200 insights: Shard manifests by year (`manifest-2026.jsonl`, `manifest-2027.jsonl`)
- At ~500 insights: Generate tag index files under `indexes/by-tag/` and `indexes/by-repo/`
- At team adoption: Split personal/team layers, add PR-based review for team insights

## Directory Structure (current + future)

```
~/.claude/learnings/
├── agent-briefing.md          # Pre-compiled for session start (1 file = full context)
├── manifest.jsonl             # Full search index
├── manifest-hot.jsonl         # Recently used / high-score subset
├── SCHEMA.md                  # This file
├── authority-sources.md       # External research guide
├── logs/                      # Raw event stream (auto-trimmed)
│   ├── commit-log.jsonl
│   ├── pr-log.jsonl
│   ├── review-log.jsonl
│   └── outcome-log.jsonl
├── insights/                  # Active insights with YAML frontmatter
│   ├── bug-track/             # Episodic: Symptoms → Root Cause → Fix
│   ├── knowledge-track/       # Semantic: Context → Guidance → When
│   ├── review-track/          # Future: Review heuristics and checklists
│   └── decision-track/        # Future: Architecture Decision Records
├── retrospectives/
│   ├── active-work.md         # Multi-day initiative tracker
│   └── last-session-summary.txt
├── reviews/                   # Archived PR review reports
│
│ # Future (scaling):
├── archive/                   # Stale insights moved here by year
│   └── 2026/
├── indexes/                   # Auto-generated fast-lookup indexes
│   ├── by-tag/                # One JSONL per top tag
│   └── by-repo/               # One JSONL per repo
└── team/                      # Future: shared team knowledge (git-based)
    ├── published/
    └── proposals/
```
