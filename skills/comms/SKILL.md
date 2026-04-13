---
name: comms
description: "Agent communication layer — check who's online, view health, manage sessions, send messages, start pipes. The situational awareness skill for multi-agent work."
allowed-tools: Bash(python3 -m agentbus*), Bash(agentbus *), Bash(cd *agentbus && agentbus *), Bash(~/bin/vm-agent --health*), Bash(~/bin/vm-agent --sessions*), Bash(~/bin/vm-agent --results*), Bash(~/bin/vm-agent --result*), Bash(bash -c "ssh vm*), Bash(lsof *), Bash(cat *inbox*), Bash(pkill *), Bash(kill *), Bash(export AGENTBUS*), Bash(curl *), Monitor
inputs: ["request"]
---

# Comms — Agent Communication Layer

Just describe what you want. The skill figures out the subcommand.

## Step 1: Classify Intent

| Signal | Intent | Read file |
|--------|--------|-----------|
| No args, "status", "dashboard", "how's", "sitrep" | **Dashboard** | `dashboard.md` |
| "who", "agents", "online" | **Who** | `dashboard.md` |
| "health", "infra", "tunnel", "nats" | **Health** | `dashboard.md` |
| "session", "sessions", "active sessions" | **Sessions** | `dashboard.md` |
| "results", "anything new", "pending" | **Results** | `tasks.md` |
| "ack", "clear", "archive", "mark read" | **Ack** | `tasks.md` |
| "send", "tell", "ask", "run on" + agent name | **Send** | `send.md` |
| "task", "tasks", "working", "completed", "failed", "cancel" | **Tasks** | `tasks.md` |
| "pipe", "channel", "connect to", "open" | **Pipe** | `advanced.md` |
| "a2a", "gateway", "http", "stream", "sse" | **A2A** | `advanced.md` |
| "trust", "approve", "authorize" | **Trust** | `advanced.md` |
| "needs input", "waiting for answer", "paused" | **InputRequired** | `advanced.md` |
| "webhook", "push notification" | **Webhooks** | `advanced.md` |
| "inbox", "check messages" | **Inbox** | `tasks.md` |
| "stop", "close", "kill listener" | **Stop** | `tasks.md` |
| Connection error, timeout | **Troubleshoot** | `troubleshooting.md` |

**Agent name resolution:** "vm" → card with "vm" in name. "laptop" → card with "laptop" in name.

## Step 2: Resolve Context (once per session)

```bash
AGENTBUS_DIR="${AGENTBUS_DIR:-$HOME/workspace/.agentbus}"
AGENTS_DIR="$AGENTBUS_DIR/agents"
# Discover agents from: ls $AGENTS_DIR/*.json $AGENTS_DIR/local/*.json
# LOCAL_AGENT: card with "laptop" | TARGET_AGENT: card with "vm"
# NATS_URL: $AGENTBUS_NATS_URL | NATS_PORT: parsed from URL
```

## Step 3: Read the sub-file and execute

Based on the classified intent, `Read` the corresponding `.md` file from the same directory as this skill, then follow its instructions.

All sub-files assume the context variables (AGENTBUS_DIR, AGENTS_DIR, LOCAL_AGENT, TARGET_AGENT, NATS_URL) are resolved.
