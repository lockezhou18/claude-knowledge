---
id: know-060
track: knowledge
type: episodic
repos: ["agentbus"]
tags: ["agentbus", "vm", "deploy", "nats", "ssh", "systemd", "ops"]
severity: medium
rot_rate: slow
status: active
created: 2026-04-12
last_verified: 2026-04-12
use_count: 0
outcome_score: 0
origin_skill: learn
related_to: ["know-054"]
feeds_into: "aha-007"
---

## AgentBus VM Deployment: Operational Facts

**When deploying agentbus code to the VM, use file-sync (ssh cat pipe) + systemd restart — the VM copy is not a git repo.**

### NATS Tunnel
- The SSH tunnel to VM NATS runs on **port 14222**, not 4222
- `AGENTBUS_NATS_URL=nats://bizhou-laptop:laptop-agent-token-2026@localhost:14222`
- SSH tunnel process: `ssh vm -L 14222:localhost:4222 -N`
- Always check `lsof -i :14222` to verify tunnel is up, not port 4222

### VM Deployment Flow
1. The VM copy at `/home/bizhou/workspace/.agentbus/` has **no `.git` directory**
2. `scp` fails due to SSH login banner ("Received message too long" error)
3. Use pipe instead: `cat local/file | ssh vm 'cat > remote/file'`
4. After syncing files: `pip3 install -e /home/bizhou/workspace/.agentbus`
5. Restart listener: `systemctl --user restart agentbus-listener`
6. Verify: `systemctl --user status agentbus-listener`

### When to Apply
- After any code change to files that run on the VM (`adapters/claude.py`, `agentbus/claude_listener.py`, `agentbus/listener.py`)
- The laptop-side code takes effect immediately via `pip install -e .`
- VM-side code requires explicit sync + restart
