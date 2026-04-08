---
name: vm-remote
description: Remote execution on VM bizhou-ld2.linkedin.biz. Use when building, testing, running heavy commands, or syncing code to the VM. Provides vm-run (sync+build), vm-sync (sync only), and direct SSH.
allowed-tools: Bash(bash -c "ssh vm*), Bash(bash -c "scp*), Bash(bash -c "rsync*), Bash(bash -c "cd * && vm-run*), Bash(bash -c "vm-run*), Bash(export PATH*vm-run*)
---

# VM Remote Execution — Tier 1.5 Capability

Remote execution hands for VM `bizhou-ld2.linkedin.biz`. Other skills invoke this capability for builds, tests, and remote commands.

## Tools

### vm-run (sync + execute)
Detects current git repo, rsyncs source to VM, runs command remotely. Falls back to local on failure.

```bash
# From any repo path — syncs to vm:~/workspace/<repo-name>
bash -c "cd /path/to/local/repo && vm-run mint build"
bash -c "cd /path/to/local/repo && vm-run mint test"
bash -c "cd /path/to/local/repo && vm-run ./gradlew compileJava"
```

### vm-sync (sync only, no command)
Sync code to VM without running anything. Useful before debugging on VM or when you need to sync multiple repos before a cross-repo build.

```bash
# Sync current repo
bash -c "cd /path/to/local/repo && vm-run echo 'sync complete'"

# Sync specific path
bash -c "rsync -az --delete --exclude='.gradle' --exclude='build' --exclude='out' --exclude='.git' -e ssh /local/repo/ vm:~/workspace/repo-name/"
```

### Direct SSH (non-repo commands)
For commands not tied to a repo — service status, gRPC calls, log checking.

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
vm-run has 3-layer fallback:
1. **VM unreachable** (VPN down, SSH timeout) → runs locally
2. **Rsync fails** → runs locally
3. **Remote build fails** → runs locally

## VM Details
- **Host**: bizhou-ld2.linkedin.biz (alias: `vm`)
- **SSH config**: `~/.ssh/config.custom` (passwordless via LinkedIn key)
- **OS**: CBL-Mariner 2.0 (Linux)
- **Package manager**: tdnf
- **VM repo path**: `~/workspace/<repo-name>`
- **Installed**: Claude CLI, code-server, tmux, mint

## When Other Skills Should Use This

| Skill | Uses vm-remote for |
|-------|-------------------|
| `/implement` | `vm-run mint build`, `vm-run mint test` after code changes |
| `/investigate` | `ssh vm 'grpcurli ...'` for live service queries |
| `/deploy-check` | `ssh vm 'go-status <service>'` |
| `/ship` | `vm-run mint build && vm-run mint test` pre-PR validation |
| `/pr-fix` | `vm-run ./gradlew compileJava` after fixing CI issues |
| `/validate-qprod` | `vm-run mint test` for QProd validation |
| `/oncall` | `ssh vm 'curli ...'`, `ssh vm 'grpcurli ...'` for investigation |
