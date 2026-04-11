---
id: know-054
track: knowledge
type: semantic
repos: ["*"]
tags: [agentbus, vm, delegate, nats, multi-agent, architecture, async, monitor]
severity: high
rot_rate: slow
status: active
created: 2026-04-10
last_verified: 2026-04-10
use_count: 0
outcome_score: 0
summary: "AgentBus VM agent: NATS messaging between laptop and VM Claude. /delegate skill with sync/async/auto modes. Monitor tool for real-time async notifications."
file: "staging/know-054.md"
---

When delegating work to the VM, use `/delegate` which routes through AgentBus (NATS) for thinking tasks and SSH/vm-run for shell commands.

**Three modes:** sync (default), async (--async + Monitor), auto (--auto, multi-round loop).

**Key insight:** Claude Code's Monitor tool + NATS subscriber (watch_result.py) gives real-time async notifications — cleaner than file-drop + polling. Session resume (Level 1) enables multi-turn VM conversations.

**How to apply:** For VM tasks, use `/delegate` instead of raw SSH. For async, use `--async`. For autonomous loops, use `--auto`.
