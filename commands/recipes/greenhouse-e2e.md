---
name: greenhouse-e2e
description: Open Greenhouse sandbox, load auth, navigate to integration, verify state
inputs: ["target_page"]
chain_to: investigate
chain_when: "unexpected UI state or missing data"
project: connected-project-phase2
---

## Auth Storage

Browser auth state: `~/.playwright-cli/greenhouse-auth.json`

## Steps

1. **Check playwright-cli is available:**
   ```bash
   which playwright-cli 2>/dev/null || npm install -g @playwright/cli@latest
   ```

2. **Check for saved Greenhouse auth:**
   ```bash
   ls -la ~/.playwright-cli/greenhouse-auth.json 2>/dev/null
   ```
   - If exists → go to Step 4
   - If missing → go to Step 3

3. **Login to Greenhouse (interactive — user completes SSO):**
   ```bash
   playwright-cli open --headed https://app.greenhouse.io/users/sign_in
   ```
   - Credentials: tiyer+sandbox@linkedin.com (see test-environments.md)
   - Wait for user to complete login
   - Save auth state:
   ```bash
   playwright-cli state-save ~/.playwright-cli/greenhouse-auth.json
   ```

4. **Open browser and load auth:**
   ```bash
   playwright-cli open --headed
   playwright-cli state-load ~/.playwright-cli/greenhouse-auth.json
   ```

5. **Navigate to target page:**
   - If `{{target_page}}` provided: `playwright-cli goto {{target_page}}`
   - If not provided, default to dashboard: `playwright-cli goto https://app.greenhouse.io/dashboard`

6. **Verify auth worked:**
   ```bash
   playwright-cli snapshot
   ```
   - If snapshot shows login page → auth expired, delete saved state and go to Step 3
   - If snapshot shows dashboard/target → success

7. **Navigate to Connected Projects integration (if applicable):**
   - LiHA Dash: HPCP Test Contract - Greenhouse - LiHA enabled (Contract ID: 2011455851)
   - Take snapshot for verification:
   ```bash
   playwright-cli snapshot
   ```

## Expected Output

Browser open on the target Greenhouse page, authenticated, ready for interaction.

## On Failure

- Auth state expired → delete `~/.playwright-cli/greenhouse-auth.json`, re-login (Step 3)
- Page shows unexpected content → chain to `/investigate` with the snapshot as evidence
- Browser fails to open → check `playwright-cli open --headed` manually
