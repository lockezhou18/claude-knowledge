---
name: comms
description: "Agent communication layer — check who's online, view health, manage sessions, send messages, start pipes. The situational awareness skill for multi-agent work."
allowed-tools: Bash(python3 -m agentbus*), Bash(agentbus *), Bash(cd *agentbus && agentbus *), Bash(~/bin/vm-agent --health*), Bash(~/bin/vm-agent --sessions*), Bash(~/bin/vm-agent --results*), Bash(~/bin/vm-agent --result*), Bash(bash -c "ssh vm*), Bash(lsof *), Bash(cat *inbox*), Bash(pkill *), Bash(kill *), Bash(export AGENTBUS*), Bash(curl *), Monitor
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
/comms tasks                        — task dashboard across agents
/comms tasks working                — what's in flight
/comms trust a2a-gw-bizhou-vm       — approve untrusted agent (TOFU)
/comms a2a status                   — A2A gateway health
```

## Step 1: Classify the Request

Read the user's input and classify into one of these intents:

| Signal in user's words | Intent | Route to |
|------------------------|--------|----------|
| No args, "status", "dashboard", "overview", "how's", "what's up", "sitrep" | **Dashboard** | Run full dashboard (includes tasks + trust) |
| "who", "agents", "list agents", "online", "registered", "available" | **Who** | List agents |
| "health", "healthy", "infra", "tunnel", "nats", "connected", "reachable" | **Health** | Infra check |
| "session", "sessions", "active sessions", "conversations" | **Sessions** | List sessions |
| "results", "anything new", "pending", "async", "what came back" | **Results** | Show results |
| "ack", "clear", "archive", "mark read", "dismiss", "clean up results" | **Ack** | Archive results |
| "send", "tell", "ask", "say to", "message", "run on" + agent name | **Send** | Send to agent |
| "pipe", "channel", "connect to", "open", "bidirectional", "listen to" | **Pipe** | Start channel |
| "inbox", "incoming", "check messages", "what did.*send" | **Inbox** | Read inbox file |
| "stop", "close", "disconnect", "kill listener", "stop listening" | **Stop** | Kill listener |
| "task", "tasks", "what's running", "in flight", "working", "completed", "what did vm do", "any errors", "what failed", "what finished" | **Tasks** | Task dashboard |
| "trust", "approve", "allow", "accept", "authorize", "let it in", "add to whitelist" + agent name | **Trust** | Approve agent (TOFU) |
| "a2a", "gateway", "http", "external", "is the gateway up", "a2a status" | **A2A** | A2A gateway status |

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

### Tasks (v0.3.0)

Query the task lifecycle store on the VM agent.

**Natural language → command:**

| User says | Interpretation | Command |
|-----------|---------------|---------|
| "tasks", "show tasks", "task list" | all tasks | `agentbus tasks --target bizhou-vm` |
| "what's running", "anything in flight", "what's the vm doing" | working tasks | `agentbus tasks --target bizhou-vm --state working` |
| "what finished", "completed tasks", "what got done" | completed | `agentbus tasks --target bizhou-vm --state completed` |
| "any errors", "what failed", "what broke" | failed | `agentbus tasks --target bizhou-vm --state failed` |
| "what about task abc123", "details on that task" | specific task | `agentbus tasks --target bizhou-vm <task_id>` |
| "cancel that", "stop the build", "kill it" | cancel | `agentbus cancel <task_id> --target bizhou-vm` |

```bash
cd $AGENTBUS_DIR && agentbus tasks --target bizhou-vm
cd $AGENTBUS_DIR && agentbus tasks --target bizhou-vm --state working
cd $AGENTBUS_DIR && agentbus tasks --target bizhou-vm --state failed
cd $AGENTBUS_DIR && agentbus tasks --target bizhou-vm --context <context_id>
cd $AGENTBUS_DIR && agentbus tasks --target bizhou-vm <task_id>
cd $AGENTBUS_DIR && agentbus cancel <task_id> --target bizhou-vm
```

Present as:
```
=== Tasks on bizhou-vm ===
  [>] 2026-04-12T10:30 abc123.. working          mint build hp-ats...
  [+] 2026-04-12T10:28 def456.. completed        echo hello
  [-] 2026-04-12T10:25 ghi789.. failed            grpcurli ...

  3 task(s)
```

---

### Trust (TOFU — v0.3.0)

Approve an untrusted agent. Used when Guardian rejects a sender with: "Agent 'X' detected on bus but not trusted."

**Natural language → command:**

| User says | Interpretation | Command |
|-----------|---------------|---------|
| "trust the gateway", "approve a2a-gw" | trust A2A gateway | `agentbus trust a2a-gw-bizhou-vm --target bizhou-vm` |
| "let it in", "authorize that agent", "accept <name>" | trust named agent | `agentbus trust <name> --target bizhou-vm` |

```bash
cd $AGENTBUS_DIR && agentbus trust <agent_name> --target bizhou-vm
```

This writes an agent card to the VM's agents directory. One-time — persistent across restarts.

**Auto-detect from error:** If a previous command failed with "Agent 'X' detected on bus but not trusted", extract the agent name from the error and suggest the trust command.

---

### A2A (v0.3.0)

Check A2A gateway status.

```bash
# Check if gateway is running (local process)
lsof -i :8080 2>/dev/null | grep -c LISTEN && echo "A2A Gateway: OK (port 8080)" || echo "A2A Gateway: NOT RUNNING"

# Fetch the agent card
curl -s http://localhost:8080/.well-known/agent-card 2>/dev/null | python3 -m json.tool || echo "(gateway not reachable)"
```

Present as:
```
=== A2A Gateway ===
  Status:  OK (port 8080)
  Agent:   bizhou-vm
  Skills:  8
  URL:     http://localhost:8080
```

**SSE Streaming (v0.3.1):** The gateway supports real-time streaming via `POST /message/stream`. Returns Server-Sent Events (submitted → working → completed → done).

**Natural language → A2A commands:**

| User says | Interpretation | Command |
|-----------|---------------|---------|
| "stream a message to the gateway", "watch it in real-time" | SSE stream | `curl -N -X POST http://localhost:8080/message/stream -H 'Content-Type: application/json' -d '{"role":"user","parts":[{"type":"text","text":"..."}]}'` |
| "send via a2a", "http message" | Sync A2A send | `curl -X POST http://localhost:8080/message/send -H 'Content-Type: application/json' -d '{"role":"user","parts":[{"type":"text","text":"..."}]}'` |
| "start the gateway", "run a2a server" | Start gateway | `cd $AGENTBUS_DIR && agentbus a2a-server --agent bizhou-vm --port 8080` |

---

### Agent Card Setup (v0.3.1)

Personal agent cards go in `agents/local/` (gitignored). Copy from examples:
```bash
cp $AGENTBUS_DIR/agents/examples/bizhou-vm.json $AGENTBUS_DIR/agents/local/my-vm.json
# Edit name, capabilities, etc.
```

The listener loads cards from the `agents/` directory (including subdirectories).

---

## Dashboard Enhancement (v0.3.1)

When running the full dashboard, include tasks and A2A status. Tasks are **persistent** (FileTaskStore) — they survive listener restarts.

```
=== AgentBus Comms ===
  Tunnel:    OK / DOWN
  NATS:      OK / DOWN
  Agents:    N registered
  Sessions:  ...
  Results:   N new
  Tasks:     N total (M working, K completed)
  A2A:       OK (port 8080) / NOT RUNNING
```

Add these to the parallel dashboard queries:
```bash
# 6. Tasks summary
cd $AGENTBUS_DIR && agentbus tasks --target bizhou-vm 2>/dev/null | tail -1 || echo "    (unreachable)"

# 7. A2A gateway
lsof -i :8080 2>/dev/null | grep -c LISTEN && echo "    OK (port 8080)" || echo "    not running"
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
