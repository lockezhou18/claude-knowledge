# Compound — Close the Loop

Run Phase 6 of the engineering pipeline: extract learnings from this session and prepare the knowledge base for the next one.

## Step 0: Consume In-Session Captures (tier chain)

`/compound` is the **end-of-session batch processor** for the tier capture chain:

```
/learn (fact, +1.0)
   ↓ (escalates when 3+ learns cluster)
/aha (connection, +1.5)
   ↓ (escalates when approach changes)
/eureka (breakthrough, +2.0)
   ↓ (end-of-session)
/compound (batch synthesis + routing)
```

Before running Step 1, read any in-session captures to include them in synthesis:

- `~/.claude/learnings/staging/learn-*.md` — raw facts captured mid-session
- `~/.claude/learnings/staging/aha-*.md` — connections across learns
- `~/.claude/learnings/staging/eureka-*.md` — breakthroughs

Each will have `origin_skill: learn|aha|eureka` frontmatter and a pre-scored tier (+1.0 / +1.5 / +2.0). Treat these as **privileged input** — they were captured with intent at the moment of insight, not reconstructed after the fact.

If the user hasn't used `/learn` / `/aha` / `/eureka` this session (common), skip this step silently.

## Step 1: Gather Context

Read these files to understand what happened this session:
- `~/.claude/learnings/logs/commit-log.jsonl` (recent commits)
- `~/.claude/learnings/logs/pr-log.jsonl` (recent PRs)
- `~/.claude/learnings/logs/review-log.jsonl` (review findings)
- `~/.claude/learnings/logs/outcome-log.jsonl` (past insight outcomes)
- `~/.claude/learnings/retrospectives/active-work.md` (ongoing initiatives)
- `~/.claude/learnings/manifest.jsonl` (existing insights)
- `~/.claude/projects/-Users-bizhou/memory/MEMORY.md` (memory index)

Also check recent git history: `git log --oneline -20` in the current repo.

## Step 2: Plan vs Reality

Summarize to the user:
- What was accomplished this session
- Where you deviated from plan and why

## Step 3: Score Retrieved Insights

This is how insights earn scores and eventually graduate or get pruned. Without this step, insights accumulate retrievals but never get judged.

1. **Check what was retrieved**: Read `outcome-log.jsonl` for `"retrieved"` events from this session
2. **For each retrieved insight**, judge honestly:
   - **helped** (+1.0) — I acted on this insight and it led to a better outcome than I would have reached without it
   - **irrelevant** (0) — It was retrieved but didn't apply to what I was doing
   - **wrong** (-1.0) — Following this insight would have led me astray, or it contained outdated/incorrect information
3. **Log scored outcomes** to `outcome-log.jsonl`:
   ```json
   {"timestamp": "ISO", "insight_id": "know-XXX", "event": "scored", "delta": 1.0, "detail": "why it helped/was wrong"}
   ```
4. **Bias check**: Default to `irrelevant` (0) when uncertain. Only score `helped` if you can point to a specific action that was better because of the insight. The bar for `helped` is: "I would have done something worse without this."

**Why this matters**: The dream engine decays scores over time (Ebbinghaus). Without positive `helped` scores flowing in, every insight slowly decays to 0 and nothing ever graduates. This step is the pump that keeps the system alive.

## Step 4: Generate Insights

Identify learnings using **6 analytical perspectives** (inspired by Pluton dreaming system):

1. **Practical** — What tools, commands, patterns saved time or caused friction?
2. **Epistemic** — What new knowledge was gained about systems, APIs, architecture?
3. **Temporal** — How did things evolve during the session? What changed from start to end?
4. **Metacognitive** — Where did reasoning go wrong? What blind spots were exposed?
5. **Social/team** — What stakeholder context, team decisions, or cross-team patterns emerged?
6. **Causal** — What caused what? "X happened because Y" — the 5 Whys.

For each insight found, ask: "Would this help a future session working in the same area?"

Format each insight as: **"When [situation], do [action] because [reason]"**

Categorize:
- **Bug-track** (episodic): Symptoms → Root Cause → Fix → Prevention
- **Knowledge-track** (semantic): Context → Guidance → When to Apply

Write insight files to `~/.claude/learnings/staging/` with YAML frontmatter per `~/.claude/learnings/SCHEMA.md`. Use tags from the taxonomy. Set `rot_rate` appropriately.

Append each insight to `~/.claude/learnings/manifest.jsonl` with `summary_tokens` for search.

**Before writing**: check manifest for overlap. Update existing insight if high overlap. Don't create duplicates.

## Step 5: Reflection

Actively look for synthesis opportunities:

1. Read `~/.claude/learnings/manifest.jsonl` — group bug-track insights by shared tags
2. If 2+ episodic insights share 3+ tags, they likely share a pattern
3. **Propose the synthesis to the user** — don't auto-create. Say: "I notice [bug-X] and [bug-Y] share the same pattern: [description]. Want me to synthesize into a semantic insight?"
4. If approved, write the semantic insight with `synthesized_from: [source IDs]` and mark sources with `synthesized_into`
5. Also check: are there 2+ wrong-approach feedback signals on the same dimension? If so, propose an **anti-pattern** insight: "When [X], do NOT [Y] because [past failures Z1, Z2]"

## Step 6: Maintenance

- Increment `use_count` and update `outcome_score` for insights used this session
- Flag insights past their `rot_rate` threshold as `status: stale`
- Prune insights with `outcome_score < -2` (set `status: pruned`)
- Graduate insights with `use_count >= 3 AND outcome_score >= 2.0` to `~/.claude/projects/-Users-bizhou/memory/` — update memory MEMORY.md index
- Update `~/.claude/learnings/retrospectives/active-work.md` — add/update current initiatives, clear completed ones
- **Archive artifacts**: If a feature/fix was completed this session, save references alongside insights:
  - Plan file path (from Phase 3 or docs/plans/)
  - PR link (from pr-log.jsonl)
  - Key design decisions made (from conversation)
  - Branch name and commit range
  This preserves the full chain: plan → implementation → PR → learnings. Future sessions can trace back to why something was built a certain way.
- Trim JSONL logs to last 50 entries

## Step 7: Rebuild Briefing

Regenerate `~/.claude/learnings/agent-briefing.md` with:
- Active work (from active-work.md)
- This session summary (what was done, key decisions, what's next)
- Hot insights (top 5-10 by recency + score, filtered for current repo context)
- Recent patterns (recurring themes from logs last 7 days)
- Stale alerts (insights needing re-verification)
- Quick stats (total insights, hot count, graduation candidates, stale count)

Rebuild `manifest-hot.jsonl`: entries from manifest.jsonl where `use_count > 0` OR created in last 30 days.

Write `last-session-summary.txt` as backup handoff (under 100 words).

## Step 8: Feedback Classification (Behavioral RL)

Review the full conversation and classify each user response as a feedback signal. This is how the agent learns to behave better, not just know more.

### 7a. Classify Signals

For each user turn, assess in context of what the agent just did:

```
+2.0  STRONG_POSITIVE   — explicit praise, enthusiastic acceptance, "fantastic", "perfect", "awesome"
+1.0  ACCEPTANCE         — moves forward with output, no correction needed
+0.5  MILD_POSITIVE      — "sounds good", "nice", "cool", accepts with minor edits
 0.0  NEUTRAL            — topic change, ambiguous, moving on (DEFAULT)
-0.1  SOFT_CLARIFICATION — "I mean...", "actually...", "yah I mean..." — just clarifying, not upset. Soft redirect.
-0.2  GENTLE_REDIRECT    — "how do you feel we...", "meanwhile I feel...", "what do you think about..." — suggesting a different direction.
-0.5  CORRECTION         — repeated redirects on same point, "could you check this", clear course change needed
-1.0  STRONG_CORRECTION  — "that's not right", "no don't do that", explicit pushback with reason
-2.0  REJECTION          — fundamental disagreement, "stop", "wrong", rejecting the entire approach
```

**Context matters:** "Could you check" after debugging = positive (asking for verification). "Could you check" after the agent fabricated values = correction. Same words, different signals. Read intent, not keywords.

**Skill invocations are strong signals:** When the user invokes a knowledge skill, it's explicit positive feedback on the work that led to it:
- `/eureka` → +2.0 on all behavioral dimensions active in the preceding work (the approach produced a breakthrough)
- `/aha` → +1.5 (the approach surfaced a non-obvious pattern)
- `/learn` → +1.0 (the approach produced useful knowledge)
- `/compound` → +0.5 (the session was substantial enough to close the loop)

Additionally, meta/sharing skills signal session-level value:
- `/share` → +1.5 on all session behaviors (work was valuable enough to package for others)
- `/export-session` → +1.5 (session was worth preserving as a whole)

Retroactively score the behaviors that led to the skill invocation. If `/eureka` follows an investigation, score `hypothesis_first`, `research_depth`, and `tool_choice` for the investigation positively. The agent should learn: "whatever I did in the last 10 minutes before the user said /eureka — do more of that."

**Distinguishing correction vs context update:** If user references what agent just said ("actually that approach won't work") → correction (-1). If user introduces new info ("oh also, I forgot to mention...") → context update (0).

### 7b. Log Signals

Append to `~/.claude/learnings/logs/feedback-log.jsonl`:
```json
{
  "ts": "ISO timestamp",
  "signal": -1.0,
  "act": "CORRECTION",
  "dimension": "hypothesis_first|solution_simplicity|tool_choice|ask_vs_assume|research_depth|code_quality|other",
  "agent_action": "what the agent did that triggered the feedback",
  "user_context": "brief quote of user's correction/praise",
  "tags": ["relevant", "tags"]
}
```

### 7c. Update Preference Profile

Read `~/.claude/learnings/preference-profile.md`. For each behavioral dimension:
1. Calculate updated reward average from new + existing signals
2. If dimension has 3+ signals AND average is below -0.3 → generate or strengthen a behavioral preference
3. If dimension has 3+ signals AND average is above +0.5 → note as confirmed working approach
4. Update the dimension tracking table

**Rules:**
- Require 3+ signals before writing any preference (avoid over-correction from single incidents)
- Use exponential moving average (alpha=0.3) to smooth spikes
- Tentative preferences (1-2 signals) are noted but don't change behavior
- Strong preferences (7+ signals) are added to agent-briefing.md for every-session loading

### 7d. Track Intellectual Honesty

If the agent pushed back on the user's suggestion AND the user ultimately agreed → score +2.0 on "intellectual_honesty" dimension. This prevents sycophancy — the system should reward successful pushback, not just agreement.

## Step 9: Skill Proposals

Review what happened this session and look for new skill opportunities:

1. **Repetitive workflows**: Did you perform a multi-step workflow (5+ steps) that could be generalized? E.g., "check PEM → check logs → check deploy → compare versions" = potential `/deploy-debug` skill.
2. **Friction points**: Were there moments where you had to explain the same context repeatedly, or manually do something that should be automated?
3. **Cross-session patterns**: Check `~/.claude/learnings/logs/` — do the same types of tasks keep recurring across sessions? That's a skill waiting to be born.
4. **Existing skill gaps**: Did the user try to use a skill that doesn't exist, or use one in a way it wasn't designed for?

**For each candidate, assess:**
- Would this recur? (If one-time, skip)
- Can it be generalized beyond this specific case?
- Is it worth the token cost of loading the skill prompt?

**Present proposals to the user** (don't auto-create):
```
### Skill Proposals
- `/skill-name` — [what it does]. Noticed because: [what triggered the idea].
```

Let the user decide. If approved, create the skill file in `~/.claude/commands/`.

## Step 10: Present Summary

Show the user:
- Insights generated (count and one-line summaries)
- Insights graduated to memory (if any)
- Insights pruned (if any)
- Stale insights flagged (if any)
- Skill proposals (if any)
- Updated briefing stats
