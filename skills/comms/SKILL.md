---
name: comms
description: "Agent communication layer — check who's online, view health, manage sessions, send messages, start pipes. The situational awareness skill for multi-agent work."
allowed-tools: Bash(python3 -m agentbus*), Bash(agentbus *), Bash(cd *agentbus && agentbus *), Bash(~/bin/vm-agent --health*), Bash(~/bin/vm-agent --sessions*), Bash(~/bin/vm-agent --results*), Bash(~/bin/vm-agent --result*), Bash(bash -c "ssh vm*), Bash(lsof *), Bash(cat *inbox*), Bash(pkill *), Bash(kill *), Bash(export AGENTBUS*), Bash(curl *), TaskOutput
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
/comms trust a2a-gw-$TARGET_AGENT       — approve untrusted agent (TOFU)
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
| "a2a", "gateway", "http", "external", "is the gateway up", "a2a status", "stream", "sse" | **A2A** | A2A gateway status + streaming |
| "needs input", "waiting for answer", "paused", "input required", "answer the question" | **InputRequired** | Resume paused tasks |
| "webhook", "push notification", "notify me", "callback" | **Webhooks** | Manage push notifications |

**Agent name resolution:** Match user's words against registered agent card names. "vm" → card with "vm" in name. "laptop" → card with "laptop" in name.

## Step 2: Resolve Context (run once per session)

Before any command, discover the environment dynamically:

```bash
# 1. Find agentbus dir
AGENTBUS_DIR="${AGENTBUS_DIR:-$HOME/workspace/.agentbus}"
AGENTS_DIR="$AGENTBUS_DIR/agents"

# 2. Discover agents (read card files — determine LOCAL_AGENT and TARGET_AGENT)
ls $AGENTS_DIR/*.json $AGENTS_DIR/local/*.json 2>/dev/null

# 3. NATS URL from env
echo "${AGENTBUS_NATS_URL:-nats://localhost:4222}"

# 4. NATS port (for health check)
# Parse from NATS_URL or use AGENTBUS_NATS_PORT env var
```

From the agent cards, determine:
- **LOCAL_AGENT**: Card with "laptop" in name, or `AGENTBUS_FROM` env var
- **TARGET_AGENT**: Card with "vm" in name, or the non-local agent
- **NATS_URL**: `AGENTBUS_NATS_URL` env var
- **NATS_PORT**: Port from NATS_URL, or `AGENTBUS_NATS_PORT`

Use these variables in ALL commands below. **Never hardcode agent names or URLs.**

## Step 3: Execute

---

### Dashboard (default)

Run all in parallel where possible, present as unified view:

```bash
# 1. Tunnel
lsof -i :$NATS_PORT 2>/dev/null | grep -c LISTEN

# 2. Health
cd $AGENTBUS_DIR && python3 -m agentbus.cli health --port $NATS_PORT

# 3. Agents
cd $AGENTBUS_DIR && python3 -m agentbus.cli agents --agents-dir $AGENTS_DIR

# 4. Sessions (catch timeout gracefully)
cd $AGENTBUS_DIR && python3 -c "
import asyncio, sys, os
sys.path.insert(0, '.')
from agentbus.send import send_message
try:
    r = asyncio.run(send_message('$LOCAL_AGENT', '$TARGET_AGENT', {'meta':'list_sessions'}, os.environ['AGENTBUS_NATS_URL'], '$AGENTS_DIR', timeout=8))
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
lsof -i :$NATS_PORT 2>/dev/null | grep LISTEN && echo "Tunnel: OK" || echo "Tunnel: DOWN"
cd $AGENTBUS_DIR && python3 -m agentbus.cli health --port $NATS_PORT
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

### Send — Mode-Aware Router

Choose the right transport based on natural language:

**Step A: Determine transport mode**

| User says | Mode | Why |
|-----------|------|-----|
| "tell vm to X", "ask vm Y", "send message" | **NATS Sync** | Direct, one-shot |
| "run this in the background", "don't wait" | **NATS Async** | Long-running |
| "build then test then fix", "keep going" | **NATS Auto** | Multi-round loop |
| "open a channel", "talk to vm", "chat" | **Pipe** | Ongoing conversation |
| "stream it", "watch live", "show progress" | **SSE Streaming** | Real-time visibility |
| "send via http", "a2a message" | **A2A HTTP** | External protocol |
| Known long task (`mint build`, `mint test`) | **NATS Async** | Inferred from task type |

**Step B: Execute**

```bash
# NATS Sync:
cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT -m "<message>" --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR

# NATS Sync (shell):
cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT -c "<command>" --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR

# NATS Async:
cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT -m "<message>" --async --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR
# Then start background watcher for result (see subscribe-before-send below)

# Pipe:
cd $AGENTBUS_DIR && agentbus pipe --agent $LOCAL_AGENT --to $TARGET_AGENT --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR

# SSE Streaming (needs A2A gateway running):
curl -N -X POST http://localhost:8080/message/stream -H 'Content-Type: application/json' -d '{"role":"user","parts":[{"type":"text","text":"<message>"}]}'

# A2A HTTP Sync:
curl -X POST http://localhost:8080/message/send -H 'Content-Type: application/json' -d '{"role":"user","parts":[{"type":"text","text":"<message>"}]}'
```

**CRITICAL — Subscribe-Before-Send for async:** Use a **background Bash task** to catch results in real-time. Start the watcher BEFORE firing the task — NATS drops events with no subscriber.

```
Step 1 → Bash: TASK_ID=$(python3 -c "import uuid; print(uuid.uuid4())")
Step 2 → Bash(run_in_background=true): cd $AGENTBUS_DIR && python3 -m agentbus.watch_result --task-id $TASK_ID --count 1 --timeout 600 --nats-url "$AGENTBUS_NATS_URL"
Step 3 → Bash: cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT -m "<message>" --async --task-id $TASK_ID --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR
```

The background Bash task runs in the background. When the result arrives via NATS, a `<task-notification>` is automatically injected into this conversation with the output file path. Use `Read` on that path to get the result. No polling needed.

**Safety net** (if watcher times out): poll the task store:
```bash
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT <task_id>
```

**Step C: Present result based on mode**

| Mode | How result arrives |
|------|-------------------|
| NATS Sync | Blocks, show reply directly |
| NATS Async | Background watcher catches it via `<task-notification>`, show when ready |
| Pipe | Interactive — each message gets a reply inline |
| SSE | Events stream in real-time: submitted → working → completed |
| A2A HTTP | JSON response with task object |

---

### Pipe (Bidirectional Channel — v0.3.1)

The `agentbus pipe` command handles everything: bidirectional messaging, context_id for task tracking, and inline task state events.

**Natural language → command:**

| User says | Interpretation | Command |
|-----------|---------------|---------|
| "open a channel to vm", "pipe to vm", "connect to vm" | Interactive pipe | `cd $AGENTBUS_DIR && agentbus pipe --agent $LOCAL_AGENT --to $TARGET_AGENT --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR` |
| "pipe with hooks", "channel with handler" | Pipe + shell hook | Add `--on-message "./handler.sh"` |

```bash
# Interactive pipe (type messages, see replies + task events inline)
cd $AGENTBUS_DIR && agentbus pipe \
  --agent $LOCAL_AGENT \
  --to $TARGET_AGENT \
  --nats-url "$AGENTBUS_NATS_URL" \
  --agents-dir $AGENTS_DIR
```

**What the pipe provides:**
- **Bidirectional**: both sides send and receive simultaneously
- **context_id**: auto-generated session ID links all tasks created during the pipe
- **Task events inline**: when async tasks run, state changes (working → completed) appear in the pipe
- **Shell detection**: commands like `mint build` auto-route as shell; questions route as thinking

Tell the user:
"Pipe to <agent> is open. Type messages and press Enter. Shell commands auto-detected. Async task updates appear inline. Ctrl+C to close."

**To see tasks from a pipe session later:**
```bash
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --context <pipe-session-id>
```

---

### Inbox

```bash
cat ~/agentbus-inbox.log 2>/dev/null || echo "(no messages yet)"
```

---

### Stop

```bash
pkill -f "hook_listener.*$LOCAL_AGENT" 2>/dev/null && echo "Listener stopped" || echo "No listener running"
```

---

### Tasks (v0.3.0)

Query the task lifecycle store on the VM agent.

**Natural language → command:**

| User says | Interpretation | Command |
|-----------|---------------|---------|
| "tasks", "show tasks", "task list" | all tasks | `agentbus tasks --target $TARGET_AGENT` |
| "what's running", "anything in flight", "what's the vm doing" | working tasks | `agentbus tasks --target $TARGET_AGENT --state working` |
| "what finished", "completed tasks", "what got done" | completed | `agentbus tasks --target $TARGET_AGENT --state completed` |
| "any errors", "what failed", "what broke" | failed | `agentbus tasks --target $TARGET_AGENT --state failed` |
| "what about task abc123", "details on that task" | specific task | `agentbus tasks --target $TARGET_AGENT <task_id>` |
| "cancel that", "stop the build", "kill it" | cancel | `agentbus cancel <task_id> --target $TARGET_AGENT` |

```bash
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --state working
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --state failed
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --context <context_id>
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT <task_id>
cd $AGENTBUS_DIR && agentbus cancel <task_id> --target $TARGET_AGENT
```

Present as:
```
=== Tasks on $TARGET_AGENT ===
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
| "trust the gateway", "approve a2a-gw" | trust A2A gateway | `agentbus trust a2a-gw-$TARGET_AGENT --target $TARGET_AGENT` |
| "let it in", "authorize that agent", "accept <name>" | trust named agent | `agentbus trust <name> --target $TARGET_AGENT` |

```bash
cd $AGENTBUS_DIR && agentbus trust <agent_name> --target $TARGET_AGENT
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
  Agent:   $TARGET_AGENT
  Skills:  8
  URL:     http://localhost:8080
```

**SSE Streaming (v0.3.1):** The gateway supports real-time streaming via `POST /message/stream`. Returns Server-Sent Events (submitted → working → completed → done).

**Natural language → A2A commands:**

| User says | Interpretation | Command |
|-----------|---------------|---------|
| "stream a message to the gateway", "watch it in real-time" | SSE stream | `curl -N -X POST http://localhost:8080/message/stream -H 'Content-Type: application/json' -d '{"role":"user","parts":[{"type":"text","text":"..."}]}'` |
| "send via a2a", "http message" | Sync A2A send | `curl -X POST http://localhost:8080/message/send -H 'Content-Type: application/json' -d '{"role":"user","parts":[{"type":"text","text":"..."}]}'` |
| "start the gateway", "run a2a server" | Start gateway | `cd $AGENTBUS_DIR && agentbus a2a-server --agent $TARGET_AGENT --port 8080` |

---

### Input Required (v0.3.1)

When a task pauses because the agent needs user input:

| User says | Interpretation | Command |
|-----------|---------------|---------|
| "what's waiting for input", "anything paused" | Find paused tasks | `cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --state input_required` |
| "answer with X", "tell it X" | Resume task | `cd $AGENTBUS_DIR && echo '{"resume_task_id":"<id>","message":"<answer>"}' | agentbus send --to $TARGET_AGENT --stdin` |

---

### Webhooks (v0.3.1)

Manage push notification callbacks on A2A gateway tasks:

| User says | Interpretation | Command |
|-----------|---------------|---------|
| "notify me when done", "webhook for this task" | Register webhook | `curl -X POST http://localhost:8080/tasks/<id>/pushNotificationConfigs -H 'Content-Type: application/json' -d '{"url":"<callback-url>"}'` |
| "check webhooks", "what's watching this task" | List webhooks | `curl http://localhost:8080/tasks/<id>/pushNotificationConfigs` |
| "remove webhooks" | Delete all for task | `curl -X DELETE http://localhost:8080/tasks/<id>/pushNotificationConfigs` |

Webhooks fire on every terminal state change (completed, failed, canceled). Works for both `/message/send` and `/message/stream`.

---

### Agent Card Setup (v0.3.1)

Personal agent cards go in `agents/local/` (gitignored). Copy from examples:
```bash
cp $AGENTBUS_DIR/agents/examples/$TARGET_AGENT.json $AGENTBUS_DIR/agents/local/my-vm.json
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
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT 2>/dev/null | tail -1 || echo "    (unreachable)"

# 7. A2A gateway
lsof -i :8080 2>/dev/null | grep -c LISTEN && echo "    OK (port 8080)" || echo "    not running"
```

---

## Troubleshooting

If any command fails:

| Symptom | Fix |
|---------|-----|
| Tunnel DOWN | `bash -c "ssh -f -N -L $NATS_PORT:localhost:4222 vm"` |
| NATS DOWN | Check VM: `bash -c "ssh vm 'docker ps \| grep nats'"` |
| "No responders" | VM listener not running: `bash -c "ssh vm 'tmux attach -t agentbus'"` |
| Timeout on sessions | VM listener crashed — restart: `bash -c "ssh vm 'tmux send-keys -t agentbus C-c; sleep 2; tmux send-keys -t agentbus \"cd ~/agentbus && agentbus listen --agent $TARGET_AGENT --workspace ~/workspace\" Enter'"` |
| Auth expired | Kerberos: `! kinit`; Claude on VM: `! ssh -t vm 'claude auth login'` |
