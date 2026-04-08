---
name: ui-smoke-test
description: Post-deploy UI smoke test — open target URL, verify key elements, screenshot for evidence
inputs: ["url", "expected_elements"]
chain_to: investigate
chain_when: "expected element missing or page error detected"
project: null
---

## Steps

1. **Check playwright-cli is available:**
   ```bash
   which playwright-cli 2>/dev/null || npm install -g @playwright/cli@latest
   ```

2. **Open browser and navigate:**
   ```bash
   playwright-cli open --headed {{url}}
   ```

3. **Load auth if needed:**
   - If URL is LinkedIn internal → `playwright-cli state-load ~/.playwright-cli/linkedin-auth.json` (if exists)
   - If URL is Greenhouse → `playwright-cli state-load ~/.playwright-cli/greenhouse-auth.json` (if exists)
   - If no saved auth and page shows login → prompt user to login interactively, then save state

4. **Take snapshot and verify expected elements:**
   ```bash
   playwright-cli snapshot
   ```
   - Check snapshot for each item in `{{expected_elements}}`
   - For each element: present (PASS) or missing (FAIL)

5. **Take screenshot for evidence:**
   ```bash
   playwright-cli screenshot
   ```
   - Screenshot saved to `.playwright-cli/` directory

6. **Check browser console for errors:**
   ```bash
   playwright-cli console
   ```
   - Flag any `error` level entries
   - Flag any failed network requests (4xx, 5xx)

7. **Report results:**
   ```
   UI Smoke Test: {{url}}
   ────────────────────────
   Element checks:
     ✓ [element1] — found
     ✗ [element2] — MISSING
   Console errors: [count]
   Screenshot: [path]
   Result: PASS / FAIL
   ```

## Expected Output

All expected elements present, no console errors, screenshot saved.

## On Failure

- Missing expected elements → chain to `/investigate` with snapshot + screenshot as evidence
- Console errors (5xx) → chain to `/investigate` focusing on backend service health
- Auth failure → run `/recipe auth-preflight` or re-login interactively
- If post-deploy → include deploy version and fabric in the investigation context
