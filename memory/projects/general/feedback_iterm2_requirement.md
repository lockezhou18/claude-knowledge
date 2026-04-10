---
name: iTerm2 required for VM clipboard
description: User uses iTerm2 (not Terminal.app) — required for OSC 52 clipboard over SSH to VM
type: feedback
originSessionId: ff5580ff-db76-4d24-a0b7-f89a26dbc58e
---
Use iTerm2 as the terminal, not Apple Terminal.app. Terminal.app does not support OSC 52, which is required for clipboard copy/paste to work over SSH to the VM tmux sessions.

**Why:** OSC 52 escape sequences are the mechanism that sends clipboard data from VM tmux back to the local machine. Terminal.app silently drops them.

**How to apply:** When troubleshooting clipboard issues with the VM, first check the terminal emulator. If the user is in Terminal.app, suggest switching to iTerm2.
