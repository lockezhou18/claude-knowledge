---
name: delegate
description: "Delegate tasks to the VM agent. Just describe what you want in natural language — the skill figures out the mode, transport, and flags automatically."
allowed-tools: Bash(bash -c "ssh vm*), Bash(bash -c "scp*), Bash(bash -c "rsync*), Bash(bash -c "cd * && vm-run*), Bash(bash -c "vm-run*), Bash(export PATH*vm-run*), Bash(~/bin/vm-agent*), Bash(cd *agentbus && agentbus *), Bash(curl *), Monitor
inputs: ["task"]
---

# Delegate — Send Work to the VM Agent

Just say what you want. The skill figures out the rest.

## Step 0: Resolve Context (once per session)

```bash
AGENTBUS_DIR="${AGENTBUS_DIR:-$HOME/workspace/.agentbus}"
AGENTS_DIR="$AGENTBUS_DIR/agents"
# Discover agents from: ls $AGENTS_DIR/*.json $AGENTS_DIR/local/*.json
# LOCAL_AGENT: card with "laptop" | TARGET_AGENT: card with "vm"
# NATS_URL: $AGENTBUS_NATS_URL
```

## Step 1: Classify the Request

**A. Mode** (3 layers — explicit > task-type > conversation pattern):

| Signal | Mode |
|--------|------|
| "background", "async", "don't wait" | **Async** |
| "keep going until", "loop until green" | **Auto** |
| "talk to vm", "open a channel" | **Pipe** |
| `mint build`, `mint test`, `gradlew` | **Async** (inferred) |
| `go-status`, `echo`, `ls` | **Sync** (instant) |
| "review", "investigate", "analyze" | **Sync** (thinking) |
| Multi-step: "build then test" | **Auto** |

**B. Shell or Think?**

| Signal | Type | Execute |
|--------|------|---------|
| Exact command (`mint`, `go-status`, `grpcurli`, `ls`) | Shell | `~/bin/vm-agent "<cmd>"` |
| Reasoning ("review", "investigate", "what", "why") | Think | `~/bin/vm-agent -t "<msg>"` |
| Ambiguous | Think | Safer — VM Claude runs shell itself |
| grpcurli/curli with complex JSON | Think | Always `-t` — quoting mangles JSON in shell mode |

**C. Repo?** If user mentions a repo → `--repo <name>`. If unclear → omit.

**D. Fresh?** "fresh"/"new"/"start over" → `--new`. Otherwise auto-resumes.

## Step 2: Build and Execute

```bash
~/bin/vm-agent "<shell command>"              # Shell sync
~/bin/vm-agent -t "<message>"                 # Think sync
~/bin/vm-agent -t --repo <repo> "<message>"   # Think sync + repo
~/bin/vm-agent --async "<message>"            # Async
~/bin/vm-agent --auto "<message>"             # Auto (multi-round)
~/bin/vm-agent --new -t "<message>"           # Fresh session
```

**If Async or Auto** → Read `async.md` for subscribe-before-send pattern.
**For task tracking, pipe, A2A, input-required** → Read `lifecycle.md`.

## Session Management

```
~/bin/vm-agent --sessions      # check active sessions
~/bin/vm-agent --end-session   # end current session
~/bin/vm-agent --health        # health check
```

## Fallback Chain
1. AgentBus unreachable → SSH: `bash -c "ssh vm '...'"`
2. VM unreachable → run locally
3. VM agent escalates → show to user

## Troubleshooting
- NATS tunnel down → vm-agent auto-creates. If fails → check VPN, `klist`
- Listener not running → `bash -c "ssh vm 'tmux attach -t agentbus'"`
- Claude auth expired → `! ssh -t vm 'claude auth login'`
