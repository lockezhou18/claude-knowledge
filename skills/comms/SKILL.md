---
name: comms
description: "Agent communication layer — check who's online, view health, manage sessions, send messages, start pipes. The situational awareness skill for multi-agent work."
allowed-tools: Bash(python3 -m agentbus*), Bash(agentbus *), Bash(~/bin/vm-agent --health*), Bash(~/bin/vm-agent --sessions*), Bash(~/bin/vm-agent --results*), Bash(~/bin/vm-agent --result*), Bash(bash -c "ssh vm*), Bash(lsof *), Bash(cat */results/*.json*), Monitor
inputs: ["subcommand"]
---

# Comms — Agent Communication Layer

Situational awareness for the multi-agent network. Check who's reachable, view sessions, send quick messages, manage listeners.

```
/comms              — full dashboard (health + agents + sessions + results)
/comms status       — same as above
/comms who          — list agents and capabilities
/comms health       — NATS, tunnel, infra check
/comms sessions     — active stateful sessions
/comms results      — unread async results
/comms ack          — archive all results (mark as seen)
/comms ack <id>     — archive one specific result
/comms send <agent> <message>  — quick send
/comms pipe <agent> — start bidirectional pipe
/comms listen       — start hook listener on this machine
```

## Environment

```bash
export AGENTBUS_NATS_URL="nats://bizhou-laptop:laptop-agent-token-2026@localhost:14222"
AGENTS_DIR="$HOME/workspace/.agentbus/agents"
AGENTBUS_DIR="$HOME/workspace/.agentbus"
```

Always set these before running any agentbus command.

## Subcommand Routing

Parse the user's input after `/comms` and route:

### `/comms` or `/comms status` — Full Dashboard

Run all of these and present as a unified view:

```bash
# 1. Tunnel check
lsof -i :14222 2>/dev/null | grep -c LISTEN

# 2. Health
cd $AGENTBUS_DIR && python3 -m agentbus.cli health --port 14222

# 3. Agents
cd $AGENTBUS_DIR && python3 -m agentbus.cli agents --agents-dir $AGENTS_DIR

# 4. Sessions (may timeout if VM listener is down — catch gracefully)
cd $AGENTBUS_DIR && python3 -c "
import asyncio, sys, os
sys.path.insert(0, '.')
from agentbus.send import send_message
try:
    r = asyncio.run(send_message('bizhou-laptop', 'bizhou-vm', {'meta':'list_sessions'}, os.environ['AGENTBUS_NATS_URL'], '$AGENTS_DIR', timeout=8))
    sessions = r.get('sessions', {})
    if not sessions: print('    (no active sessions)')
    for k,v in sessions.items():
        print(f'    {k}: session={v[\"session_id\"][:12]}.. idle={v.get(\"idle_seconds\",0)}s')
except: print('    (VM unreachable)')
"

# 5. Unread async results
cd $AGENTBUS_DIR && python3 -m agentbus.cli results 2>/dev/null || echo "    (no results)"
```

Present as:

```
=== AgentBus Comms ===
  Tunnel:    OK / DOWN
  NATS:      OK / DOWN
  Agents:    N registered
    name1    [status] description
    name2    [status] description
  Sessions:  N active
    key      session=... idle=...s
  Results:   N pending
```

### `/comms who` — List Agents

```bash
cd $AGENTBUS_DIR && python3 -m agentbus.cli agents --agents-dir $AGENTS_DIR
```

### `/comms health` — Infrastructure Check

```bash
# Check tunnel
lsof -i :14222 2>/dev/null | grep LISTEN && echo "Tunnel: OK" || echo "Tunnel: DOWN"

# AgentBus health
cd $AGENTBUS_DIR && python3 -m agentbus.cli health --port 14222

# VM agent health (if reachable)
~/bin/vm-agent --health 2>&1 || echo "(VM unreachable)"
```

### `/comms sessions` — Active Sessions

Try vm-agent first (faster, handles errors), fall back to CLI:

```bash
# Primary: via vm-agent (catches timeouts gracefully)
~/bin/vm-agent --sessions 2>&1 || echo "(VM unreachable — listener may be down)"
```

### `/comms results` — Async Results

```bash
# List unread results
cd $AGENTBUS_DIR && python3 -m agentbus.cli results

# Include archived (already ack'd)
cd $AGENTBUS_DIR && python3 -m agentbus.cli results --all

# Detail for a specific task
cd $AGENTBUS_DIR && python3 -m agentbus.cli results <task_id>

# Raw JSON output
cd $AGENTBUS_DIR && python3 -m agentbus.cli results --json
```

### `/comms ack` — Acknowledge Results

Move results to `.archive/` — acknowledged but kept for audit.

```bash
# Archive all unread results
cd $AGENTBUS_DIR && python3 -m agentbus.cli ack

# Archive one specific result
cd $AGENTBUS_DIR && python3 -m agentbus.cli ack <task_id>
```

After ack, results no longer show in `/comms results` but are visible with `--all`.

### `/comms send <agent> <message>` — Quick Send

Parse agent name and message from the input, then:

```bash
cd $AGENTBUS_DIR && python3 -m agentbus.cli send \
  --to <agent> --from bizhou-laptop \
  --message "<message>" \
  --nats-url "$AGENTBUS_NATS_URL" \
  --agents-dir $AGENTS_DIR \
  --timeout 30
```

If the message looks like a shell command (starts with known tool: `mint`, `echo`, `ls`, etc.), use `--command` instead of `--message`.

For async: if user says "in the background" or "async", add `--async` and start Monitor:

```bash
# After getting the task_id from the async response:
Monitor: cd $AGENTBUS_DIR && python3 -m agentbus.watch_result --task-id <task_id> --count 1 --timeout 600 --nats-url "$AGENTBUS_NATS_URL"
```

### `/comms pipe <agent>` — Bidirectional Pipe

```bash
cd $AGENTBUS_DIR && python3 -m agentbus.cli pipe \
  --agent bizhou-laptop --to <agent> \
  --nats-url "$AGENTBUS_NATS_URL" \
  --agents-dir $AGENTS_DIR
```

Tell the user: "Starting bidirectional pipe. Type messages to send, incoming messages appear inline. Ctrl+C to stop."

### `/comms listen` — Start Hook Listener

Ask the user what the hook command should be, or use a sensible default:

```bash
# Default: log to file + print
cd $AGENTBUS_DIR && python3 -m agentbus.cli listen \
  --agent bizhou-laptop \
  --on-message 'echo "[$(date +%H:%M:%S)] from=$AGENTBUS_FROM: $AGENTBUS_MESSAGE" | tee -a ~/agentbus-inbox.log' \
  --nats-url "$AGENTBUS_NATS_URL" \
  --agents-dir $AGENTS_DIR

# Custom hook example:
cd $AGENTBUS_DIR && python3 -m agentbus.cli listen \
  --agent bizhou-laptop \
  --on-message '<user-provided-command>' \
  --nats-url "$AGENTBUS_NATS_URL" \
  --agents-dir $AGENTS_DIR
```

## Troubleshooting

If any command fails:

| Symptom | Fix |
|---------|-----|
| Tunnel DOWN | `bash -c "ssh -f -N -L 14222:localhost:4222 vm"` |
| NATS DOWN | Check VM: `bash -c "ssh vm 'docker ps \| grep nats'"` |
| "No responders" | VM listener not running: `bash -c "ssh vm 'tmux attach -t agentbus'"` |
| Timeout on sessions | VM listener crashed — restart: `bash -c "ssh vm 'cd ~/agentbus && tmux send-keys -t agentbus C-c; sleep 2; tmux send-keys -t agentbus \"python3 -m agentbus.claude_listener --agent bizhou-vm --nats-url nats://bizhou-vm:vm-agent-token-2026@localhost:4222 --agents-dir ./agents --workspace ~/workspace\" Enter'"` |
| Auth expired | Kerberos: `! kinit`; Claude on VM: `! ssh -t vm 'claude auth login'` |
