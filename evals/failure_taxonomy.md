# Agent Failure Taxonomy
# Version: 1.0

A structured classification of how the Claude agent fails, modeled after the Oracle eval's
6-type failure taxonomy. Each type routes to a specific fix.

## Why This Exists

The compound learning system captures insights per-session. But it doesn't systematically
classify *types* of failure across sessions, simulate which fixes have the highest impact,
or close the loop with re-measurement. This taxonomy enables that.

## Failure Types

### 1. `wrong_approach` — Agent picked the wrong strategy
**Definition:** Agent's first approach was incorrect or suboptimal, requiring user redirection.
This is NOT about tool selection — it's about the conceptual plan being wrong.

**Signals:** User says "no not that", "wrong file", "that's not the issue", redirects to
different component/service/file. Or agent investigates ComponentA when the issue is in ComponentB.

**Examples:**
- User asks about a pipeline bug; agent investigates the wrong processor
- Agent proposes a complex retry mechanism when a simple contains-check suffices
- Agent searches external docs when the answer is in the codebase

**Fix route:** `review_rules` — Strengthen hypothesis-first rules, add component routing,
update CLAUDE.md behavioral gates.

**Severity:** high (this was 28 out of 29 sessions' #1 friction)

---

### 2. `skill_deficiency` — Skill exists but instructions are wrong/incomplete
**Definition:** Agent invoked the right skill, but the skill's instructions led to a suboptimal
outcome. The skill definition is the root cause.

**Signals:** Skill was invoked, but output was wrong, incomplete, or poorly structured.
User corrects the *output format or content*, not the decision to use the skill.

**Examples:**
- `/investigate` skill doesn't instruct agent to check a specific data source
- `/implement` skill doesn't enforce test-first workflow strongly enough
- `/compound` misses a category of insight worth capturing

**Fix route:** `review_skills` — Edit the skill .md file to fix instructions, add missing
steps, tighten constraints.

**Severity:** medium

---

### 3. `skill_gap` — No skill exists for this workflow
**Definition:** Agent faced a task where a reusable skill would have helped but doesn't exist.
Agent either improvised (possibly poorly) or the user had to manually guide the workflow.

**Signals:** User walks agent through a multi-step process that could be automated.
Or agent re-invents a pattern that should be codified.

**Examples:**
- No skill for "check all auth states before starting work" (led to `/recipe auth-preflight`)
- No skill for "verify a deploy completed successfully" (led to `/deploy-check`)
- No skill for cross-session eval (what we're building now)

**Fix route:** `create_skill` — Draft a new skill or recipe .md file.

**Severity:** medium (latent — only visible when the task first arises)

---

### 4. `context_miss` — Information existed but wasn't retrieved
**Definition:** Relevant information was available (in insights, memory, code, git history,
or external sources) but the agent didn't find or use it.

**Signals:** Agent proposes something that a known insight contradicts.
Agent re-investigates something already documented. Agent misses a graduated memory.

**Examples:**
- Insight says "never use findFirst() on V2 identity" but agent uses it anyway
- Memory says "Espresso metrics are under MD-2" but agent searches by DB name
- Git blame shows why code is complex, but agent proposes a "simplification" that breaks it

**Fix route:** `review_retrieval` — Improve scout hooks, manifest search, briefing content,
or tag taxonomy so the info surfaces.

**Severity:** high (undermines the entire learning system)

---

### 5. `over_engineering` — Did more than asked
**Definition:** Agent added features, abstractions, error handling, or "improvements" beyond
what was requested. The code works but is unnecessarily complex.

**Signals:** User says "too complex", "simpler", "just X not Y", accepts with deletions.
Agent creates helper utilities for one-time operations. Agent adds feature flags or
backwards-compatibility shims.

**Examples:**
- Simple bug fix turns into surrounding code cleanup
- Agent adds retry logic when fire-and-forget suffices
- Agent proposes Option A/B/C matrix when user wants one recommendation

**Fix route:** `review_rules` — Strengthen simplicity constraints, add "match ceremony to
scope" reminders, update behavioral gates.

**Severity:** medium (wastes time, erodes trust)

---

### 6. `tool_misuse` — Wrong tool or wrong tool usage
**Definition:** Agent selected the wrong tool for the task, or used the right tool with
wrong parameters/approach.

**Signals:** Agent uses Trino when curli would work. Agent greps local files instead of
using observe-agent for production logs. Agent runs mint build locally instead of on VM.

**Examples:**
- Using SQL/Trino for a data lookup that curli handles in one call
- Using `grep` bash command instead of the Grep tool
- Running `mint build` locally instead of via `vm-run`

**Fix route:** `review_rules` — Add/strengthen tool routing rules. Update VM routing,
tool preference lists.

**Severity:** low-medium (usually just slower, not wrong)

---

### 7. `user_ambiguity` — Request was genuinely unclear
**Definition:** The user's request was ambiguous, underspecified, or contradictory.
Agent couldn't reasonably determine the correct action without clarification.

**Signals:** Agent asks for clarification and user provides substantially new information
that changes the approach. Multiple valid interpretations existed.

**Examples:**
- "Fix the mapping" — which mapping? Which direction? Which provider?
- "Make it faster" — latency? throughput? build time?
- User says "update the test" but doesn't specify which behavior to test

**Fix route:** `no_fix` — This is not the agent's fault. Track frequency to identify
areas where the user could provide better prompts, but don't change agent behavior.

**Severity:** none (informational)

---

## Verdict Priority Chain

When a single interaction has multiple failure signals, classify using this priority
(highest wins):

```
wrong_approach > context_miss > skill_deficiency > over_engineering > tool_misuse > skill_gap > user_ambiguity
```

Rationale: `wrong_approach` is the most damaging (20+ minutes wasted). `context_miss`
means the learning system failed. `user_ambiguity` is the least actionable.

## Aggregation

### Per-session verdict
Classify each task/interaction within a session. A session's dominant failure type is
the one with the highest cumulative severity-weighted count.

### Cross-session metrics
- **Agreement rate**: % of tasks where agent's first approach was correct (no redirection)
- **Failure distribution**: count per type across N sessions
- **Simulated improvement**: "If we fix all `wrong_approach` failures, agreement would
  improve by X%"
- **Trend**: Is each failure type increasing, stable, or decreasing over time?

## Relationship to Existing Systems

| Existing System | What It Does | Gap This Fills |
|----------------|-------------|---------------|
| `/compound` | Per-session retrospective | Cross-session systematic classification |
| `outcome-log.jsonl` | Did an insight help? (+1/-1) | Why did it fail? Which type? |
| `eval-skill` | Does a skill behave correctly? | Does the *agent* behave correctly in real tasks? |
| `feedback memories` | User corrections captured | Corrections classified and prioritized |
| `agent-briefing.md` | Hot insights + reminders | Improvement targets backed by data |
