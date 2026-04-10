# Dream — Memory Consolidation

Run the full dream cycle: mechanical consolidation (dream.py) followed by intelligent review (LLM-powered). Use overnight via VM cron, or manually when you want to consolidate now.

**Usage:** `/dream` or `/dream --quick` (skip intelligent phase)

## Phase 1: Mechanical (dream.py)

Run the standalone dream script — deterministic, no LLM calls:

```bash
python3 ~/projects/compound-learning-ecosystem/memory-migration/scripts/dream.py
```

This handles:
- **NREM**: Score staging insights from outcome-log.jsonl
- **REM**: Graduate (score>=2 + uses>=3), prune (score<-2), flag stale (>90 days)
- **SORT**: Classify Claude's flat writes in memory/ root into correct subdirs
- **REBUILD**: Rebuild all MEMORY.md indexes (global + projects + rules/guides)
- **PROJECTS**: Process per-project memories (staleness, duplicates)
- **SYNTHESIZE**: Cross-project pattern detection, insight↔project linking

Report the results to the user after running.

## Phase 2: Intelligent Review (LLM-powered)

After dream.py runs, review the results and do what the script can't:

### 2a. Sort Ambiguous Files
Check if dream.py left any unsorted files (reported in its output as "UNSORTED"). For each:
- Read the file content
- Determine the correct subdirectory based on semantic understanding
- Move it there
- If it's project-specific, identify which project

### 2b. Review Stale Content
For any files flagged stale by dream.py:
- Read the file
- Check if the content is still accurate (read referenced code files, check if APIs/patterns still exist)
- If still valid: update `last_verified` date
- If outdated: update the content, or mark for user review
- If obsolete: suggest removal to the user

### 2c. Cross-Project Synthesis
Look for patterns that dream.py's keyword matching might miss:
- Read project memories from the top 2-3 active projects
- Identify recurring themes, repeated feedback, common gotchas
- For each pattern found in 2+ projects:
  - Check if a staging insight already covers it
  - If not, draft a new insight: "When [situation], do [action] because [reason]"
  - Write to `~/claude-knowledge/learnings/staging/` with proper frontmatter
  - Add to manifest.jsonl

### 2d. Memory Quality Check
Scan memory/MEMORY.md (the global index):
- Are all links valid? (check files exist)
- Are descriptions helpful? (update empty ones)
- Is the index under 200 lines?
- Any sections getting too large? (suggest splitting)

### 2e. Graduation Candidates
Check staging insights approaching graduation threshold:
- List insights with use_count >= 2 OR outcome_score >= 1.5
- For each, assess: is this ready to graduate, or does it need more validation?
- Report candidates to user

## Phase 3: Report

Present a summary:

```
## Dream Report

### Mechanical (dream.py)
- Outcomes processed: N
- Graduated: N insights
- Pruned: N insights
- Stale flagged: N
- Files sorted: N
- Cross-project patterns: N

### Intelligent Review
- Ambiguous files resolved: N
- Stale content reviewed: N (N updated, N still valid, N suggested removal)
- New insights synthesized: N
- Broken links fixed: N
- Graduation candidates: [list]

### Next Session
- [What to watch for based on dream findings]
```

## When to Use

- **Manual**: `/dream` after a long session or when switching contexts
- **VM cron**: Runs nightly at 3:47am (mechanical only by default)
- **Lazy trigger**: Scout hook suggests `/dream` if last dream was >36h ago
- **After `/compound`**: Good to pair — compound captures session learnings, dream consolidates across sessions

## Options

- `/dream` — Full cycle (mechanical + intelligent)
- `/dream --quick` — Mechanical only (dream.py), skip intelligent review
- `/dream --review-only` — Skip dream.py, just do intelligent review on current state
- `/dream --project <name>` — Focus on a specific project's memories
