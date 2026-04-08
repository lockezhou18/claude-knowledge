# Learn — Quick-Save an Insight

Save a specific insight right now without running the full compound phase. Use when you notice something worth remembering mid-session.

**Usage:** `/learn [what you learned]`

If no argument provided, ask the user: "What did you learn or notice that should be saved?"

## Skill Family: Knowledge Capture (Tier 1)

```
/learn (fact, +1.0) → /aha (connection, +1.5) → /eureka (breakthrough, +2.0)
```

- **Chains to:** `/aha` (when 3+ related learns cluster), `/compound` (end-of-session)
- **Called by:** `/investigate`, `/explore`, `/research`, `/compound`
- **Escalate to `/aha`** when you notice the insight connects multiple prior learns
- **Escalate to `/eureka`** when the insight fundamentally changes how things should be done
- **Graduation:** standard path — `use_count >= 3 AND outcome_score >= 2.0`

## Step 1: Classify the Insight

From the user's description, determine:
- **Track**: `bug` (specific incident/fix) or `knowledge` (general pattern/guidance)
- **Type**: `episodic` (this specific thing happened) or `semantic` (general principle)
- **Repos**: Which repos does this apply to? `["*"]` if global.
- **Tags**: Pick 3-7 from the taxonomy in `~/.claude/learnings/SCHEMA.md`. Use existing tags when possible.
- **Severity**: How impactful? `critical` / `high` / `medium` / `low`
- **Rot rate**: How fast will this become stale? `permanent` / `slow` / `medium` / `fast` / `volatile`
- **Origin skill**: `learn` (set `origin_skill: learn` in frontmatter)

## Step 2: Check for Overlap AND Cluster Detection

Read `~/.claude/learnings/manifest.jsonl`. Two checks:

**Overlap check:**
- **High overlap**: Update the existing insight file and manifest entry instead of creating new.
- **Moderate overlap**: Create new but add `related_to` cross-reference.
- **No overlap**: Create new.

**Cluster detection** (new):
- Count existing `/learn` insights with overlapping tags in the same repo(s).
- If **3+ related learns** already exist on the same topic area, suggest to the user:
  > "I notice 3+ related learns around [topic]. Want to `/aha` to synthesize them into a pattern?"
- Don't force it — just suggest. The user may not be ready to generalize yet.

## Step 3: Write the Insight

Write to `~/.claude/learnings/insights/bug-track/` or `knowledge-track/` with:
- Filename: `YYYY-MM-DD-short-description.md`
- Full YAML frontmatter per SCHEMA.md, including `origin_skill: learn`
- Body in the appropriate format:
  - Bug-track: Symptoms → Root Cause → Fix → Prevention
  - Knowledge-track: Context → Guidance → When to Apply
- Format the core learning as: **"When [situation], do [action] because [reason]"**

## Step 4: Update Manifest

Append one-line JSON to `~/.claude/learnings/manifest.jsonl` with all frontmatter fields + `summary_tokens` + `file` path.

If the insight is high-value (severity critical/high), also append to `manifest-hot.jsonl`.

## Step 5: Log Feedback Signal

The user invoking `/learn` is a +1.0 ACCEPTANCE signal — the preceding work produced useful knowledge. Immediately append to `~/.claude/learnings/logs/feedback-log.jsonl`:
```json
{"ts": "ISO timestamp", "signal": 1.0, "act": "SKILL_INVOCATION", "dimension": "research_depth", "agent_action": "preceding work that led to this learn", "user_context": "/learn invoked", "skill": "learn"}
```

Also retroactively score the behaviors that led to this insight — if an investigation or research phase produced the knowledge, those approaches get +1.0.

## Step 6: Confirm

Tell the user:
- Insight ID and file path
- Track/type/tags assigned
- Whether it was a new insight or an update to existing
- If cluster detected: suggest `/aha` synthesis
