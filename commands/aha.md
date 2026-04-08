# Aha — Capture a Connection

Save a moment of synthesis — when you see a pattern across incidents, a connection between systems, or realize that separate problems share a root cause. This is how episodic memories become semantic wisdom.

**Usage:** `/aha [the connection you see]`

If no argument, ask: "What pattern or connection did you just notice?"

## Skill Family: Knowledge Capture (Tier 1)

```
/learn (fact, +1.0) → /aha (connection, +1.5) → /eureka (breakthrough, +2.0)
```

- **Chains to:** `/eureka` (when connection reveals a fundamentally better approach)
- **Chains from:** `/learn` (when 3+ learns cluster on same topic)
- **Called by:** `/investigate` (root cause matches prior incidents), `/compound` (retrospective)
- **Escalate to `/eureka`** when the connection doesn't just explain — it changes the approach
- **De-escalate to `/learn`** if on reflection it's a single fact, not a cross-cutting pattern
- **Graduation:** fast-track — `use_count >= 2 AND outcome_score >= 1.5` (patterns are inherently higher value)

## What Makes an Aha Different from a Learn

- `/learn` = a fact: "Service X uses config Y"
- `/aha` = a connection: "The timeout in service X and the retry storm in service Y are caused by the same upstream bottleneck"
- Aha insights are ALWAYS `type: semantic` — they're generalizations synthesized from specific observations.

## Step 1: Capture the Connection

Ask the user (if not already clear):
- What separate things are connected?
- What's the common thread or root cause?
- What does this mean for future work?

## Step 2: Find the Source Episodes

Search `~/.claude/learnings/manifest.jsonl` for the episodic insights that this aha connects. These are the raw observations that led to the synthesis.

Link them: set `synthesized_from: ["episode-id-1", "episode-id-2", ...]` in the new insight.

**Auto-suggest sources:** If the user just says the pattern without listing sources, search the manifest by overlapping tags and repos to find likely candidates. Present them: "I found these related learns — are these what you're connecting?"

## Step 3: Write the Insight

Write to `~/.claude/learnings/insights/knowledge-track/` with:
- `type: semantic`
- `severity`: based on how impactful the connection is
- `rot_rate`: usually `slow` or `permanent` — patterns decay slower than facts
- Tags: combine tags from all source episodes + add `pattern` tag
- `origin_skill: aha`

**Body format:**
```markdown
## Pattern
The generalized pattern: "When [A happens] and [B happens], the root cause is usually [C]."

## Evidence
- [Episode 1]: what happened, link to insight
- [Episode 2]: what happened, link to insight
- [Episode N]: ...

## Implication
What this means going forward. How should future work account for this pattern?

## When to Apply
Specific triggers: "When you see X in combination with Y, suspect Z."
```

## Step 4: Update Source Episodes (Bidirectional Linking)

For each source episodic insight, update its frontmatter:
- Add `synthesized_into: "new-aha-id"` — creates aha → episodes link
- Add `feeds_into: "new-aha-id"` on any `/learn` insights that fed this — creates learn → aha forward link

This bidirectional linking means:
- Future sessions finding a `/learn` can see it was synthesized into a broader pattern
- Future sessions finding the `/aha` can trace back to the raw evidence

## Step 5: Update Manifest

Append to `manifest.jsonl` and `manifest-hot.jsonl` (aha insights are always hot — they're high-signal).

## Step 6: Log Feedback Signal

`/aha` = +1.5 signal. Append to `~/.claude/learnings/logs/feedback-log.jsonl`:
```json
{"ts": "ISO timestamp", "signal": 1.5, "act": "SKILL_INVOCATION", "dimension": "research_depth", "agent_action": "investigation that surfaced this pattern", "user_context": "/aha invoked", "skill": "aha"}
```

## Step 7: Confirm

Tell the user:
- The pattern captured
- Which episodes it connects (with bidirectional links established)
- The "When to Apply" trigger for future sessions
- If the connection seems to reveal a fundamentally better approach: suggest `/eureka`
