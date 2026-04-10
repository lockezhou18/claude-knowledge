---
name: vm-remote
description: Remote execution on VM bizhou-ld2.linkedin.biz. Shell commands via SSH/vm-run, thinking tasks via agentbus (claude -p on VM). Use when building, testing, running heavy commands, or delegating work to the VM agent.
allowed-tools: Bash(bash -c "ssh vm*), Bash(bash -c "scp*), Bash(bash -c "rsync*), Bash(bash -c "cd * && vm-run*), Bash(bash -c "vm-run*), Bash(export PATH*vm-run*), Bash(~/bin/vm-agent*)
---

# VM Remote Execution — Tier 1.5 Capability

Remote execution hands for VM `bizhou-ld2.linkedin.biz`. Two transport modes:
- **SSH/vm-run**: sync code + run shell commands (builds, tests, deploys)
- **AgentBus**: delegate thinking tasks to a Claude agent on VM (review, investigate, analyze)

## Transport Selection

| Task | Transport | Command |
|------|-----------|---------|
| Build/compile | SSH (vm-run) | `bash -c "cd /repo && vm-run mint build"` |
| Run tests | SSH (vm-run) | `bash -c "cd /repo && vm-run mint test"` |
| gRPC/REST calls | SSH (direct) | `bash -c "ssh vm 'grpcurli ...'"` |
| Service status | SSH (direct) | `bash -c "ssh vm 'go-status ...'"` |
| **Code review** | **AgentBus** | `~/bin/vm-agent -t "review the changes in ..."` |
| **Investigation** | **AgentBus** | `~/bin/vm-agent -t "investigate why ..."` |
| **Analysis** | **AgentBus** | `~/bin/vm-agent -t "analyze the test failures"` |
| **Any thinking** | **AgentBus** | `~/bin/vm-agent -t "..."` |
| Fire-and-forget | AgentBus | `~/bin/vm-agent --async "run full test suite"` |

**Rule:** Shell commands → SSH. Thinking tasks → AgentBus. If unsure, use AgentBus (it handles both).

## AgentBus (NEW — Claude agent on VM)

A persistent Claude Code listener on the VM receives tasks via NATS messaging.

### Quick usage
```bash
# Shell command on VM
~/bin/vm-agent "mint build hp-ats-integration-mt"

# Thinking task (claude -p on VM with full tools)
~/bin/vm-agent -t "Review the latest changes in hp-ats-integration-mt and summarize"

# Fire-and-forget (async)
~/bin/vm-agent --async "Run full test suite for hp-ats-integration-mt"

# JSON output (for programmatic use)
~/bin/vm-agent --json "go-status hp-ats-integration-mt"
```

### How it works
```
Laptop → NATS (SSH tunnel :4222) → VM claude_listener → claude -p / bash → result back
```

- NATS server runs on VM (tmux: nats)
- Claude listener runs on VM (tmux: agentbus)
- SSH config auto-forwards port 4222
- vm-agent creates tunnel if not present

### When to use AgentBus vs SSH

**Use AgentBus when:**
- The task requires Claude to THINK (review, investigate, analyze, explain)
- You want the VM's Claude to use its own tools (Read, Grep, Bash)
- The task is long-running and you want async results
- You need structured JSON output

**Use SSH/vm-run when:**
- Simple shell command (mint build, gradlew, go-status)
- You need code synced before running (vm-run handles this)
- The PreToolUse hook auto-intercepts (mint/gradlew)

## SSH/vm-run (existing)

### vm-run (sync + execute)
Detects current git repo, rsyncs source to VM, runs command remotely. Falls back to local on failure.

```bash
# From any repo path — syncs to vm:~/workspace/<repo-name>
bash -c "cd /path/to/local/repo && vm-run mint build"
bash -c "cd /path/to/local/repo && vm-run mint test"
bash -c "cd /path/to/local/repo && vm-run ./gradlew compileJava"
```

### Direct SSH (non-repo commands)
```bash
bash -c "ssh vm 'go-status hp-ats-integration-mt'"
bash -c "ssh vm 'grpcurli ...'"
bash -c "ssh vm 'ls ~/workspace/'"
```

### File Transfer
```bash
bash -c "scp vm:~/workspace/repo/file.txt /tmp/"
bash -c "scp /tmp/file.txt vm:~/workspace/repo/"
```

## CRITICAL: Always use `bash -c` wrapper
Direct `ssh` commands are blocked by Claude Code permissions. Always wrap in `bash -c "..."`.

## Automatic Routing
The PreToolUse hook `vm-route-builds.py` auto-intercepts:
- `mint build`, `mint test`, `mint precommit`, `mint snapshot`, `mint run-local`
- `./gradlew <anything>`

When intercepted, the hook blocks the local command and instructs Claude to use `vm-run` instead.

## Fallback Chain
1. **AgentBus unreachable** (NATS down, tunnel dead) → fall back to SSH
2. **VM unreachable** (VPN down, SSH timeout) → run locally
3. **Remote build fails** → run locally

## VM Details
- **Host**: bizhou-ld2.linkedin.biz (alias: `vm`)
- **SSH config**: `~/.ssh/config.custom` (passwordless via LinkedIn key, port 4222 forwarded)
- **OS**: CBL-Mariner 2.0 (Linux x86_64)
- **VM repo path**: `~/workspace/<repo-name>`
- **Installed**: Claude CLI v2.1.101, code-server, tmux, mint, nats-server v2.12.6
- **AgentBus**: ~/agentbus (claude_listener, agents, NATS config)

## When Other Skills Should Use This

| Skill | Uses vm-remote for |
|-------|-------------------|
| `/implement` | `vm-run mint build`, `vm-run mint test` after code changes |
| `/investigate` | `vm-agent -t "investigate ..."` OR `ssh vm 'grpcurli ...'` |
| `/deploy-check` | `ssh vm 'go-status <service>'` |
| `/ship` | `vm-run mint build && vm-run mint test` pre-PR validation |
| `/pr-fix` | `vm-run ./gradlew compileJava` after fixing CI issues |
| `/improve-agent` | `vm-agent -t "run eval pipeline on sessions"` |
| `/oncall` | `ssh vm 'curli ...'`, `vm-agent -t "investigate alert"` |
| `/dream` | `vm-agent --async "run dream.py consolidation"` |
