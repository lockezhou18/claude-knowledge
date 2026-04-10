---
name: Parallel debugging agents
description: When debugging cross-service issues (HP/IP/mcm-mt), spawn parallel agents instead of sequential investigation
type: feedback
---

When debugging issues that span multiple services (hp-ats-integration-mt, talent-partner-integrations-mt, mcm-mt), spawn parallel agents to search logs in each service simultaneously rather than investigating one at a time.

**Why:** Sequential investigation wastes time — while waiting for one log search, the other services' logs could already be fetched. Wrong-theory debugging is amplified when you commit to one service's logs before seeing the full picture across services.

**How to apply:** Use the Agent tool with multiple parallel invocations:
```
Agent 1: "Search hp_ats_integration_mt_logs for ..."
Agent 2: "Search mcm_mt_logs for ..."
Agent 3: "Search talent_partner_integrations_mt_logs for ..."
```
Combine findings before forming a hypothesis. This is especially valuable for treeId-based tracing where the same request flows through multiple services.
