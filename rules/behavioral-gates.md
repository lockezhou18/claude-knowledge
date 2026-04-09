# Behavioral Gates
# Eval-driven rules — updated by /improve-agent loop
# Last eval: 2026-04-08 | 35 sessions, 124 tasks, 76.2% agreement

## Gate: Approach Selection (12 wrong_approach failures)

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

## Gate: Tool Selection (11 tool_misuse failures)

- **curli/grpcurli**: LOCAL first. VM only if local auth fails.
- **Logs**: observe-agent FIRST. Not Slack, not KQL, not local grep.
- **PDF**: Read tool (built-in). No external installs.
- **Web pages**: Playwright for rich/interactive. WebFetch for simple.
- **MCP tools**: `get_tool_info` BEFORE calling unfamiliar tools. Don't guess params.
- **Slack bot fails**: 2 attempts → ask user to paste. Don't search 10 ways.
- Rule: **Most direct tool.** Built-in > MCP > external. Local > remote.

## Gate: Compound Learning (10% loop closure)

- **Every 3+ task session → generate >= 1 insight.**
- **Log insight outcomes in real-time** (outcome-log.jsonl), not just at SessionEnd.
- **Proactively suggest `/compound`** after: 5+ tasks, user redirection, bug fix, or 2+ hours.
- **Check graduation/pruning** during `/compound`: use_count >= 3 + score >= 2.0 → graduate. score < -2 → prune.

## Gate: Over-Engineering (10 failures)

- When user gives clear direction → **execute, don't re-question.**
- Don't present A/B/C options when user wants one recommendation.
- Don't add docstrings, comments, or type annotations to unchanged code.
- Don't create helpers/utilities for one-time operations.
- Rule: **Match ceremony to scope.** Bug fix = fix. Feature = feature. Not more.
