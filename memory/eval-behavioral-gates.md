---
name: Eval-driven behavioral gates
description: Rules derived from /improve-agent eval loop (35 sessions, 124 tasks). Updated automatically by the eval system. Last eval 2026-04-08.
type: feedback
originSessionId: 27db5d4c-f39d-4ca8-b029-b22a12079f15
---
## Approach Selection (12 wrong_approach failures, +9.7% if fixed)

- Ask which component FIRST. Present 2-3 hypotheses. Wait for confirmation.
- "Compare with our system" / "I feel like X" → lead with mapping to our context, not standalone description.
- "Check" / "monitor" / "verify" → read-only. Do NOT initiate actions.
- 3-strike rule: same tool, same error, 3x → switch strategy or ask.
- When redirected, HARD STOP. Pivot immediately.

## Tool Selection (11 tool_misuse failures, +8.9% if fixed)

- curli/grpcurli: LOCAL first. VM only if local auth fails.
- Logs: observe-agent FIRST. Not Slack, not KQL, not local grep.
- PDF: Read tool (built-in). Web pages: Playwright for rich, WebFetch for simple.
- MCP tools: get_tool_info BEFORE calling unfamiliar tools.
- Most direct tool: Built-in > MCP > external. Local > remote.

## Principle Adherence (61 violations, 85.1% adherence)

- **Verify before asserting** (14 violations): Cross-check mental models. "Is this really X?"
- **Never guess values** (13 violations): Specific values require specific sources. No source = "I'd need to verify."
- **Assume complex** (9 violations): Check file count, callers, tests before estimating scope.
- **Cite file:line** (7 violations): Every code behavior claim needs a source.

## Compound Learning (10% loop closure)

- Every 3+ task session → generate >= 1 insight.
- Log insight outcomes in real-time, not just at SessionEnd.
- Proactively suggest /compound after: 5+ tasks, user redirection, bug fix, or 2+ hours.

## Over-Engineering (10 failures)

- When user gives clear direction → execute, don't re-question.
- Match ceremony to scope. Bug fix = fix. Feature = feature. Not more.
