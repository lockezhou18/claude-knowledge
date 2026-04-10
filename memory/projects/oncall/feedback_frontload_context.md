---
name: Front-load Context for Oncall Sessions
description: Start oncall sessions by fetching JIRA ticket context first via MCP before investigating logs
type: feedback
---

When starting an oncall investigation, always front-load context in this order:
1. Fetch JIRA ticket details first (if ticket exists)
2. Identify service, fabric, time window, symptoms
3. Check recent deployments for the affected service
4. THEN search logs

**Why:** Multiple oncall sessions involve the same stack (Java/gRPC/Trino/HDFS/JIRA/Rootly). Setting context upfront saves repeated orientation time and reduces wrong-approach friction.

**How to apply:** Every oncall investigation session. Use the structured prompt: ticket ID + service + fabric + preferred investigation order.
