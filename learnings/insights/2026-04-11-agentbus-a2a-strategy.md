---
id: know-058
track: knowledge
type: semantic
status: active
name: "AgentBus strategic direction: become an A2A implementation with NATS speed"
description: "QA + research confirmed AgentBus should add A2A HTTP transport adapter while keeping NATS for internal speed. Only 3 systems do cross-machine agent-to-agent (A2A, MAF, AgentBus). This positions AgentBus as the only A2A implementation with NATS performance + Claude session resume."
created: 2026-04-11
last_verified: 2026-04-11
repos: ["agentbus"]
tags: ["agentbus", "a2a", "architecture", "strategy", "multi-agent", "nats", "distributed"]
severity: high
rot_rate: slow
use_count: 0
outcome_score: 0.0
origin_skill: learn
feeds_into: "aha-007"
---

## Context

QA audit + competitive research (April 2026) across all major multi-agent frameworks.

## Key Finding: The Landscape

Only **3 systems** do cross-machine agent-to-agent communication:
- **Google A2A** — HTTP/JSON-RPC, v1.0 (March 2026), Linux Foundation. The protocol standard.
- **MS Agent Framework** — gRPC + A2A, successor to dead AutoGen. Enterprise-grade.
- **AgentBus** — NATS, Claude-native, lightweight. Personal project.

Everything else is single-machine only:
- CrewAI (48.6k stars), LangGraph, OpenAI Agents SDK, smolagents, Mastra, Claude Agent Teams — all in-process, no network protocol.
- BeeAI (Linux Foundation) — A2A-native new entrant, worth watching (v0.1.79).

## Strategic Direction

**When building AgentBus's next transport, implement A2A HTTP as an adapter — because A2A is becoming the standard and alignment beats competition.**

- Keep NATS for internal speed (real-time pub/sub, SSH tunnel, low latency)
- Add A2A HTTP transport so agents can speak both protocols
- This makes AgentBus an A2A implementation, not a competitor
- Unique value: only A2A-compatible system with NATS performance + Claude session resume + Guardian security + hook protocol

## AgentBus's Unique Advantages (validated by QA testing)

1. **NATS real-time** — pub/sub faster than HTTP polling/SSE
2. **Claude adapter with session resume** — nobody else has this
3. **Hook protocol** (stdin/stdout/env vars) — any script becomes an agent
4. **Guardian** — message-level injection detection, no other framework has this
5. **Setup simplicity** — pip install + NATS binary vs gRPC + .NET (MAF)

## AgentBus's Gaps vs A2A

- No formal task lifecycle (create/get/cancel/status) — A2A has first-class Tasks
- No HTTP transport — can't interop with A2A agents
- Python only — A2A has SDKs in 5+ languages
- No streaming daemon (Level 2) — each dispatch spawns new process

## When to Apply

When planning the next major AgentBus feature, prioritize A2A HTTP transport adapter over Level 2 daemon or new features. Alignment with the emerging standard is more valuable than internal optimization.
