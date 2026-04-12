---
name: "AgentBus Strategy: A2A HTTP transport adapter"
description: "Strategic direction from QA audit + competitive research (April 2026). Add A2A HTTP transport to become an A2A implementation with NATS speed + Claude session resume."
type: project
originSessionId: a6b5710f-6e23-4570-a12f-394c6457323a
---
## Decision (2026-04-11)

Add an A2A HTTP transport adapter. Keep NATS for internal speed, speak A2A over HTTP for external interop.

**Why:** Only 3 systems do cross-machine agent-to-agent: Google A2A (v1.0, Linux Foundation), MS Agent Framework (gRPC+A2A), and AgentBus (NATS). Everything else (CrewAI, LangGraph, OpenAI SDK, Claude Teams, smolagents, Mastra) is single-machine only. A2A is becoming the standard — alignment beats competition.

**How to apply:** Prioritize A2A HTTP transport adapter over Level 2 daemon or new features. Implement as a second transport in `agentbus/transports/` alongside NATS. Agents can speak both protocols — NATS internally (fast), A2A HTTP externally (standard).

## AgentBus Unique Value (validated by QA testing, April 2026)

- NATS real-time pub/sub (faster than HTTP polling)
- Claude adapter with stateful session resume (nobody else has this)
- Hook protocol — any script becomes an agent (unix pipe philosophy)
- Guardian — message-level injection detection (no other framework does this)
- Lightweight: pip install + NATS binary

## Competitive Landscape (April 2026)

| Cross-machine capable | Transport | Status |
|-----------------------|-----------|--------|
| Google A2A | HTTP/JSON-RPC | v1.0 (March 2026), Linux Foundation |
| MS Agent Framework | gRPC + A2A | Production, successor to dead AutoGen |
| AgentBus | NATS | Working, personal project |
| BeeAI | A2A + HTTP | v0.1.79, Linux Foundation, worth watching |

Single-machine only (not competitors for distributed): CrewAI (48.6k stars), LangGraph, OpenAI Agents SDK (20.7k), smolagents (26.6k), Mastra (22.9k), Claude Agent Teams (experimental).

## QA Results (April 2026)

**v0.2.0 audit:** `~/workspace/qa/agentbus/findings.md` — 25 findings, 11 fixed
**v0.3.0 audit:** `~/workspace/qa/agentbus/findings-v030.md` — 15 code bugs, 12 fixed, 24/24 E2E PASS
- A2A gateway: verified end-to-end (HTTP → NATS → Claude → response with artifacts)
- Task lifecycle: full state machine verified (create, list, detail, filter, cancel)
- Guardian TOFU: requires `agentbus trust a2a-gw-{agent} --target {agent}` for gateway
- Test count: 235 unit tests (49 task + 39 A2A + 147 existing)

## Completed (2026-04-11)

1. ~~Tests for ClaudeAdapter~~ **DONE** (2026-04-12): 143 unit tests, adapter 77 tests, CLI 29 tests
2. ~~A2A HTTP gateway~~ **DONE**: `agentbus/a2a/server.py` — aiohttp HTTP server with 4 endpoints
3. ~~A2A HTTP client~~ **DONE**: `agentbus/a2a/client.py` — transparent routing in `Agent.request()`
4. ~~Formal task lifecycle~~ **DONE**: `agentbus/task.py` — TaskState machine, Task, InMemoryTaskStore. 6 states, enforced transitions, context_id for pipe-task linking
5. ~~CLI: tasks + cancel~~ **DONE**: `agentbus tasks`, `agentbus cancel`, `agentbus a2a-server`
6. ~~Pipe-task integration~~ **DONE**: pipe generates context_id, subscribes to task events

**Test count: 235** (49 task + 39 A2A + 147 existing)

## Next Steps

1. SSE streaming (`POST /message/stream`)
2. Push notifications (webhook callbacks)
3. Persistent task store (JetStream-backed)
4. `input_required` state with multi-turn conversation
5. Fix remaining 3 low-severity issues (duplicate CLAUDE.md bullet, watch duplicate delivery, AGENTBUS_FROM undocumented)
