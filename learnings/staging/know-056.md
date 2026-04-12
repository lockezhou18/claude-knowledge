---
id: "know-056"
track: "knowledge"
type: "semantic"
repos: [.agentbus]
tags: [guardian, a2a, auth, trust, agentbus]
severity: "high"
rot_rate: "slow"
created: "2026-04-12"
last_verified: "2026-04-12"
use_count: 1
outcome_score: 0.93
status: "active"
synthesized_into: [know-059, aha-007]
---

## Context

When the A2A HTTP gateway dispatches messages to NATS agents, the gateway uses a dynamic identity (`a2a-gw-{agent_name}`) that is not pre-registered in the target agent's Guardian registry. Unit tests pass because they pre-register the gateway in mock registries, but E2E fails because the VM has its own separate registry.

## Guidance

After deploying an A2A gateway, run `agentbus trust a2a-gw-{agent} --target {agent}` to register the gateway identity. The Guardian uses a TOFU (Trust On First Use) model — it detects the gateway via heartbeats but won't allow requests until explicitly trusted.

## When to Apply

When setting up A2A gateway for any agent. When debugging "unknown sender" rejections in production. When unit tests pass but E2E fails for auth/identity reasons — check if dynamic agent names are registered in all participating registries.
