---
name: vm-login
description: SSH into a LinkedIn dev VM using interactive tmux session
inputs: ["hostname"]
chain_to: investigate
chain_when: "connection refused or timeout"
---

## Steps
1. Launch a tmux session for interactive SSH: use `linkedin-cli-tools:interactive-cli` or suggest `! ssh {{hostname}}`
2. If SSH requires password/2FA, prompt the user to enter credentials in the tmux popup via `linkedin-cli-tools:launch-tmux`
3. Confirm connection by checking for a shell prompt

## Expected Output
Active SSH session to {{hostname}} with a working shell.

## On Failure
- **Connection refused / timeout**: Check VPN is connected, host is reachable (`ping {{hostname}}`). Chain to `/investigate` if persistent.
- **Auth failure**: Run `! kinit` to refresh Kerberos ticket, then retry.
- **Host not found**: Verify hostname spelling. LinkedIn VMs follow pattern `<user>-ld<N>.linkedin.biz`.
