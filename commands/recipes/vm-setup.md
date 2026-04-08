---
name: vm-setup
description: Bootstrap a new LinkedIn dev VM with Claude Code, code-server, tmux, and knowledge sync
inputs: ["hostname"]
chain_to: investigate
chain_when: "setup step fails"
---

## Prerequisites
- SSH access to {{hostname}} works (`ssh {{hostname}}`)
- Kerberos ticket valid (`klist`)

## Steps

### 1. Install Claude Code CLI
```bash
ssh {{hostname}} 'curl -fsSL https://claude.ai/install.sh | sh'
```

### 2. Install code-server (VS Code in browser)
```bash
ssh {{hostname}} 'curl -fsSL https://code-server.dev/install.sh | sh'
```

### 3. Configure tmux
```bash
ssh {{hostname}} 'cat > ~/.tmux.conf << "TMUX"
set -g mouse on
set -g history-limit 50000
set -g status-right "#H | %Y-%m-%d %H:%M"
set -g default-terminal "screen-256color"
# Name sessions for workstreams
TMUX'
```

### 4. Clone knowledge repo
```bash
ssh {{hostname}} 'git clone git@github.com:bizhou/claude-knowledge.git ~/claude-knowledge'
```

### 5. Run install.sh (symlinks + cron)
```bash
ssh {{hostname}} 'cd ~/claude-knowledge && ./install.sh'
```

### 6. Set up mutagen sync for code repos
```bash
# On LOCAL machine:
mutagen sync create --name=workspace ~/workspace {{hostname}}:~/workspace \
  --ignore-vcs --ignore=".gradle,build,out,node_modules,.idea"
```

### 7. Create persistent Claude tmux session
```bash
ssh {{hostname}} 'tmux new-session -d -s claude "claude"'
```

### 8. Verify
```bash
ssh {{hostname}} 'ls -la ~/.claude/rules ~/.claude/commands ~/.claude/skills ~/.claude/learnings && echo "Knowledge: OK"'
ssh {{hostname}} 'which claude && echo "Claude CLI: OK"'
ssh {{hostname}} 'tmux list-sessions'
```

## Expected Output
- Claude Code CLI installed and working
- code-server running (accessible at {{hostname}}:8080)
- tmux session "claude" running with Claude Code
- Knowledge files symlinked from ~/claude-knowledge
- Hourly cron auto-syncing knowledge to GitHub
- mutagen syncing workspace bidirectionally

## On Failure
- SSH fails → check VPN + Kerberos (`! kinit`)
- git clone fails → check SSH key on VM (`ssh {{hostname}} 'cat ~/.ssh/id_rsa.pub'`)
- Claude install fails → check VM has internet access, try manual install
- mutagen fails → `brew install mutagen-io/mutagen/mutagen` locally first
