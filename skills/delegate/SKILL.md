---
name: delegate
description: "Delegate tasks to the VM agent. Just describe what you want in natural language — the skill figures out the mode, transport, and flags automatically."
allowed-tools: Bash(bash -c "ssh vm*), Bash(bash -c "scp*), Bash(bash -c "rsync*), Bash(bash -c "cd * && vm-run*), Bash(bash -c "vm-run*), Bash(export PATH*vm-run*), Bash(~/bin/vm-agent*), Bash(cd *agentbus && agentbus *), Bash(curl *), Monitor
inputs: ["task"]
---

# Delegate — Send Work to the VM Agent

Just say what you want. The skill figures out the rest.

## Step 0: Resolve Context (run once per session)

Before any command, discover the environment. Read these to determine agent names, NATS URL, and paths:

```bash
# 1. Find agentbus dir
AGENTBUS_DIR="${AGENTBUS_DIR:-$HOME/workspace/.agentbus}"
AGENTS_DIR="$AGENTBUS_DIR/agents"

# 2. Discover agents (read card files)
ls $AGENTS_DIR/*.json $AGENTS_DIR/local/*.json 2>/dev/null

# 3. Resolve NATS URL from env
echo "${AGENTBUS_NATS_URL:-nats://localhost:4222}"
```

From the agent cards, determine:
- **LOCAL_AGENT**: Card with "laptop" in name, or `AGENTBUS_FROM` env var
- **TARGET_AGENT**: Card with "vm" in name, or the non-local agent
- **NATS_URL**: `AGENTBUS_NATS_URL` env var

Use these variables in ALL commands below. **Never hardcode agent names** — different users have different card names.

```
/delegate review the latest PR for hp-ats-integration-mt
/delegate run mint build
/delegate check go-status for hp-ats-integration-mt
/delegate investigate why the pipeline is stuck
/delegate run the full test suite in the background
/delegate build, test, fix failures, and re-test until green
/delegate what are the last 5 commits in hp-ats-integration-mt
```

## Step 1: Understand the Request — Mode Decision Engine

The skill chooses the right mode from natural language. Three layers of signals:

### Layer 1: Explicit signals (highest priority)

| User says | Mode |
|-----------|------|
| "in the background", "async", "don't wait", "fire and forget" | **Async** |
| "keep going until", "fix and re-test", "loop until green" | **Auto** |
| "talk to vm", "open a channel", "interactive", "chat with" | **Pipe** |
| "stream it", "show me live", "watch progress", "real-time" | **SSE Streaming** |
| "via http", "a2a", "send to gateway" | **A2A Sync** |

### Layer 2: Task-type inference (if no explicit signal)

| Task type | Default mode | Reason |
|-----------|-------------|--------|
| `mint build`, `mint test`, `gradlew`, full test suites | **Async** | Known long-running (30s+) |
| `go-deploy`, `go-status` | **Sync** | Quick status checks |
| `echo`, `ls`, `cat`, `uname`, `pwd` | **Sync** | Instant commands |
| "review", "investigate", "analyze" (thinking) | **Sync** | User typically waits for reasoning |
| "build then test then deploy" (multi-step) | **Auto** | Sequential loop |
| Follow-up to a previous question | **Pipe** or resume same session | Conversational |

### Layer 3: Conversation pattern (lowest priority)

| Pattern | Mode |
|---------|------|
| Single question, expects one answer | **Sync** |
| User asked 2+ follow-up questions to the same agent | Suggest **Pipe** |
| User is monitoring external system | Suggest **SSE Streaming** |
| User will switch to other work while waiting | **Async** |

### Mode → Execution mapping

| Mode | Execute with | Result delivery |
|------|-------------|-----------------|
| **Sync** | `~/bin/vm-agent "<cmd>"` or `~/bin/vm-agent -t "<msg>"` | Block, show result |
| **Async** | `~/bin/vm-agent --async "<msg>"` + Monitor | Background, notify when done |
| **Auto** | `~/bin/vm-agent --auto "<msg>"` + Monitor | Multi-round, stream checkpoints |
| **Pipe** | `agentbus pipe --agent $LOCAL_AGENT --to $TARGET_AGENT` | Interactive bidirectional |
| **SSE Streaming** | `curl -N POST http://localhost:8080/message/stream` | Real-time HTTP events |
| **A2A Sync** | `curl POST http://localhost:8080/message/send` | HTTP request/response |

**B. Shell or thinking?**

| Signal | Type | How to execute |
|--------|------|----------------|
| Exact command: `mint build`, `mint test`, `gradlew`, `go-status`, `grpcurli`, `curli`, `echo`, `ls`, `cat`, `grep` | **Shell** | `~/bin/vm-agent "<command>"` |
| Needs reasoning: "review", "investigate", "explain", "analyze", "what", "why", "how", "check", "find", "compare" | **Think** | `~/bin/vm-agent -t "<message>"` |
| Ambiguous | **Think** | Safer — VM Claude can run shell commands itself |

**C. Which repo?**

If the user mentions a repo name (e.g., "hp-ats-integration-mt", "mcm-mt"), add `--repo <name>`.
If working in a repo directory, infer from cwd.
If unclear, omit — VM agent uses ~/workspace.

**D. Fresh or continue?**

If "fresh", "new", "start over" → add `--new`
If follow-up to previous delegate → omit (auto-resumes)

## Step 2: Build and Run the Command

Assemble the `~/bin/vm-agent` command from the classification:

```bash
# Shell sync:
~/bin/vm-agent "<shell command>"

# Think sync:
~/bin/vm-agent -t "<message>"

# Think sync with repo:
~/bin/vm-agent -t --repo <repo> "<message>"

# Async (any):
~/bin/vm-agent --async "<message>"

# Auto (multi-round):
~/bin/vm-agent --auto "<message>"

# Fresh session:
~/bin/vm-agent --new -t "<message>"
```

## Step 3: For Async/Auto — Start Monitor

After firing an async or auto task, start the Monitor to watch for results:

```bash
# Get the task_id from the async response, then:
# (run from ~/projects/compound-learning-ecosystem/agentbus)

# Async (one result):
Monitor: python3 -m agentbus.watch_result --task-id <task_id> --count 1 --timeout 600

# Auto (stream checkpoints):
Monitor: python3 -m agentbus.watch_result --task-id <task_id> --count 0 --timeout 1800
```

Tell the user: "Task delegated. I'm watching for results — keep working."

## Step 4: Present Result

- **Sync**: show the result directly
- **Async**: Monitor catches result → present it when it arrives
- **Escalation**: if VM agent returns "ESCALATE:", show the escalation to the user with the suggested action
- **Retry**: Async tasks auto-retry up to 2 times on transient failures (3s → 6s → 12s backoff). Tell user: "Task failed but retrying..." if you see retry logs. Override with `max_retries` in payload (0 = no retry, try once).

### Retry-aware natural language

| User says | Interpretation |
|-----------|---------------|
| "try again if it fails", "keep trying", "retry" | Add `max_retries: 3` to payload |
| "just try once", "no retries", "one shot" | Add `max_retries: 0` to payload |
| "keep retrying until it works" | Use auto mode (`--auto`) instead — that's the multi-round loop |

## Examples

| User says | Classification | Command |
|-----------|---------------|---------|
| "run mint build" | shell, sync | `~/bin/vm-agent "mint build"` |
| "build hp-ats-integration-mt" | shell, sync | `~/bin/vm-agent "cd ~/workspace/connected_project_phase2/hp-ats-integration-mt && mint build"` |
| "review the latest PR" | think, sync | `~/bin/vm-agent -t "review the latest PR"` |
| "what are the last 5 commits" | think, sync | `~/bin/vm-agent -t "what are the last 5 commits"` |
| "investigate why the build failed in hp-ats" | think, sync, repo | `~/bin/vm-agent -t --repo hp-ats-integration-mt "investigate why the build failed"` |
| "run the test suite in the background" | shell, async | `~/bin/vm-agent --async "mint test"` + Monitor |
| "build, test, fix, re-test until green" | think, auto | `~/bin/vm-agent --auto "build, test, fix failures, re-test"` + Monitor |
| "check go-status for hp-ats" | shell, sync | `~/bin/vm-agent "go-status hp-ats-integration-mt"` |
| "run grpcurli to get HireEntityRequest 123" | think, sync | `~/bin/vm-agent -t "run grpcurli to get HireEntityRequest with requestId 123 from ManagedEntityCrudHireEntityRequest on ei-ltx1"` |
| "start fresh — analyze the test failures" | think, sync, new | `~/bin/vm-agent --new -t "analyze the test failures"` |

**Note on grpcurli/curli with complex JSON**: Always use **think mode** (`-t`). The VM Claude builds the command locally with correct escaping. Don't try to pass complex JSON through shell mode — quoting mangles it.

## Step 5: Task Lifecycle (v0.3.1)

After async/auto delegation, use the task store for lifecycle tracking. Tasks are **persistent** (FileTaskStore) — they survive listener restarts. No more lost state.

**A. Check task status:**
```bash
# After async delegation returns task_id:
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT <task_id>
```

**B. List delegated tasks:**
```bash
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --state working    # what's in flight
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --state completed  # what finished
```

**C. Cancel a running task:**
```bash
cd $AGENTBUS_DIR && agentbus cancel <task_id> --target $TARGET_AGENT
```
Tell user: "Task canceled. Note: the background process on VM may still be running (cancel is state-only in v0.3.0)."

**D. Track multi-step delegations with context_id:**
For auto-mode (`--auto`), the listener creates tasks with context_id. Query all tasks from a delegation:
```bash
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --context <context_id>
```

### Natural language → task command

| User says | Action |
|-----------|--------|
| "what's the status", "how's it going", "is it done yet", "check on that" | `agentbus tasks --target $TARGET_AGENT <last_task_id>` |
| "cancel it", "stop that", "kill the build", "abort", "nevermind" | `agentbus cancel <last_task_id> --target $TARGET_AGENT` |
| "what's running", "anything in flight", "what's the vm doing" | `agentbus tasks --target $TARGET_AGENT --state working` |
| "show all tasks", "task history", "what did the vm do" | `agentbus tasks --target $TARGET_AGENT` |
| "what failed", "any errors", "what broke" | `agentbus tasks --target $TARGET_AGENT --state failed` |
| "show everything from that pipe session" | `agentbus tasks --target $TARGET_AGENT --context <context_id>` |

**Remembering the last task_id:** After any async delegation, remember the returned `task_id` so follow-up questions ("is it done?", "cancel it") can reference it without the user repeating it.

## Step 6: Interactive Pipe (v0.3.1)

For ongoing conversation with the VM agent (not one-shot delegation):

| User says | Interpretation | Command |
|-----------|---------------|---------|
| "open a channel", "start a pipe", "talk to vm" | Interactive pipe | `cd $AGENTBUS_DIR && agentbus pipe --agent $LOCAL_AGENT --to $TARGET_AGENT --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR` |

The pipe generates a `context_id` — all tasks created during the conversation are linked. Task state events (working → completed) appear inline. After closing, review with `agentbus tasks --context <session-id>`.

## Step 7: A2A Streaming (v0.3.1)

For external/HTTP clients, delegate via A2A gateway with real-time SSE streaming:

| User says | Interpretation |
|-----------|---------------|
| "stream that to the gateway", "watch it via http" | Use A2A SSE endpoint |
| "send via a2a" | Use A2A sync endpoint |

```bash
# SSE streaming — see submitted→working→completed in real-time:
curl -N -X POST http://localhost:8080/message/stream \
  -H 'Content-Type: application/json' \
  -d '{"role":"user","parts":[{"type":"text","text":"<message>"}]}'

# Sync (blocks until complete):
curl -X POST http://localhost:8080/message/send \
  -H 'Content-Type: application/json' \
  -d '{"role":"user","parts":[{"type":"text","text":"<message>"}]}'
```

**Note:** A2A gateway must be running (`agentbus a2a-server --agent $TARGET_AGENT --port 8080`).

## Step 8: Input Required (v0.3.1)

If a delegated task pauses because Claude needs more information:

1. Task transitions to `input_required` — you'll see this in task status or pipe events
2. The question appears in the result: `"status": "input_required", "result": "Which branch should I use?"`
3. Resume with follow-up:
```bash
echo '{"resume_task_id": "<task_id>", "message": "use the main branch"}' | cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT --stdin
```

| User says | Interpretation |
|-----------|---------------|
| "it's asking a question", "answer with X" | Send resume with `resume_task_id` |
| "which task needs input" | `agentbus tasks --target $TARGET_AGENT --state input_required` |

## Step 9: Workflow Delegation (v0.3.1)

For multi-step sequences (build → test → deploy):

Workflows create a parent task with child steps. Each step runs sequentially. If a step fails, the workflow stops.

Currently used programmatically. Natural language mapping:

| User says | Interpretation |
|-----------|---------------|
| "build then test then deploy" | Use auto mode (`--auto`) — simpler than workflow for sequential |
| "run these 3 things in order: X, Y, Z" | Consider workflow if steps are independent commands |

## Session Management

```
/delegate check active sessions       → ~/bin/vm-agent --sessions
/delegate end the current session      → ~/bin/vm-agent --end-session
/delegate health check                 → ~/bin/vm-agent --health
```

## Fallback Chain
1. **AgentBus unreachable** → fall back to SSH (`bash -c "ssh vm '...'"`)
2. **VM unreachable** → run locally
3. **VM agent escalates** → present escalation to user

## Troubleshooting
- **NATS tunnel down**: vm-agent auto-creates. If fails → check VPN, `klist`
- **Listener not running**: `bash -c "ssh vm 'tmux attach -t agentbus'"`
- **Claude -p auth expired**: `! ssh -t vm 'claude auth login'`
- **Health check**: `~/bin/vm-agent --health`
