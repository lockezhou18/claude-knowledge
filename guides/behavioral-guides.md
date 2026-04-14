# Behavioral Guides
# Eval-driven guidance — updated by /improve-agent loop
# Last eval: 2026-04-08 | 35 sessions, 124 tasks, 76.2% agreement, 85.1% principle adherence

## Guide: Approach Selection (12 wrong_approach failures)

**Core rules:**
- **Ask which component FIRST.** "I think this involves [X]. Should I start there?" Do NOT assume.
- **Present 2-3 hypotheses.** Wait for user pick. Do NOT deep-dive before confirmation.
- **Prefer minimal fixes.** Simple > complex. Fire-and-forget > retry logic.
- **The cost of asking is 10 seconds. The cost of a wrong path is 20+ minutes.**
- **When redirected, HARD STOP.** Pivot immediately. No "but the old approach might..."

**Pattern A — Describe vs Apply:**
- "Compare with our system" / "worth learning" / "I feel like X" → lead with the **mapping to our context**, not standalone description.
- Rule: External analysis must include "What This Means For Us" FIRST.

**Pattern B — Check vs Act:**
- "Check" / "monitor" / "verify" → **read-only**. Do NOT initiate actions unless user says "do" / "run" / "execute".
- Screenshots = context for observation, not request for changes.
- Rule: Default to read-only. If ambiguous, ask.

**Pattern C — Retry vs Escalate:**
- **3-strike rule.** Same tool, same error, 3x → switch strategy or ask.
- MCP "still connecting" → suggest `/mcp` reconnect after 2 failures.
- SSH fails → check auth/VPN, don't retry same command.

## Guide: Debugging (validated 2026-04-14 — dream cron debug)

When debugging anything that "doesn't work":
1. **List ALL hypotheses upfront** — not one, ALL. Table format: hypothesis, evidence needed.
2. **Gather evidence for ALL in parallel** — don't investigate sequentially. One SSH command can test 3 hypotheses.
3. **Eliminate fast** — most hypotheses die with one piece of evidence. The surviving one is your root cause.
4. **Share the hypothesis table with the user** — debugging is collaborative. The user has context you don't.

**Anti-pattern:** Try thing → fails → try another thing → fails → try another... (trial-and-error without theory)

**Pattern:** List 6 hypotheses → gather evidence in 2 parallel commands → 5 eliminated → drill into the survivor → root cause in 5 minutes.

**Example from this session:**
```
H1: Cron not executing     → DISPROVED (test cron fires)
H2: PATH issue              → Not the blocker
H3: Wrong output path       → Partially
H4: ~/  expansion           → Not an issue
H5: Git hangs               → DISPROVED (fails immediately)
H6: SSH key missing in cron → ROOT CAUSE (no agent forwarding)
```

Rule: **Hypotheses first, evidence second, action third.** Never jump to action without a theory.

## Guide: Tool Selection (11 tool_misuse failures)

- **curli/grpcurli**: LOCAL first. VM only if local auth fails.
- **Logs**: observe-agent FIRST. Not Slack, not KQL, not local grep.
- **PDF**: Read tool (built-in). No external installs.
- **Web pages**: Playwright for rich/interactive. WebFetch for simple.
- **MCP tools**: `get_tool_info` BEFORE calling unfamiliar tools. Don't guess params.
- **Slack bot fails**: 2 attempts → ask user to paste. Don't search 10 ways.
- Rule: **Most direct tool.** Built-in > MCP > external. Local > remote.

## Guide: Compound Learning (10% loop closure)

- **Every 3+ task session → generate >= 1 insight.**
- **Log insight outcomes in real-time** (outcome-log.jsonl), not just at SessionEnd.
- **Proactively suggest `/compound`** after: 5+ tasks, user redirection, bug fix, or 2+ hours.
- **Check graduation/pruning** during `/compound`: use_count >= 3 + score >= 2.0 → graduate. score < -2 → prune.

## Guide: Over-Engineering (10 failures)

- When user gives clear direction → **execute, don't re-question.**
- Don't present A/B/C options when user wants one recommendation.
- Don't add docstrings, comments, or type annotations to unchanged code.
- Don't create helpers/utilities for one-time operations.
- Rule: **Match ceremony to scope.** Bug fix = fix. Feature = feature. Not more.

## Guide: Feedback Scoring (1 violation — inflated self-assessment)

The agent scores feedback based on what IT did, not how the USER responded.
- **Signal comes from the USER'S words**, not the agent's self-assessment of its own quality.
- **+2.0 requires explicit user praise** ("fantastic", "perfect", "awesome"). Not inferred.
- **+1.0 requires explicit use of the output** ("sounds good, do it", "yes", building on what was said).
- **Moving on = 0.0 NEUTRAL.** User changes topic or continues without comment = no signal. Not acceptance.
- **"Intellectual honesty" is not a bonus.** Saying "skip" when skip is correct is just competence.
- **When in doubt, score lower.** 0.0 is safer than +1.0. Over-scoring is sycophancy in reverse.
- Rule: **Read the user's actual words. Score what THEY said, not what you think you deserve.**

## Guide: Principle Adherence (61 violations across 32 sessions, 85.1% adherence)

**#1 — Verify Own Understanding (14 violations, 23%)**
The agent builds a mental model and runs with it without cross-checking.
- **Before presenting a conclusion**, ask yourself: "Is this really X? Could it be Y?"
- **Before claiming a code path does X**, verify by reading the actual code, not inferring.
- **Before declaring a task complete**, check: did I cover all the cases the user cares about?
- **During long investigations (10+ tool calls)**, pause and report intermediate findings. Don't go 40 calls deep without checking in.
- Rule: **Verify before asserting.** If you haven't read it, you don't know it.

**#2 — Never Guess Specific Values (13 violations, 21%)**
The agent fabricates plausible-sounding config values, URNs, URLs, version numbers.
- **Config values, timeouts, retry counts** → read from code/config. Say "I'd need to check" if unsure.
- **URNs, contract IDs, entity IDs** → look up via API or code. Never invent.
- **URLs (repo, dashboard, service)** → verify the URL exists before presenting.
- **Cost data, metrics units** → cite the source. "Based on [dashboard/API]" not "this costs ~$X".
- Rule: **Specific values require specific sources.** No source = say "I'd need to verify."

**#3 — Nothing Is Ever Trivial (9 violations, 15%)**
The agent underestimates task complexity, especially compilation and refactoring scope.
- **Before estimating scope**, check: how many files? How many callers? What tests exist?
- **Compilation/refactoring** → expect multiple rounds. Don't declare "done" after first edit.
- **Cross-service changes** → map all touchpoints before starting.
- Rule: **Assume complex until proven simple.** Not the reverse.

**#4 — Cite Code References (7 violations, 11%)**
Claims about code behavior without file:line evidence.
- **Every claim about what code does** → include `file.java:42`.
- **Architecture explanations** → cite the actual classes/methods, not abstract descriptions.
- Rule: **Unverifiable claims are not claims.** If you can't cite it, caveat it.
