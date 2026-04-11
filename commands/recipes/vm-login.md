---
name: vm-login
description: SSH into LinkedIn dev VM
---

One command: `! ssh -t vm 'tmux attach || tmux new'`

If SSH fails: check VPN (`ping vm`), refresh Kerberos (`! kinit`).
