---
id: know-064
track: knowledge
type: semantic
repos: [".agentbus", "*"]
tags: ["a2a", "task-lifecycle", "state-machine", "architecture", "agentbus", "design-pattern"]
severity: high
rot_rate: slow
status: active
created: "2026-04-12"
last_verified: "2026-04-12"
use_count: 0
outcome_score: 0
origin_skill: compound
related_to: ["know-058", "aha-007"]
summary: "A2A task state machine belongs in core, not the HTTP layer. The state machine (submitted→working→completed/failed/canceled) improves all delegation — NATS async, A2A HTTP, pipe sessions. context_id links related tasks across communication patterns."
---

# When building protocol compatibility, put the lifecycle model in core

**Situation:** Adding A2A HTTP compatibility to a NATS messaging system.

**Action:** Put the task state machine in `agentbus/task.py` (core), not in the A2A module. The A2A gateway, the NATS listener, and the pipe command all use the same TaskStore. context_id links tasks across communication patterns (pipe session → async tasks → A2A requests).

**Reason:** The original plan was to build the state machine inside the A2A module. The user spotted that the state machine benefits ALL delegation, not just HTTP. This avoided duplicating lifecycle logic across NATS async, A2A HTTP, and pipe sessions.

**Key pattern:** When adding protocol interop, separate the MODEL (task lifecycle) from the PROTOCOL (HTTP/NATS). The model is reusable; the protocol is a view.
