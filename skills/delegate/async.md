# Async/Auto — Subscribe-Before-Send

**CRITICAL:** NATS is fire-and-forget. Start watcher BEFORE sending.

## Execution order (3 sequential tool calls):

```
Step 1 → Bash: TASK_ID=$(python3 -c "import uuid; print(uuid.uuid4())")

Step 2 → Bash(run_in_background=true):
  cd $AGENTBUS_DIR && python3 -m agentbus.watch_result --task-id $TASK_ID --count 1 --timeout 600 --nats-url "$AGENTBUS_NATS_URL"

Step 3 → Bash: ~/bin/vm-agent --async "<message>"
```

**For auto mode** (stream checkpoints, longer timeout):
```
Step 2 → count 0, timeout 1800
Step 3 → ~/bin/vm-agent --auto "<message>"
```

**Note:** `vm-agent` does NOT support `--task-id` passthrough. Use `agentbus send -c` directly if you need task ID control:
```bash
cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT -c "<command>" --async --task-id $TASK_ID --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR
```

Result auto-arrives via `<task-notification>`. Read the output file path.

**Safety net:** `cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT <task_id>`

Tell user: "Task delegated. Results will appear here automatically — keep working."

## Present Result with Stats

```
### Stats
- Duration: Xs, N turns, [thinking/shell] mode
- Session: [session_id] (reusable)
```

## Result Handling

- **Sync**: show directly
- **Async**: watcher catches → present when arrives
- **Escalation**: if "ESCALATE:" in result → show to user with suggested action
- **Retry**: auto-retry 2x on transient failures (3s→6s→12s). Override: `max_retries` in payload

| User says | Retry behavior |
|-----------|---------------|
| "retry", "keep trying" | `max_retries: 3` |
| "just try once", "no retries" | `max_retries: 0` |
| "keep retrying until it works" | Use `--auto` mode instead |

## Examples

| User says | Command |
|-----------|---------|
| "run mint build" | `~/bin/vm-agent "mint build"` (but async — known long) |
| "build hp-ats" | `~/bin/vm-agent "cd ~/workspace/connected_project_phase2/hp-ats-integration-mt && mint build"` |
| "run the test suite in the background" | `~/bin/vm-agent --async "mint test"` |
| "build, test, fix, re-test until green" | `~/bin/vm-agent --auto "build, test, fix, re-test"` |
