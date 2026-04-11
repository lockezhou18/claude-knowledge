---
name: delegate
description: "Delegate tasks to the VM agent or other agents. Shell commands, thinking tasks (claude -p with tools), multi-turn sessions with auto-resume. Async with real-time Monitor notifications."
allowed-tools: Bash(bash -c "ssh vm*), Bash(bash -c "scp*), Bash(bash -c "rsync*), Bash(bash -c "cd * && vm-run*), Bash(bash -c "vm-run*), Bash(export PATH*vm-run*), Bash(~/bin/vm-agent*), Monitor
inputs: ["task"]
---

# Delegate — Send Work to Another Agent

Delegate tasks to the VM agent (or future agents). Three execution modes:
- **Sync**: block until result (default)
- **Async**: fire task, Monitor watches for result, Claude interjects when done
- **Auto**: multi-round autonomous loop with real-time progress via Monitor

## Usage

```
/delegate mint build hp-ats-integration-mt            # sync shell command
/delegate -t review the latest PR changes             # sync thinking task
/delegate --async run full test suite                  # async with Monitor
/delegate --auto build, test, fix failures, re-test   # autonomous loop with Monitor
/delegate --sessions                                  # list active sessions
```

## Steps

### 1. Classify the Request

| Signal | Mode | Transport |
|--------|------|-----------|
| `mint build`, `gradlew`, `go-status`, `grpcurli` | Shell (sync) | SSH/vm-run |
| `review`, `investigate`, `analyze`, `explain` | Think (sync) | AgentBus |
| `--async` flag | Async + Monitor | AgentBus |
| `--auto` flag | Auto loop + Monitor | AgentBus |
| `--sessions`, `--end-session` | Meta | AgentBus |

### 2. Execute — Sync Mode (default)

**Shell (SSH/vm-run):**
```bash
bash -c "cd /path/to/local/repo && vm-run mint build"
```

**Think (AgentBus):**
```bash
~/bin/vm-agent -t "<message>"
```

**Think with repo context:**
```bash
~/bin/vm-agent -t --repo <repo-name> "<message>"
```

### 3. Execute — Async Mode (--async)

Two steps: fire the task, then start Monitor to watch for the result.

**Step A: Fire the task**
```bash
~/bin/vm-agent --async "<message>"
```
This returns a task_id (from the ACK response).

**Step B: Start Monitor to watch for result**
Use the Monitor tool to run the NATS watcher script:
```
Monitor: python3 -m agentbus.watch_result --task-id <task_id> --timeout 600
```
Working directory must be: `~/projects/compound-learning-ecosystem/agentbus`

The Monitor streams results back in real-time. When the VM agent finishes,
Claude sees the output line and can inform the user immediately — no polling,
no file drops, no waiting for the next prompt.

### 4. Execute — Auto Mode (--auto)

For multi-round tasks (build → test → fix → re-test):

**Step A: Fire with auto flag**
```bash
~/bin/vm-agent --auto "<message>"
```

**Step B: Monitor watches for checkpoints**
```
Monitor: python3 -m agentbus.watch_result --task-id <task_id> --count 0 --timeout 1800
```
Count=0 means unlimited — Monitor stays alive and reports each checkpoint:
```
[step 1/5] [success] build succeeded
[step 2/5] [success] 3 tests failed, fixing...
[step 3/5] [success] re-running tests
[step 4/5] [success] all tests pass
```

### 5. Multi-Turn Conversations

AgentBus sessions auto-resume. Follow-ups continue the previous conversation:

```
/delegate -t --repo hp-ats-integration-mt investigate the build failure
/delegate -t now fix it              ← auto-resumes, has full context
/delegate -t run the tests           ← still same session
```

Sessions expire after 1 hour idle. Use `--new` to start fresh.

### 6. Session Management

```bash
~/bin/vm-agent --sessions          # list active sessions
~/bin/vm-agent --end-session       # end current session
~/bin/vm-agent --new -t "<msg>"    # force new session
~/bin/vm-agent --results           # show completed async results
```

## When Other Skills Invoke This

| Calling Skill | How |
|---------------|-----|
| `/implement` | `vm-run mint build` (sync shell) |
| `/investigate` | `vm-agent -t "investigate ..."` (sync think) or `ssh vm 'grpcurli ...'` |
| `/deploy-check` | `ssh vm 'go-status ...'` (sync shell) |
| `/ship` | `vm-run mint build && vm-run mint test` (sync shell) |
| `/pr-fix` | `vm-run ./gradlew compileJava` (sync shell) |
| `/improve-agent` | `vm-agent --async -t "run eval pipeline"` + Monitor (async think) |
| `/oncall` | `vm-agent -t "investigate alert"` (sync think) |
| `/dream` | `vm-agent --auto "run dream.py"` + Monitor (auto) |

## Transport Details

### SSH/vm-run (sync shell)
- `vm-run` detects current repo, rsyncs to VM, runs command remotely
- Falls back to local if VM unreachable
- PreToolUse hook auto-intercepts `mint build`, `gradlew`
- Always use `bash -c "..."` wrapper

### AgentBus (sync/async/auto thinking)
- NATS-backed messaging (SSH tunnel port 4222)
- Persistent Claude listener on VM (tmux: agentbus)
- Sessions auto-resume per sender + repo
- `~/bin/vm-agent` CLI handles tunnel, routing, session mgmt
- Results via Monitor tool (real-time NATS subscription)

### Monitor Integration (async/auto only)
- `agentbus/watch_result.py` subscribes to NATS result subjects
- Monitor tool runs it in background, streams output to Claude
- No file drops, no polling, no scout hooks — native real-time
- For async: `--count 1` (stop after one result)
- For auto: `--count 0` (stream all checkpoints)

## Fallback Chain
1. **AgentBus unreachable** (NATS/tunnel down) → fall back to SSH
2. **VM unreachable** (VPN/SSH down) → run locally
3. **Remote command fails** → run locally

## Troubleshooting
- **NATS tunnel down**: vm-agent auto-creates. If fails → check VPN, `klist`
- **Listener not running**: `bash -c "ssh vm 'tmux attach -t agentbus'"`
- **NATS not running**: `bash -c "ssh vm 'tmux attach -t nats'"`
- **Monitor timeout**: increase `--timeout` in watch_result.py call
