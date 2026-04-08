# Eureka — Capture a Breakthrough

Save a breakthrough discovery — a novel solution, non-obvious approach, or fundamental insight that changes how things should be done. Eurekas are rare and high-value. They often lead to architecture changes, new tools, or significant productivity improvements.

**Usage:** `/eureka [the breakthrough]`

If no argument, ask: "What did you discover that changes things?"

## Skill Family: Knowledge Capture (Tier 1)

```
/learn (fact, +1.0) → /aha (connection, +1.5) → /eureka (breakthrough, +2.0)
```

- **Chains from:** `/aha` (when a connection reveals something fundamental), `/investigate` (when fix reveals a better paradigm)
- **Chains to:** memory/rules promotion (immediate candidate), `/share` (team-level impact)
- **Called by:** `/compound` (retrospective)
- **De-escalate to `/aha`** if on reflection it connects dots but doesn't change the approach
- **De-escalate to `/learn`** if on reflection it's a single non-obvious fact
- **Graduation:** immediate candidate — ask user at capture time if it should promote to `memory/` or `~/.claude/rules/`

## What Makes a Eureka Different

- `/learn` = a fact: "Config X has value Y"
- `/aha` = a connection: "Problem A and problem B share root cause C"
- `/eureka` = a breakthrough: "We can eliminate the entire class of problem by doing Z instead"

Eurekas are about finding a fundamentally better way — not just fixing a bug or connecting dots, but discovering an approach that makes previous approaches obsolete.

## Step 1: Capture the Breakthrough

Ask the user (if not already clear):
- What's the new approach or discovery?
- What does it replace or make unnecessary?
- Why is this non-obvious? (What did people assume before that turned out wrong?)
- How big is the impact? (One service? All services? The team's workflow?)

## Step 2: Validate the Insight

Before saving, do a quick sanity check:
- Search `~/.claude/learnings/manifest.jsonl` — has someone already documented this?
- Search the codebase — is there evidence this was tried before and abandoned? Why?
- Search company knowledge (Jira, Confluence) — any prior art or design docs about this approach?

If prior art exists, present it to the user. The eureka might still be valid (maybe the prior attempt was abandoned for reasons that no longer apply), but the user should know.

**Check the /aha chain:** Did this eureka emerge from a pattern captured via `/aha`? If so, link it: set `emerged_from: "aha-id"` in frontmatter. This traces the full knowledge lifecycle: learns → aha → eureka.

## Step 3: Write the Insight

Write to `~/.claude/learnings/insights/knowledge-track/` with:
- `type: semantic`
- `severity: critical` or `high` — eurekas are always high-impact
- `rot_rate: slow` or `permanent` — breakthroughs are durable knowledge
- Tags: relevant domain tags + `eureka` tag
- `origin_skill: eureka`
- Add `paths` if this applies to specific code areas
- Add `emerged_from` if this traces back to an `/aha`

**Body format:**
```markdown
## Breakthrough
One-sentence summary of what was discovered.

## The Old Way
How things were done before. What was assumed. Why it was limiting.

## The New Way
The new approach. Why it works. Why it's fundamentally better, not just incrementally.

## Impact
- What it replaces or makes unnecessary
- Estimated scope: one service / team-wide / org-wide
- What needs to change to adopt this

## Risks & Caveats
- What could go wrong with the new approach
- Edge cases where the old way might still be needed
- Migration considerations

## Next Steps
Concrete actions to put this breakthrough into practice.
```

## Step 4: Flag for Promotion (Immediate Graduation)

Eurekas skip the normal graduation path:
- Always add to `manifest-hot.jsonl`
- If impact is team-wide, set `visibility: "team"` (for future team sharing via `/share`)
- **Ask the user immediately:** "Should this become a permanent rule in memory or CLAUDE.md?"
  - If yes → write to `memory/` or update `~/.claude/rules/MEMORY.md` directly
  - If not yet → keep in insights with `graduation_candidate: true`
- If it supersedes an existing insight, set `superseded_by` on the old one

## Step 5: Check if This Changes Existing Rules

Read `~/.claude/rules/MEMORY.md`. Does this eureka contradict or improve any existing rule or principle? If so, suggest the update to the user.

Also check: does this eureka suggest a new **skill**? If the breakthrough is a reusable workflow pattern, suggest `/integrate` to wire it into the ecosystem.

## Step 6: Log Feedback Signal

`/eureka` = +2.0 signal (strongest). Append to `~/.claude/learnings/logs/feedback-log.jsonl`:
```json
{"ts": "ISO timestamp", "signal": 2.0, "act": "SKILL_INVOCATION", "dimension": "research_depth", "agent_action": "work that produced this breakthrough", "user_context": "/eureka invoked", "skill": "eureka"}
```

Retroactively score ALL behavioral dimensions active in the preceding work at +2.0 — the approach that led to a eureka is worth reinforcing across the board.

## Step 7: Confirm

Tell the user:
- The breakthrough captured
- Impact assessment
- The full knowledge chain if traceable: `/learn` facts → `/aha` pattern → `/eureka` breakthrough
- Whether any existing insights are superseded
- Suggested next steps to put it into practice
- Whether any rules should be updated
- If team-wide impact: suggest `/share`
