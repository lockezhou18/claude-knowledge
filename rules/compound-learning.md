---
description: "Compound learning system spec — insight lifecycle, search strategy, hooks. Loaded on demand during /compound, SessionEnd, and insight operations."
globs:
  - "**"
---

# Compound Learning System (Agent-Managed)
The agent (Claude) owns the knowledge base. The human works; the agent learns around them.
See ~/.claude/learnings/SCHEMA.md for the full data model.

## How the Agent Searches (see SCHEMA.md for full details)

**Step 1: Classify task type** from user prompt (debug/implement/refactor/configure/investigate/review/migrate/oncall). This determines which tracks to search and which tags to boost.

**Step 2: Tiered retrieval:**
1. **Tier 1 — Briefing (1 call):** Read `agent-briefing.md`. Pre-compiled. Answers most prompts.
2. **Tier 2 — Manifests (2-4 calls):** `manifest-hot.jsonl` > `manifest.jsonl`. Score with three-signal formula: `(1.0 x recency) + (2.5 x relevance) + (1.5 x importance)`. Read top 3-5 matches.
3. **Tier 3 — Company knowledge:** Jira, Confluence, Slack, GitHub Pages.
4. **Tier 4 — External knowledge:** Official docs, engineering blogs, research papers. See `authority-sources.md`.

**Step 3: Score and rank** using:
- **Recency:** exponential decay based on `rot_rate` (permanent/slow/medium/fast/volatile)
- **Relevance:** tag Jaccard similarity + keyword overlap + repo match (no embeddings needed)
- **Importance:** outcome_score normalized to 0-1
- **Episodic boost** (debug/oncall only): situation matching on error patterns, repo, file paths

**Step 4: Path-scoped filtering.** Insights with `paths` globs only surface when working in matching directories.

The UserPromptSubmit hook automates Steps 1-2. During Phase 1 (Research), go deeper manually.

## How the Agent Writes
- Every insight file gets YAML frontmatter (id, track, repos, tags, severity, dates, scores, status)
- Every insight gets a one-line entry in manifest.jsonl (the search index)
- Format insights as: "When [situation], do [action] because [reason]"
- Check manifest for overlap before writing. One source of truth per topic.

## How the Agent Maintains
- **Outcome tracking:** During work, log to outcome-log.jsonl when an insight helps (+1) or misleads (-1). This updates outcome_score.
- **Graduation:** use_count >= 3 AND outcome_score >= 2.0 > promote from staging to memory/insights/ (permanent). Handled by dream.py overnight.
- **Pruning:** outcome_score < -2 > set status="pruned", remove from active searches. Handled by dream.py.
- **Staleness:** last_verified > 90 days with code references > flag as stale, verify before using. Handled by dream.py.
- **Meta-learning:** When the system gives bad advice, log it, fix the source insight, and check if the pattern is systemic.

## Multi-Session Continuity
- `active-work.md` tracks multi-day initiatives (not overwritten between sessions)
- `last-session-summary.txt` is the quick handoff for the next session
- The scout hook reads both at session start

## Automated Hooks
- **UserPromptSubmit:** Knowledge scout searches before every prompt (tiered loading)
- **PostToolUse (git commit):** Logs commit context to commit-log.jsonl
- **PostToolUse (gh pr create):** Logs PR + runs multi-persona review (correctness, security, performance, maintainability, API contract, data migration — conditional activation based on diff content, confidence-gated findings)
- **SessionEnd:** Full compound phase — retrospective, insight generation, manifest maintenance, graduation, pruning, freshness audit, skill proposals, watchlist check

## Insight Lifecycle

```
~/.claude/learnings/
├── manifest.jsonl           # SEARCH INDEX — agent reads this first, not every file
├── SCHEMA.md                # Frontmatter spec for insight files
├── staging/                 # Pre-graduation insights with scoring metadata
├── logs/                    # Raw event stream (auto-trimmed to 50 entries)
│   ├── commit-log.jsonl
│   ├── pr-log.jsonl
│   ├── review-log.jsonl
│   ├── outcome-log.jsonl
│   └── dream-log.jsonl
├── insights/                # Legacy location (migrating to staging/)
│   ├── bug-track/           # Symptoms > Root Cause > Fix > Prevention
│   └── knowledge-track/     # Context > Guidance > When-to-apply
├── retrospectives/
│   ├── active-work.md       # Multi-day initiative context (persists across sessions)
│   ├── last-session-summary.txt  # handoff to next session
│   └── last-dream.txt       # what dream.py changed overnight
└── reviews/                 # Archived PR review reports
```

New insights > `staging/{id}.md` > score via outcome tracking > graduate to `memory/insights/` when threshold met > or prune when score negative > or flag stale when >90 days unverified.
