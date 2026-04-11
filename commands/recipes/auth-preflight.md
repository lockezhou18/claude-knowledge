---
name: auth-preflight
description: Check auth states before starting work
---

Auth checks are now part of the scout hook (runs at session start automatically).

For manual check: `klist && gh auth status && az account show 2>/dev/null`

If something's expired: `! kinit`, `! gh auth login`, `! az login`.
