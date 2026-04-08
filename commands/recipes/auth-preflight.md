---
name: auth-preflight
description: Check all common auth states and report what needs refreshing before starting work
inputs: []
chain_to: null
chain_when: null
project: null
---

## Steps

1. **Check Kerberos/SSH auth:**
   ```
   klist 2>&1 || echo "NO_KERBEROS"
   ```
   - If expired or missing: suggest `! kinit`

2. **Check GitHub CLI auth:**
   ```
   gh auth status 2>&1
   ```
   - If not authenticated: suggest `! gh auth login`

3. **Check Azure CLI auth (for KQL/logs):**
   ```
   az account show 2>&1 || echo "NO_AZURE"
   ```
   - If expired or missing: suggest `! az login`

4. **Check SSH connectivity to prod shell (prod-shell07):**
   ```
   ssh -o ConnectTimeout=5 -o BatchMode=yes prod-shell07 echo ok 2>&1 || echo "SSH_FAILED"
   ```
   - If failed: suggest `! kinit` first, then retry

5. **Check browser auth states (for playwright-cli):**
   ```bash
   ls -la ~/.playwright-cli/greenhouse-auth.json 2>/dev/null && echo "GREENHOUSE_AUTH: saved" || echo "GREENHOUSE_AUTH: MISSING"
   ls -la ~/.playwright-cli/linkedin-auth.json 2>/dev/null && echo "LINKEDIN_AUTH: saved" || echo "LINKEDIN_AUTH: MISSING"
   ```
   - If missing and needed: suggest `/recipe greenhouse-e2e` or interactive login + `playwright-cli state-save`

6. **Check gRPC cert validity (for grpcurli):**
   ```
   ls -la ~/.ssh/*.pem 2>/dev/null && openssl x509 -enddate -noout -in ~/.ssh/*.pem 2>/dev/null || echo "NO_CERTS"
   ```
   - If expired: suggest cert renewal steps

6. **Report summary:**
   - List each auth context as VALID / EXPIRED / MISSING
   - For anything not valid, provide the exact `!` command to fix it
   - Only suggest tmux if a flow requires interactive multi-step input (e.g., 2FA)

## Expected Output

```
Auth Preflight Report:
  Kerberos:  VALID (expires in 8h)
  GitHub:    VALID
  Azure:     EXPIRED → run: ! az login
  SSH:       VALID
  Browser (Greenhouse): SAVED → run /recipe greenhouse-e2e to verify
  Browser (LinkedIn):   MISSING → login interactively when needed
  gRPC cert: VALID (expires in 29d)
```

## On Failure
If multiple auth contexts are broken and `!` commands aren't working, fall back to tmux for interactive troubleshooting. Chain to /investigate if auth failures seem systemic (e.g., VPN issue, credential store corruption).
