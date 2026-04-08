# Checkpoint — Quick Knowledge Sync

Lightweight mid-session sync. Keeps the data flowing without the full /compound ceremony.
Run this at natural breakpoints — finished a bug fix, switching context, before a meeting.

**Usage:** `/checkpoint` or `/checkpoint [brief note of what just happened]`

Takes ~30 seconds. No insight generation, no synthesis, no briefing rebuild.

## What It Does

### 1. Log Feedback Signals (quick scan)
Scan the last ~10 conversation turns. For each user response, classify:
- Was it positive (+1/+2)? Log it.
- Was it a soft redirect (-0.1/-0.2)? Log it.
- Neutral? Skip.

Append to `~/.claude/learnings/logs/feedback-log.jsonl`. Don't overthink — fast classification.

### 2. Bump use_counts
Check which insights from the knowledge base were referenced or used since the last checkpoint. For each one, increment `use_count` in `~/.claude/learnings/manifest.jsonl`.

Also log to `~/.claude/learnings/logs/outcome-log.jsonl` if any insight helped (+1) or misled (-1).

### 3. Update Active Work
Append a one-liner to `~/.claude/learnings/retrospectives/active-work.md` under the current initiative:
- What was just done
- What's next

### 4. Quick Worklog Entry
Append to `~/.claude/learnings/logs/worklog.jsonl`:
```json
{"ts": "ISO timestamp", "type": "checkpoint", "summary": "[what was done]", "source": "auto"}
```

### 5. Done
Say: "Checkpoint saved." and continue working. No summary, no proposals, no ceremony.

## What It Does NOT Do
- Generate insights (that's /compound)
- Rebuild briefing (that's /compound)
- Classify every turn (just the last ~10)
- Propose skills (that's /compound)
- Run maintenance (that's /compound)
- Synthesize patterns (that's /compound)

## When to Suggest
The agent should suggest `/checkpoint` when:
- 1+ hours since last checkpoint or compound
- User just finished a task (committed, merged, resolved a ticket)
- User is switching context ("ok now let's look at...")
- User says "let me take a break" or "brb"
