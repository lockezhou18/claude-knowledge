---
id: know-047
track: knowledge
type: semantic
repos: [*]
tags: [vm, setup, infrastructure, claude-code, parity, checklist]
severity: high
created: "2026-04-08"
last_verified: "2026-04-08"
use_count: 10
outcome_score: 0.0
status: active
rot_rate: slow
origin_skill: compound
---

## VM parity checklist — what to sync when setting up Claude on a remote VM

When bootstrapping a VM for Claude Code development, these gaps exist between a mature local setup and a fresh VM:

1. **git config** — no .gitconfig on VM. Create with user.name, email, LFS filters, credential helper.
2. **Claude hooks** — copy from local `~/.claude/hooks/`. Skip `vm-route-builds.py` (not needed on VM — builds run natively). Adapt all paths from `/Users/` to `/home/`.
3. **Claude settings.json** — needs hooks config, core permissions, plugins, marketplace config. All paths must use VM home directory.
4. **tmux clipboard** — local uses `pbcopy`, VM needs OSC 52 yank script. Requires iTerm2 (not Terminal.app).
5. **SSH config** — add `LocalForward 8080 localhost:8080` for code-server auto-tunnel.
6. **gh auth** — interactive login required (`ssh -t vm 'gh auth login'`).
7. **Knowledge symlinks** — claude-knowledge repo cloned, `install.sh` run to symlink commands/skills/rules/learnings.

**What NOT to copy:** `vm-route-builds.py` hook, SSH/SCP-related permissions (not needed on VM), `settings.local.json` (accumulates via auto-allowlist on VM independently).
