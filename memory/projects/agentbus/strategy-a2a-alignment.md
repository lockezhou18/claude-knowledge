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

Full audit at `~/workspace/qa/agentbus/findings.md` and `retest-report.md`.
- 25 findings, 11 code fixes applied and verified
- 17/18 CLI commands pass, pipe bidirectional confirmed
- Test coverage is 3/10 — ClaudeAdapter has zero tests (top priority)
- Architecture rated 8/10, code quality 6/10, idea 9/10

## Next Steps

1. A2A HTTP transport adapter in `agentbus/transports/a2a_http.py`
2. ~~Tests for ClaudeAdapter~~ **DONE** (2026-04-12): 143 unit tests, adapter 77 tests, CLI 29 tests
3. Formal task lifecycle (create/get/cancel/status) — align with A2A Tasks
4. Fix remaining 3 low-severity issues (duplicate CLAUDE.md bullet, watch duplicate delivery, AGENTBUS_FROM undocumented)
