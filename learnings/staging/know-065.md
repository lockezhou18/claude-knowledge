---
id: know-065
track: knowledge
type: semantic
repos: [".agentbus", "*"]
tags: ["auth", "trust", "tofu", "guardian", "distributed", "identity", "design-pattern"]
severity: high
rot_rate: slow
status: active
created: "2026-04-12"
last_verified: "2026-04-12"
use_count: 0
outcome_score: 0
origin_skill: compound
related_to: ["know-056", "know-059"]
summary: "TOFU (Trust On First Use) for distributed agents: Presence = discovery (who's knocking), Registry = trust (who's approved). Guardian checks both — detected-but-untrusted gets actionable error. One-time `agentbus trust` writes card to registry permanently."
---

# When dynamic agents need identity across machines, use TOFU not file sync

**Situation:** A2A gateway on laptop creates an agent identity unknown to the VM's Guardian.

**Wrong approaches tried:**
1. Auto-create card file and sync via mutagen → works for personal use, not production
2. Impersonate a known agent identity → wrong security model
3. Auto-trust via heartbeats → no explicit approval, security concern

**Right approach:** TOFU (Trust On First Use):
- **Presence** (heartbeats) = discovery layer. Tells Guardian "this agent is on the bus."
- **Registry** (file cards) = trust layer. Explicit approval required.
- Guardian rejection message includes the exact trust command: `agentbus trust <name> --target <listener>`
- Trust is one-time and persistent (card written to agents dir, survives restarts)
- NATS connection auth is the outer trust boundary — you can't send heartbeats without credentials

**Key insight:** Three bad approaches were tried before reaching TOFU. The progression: card sync (personal) → impersonation (wrong) → auto-trust (insecure) → TOFU (correct). Each rejection from the user refined the design toward production readiness.
