---
id: "know-058"
track: "knowledge"
type: "semantic"
repos: [".agentbus"]
tags: ["qa", "e2e", "unit-test", "mock", "registry", "agentbus"]
severity: "high"
rot_rate: "slow"
created: "2026-04-12"
last_verified: "2026-04-12"
use_count: 1
outcome_score: 1
status: "active"
synthesized_into: "know-059"
---

## Context

AgentBus unit tests use mock registries where all agent identities are pre-registered. In production, each participant has its own registry loaded from disk. Dynamic agents (like A2A gateway `a2a-gw-*`) register in-memory during their process lifetime but are unknown to other participants' registries. This means unit tests can pass while E2E fails for identity/auth reasons.

## Guidance

When testing distributed systems with per-participant auth/registries:
1. Unit tests that pre-register all agents in mock registries are necessary but insufficient
2. E2E tests must verify the trust/registration flow — dynamic agents need explicit registration on all participants
3. The gap is always in **cross-process state** — what one process knows that another doesn't

## When to Apply

When adding new dynamic agent types to agentbus. When debugging "tests pass, production fails" for any auth/identity system. When reviewing test coverage for distributed features.
