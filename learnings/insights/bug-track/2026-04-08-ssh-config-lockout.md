---
id: bug-009
track: bug
type: episodic
repos: ["*"]
tags: ["ssh", "config", "lockout", "vm", "authentication"]
severity: medium
rot_rate: slow
status: active
created: "2026-04-08"
last_verified: "2026-04-08"
use_count: 0
outcome_score: 0
---

# SSH Config Lockout: Adding Hostname Before Key Is Deployed

## Symptoms
`Permission denied (publickey,password,keyboard-interactive)` — can't SSH at all, not even with password.

## Root Cause
Added `bizhou-ld2.linkedin.biz` to `~/.ssh/config.custom` Host line which had `PreferredAuthentications publickey` and `NumberOfPasswordPrompts 0`. The LinkedIn public key wasn't yet in the VM's `authorized_keys`, so publickey auth failed and password fallback was disabled.

## Fix
1. Revert config.custom to remove the full hostname
2. SSH with password using the full hostname (falls back to managed config which allows password)
3. Copy the public key to VM's authorized_keys
4. Re-add hostname to config.custom

## Prevention
When setting up SSH key auth for a new host: always copy the key FIRST (via password auth), THEN add the host to publickey-only config.
