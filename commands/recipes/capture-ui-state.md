---
name: capture-ui-state
description: Screenshot + snapshot before/after a change for PR evidence
inputs: ["url", "label"]
chain_to: null
chain_when: null
project: null
---

## Storage

Captures stored at: `.playwright-cli/captures/{{label}}/`

## Steps

1. **Check playwright-cli is available:**
   ```bash
   which playwright-cli 2>/dev/null || npm install -g @playwright/cli@latest
   ```

2. **Create capture directory:**
   ```bash
   mkdir -p .playwright-cli/captures/{{label}}
   ```

3. **Open browser and navigate:**
   ```bash
   playwright-cli open --headed {{url}}
   ```
   - Load auth state if needed (check for saved auth matching the domain)

4. **Capture BEFORE state:**
   ```bash
   playwright-cli screenshot
   # Move to named location
   cp .playwright-cli/screenshot-*.png .playwright-cli/captures/{{label}}/before.png
   playwright-cli snapshot > .playwright-cli/captures/{{label}}/before-snapshot.yml
   ```

5. **Pause for user to make the change:**
   Tell user:
   > Before state captured. Make your change now (deploy, config update, etc.).
   > When ready, say "continue" to capture the after state.

6. **Capture AFTER state:**
   ```bash
   playwright-cli reload
   playwright-cli screenshot
   cp .playwright-cli/screenshot-*.png .playwright-cli/captures/{{label}}/after.png
   playwright-cli snapshot > .playwright-cli/captures/{{label}}/after-snapshot.yml
   ```

7. **Generate diff summary (snapshot_judge):**
   Compare before and after snapshots using LLM-as-judge:
   - Load both snapshot YAML files
   - Send to LLM with task: "User made a change to the application"
   - Criteria: "Identify all visible differences between before and after states. Classify each as intentional change, improvement, or potential regression."
   - Returns: confidence score + structured list of changes

8. **Report:**
   ```
   UI Capture: {{label}}
   ────────────────────────
   Before: .playwright-cli/captures/{{label}}/before.png
   After:  .playwright-cli/captures/{{label}}/after.png
   
   Changes detected (confidence: 0.92):
     ✓ [intentional] Button text changed from "Save" to "Submit"
     ✓ [improved] Loading spinner added during async operation
     ⚠ [check] Padding reduced on header — verify if intentional
   
   Ready to include in PR description.
   ```

   **Tip:** For multi-step before/after with full replay, use `/recipe ui-session compare`.

## Expected Output

Before/after screenshots and snapshots saved, diff summary generated. Files ready to reference in PR description.

## On Failure

- If page fails to load → check URL and auth state
- If reload doesn't reflect changes → wait longer, or navigate manually
- If no visible changes → verify the change was actually deployed/applied
