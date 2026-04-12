---
id: know-062
track: knowledge
type: semantic
repos: ["agentbus", "*"]
tags: ["agent-lifecycle-mt", "starfish", "agent-platform", "architecture", "skill-invocation", "agentbus", "comparison", "linkedin-infra", "orchestration"]
severity: high
rot_rate: slow
status: active
created: 2026-04-11
last_verified: 2026-04-11
use_count: 0
outcome_score: 0
origin_skill: learn
related_to: ["know-058", "know-054", "know-056"]
feeds_into: "aha-007"
---

# LinkedIn Agents Platform (Starfish) — agent-lifecycle-mt Architecture

## Context

Deep-dive comparison of three agent systems: agent-lifecycle-mt (LinkedIn's Agents Platform middleware), talent-agent-service (domain app for hiring AI), and AgentBus (personal NATS-based messaging bus).

## Guidance

### agent-lifecycle-mt is a Real Orchestration Middleware (Not a Wrapper)

**When reasoning about LinkedIn's agent infra**, know that agent-lifecycle-mt provides 10 APIs:
1. **AgentLifecyclePlugin** — messaging-extension plugin, routes message/thread events to agents
2. **SkillInvocationApi** — 7 RPCs: sync, async+callback, deferred, individual/collective workflows, cancel
3. **AgentConversationApi** — agent-to-agent and agent-to-user messaging via LinkedIn Messaging
4. **AgentLifecycleApi** — guaranteed delivery via samza-attemptor + Kafka durable retry
5. **AgentAuthnTokenApi** — agent auth tokens + session invalidation
6. **ThreadControlsApi** — per-agent message processing state
7. **MessageStateApi** — message processing state tracking (Espresso-backed)
8. **McpRequestHandler** — MCP server exposing skills as MCP tools
9. **EchoAgentApi / EchoSkillApi** — E2E test agents

### SkillInvoker Does Real Work

The invocation path: quota check → retry wrapper → route (gRPC vs HTTP vs external-HTTP) → SkillRegistry lookup → D2 discovery → dynamic protobuf method resolution → async unary call → distributed tracing.

Key: uses **dynamic protobuf** — resolves method descriptors at runtime from GAI Skill Registry. Doesn't know what skills exist at compile time.

### talent-agent-service Uses Only ~15% of the Surface

- Uses: `invokeSkillSync`, `AgentApi.onMessage`, ExperientialMemory
- Does NOT use: async callbacks, deferred responses, workflows, AgentConversationApi, MCP, thread controls, workflow cancellation
- Its internal routing is a hardcoded dict + giant Python match statement

### AgentBus ↔ agent-lifecycle-mt Mapping

| agent-lifecycle-mt | AgentBus | Gap |
|---|---|---|
| SkillRegistry + D2 | FileRegistry + heartbeat | Static files vs runtime registry |
| Kafka retry + samza | None | No durable retry in AgentBus |
| ThreadLockService | None | No distributed locking |
| Async D2 callbacks | `event.result.{id}` | Similar concept, different transport |
| Individual/collective workflows | Task FSM | AgentBus has lifecycle, no workflow orchestration |
| MCP server | Not present | Could expose agents as MCP tools |
| Agent tokens + session invalidation | TOFU trust | Simpler but less secure |
| Dynamic protobuf | JSON Envelope | Schema-free vs schema-enforced |

### Stack Architecture (Verified)

```
LinkedIn Messaging → messaging-extension → AgentLifecyclePlugin
  → ThreadLockService → MessageStateService → AgentInvoker (D2 + Kafka retry)
    → talent-agent-service (or any agent implementing AgentApi.onMessage)
      → calls back SkillInvocationApi for sub-agent invocation
        → SkillInvoker → SkillRegistry → D2 → target skill service
      → calls AgentConversationApi to reply to user
```

## When to Apply

- When designing AgentBus features — check what agent-lifecycle-mt already solved
- When comparing agent frameworks — Starfish is the enterprise-grade reference
- When scoping work on talent-agent-service — know what platform capabilities are unused
- When discussing MCP integration — agent-lifecycle-mt already bridges skills → MCP tools
