---
name: Subscribe-before-send for async VM tasks
description: Always use subscribe-before-send pattern for async agentbus tasks, and show stats block when presenting results
type: feedback
originSessionId: 44dcee41-fc7a-4a7f-a079-c1eda98caf47
---
Always use the subscribe-before-send pattern for async agentbus tasks — never fire-and-forget without a watcher.

**Why:** Manual polling caused 2-6 minute drift between task completion and result delivery. Subscribe-before-send eliminates drift entirely (near-zero latency via `<task-notification>`).

**How to apply:**
1. Generate task ID: `python3 -c "import uuid; print(uuid.uuid4())"`
2. Start watcher FIRST: use `Monitor` tool (preferred) or `Bash(run_in_background=true)` as fallback → `agentbus watch_result --task-id $ID`
3. Then send: `agentbus send --async --task-id $ID`
4. Result auto-arrives via Monitor injection or `<task-notification>`
5. Present result with stats block:
   ```
   ### Stats
   - Duration: Xs, N turns, [thinking/shell] mode
   - Session: [session_id] (reusable if you want to continue)
   ```

The stats block gives the user visibility into VM Claude's work — cost, effort, and session reusability.
