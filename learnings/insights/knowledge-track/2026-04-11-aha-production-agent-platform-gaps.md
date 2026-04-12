---
id: aha-007
track: knowledge
type: semantic
repos: ["agentbus", "*"]
tags: ["aha", "pattern", "agent-platform", "agentbus", "starfish", "agent-lifecycle-mt", "architecture", "roadmap", "production-readiness", "gap-analysis"]
severity: critical
rot_rate: slow
status: active
created: 2026-04-11
last_verified: 2026-04-11
use_count: 0
outcome_score: 0
origin_skill: aha
synthesized_from: ["know-056", "know-058", "know-060", "know-062"]
---

# Production Agent Platform: What's Needed vs What AgentBus Has

## Pattern

**A production agent platform needs 7 capability layers. AgentBus has strong Layer 1-3 but is missing Layer 4-7. The critical insight: AgentBus's unified Envelope model is architecturally superior to Starfish's two-API split — but simplicity at the wire level still requires production-grade machinery underneath.**

The 7 layers, derived from comparing agent-lifecycle-mt (LinkedIn's production platform) with AgentBus (personal project):

```
Layer 7: Protocol Interop     — speak multiple protocols (A2A, MCP, gRPC)
Layer 6: Workflow Orchestration — multi-step, conditional, collective execution
Layer 5: Durability           — survive restarts, retry on failure, idempotency
Layer 4: Operational Safety   — locking, quota, auth tokens, message state tracking
Layer 3: Task Lifecycle       — state machine, async results, cancellation
Layer 2: Identity & Security  — discovery, presence, trust, injection detection
Layer 1: Transport            — pub/sub, request/reply, subjects, codecs
```

## Evidence

### know-058 (AgentBus A2A Strategy)
AgentBus is one of only 3 systems doing cross-machine agent-to-agent communication. A2A HTTP adapter added in v0.3.0. Positions as A2A implementation with NATS speed. → **Layer 1 and 7 partially covered.**

### know-056 (Guardian TOFU Trust)
TOFU model works for small-scale. Dynamic identities (a2a-gw-*) require explicit trust registration across all participating registries. → **Layer 2 covered, but manual trust management doesn't scale.**

### know-060 (AgentBus VM Deploy Ops)
No git on VM, ssh cat pipe for sync, systemd restart for listener. InMemoryTaskStore lost on restart. → **Layer 5 missing: no persistence, no graceful restart.**

### know-062 (Starfish agent-lifecycle-mt Architecture)
10 APIs covering all 7 layers. SkillInvoker uses dynamic protobuf + D2 discovery + quota + retry + tracing. AgentConversationApi enables inter-agent messaging through LinkedIn Messaging. Kafka-backed durable retry via samza-attemptor. ThreadLockService for distributed locking. MCP server exposes skills as tools. → **Layers 4-7 fully covered at enterprise scale.**

## Gap Analysis: AgentBus vs Production

| Layer | Capability | agent-lifecycle-mt | AgentBus | Gap | Priority |
|---|---|---|---|---|---|
| **1** | Transport | D2 gRPC + Messaging + Kafka | NATS + A2A HTTP | **None** — AgentBus transport is stronger (NATS > gRPC for pub/sub) | — |
| **2** | Discovery | SkillRegistry (centralized, dynamic) | FileRegistry + heartbeat | **Minor** — file-based works at current scale | P3 |
| **2** | Security | Agent tokens + session invalidation + caller auth | Guardian TOFU + injection detection | **Minor** — TOFU adequate for personal use | P3 |
| **3** | Task lifecycle | (implicit in skill responses) | Full FSM: submitted→working→completed/failed/canceled/input_required | **AgentBus ahead** — explicit is better | — |
| **4** | Distributed locking | ThreadLockService (Espresso-backed) | None | **Gap** — concurrent message processing can race | P2 |
| **4** | Quota enforcement | Liminal quota per skill | None | **Low priority** — not needed at personal scale | P4 |
| **4** | Message state tracking | MessageStateService (Espresso) | None | **Gap** — no way to track which messages are processed | P2 |
| **5** | Durable retry | Kafka + samza-attemptor | None | **Critical gap** — failed tasks are lost forever | **P1** |
| **5** | Persistent task store | Espresso-backed | InMemoryTaskStore (lost on restart) | **Critical gap** — restart = lose all task history | **P1** |
| **5** | Idempotency | Workflow idempotencyKey | None | **Gap** — duplicate sends cause duplicate work | P2 |
| **6** | Workflow orchestration | Individual + collective skill workflows | None | **Gap** — no multi-step or conditional execution | P2 |
| **6** | Async callbacks | D2 callback service + deferred responses | event.result.{id} subjects | **Partial** — AgentBus has the pattern, not the durability | P2 |
| **7** | MCP integration | McpRequestHandler + SkillToToolSynchronizer | None | **Gap** — agents can't be consumed as MCP tools | P2 |
| **7** | Streaming | gRPC streaming + streamUpdateMessage | None (Level 2 planned) | **Gap** — no progressive response delivery | P2 |

## The Architectural Advantage AgentBus Should Preserve

**Starfish splits communication into two incompatible APIs:**
- `SkillInvocationApi` — typed protobuf RPC for function calls
- `AgentConversationApi` — text/JSON messaging through LinkedIn Messaging

This forces teams to choose: is my agent a "skill" (function) or a "conversation partner" (chat)? talent-agent-service chose "skill" and only uses 15% of the platform.

**AgentBus's unified Envelope model is better:** Same transport for chat, RPC, events, tasks, and heartbeats. Any agent can be both a function and a conversation partner. Don't split this.

**Preserve:** unified Envelope, subject-based routing, transport-agnostic design
**Add underneath:** persistence, retry, locking, MCP bridge — without breaking the simple API surface

## Concrete Roadmap

### Phase 1: Durability (P1) — "Don't Lose Work"
1. **FileTaskStore** — persist tasks to disk (JSON files in `~/.agentbus/tasks/`)
   - On restart, reload in-progress tasks and resume
   - TTL-based cleanup for completed tasks
2. **Retry on failure** — when a task fails, enqueue for retry with exponential backoff
   - Store retry count in Task metadata
   - Max 3 retries, then mark failed permanently
3. **Result persistence** — already partially done (`AGENTBUS_RESULTS_DIR`), formalize

### Phase 2: Operational Safety (P2) — "Don't Corrupt State"
4. **Message dedup** — idempotency key in Envelope, skip if already processed
5. **Task locking** — advisory lock per agent+task to prevent concurrent processing
   - File-based lock (`~/.agentbus/locks/{agent}.{task_id}.lock`)
   - Auto-release on completion or timeout
6. **Message state tracking** — track processed/pending per agent

### Phase 3: Orchestration (P2) — "Coordinate Multi-Step Work"
7. **Workflow primitives** — sequence, parallel, conditional in task dispatch
   - Build on existing Task FSM — add `parent_task_id` for hierarchical tasks
   - Parallel: dispatch N tasks, wait for all, aggregate
   - Conditional: dispatch next based on previous result
8. **Async callbacks** — durable version of current event.result pattern
   - Persist callback subscriptions to survive restarts

### Phase 4: Protocol Interop (P2) — "Play Well With Others"
9. **MCP bridge** — expose AgentBus agents as MCP tools
   - Agent card → MCP tool definition mapping
   - MCP server that translates tool calls → Agent.request()
10. **Streaming** — Level 2 Claude adapter with `--input-format stream-json`
    - Progressive response delivery via NATS subjects
    - Compatible with A2A streaming when spec adds it

### What NOT to Build
- **Centralized registry** — FileRegistry + heartbeat is fine at this scale
- **Quota enforcement** — not needed for personal/small-team use
- **Agent auth tokens** — TOFU is adequate
- **Dynamic protobuf** — JSON Envelope is more flexible, don't add schema enforcement

## When to Apply

- **Before starting any AgentBus feature**: check this roadmap — is it P1, P2, P3, or P4?
- **When comparing AgentBus to production platforms**: use the 7-layer model
- **When someone asks "can AgentBus do X?"**: map X to a layer and check the gap
- **When tempted to add enterprise features**: check "What NOT to Build" — simplicity is the advantage
- **Key principle**: Add production machinery UNDER the simple API, not instead of it
