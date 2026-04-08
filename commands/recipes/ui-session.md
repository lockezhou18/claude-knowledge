---
name: ui-session
description: Record, replay, and compare browser test sessions — deterministic UI testing with vision-based fallback
inputs: ["action", "url_or_session_id"]
chain_to: investigate
chain_when: "replay diverges from recorded session or comparison finds regression"
---

## Usage

```
/recipe ui-session record <url> [label]    # Record a new session
/recipe ui-session replay <session_id>     # Replay a recorded session
/recipe ui-session compare <before> <after> # Compare two sessions side-by-side
/recipe ui-session list                     # List all saved sessions
```

## Storage

```
~/.playwright-cli/sessions/
  {session_id}/
    manifest.json         # Session metadata (url, label, timestamp, steps)
    steps/
      01-snapshot.yml     # Playwright snapshot before action
      01-screenshot.png   # Screenshot before action
      01-action.json      # Action taken (click ref, fill value, goto url, etc.)
      02-snapshot.yml     # Snapshot after action / before next
      02-screenshot.png
      02-action.json
      ...
    auth-state.json       # Auth state at session start (if saved)
```

## Steps: record

Record a browser session by capturing every interaction + state.

1. **Open browser:**
   ```bash
   playwright-cli open --headed --persistent
   ```

2. **Load auth if available** for the target domain:
   - Check `~/.playwright-cli/*-auth.json` files for domain match
   - If found: `playwright-cli state-load <auth-file>`

3. **Navigate to starting URL:**
   ```bash
   playwright-cli goto {{url_or_session_id}}
   ```

4. **Create session directory:**
   ```bash
   session_id=$(date +%s | shasum | head -c 8)
   mkdir -p ~/.playwright-cli/sessions/${session_id}/steps
   ```

5. **Capture initial state:**
   ```bash
   playwright-cli snapshot > ~/.playwright-cli/sessions/${session_id}/steps/01-snapshot.yml
   playwright-cli screenshot  # save as 01-screenshot.png
   ```

6. **Interactive recording loop:**
   Tell user: "Session recording started. Perform your test actions using playwright-cli commands (click, fill, type, goto, etc.). Say 'done' when finished."

   For each action the user performs:
   a. **Log the action** to `{step}-action.json`:
      ```json
      {
        "step": 2,
        "command": "click",
        "args": {"ref": "e15"},
        "element_text": "Submit",
        "element_type": "button",
        "timestamp": "ISO"
      }
      ```
   b. **Capture post-action state:**
      ```bash
      playwright-cli snapshot > steps/{next_step}-snapshot.yml
      playwright-cli screenshot  # save as {next_step}-screenshot.png
      ```
   c. **Run bug detector** on the new state:
      - Check for error banners, oops pages, console errors
      - Flag any issues but continue recording

7. **Save manifest:**
   ```json
   {
     "session_id": "abc12345",
     "url": "https://app.greenhouse.io/dashboard",
     "label": "greenhouse-candidate-sync",
     "recorded_at": "2026-04-07T17:00:00Z",
     "steps": 8,
     "duration_seconds": 45,
     "auth_domain": "greenhouse.io",
     "tags": ["greenhouse", "e2e", "connected-projects"]
   }
   ```

8. **Save auth state** (for replay):
   ```bash
   playwright-cli state-save ~/.playwright-cli/sessions/${session_id}/auth-state.json
   ```

9. **Report:**
   ```
   Session recorded: ${session_id}
   URL: {{url}}
   Steps: N actions captured
   Saved to: ~/.playwright-cli/sessions/${session_id}/
   
   Replay with: /recipe ui-session replay ${session_id}
   ```

## Steps: replay

Replay a recorded session deterministically, with vision-based fallback when UI diverges.

1. **Load session manifest:**
   ```bash
   cat ~/.playwright-cli/sessions/{{url_or_session_id}}/manifest.json
   ```

2. **Open browser and load auth:**
   ```bash
   playwright-cli open --headed --persistent
   playwright-cli state-load ~/.playwright-cli/sessions/{{url_or_session_id}}/auth-state.json
   ```

3. **Navigate to starting URL** from manifest

4. **For each recorded step:**
   a. **Capture current snapshot**
   b. **Compare with recorded snapshot** (structural diff):
      - Match element refs by text content, type, and position
      - If >80% elements match → **deterministic replay**: execute the recorded action
      - If <80% match → **vision fallback**: use LLM to find the equivalent element in the current UI and adapt the action
   c. **Execute the action** (click, fill, type, goto)
   d. **Capture post-action state**
   e. **Evaluate with snapshot_judge:**
      - Compare current post-action snapshot vs recorded post-action snapshot
      - Task: the action description from the recorded step
      - If FAIL with confidence <0.5 → mark step as DIVERGED, continue
   f. **Run bug detector** on current state

5. **Compile replay report:**
   ```
   Session Replay: {{session_id}}
   ===============================
   
   Step | Action         | Replay Mode   | Result
   -----|----------------|---------------|--------
   1    | goto dashboard | deterministic | PASS
   2    | click "Jobs"   | deterministic | PASS
   3    | click "Edit"   | vision (UI changed) | PASS (adapted)
   4    | fill "Title"   | deterministic | PASS
   5    | click "Save"   | vision (new button position) | FAIL (element not found)
   
   Summary: 4/5 steps passed | 2 vision fallbacks | 1 failure
   OVERALL: PARTIAL
   ```

6. **Save replay results** to `~/.playwright-cli/sessions/{{url_or_session_id}}/replays/`

## Steps: compare

Compare two sessions (typically before/after a code change) and produce a PR-ready report.

1. **Load both session manifests**

2. **Match steps across sessions** by action type + target element text:
   - Identical action on same element → matched pair
   - Action on renamed/moved element → fuzzy match (by intent)
   - Extra/missing steps → flagged as additions/removals

3. **For each matched step pair:**
   a. Load before screenshot + after screenshot
   b. Load before snapshot + after snapshot
   c. Run `snapshot_judge` comparing the two:
      - Task: the action description
      - Criteria: "Are these UI states functionally equivalent, or does the 'after' version show a regression?"
   d. Classify: SAME / IMPROVED / REGRESSED / CHANGED (intentional)

4. **Generate comparison report** (markdown, PR-ready):
   ```markdown
   ## UI Session Comparison
   
   | Step | Action | Before | After | Verdict |
   |------|--------|--------|-------|---------|
   | 1 | Navigate to dashboard | ![before](before/01.png) | ![after](after/01.png) | SAME |
   | 2 | Click "Candidates" | ![before](before/02.png) | ![after](after/02.png) | CHANGED |
   | 3 | Verify sync status | ![before](before/03.png) | ![after](after/03.png) | IMPROVED |
   
   ### Summary
   - 2 steps unchanged
   - 1 step improved (sync status now shows timestamp)
   - 0 regressions detected
   ```

5. **Save report** to `.playwright-cli/comparisons/{before}-vs-{after}.md`

## Steps: list

1. **Scan** `~/.playwright-cli/sessions/*/manifest.json`
2. **Display:**
   ```
   Saved Sessions
   ==============
   ID        Label                    URL                           Steps  Date
   abc12345  greenhouse-candidate     app.greenhouse.io/dashboard   8      2026-04-07
   def67890  pipeline-profile-list    linkedin.com/hiring/...       5      2026-04-06
   ghi11223  smoke-test-after-deploy  hp-ats-integration-mt/...     3      2026-04-05
   ```

## Expected Output

- `record`: Session saved with all steps, screenshots, snapshots, and actions
- `replay`: Deterministic replay with vision fallback, step-by-step report
- `compare`: PR-ready markdown with side-by-side screenshots and regression verdicts
- `list`: Table of all saved sessions

## On Failure

- Auth expired during replay → prompt user to re-login, save new auth, retry
- Element not found (vision fallback also fails) → mark step FAILED, capture screenshot, continue
- Page crash / oops detected → create bug report with full context, chain to `/investigate`
- >50% steps fail → "Session is stale. Re-record with `/recipe ui-session record`"
