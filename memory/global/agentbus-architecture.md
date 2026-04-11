---
name: AgentBus VM agent architecture
description: NATS-backed messaging between laptop Claude and VM Claude agent. /delegate skill handles routing. Three modes — sync, async (Monitor), auto (multi-round).
type: reference
---

## AgentBus Architecture

Laptop Claude communicates with a persistent VM Claude agent via NATS messaging.

```
Laptop                    NATS (:4222)              VM (bizhou-ld2)
/delegate skill  ──────▶  SSH tunnel  ──────▶  claude_listener
  vm-agent CLI                                   → claude -p (think)
  vm-run (shell)                                 → bash (shell)
```

### Components
- **NATS server**: runs on VM (tmux: nats), v2.12.6 with JetStream
- **Claude listener**: runs on VM (tmux: agentbus), dispatches to claude -p or bash
- **vm-agent CLI**: ~/bin/vm-agent — handles tunnel, routing, sessions
- **watch_result.py**: NATS subscriber for Monitor tool — real-time async notifications
- **Agent cards**: agents/bizhou-vm.json, agents/bizhou-laptop.json

### Three Modes
| Mode | Flag | Behavior |
|------|------|----------|
| Sync | (default) | Block until result |
| Async | --async | Fire task + Monitor watches for result |
| Auto | --auto | Multi-round autonomous loop + Monitor shows checkpoints |

### Session Resume (Level 1)
Follow-up messages auto-resume previous conversation (same sender + repo). Sessions expire after 1 hour idle.

### Key paths
- AgentBus code: ~/projects/compound-learning-ecosystem/agentbus/
- VM deployment: vm:~/agentbus/
- Agent cards: agentbus/agents/*.json
- NATS config: agentbus/deployment/nats-bizhou.conf
- Autostart: vm:~/.bashrc sources vm-autostart.sh
