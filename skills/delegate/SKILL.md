---
name: delegate
description: "Delegate tasks to the VM agent or other agents. Shell commands, thinking tasks (claude -p with tools), multi-turn sessions with auto-resume. Via AgentBus + SSH."
allowed-tools: Bash(bash -c "ssh vm*), Bash(bash -c "scp*), Bash(bash -c "rsync*), Bash(bash -c "cd * && vm-run*), Bash(bash -c "vm-run*), Bash(export PATH*vm-run*), Bash(~/bin/vm-agent*)
inputs: ["task"]
---

# Delegate — Send Work to Another Agent

Remote execution for VM `bizhou-ld2.linkedin.biz`. Two transports:
- **SSH/vm-run**: sync code + run shell commands (builds, tests, deploys)
- **AgentBus**: delegate thinking tasks to a Claude agent on VM (review, investigate, analyze)

## User-Invocable Usage

```
/vm-remote mint build hp-ats-integration-mt           # shell command
/vm-remote -t review the latest PR changes            # thinking task (claude -p on VM)
/vm-remote -t --repo hp-ats-integration-mt explain    # thinking with repo context
/vm-remote --async run full test suite                # fire-and-forget
/vm-remote --sessions                                 # list active sessions
/vm-remote --new -t start fresh investigation         # force new session
```

## Steps (when invoked as /vm-remote)

### 1. Classify the Request

| Signal | Mode | Transport |
|--------|------|-----------|
| `mint build`, `gradlew`, `go-status`, `grpcurli`, `curli` | Shell | SSH/vm-run |
| `review`, `investigate`, `analyze`, `explain`, `plan`, `eval` | Think | AgentBus |
| `-t` or `--think` flag | Think | AgentBus |
| `--async` flag | Async | AgentBus |
| `--sessions`, `--end-session` | Meta | AgentBus |

**Rule:** Shell commands → SSH. Thinking tasks → AgentBus. If unsure, use AgentBus.

### 2. Execute

**Shell (SSH/vm-run):**
```bash
bash -c "cd /path/to/local/repo && vm-run mint build"
```

**Think (AgentBus):**
```bash
~/bin/vm-agent -t "<message>"
```

**Think with repo:**
```bash
~/bin/vm-agent -t --repo <repo-name> "<message>"
```

**Async:**
```bash
~/bin/vm-agent --async "<message>"
```

**Session management:**
```bash
~/bin/vm-agent --sessions
~/bin/vm-agent --end-session
~/bin/vm-agent --new -t "<msg>"
```

### 3. Multi-Turn Pattern

AgentBus sessions auto-resume. Follow-ups continue the previous conversation:

```
/vm-remote -t --repo hp-ats-integration-mt investigate the build failure
/vm-remote -t now fix it              ← auto-resumes, has full context
/vm-remote -t run the tests           ← still same session
```

Sessions expire after 1 hour idle. Use `--new` to start fresh.

## When Other Skills Invoke This

Other skills call vm-remote programmatically (Tier 1.5 capability):

| Calling Skill | Shell (SSH) | Think (AgentBus) |
|---------------|-------------|-------------------|
| `/implement` | `vm-run mint build`, `vm-run mint test` | — |
| `/investigate` | `ssh vm 'grpcurli ...'` | `vm-agent -t "investigate ..."` |
| `/deploy-check` | `ssh vm 'go-status ...'` | — |
| `/ship` | `vm-run mint build && vm-run mint test` | — |
| `/pr-fix` | `vm-run ./gradlew compileJava` | — |
| `/improve-agent` | — | `vm-agent --async -t "run eval pipeline"` |
| `/oncall` | `ssh vm 'curli ...'` | `vm-agent -t "investigate alert"` |
| `/dream` | — | `vm-agent --async "run dream.py"` |

## Transport Details

### SSH/vm-run
- `vm-run` detects current repo, rsyncs to VM, runs command remotely
- Falls back to local if VM unreachable
- PreToolUse hook auto-intercepts `mint build`, `gradlew`
- Always use `bash -c "..."` wrapper (direct ssh blocked by Claude Code)

```bash
bash -c "cd /path/to/repo && vm-run mint build"
bash -c "ssh vm 'go-status hp-ats-integration-mt'"
bash -c "scp vm:~/workspace/repo/file.txt /tmp/"
```

### AgentBus
- NATS-backed messaging (SSH tunnel on port 4222)
- Persistent Claude listener on VM (tmux: agentbus)
- Sessions auto-resume per sender + repo
- `~/bin/vm-agent` CLI wrapper handles tunnel, routing, session mgmt

```bash
~/bin/vm-agent "echo hello"                          # shell on VM
~/bin/vm-agent -t "review this code"                 # thinking on VM
~/bin/vm-agent -t --repo hp-ats-integration-mt "why" # with repo context
~/bin/vm-agent --async "long task"                   # fire-and-forget
~/bin/vm-agent --json "get structured output"        # JSON response
```

## Fallback Chain
1. **AgentBus unreachable** (NATS/tunnel down) → fall back to SSH
2. **VM unreachable** (VPN/SSH down) → run locally
3. **Remote command fails** → run locally

## Troubleshooting
- **NATS tunnel down**: vm-agent auto-creates. If fails → check VPN, `klist`
- **Listener not running**: `bash -c "ssh vm 'tmux attach -t agentbus'"`
- **NATS not running**: `bash -c "ssh vm 'tmux attach -t nats'"`
- **Timeout**: `--timeout 300` (default: 120s shell, 300s thinking)

## VM Details
- **Host**: bizhou-ld2.linkedin.biz (alias: `vm`)
- **SSH config**: `~/.ssh/config.custom` (ports 8080, 4222 forwarded)
- **OS**: CBL-Mariner 2.0 (Linux x86_64)
- **Installed**: Claude v2.1.101, code-server, tmux, mint, nats-server v2.12.6
- **AgentBus**: ~/agentbus (claude_listener, agents/, NATS config)
