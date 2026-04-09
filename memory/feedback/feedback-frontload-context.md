---
name: Front-load context to avoid wrong-approach friction
description: User's #1 friction source (28 instances) — always provide specific service/file/tool constraints upfront rather than exploring broadly
type: feedback
---

When investigating or debugging, front-load the specific service, file, processor, or API tool in the prompt rather than exploring broadly first.

**Why:** Across 32 sessions, 28 instances of wrong-approach friction came from Claude exploring the wrong component before the user redirected. Examples: investigating ExportStatusEventProcessor instead of ApplicationStageProcessor, using Trino instead of curli, checking contract-type instead of seat-level entitlement. Each wrong path cost 3-5 rounds of correction.

**How to apply:**
- If the user specifies a file/service/tool → go there immediately, don't explore alternatives first
- If the user doesn't specify → ask "I think this involves [ComponentA]. Should I start there?" before investigating. The cost of asking is 10 seconds; the cost of a wrong path is 20+ minutes.
- When starting any investigation, prefer the prompt pattern: "Investigate [issue] starting at [specific file/service]. Use [specific tool]. Do NOT explore [known wrong path]."
- For data lookups: default to curli/REST, not Trino/SQL
- For logs: default to observe-agent, not grep/manual Kusto
- For code fixes: target the minimal correct layer (shared service > processor)
