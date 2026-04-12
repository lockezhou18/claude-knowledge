---
id: know-066
track: knowledge
type: semantic
repos: [".agentbus", "*"]
tags: ["qa", "testing", "e2e", "iterative", "workflow", "agentbus"]
severity: medium
rot_rate: slow
status: active
created: "2026-04-12"
last_verified: "2026-04-12"
use_count: 0
outcome_score: 0
origin_skill: compound
summary: "QA-driven development cycle: build → unit test → QA audit → fix → E2E test → fix new findings → ship. The QA agent found 15 bugs that unit tests missed (signal handler race, double timeout, Guardian cross-machine identity). E2E found 2 more (CLI error swallowing, Guardian TOFU). Budget 2 QA rounds per feature."
---

# When shipping distributed features, budget 2 QA rounds

**Situation:** AgentBus v0.3.0 — unit tests all pass (235/235), but QA audit + E2E testing found 17 additional bugs.

**Pattern:** Build → 235 unit tests pass → QA audit finds 15 code bugs → fix 12 → E2E finds 2 new runtime bugs → fix both → ship.

**What unit tests missed:**
- Signal handler race condition (async safety — needs runtime context)
- Double timeout (client + server with same value — needs protocol awareness)
- Guardian cross-machine identity (different registries — needs distributed context)
- CLI error swallowing (silent failure path — needs integration context)

**Reason:** Unit tests verify component behavior. QA audits verify design correctness. E2E tests verify cross-process behavior. All three are needed for distributed systems. Budget time for 2 QA rounds — the first catches design bugs, the second catches runtime bugs exposed by fixes.
