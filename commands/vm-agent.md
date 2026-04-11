---
name: vm-agent
description: "Delegate tasks to the VM Claude agent via AgentBus. Shell commands, thinking tasks (claude -p with tools), and multi-turn conversations with session resume."
inputs: ["task"]
---

# VM Agent — Delegate to the VM

Send tasks to the persistent Claude agent on the VM (bizhou-ld2). Two modes:
- **Shell**: run commands (build, test, grpc, deploy)
- **Think**: delegate reasoning tasks (review, investigate, analyze) — runs claude -p on VM with full tools

Sessions auto-resume: follow-up messages continue the previous conversation.

## Usage

```
/vm-agent mint build hp-ats-integration-mt          # shell command
/vm-agent -t review the latest PR changes           # thinking task
/vm-agent -t --repo hp-ats-integration-mt explain   # thinking with repo context
/vm-agent --async run full test suite               # fire-and-forget
/vm-agent --sessions                                # list active sessions
```

## Steps

### 1. Parse the Request

Classify the user's request:

| Signal | Mode | Example |
|--------|------|---------|
| `mint build`, `gradlew`, `go-status`, `grpcurli`, `curli` | Shell | "mint build hp-ats-integration-mt" |
| `review`, `investigate`, `analyze`, `explain`, `plan`, `eval` | Think | "review the changes in PR #550" |
| `-t` or `--think` flag | Think | "-t why is the pipeline stuck" |
| `--async` flag | Async | "--async run the full test suite" |
| `--sessions` | Meta | list active sessions |
| `--new` | Force fresh | start new session, ignore previous |

### 2. Execute

**Shell mode:**
```bash
~/bin/vm-agent "<command>"
```

**Think mode:**
```bash
~/bin/vm-agent -t "<message>"
```

**Think with repo context:**
```bash
~/bin/vm-agent -t --repo <repo-name> "<message>"
```

**Async (fire-and-forget):**
```bash
~/bin/vm-agent --async "<message>"
```

**Session management:**
```bash
~/bin/vm-agent --sessions          # list active
~/bin/vm-agent --end-session       # end current
~/bin/vm-agent --new -t "<msg>"    # force new session
```

### 3. Present Result

Show the VM agent's response to the user. If JSON mode was used (`--json`), parse and present structured output.

For thinking tasks, the response includes:
- `result`: the agent's answer
- `session_id`: for manual resume if needed
- `is_resumed`: whether this continued a previous session
- `mode`: "thinking" or "shell-direct"

## Multi-Turn Pattern

The VM agent maintains session state. Use this for investigation workflows:

```
Step 1: /vm-agent -t --repo hp-ats-integration-mt investigate the build failure
Step 2: /vm-agent -t now fix it              ← auto-resumes, has full context
Step 3: /vm-agent -t run the tests           ← still same session
```

Sessions expire after 1 hour idle. Use `--new` to start fresh.

## When This Skill Is Invoked by Other Skills

Other skills should use vm-agent for:

| Calling Skill | Use vm-agent for |
|---------------|-----------------|
| `/implement` | `~/bin/vm-agent "mint build"` after code changes |
| `/investigate` | `~/bin/vm-agent -t "investigate why X is failing"` for VM-side analysis |
| `/ship` | `~/bin/vm-agent "mint build && mint test"` pre-PR validation |
| `/pr-fix` | `~/bin/vm-agent "gradlew compileJava"` after fixing CI |
| `/improve-agent` | `~/bin/vm-agent --async -t "run eval pipeline"` |
| `/dream` | `~/bin/vm-agent --async "python3 ~/agentbus/../scripts/dream.py"` |
| `/oncall` | `~/bin/vm-agent -t "investigate alert: <details>"` |

## On Failure

- **NATS tunnel down**: vm-agent auto-creates tunnel. If still fails → check VPN, Kerberos.
- **Listener not running**: `ssh vm 'tmux attach -t agentbus'` to check. Restart: `ssh vm 'source ~/agentbus/scripts/vm-autostart.sh'`
- **NATS not running**: `ssh vm 'tmux attach -t nats'` to check. Restart: `ssh vm 'tmux send-keys -t nats "nats-server -c ~/agentbus/deployment/nats-bizhou.conf" Enter'`
- **Timeout**: increase with `--timeout 300`. Default is 120s for shell, 300s for thinking.
