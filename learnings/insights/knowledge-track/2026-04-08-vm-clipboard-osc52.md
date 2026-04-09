---
id: know-046
track: knowledge
type: episodic
repos: ["*"]
tags: ["vm", "tmux", "clipboard", "osc52", "iterm2", "ssh", "infrastructure"]
severity: medium
created: "2026-04-08"
last_verified: "2026-04-08"
use_count: 0
outcome_score: 0.0
status: active
rot_rate: permanent
origin_skill: compound
---

## When fixing clipboard on remote VM tmux over SSH

**Check the terminal emulator FIRST.** Apple Terminal.app does not support OSC 52 — no amount of tmux/script fixes will work. iTerm2, Kitty, WezTerm, Alacritty all support it.

**The yank script approach for tmux copy-pipe:**
1. `copy-pipe-and-cancel` runs the script as a subprocess without a controlling terminal
2. Writing to `/dev/tty` FAILS — "No such device or address"
3. Fix: use `tmux list-clients -F '#{client_tty}'` to get the actual terminal device
4. For nested tmux (local tmux → SSH → VM tmux), wrap OSC 52 in DCS passthrough: `\033Ptmux;\033\033]52;c;...\a\033\\`

**tmux 3.2a gotcha:** `set-clipboard on` does NOT auto-emit OSC 52 when buffer changes via copy-mode. You need explicit `copy-pipe-and-cancel` to a yank script.

**Debugging order:** Terminal supports OSC 52? → yank script can write to TTY? → DCS passthrough for nested tmux?
