---
name: comms
description: "Agent communication layer — check who's online, view health, manage sessions, send messages, start pipes. The situational awareness skill for multi-agent work."
allowed-tools: Bash(python3 -m agentbus*), Bash(agentbus *), Bash(~/bin/vm-agent --health*), Bash(~/bin/vm-agent --sessions*), Bash(~/bin/vm-agent --results*), Bash(~/bin/vm-agent --result*), Bash(bash -c "ssh vm*), Bash(lsof *), Bash(cat *inbox*), Bash(pkill *), Bash(kill *), Bash(export AGENTBUS*), Monitor
inputs: ["request"]
---

# Comms — Agent Communication Layer

Just describe what you want. The skill figures out the subcommand.

```
/comms                              — full dashboard
/comms how's the network            — full dashboard
/comms who's online                 — list agents
/comms is everything healthy        — infra check
/comms any active sessions on vm    — sessions
/comms anything new                 — unread results
/comms clear the inbox              — ack all results
/comms tell vm to run the tests     — send to VM
/comms ask vm what OS it's running  — send thinking task
/comms open a channel to vm         — start bidirectional pipe
/comms check inbox                  — read incoming messages
/comms stop listening               — stop background listener
```

## Step 1: Classify the Request

Read the user's input and classify into one of these intents:

| Signal in user's words | Intent | Route to |
|------------------------|--------|----------|
| No args, "status", "dashboard", "overview", "how's", "what's up", "sitrep" | **Dashboard** | Run full dashboard |
| "who", "agents", "list agents", "online", "registered", "available" | **Who** | List agents |
| "health", "healthy", "infra", "tunnel", "nats", "connected", "reachable" | **Health** | Infra check |
| "session", "sessions", "active sessions", "conversations" | **Sessions** | List sessions |
| "results", "anything new", "pending", "async", "what came back" | **Results** | Show results |
| "ack", "clear", "archive", "mark read", "dismiss", "clean up results" | **Ack** | Archive results |
| "send", "tell", "ask", "say to", "message", "run on" + agent name | **Send** | Send to agent |
| "pipe", "channel", "connect to", "open", "bidirectional", "listen to" | **Pipe** | Start channel |
| "inbox", "incoming", "check messages", "what did.*send" | **Inbox** | Read inbox file |
| "stop", "close", "disconnect", "kill listener", "stop listening" | **Stop** | Kill listener |

**Agent name resolution:** If the user says "vm", resolve to `bizhou-vm`. If "laptop", resolve to `bizhou-laptop`. Match against registered agent card names.

## Step 2: Execute

### Environment (set before EVERY command)

```bash
export AGENTBUS_NATS_URL="nats://bizhou-laptop:laptop-agent-token-2026@localhost:14222"
export AGENTS_DIR="$HOME/workspace/.agentbus/agents"
export AGENTBUS_DIR="$HOME/workspace/.agentbus"
```

---

### Dashboard (default)

Run all in parallel where possible, present as unified view:

```bash
# 1. Tunnel
lsof -i :14222 2>/dev/null | grep -c LISTEN

# 2. Health
cd $AGENTBUS_DIR && python3 -m agentbus.cli health --port 14222

# 3. Agents
cd $AGENTBUS_DIR && python3 -m agentbus.cli agents --agents-dir $AGENTS_DIR

# 4. Sessions (catch timeout gracefully)
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

# 5. Unread results
cd $AGENTBUS_DIR && python3 -m agentbus.cli results 2>/dev/null || echo "    (no results)"
```

Present as:
```
=== AgentBus Comms ===
  Tunnel:    OK / DOWN
  NATS:      OK / DOWN
  Agents:    N registered
  Sessions:  ...
  Results:   ...
```

---

### Who

```bash
cd $AGENTBUS_DIR && python3 -m agentbus.cli agents --agents-dir $AGENTS_DIR
```

---

### Health

```bash
lsof -i :14222 2>/dev/null | grep LISTEN && echo "Tunnel: OK" || echo "Tunnel: DOWN"
cd $AGENTBUS_DIR && python3 -m agentbus.cli health --port 14222
~/bin/vm-agent --health 2>&1 || echo "(VM unreachable)"
```

---

### Sessions

```bash
~/bin/vm-agent --sessions 2>&1 || echo "(VM unreachable)"
```

---

### Results

```bash
# Default: unread only
cd $AGENTBUS_DIR && python3 -m agentbus.cli results

# If user asks for "all" or "everything": add --all
# If user asks about a specific task: pass the task_id
cd $AGENTBUS_DIR && python3 -m agentbus.cli results <task_id>
```

---

### Ack

```bash
# All
cd $AGENTBUS_DIR && python3 -m agentbus.cli ack

# Specific task
cd $AGENTBUS_DIR && python3 -m agentbus.cli ack <task_id>
```

---

### Send

**Classify the message type:**

| Signal | Type | Flag |
|--------|------|------|
| Exact command: `mint build`, `echo`, `ls`, `uname`, `docker`, `kubectl` | Shell | `-c` |
| Needs reasoning: "what", "why", "how", "review", "investigate", "explain" | Thinking | `-m` |
| User says "in background", "async", "don't wait" | Async | add `--async` |
| Ambiguous | Thinking | `-m` (safer) |

```bash
cd $AGENTBUS_DIR && python3 -m agentbus.cli send \
  --to <agent> \
  -m "<message>" \  # or -c "<command>" for shell
  --nats-url "$AGENTBUS_NATS_URL" \
  --agents-dir $AGENTS_DIR \
  --timeout 30
```

For async, after getting the task_id:
```bash
Monitor: cd $AGENTBUS_DIR && python3 -m agentbus.watch_result --task-id <task_id> --count 1 --timeout 600 --nats-url "$AGENTBUS_NATS_URL"
```

---

### Pipe (Bidirectional Channel)

Start a background listener + tell user they can now send.

```bash
INBOX_FILE="$HOME/agentbus-inbox.log"
cd $AGENTBUS_DIR && python3 -m agentbus.hook_listener \
  --agent bizhou-laptop \
  --on-message 'MSG=$(cat); echo "[$(date +%H:%M:%S)] from=$AGENTBUS_FROM: $AGENTBUS_MESSAGE" >> '"$INBOX_FILE"'; echo "received"' \
  --nats-url "$AGENTBUS_NATS_URL" \
  --agents-dir $AGENTS_DIR \
  --log-level WARNING &
LISTENER_PID=$!
echo "Channel open (PID: $LISTENER_PID). Incoming → $INBOX_FILE"
```

Run with `run_in_background: true`. Then tell the user:
"Channel to <agent> is open. Use `/comms send <agent> <message>` to send. Incoming messages land in ~/agentbus-inbox.log. Use `/comms inbox` to check. `/comms stop` to close."

---

### Inbox

```bash
cat ~/agentbus-inbox.log 2>/dev/null || echo "(no messages yet)"
```

---

### Stop

```bash
pkill -f "hook_listener.*bizhou-laptop" 2>/dev/null && echo "Listener stopped" || echo "No listener running"
```

---

## Troubleshooting

If any command fails:

| Symptom | Fix |
|---------|-----|
| Tunnel DOWN | `bash -c "ssh -f -N -L 14222:localhost:4222 vm"` |
| NATS DOWN | Check VM: `bash -c "ssh vm 'docker ps \| grep nats'"` |
| "No responders" | VM listener not running: `bash -c "ssh vm 'tmux attach -t agentbus'"` |
| Timeout on sessions | VM listener crashed — restart: `bash -c "ssh vm 'cd ~/agentbus && tmux send-keys -t agentbus C-c; sleep 2; tmux send-keys -t agentbus \"python3 -m agentbus.claude_listener --agent bizhou-vm --nats-url nats://bizhou-vm:vm-agent-token-2026@localhost:4222 --agents-dir ./agents --workspace ~/workspace\" Enter'"` |
| Auth expired | Kerberos: `! kinit`; Claude on VM: `! ssh -t vm 'claude auth login'` |
