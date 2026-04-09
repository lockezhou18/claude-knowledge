---
name: Self-improving eval system architecture
description: How the eval system, compound learning, Auto Memory, and Auto Dream integrate. What lives where and why.
type: project
originSessionId: 27db5d4c-f39d-4ca8-b029-b22a12079f15
---
## Three-Layer Architecture

### Layer 1: Auto Memory + Auto Dream (Anthropic Native)
**What lives here:** Summaries, preferences, graduated knowledge, eval findings.
**Format:** Markdown files with YAML frontmatter in memory/.
**Who maintains:** Auto Dream consolidates automatically (24hrs + 5 sessions).
**What should migrate here:**
- Graduated insights (promoted from compound learning)
- Eval findings (behavioral gates summary, principle scores)
- User preferences and feedback rules
- Project context and active work
- Workflow rules

**What should NOT live here:**
- Raw data (JSONL manifests, verdict JSONs, log files)
- Code (pipeline.py, hooks, skills)
- Search indexes (manifest.jsonl, manifest-hot.jsonl)
- Detailed eval artifacts (full verdicts, session exports)

### Layer 2: Compound Learning + Eval (Custom, Structured Data)
**What lives here:** The intelligence engine — structured data that requires programmatic processing.
**Format:** JSONL manifests, JSON verdicts, Python pipelines.
**Who maintains:** /compound, /improve-agent, hooks.
**What stays here:**
- manifest.jsonl (search index — Auto Dream can't parse JSONL)
- Insight files with lifecycle metadata (use_count, outcome_score, status)
- Eval verdicts (structured JSON — Auto Dream would corrupt them)
- Pipeline code (pipeline.py, judge_prompt.md, failure_taxonomy.md)
- Logs (commit-log, pr-log, feedback-log, outcome-log)
- Session exports (raw transcripts for re-judging)

### Layer 3: Behavior (Skills, Hooks, Rules)
**What lives here:** The agent's capabilities and behavioral rules.
**Format:** Markdown skills, Python hooks, rule files.
**Who maintains:** User + /improve-agent + /integrate.
**What stays here:**
- Skills (commands/*.md, recipes/*.md)
- Capability skills (skills/*/)
- Hooks (hooks/*.py)
- Detailed behavioral gates (rules/behavioral-gates.md)
- VM routing, tool priority rules

## Data Flow Between Layers

```
Layer 3 (Behavior)                Layer 2 (Intelligence)           Layer 1 (Memory)
  skills, hooks, rules              insights, eval, logs            Auto Memory files
       │                                  │                               │
       │ skill invoked                    │ insight created               │ Auto Dream
       │ during session                   │ during /compound              │ consolidates
       ▼                                  ▼                               ▼
  [SESSION happens]              [Compound learning]              [Auto Dream cycle]
       │                                  │                               │
       │ session transcript               │ graduate insight              │ prune stale
       ▼                                  ▼                               ▼
  Layer 2: eval judges          Layer 1: write memory file       Layer 1: clean index
  sessions, produces            for graduated insight              merge overlaps
  verdicts + findings                                              fix dates
       │                                                                  │
       │ improvement found                                                │
       ▼                                                                  ▼
  Layer 3: update gate          Layer 1: update eval-*.md         Next session starts
  Layer 1: update memory        Auto Dream will consolidate       with cleaner memories
```

## Migration Plan: What to Move Where

### Move TO Auto Memory (Layer 1):
1. rules/MEMORY.md engineering principles → memory/engineering-principles.md (ALREADY DONE)
2. rules/insights-rules.md → memory/debugging-preferences.md (consolidate with existing feedback)
3. Graduated insights → memory/*.md (flow: compound learning graduates → writes memory file)
4. Eval findings → memory/eval-*.md (ALREADY DONE for gates + principles)
5. Active work context → memory/ (Auto Dream can maintain this)

### Keep in Compound Learning (Layer 2):
- manifest.jsonl — Auto Dream would break the JSONL format
- Insight files with scoring metadata — Auto Dream doesn't understand use_count/outcome_score
- Verdict JSONs — structured data, not prose
- Pipeline code — not memory
- Session exports — raw data for re-judging

### Keep in Behavior (Layer 3):
- Skills — these are instructions, not memories
- Hooks — these are code, not memories
- Detailed behavioral-gates.md — too detailed for memory, loaded by scout hook
- VM routing — operational rule, not memory

## Key Principle
Auto Memory = the WHAT (facts, preferences, findings).
Compound Learning = the HOW (scoring, lifecycle, search).
Eval = the WHY (measurement, classification, improvement).
Behavior = the DO (skills, hooks, rules).

Auto Dream consolidates the WHAT. Our systems manage the HOW/WHY/DO.
