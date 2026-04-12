---
id: "know-059"
track: "knowledge"
type: "semantic"
repos: ["*"]
tags: ["testing", "distributed", "auth", "registry", "e2e", "mock"]
severity: "high"
rot_rate: "permanent"
created: "2026-04-12"
last_verified: "2026-04-12"
use_count: 0
outcome_score: 0
status: "active"
synthesized_from: ["know-056", "know-058"]
---

## Context

In distributed systems where each participant maintains its own auth/identity registry, unit tests that pre-register all identities in a shared mock registry will always pass — but production fails because each process has its own view of who's trusted. The gap is **cross-process state divergence**: what one process knows that another doesn't.

This pattern appeared twice in agentbus v0.3.0:
- A2A gateway created dynamic identity `a2a-gw-bizhou-vm` → registered in laptop registry → VM's Guardian rejected it (know-056)
- All unit tests passed because mock registries contained both parties → E2E failed (know-058)

## Guidance

When testing distributed identity/auth:
1. **Unit tests with shared mocks are necessary but insufficient** — they verify logic, not trust propagation
2. **E2E tests must verify the registration/trust flow itself** — dynamic identities need explicit registration on all participants
3. **The diagnostic question is always:** "Does process B know about entity X that process A created?" If the answer depends on shared state that only exists in-memory during tests, you have this bug.
4. **Fix pattern:** Either pre-register identities on disk (agent cards, config files) or implement a trust-on-first-use protocol with an explicit approval step.

## When to Apply

When adding dynamic participants to any system with per-process auth (agent buses, microservice meshes, API gateways). When unit tests pass but E2E fails for auth/identity reasons. When reviewing test coverage for any feature that creates new identities at runtime.
