# Send — Mode-Aware Router

## Determine transport mode

| User says | Mode |
|-----------|------|
| "tell vm to X", "ask vm Y" | **NATS Sync** |
| "in the background", "don't wait" | **NATS Async** |
| Known long task (`mint build`, `mint test`) | **NATS Async** |
| "build then test then fix", "keep going" | **NATS Auto** |
| "stream it", "watch live" | **SSE Streaming** |
| "via http", "a2a" | **A2A HTTP** |

## Execute

```bash
# Sync (message/thinking):
cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT -m "<message>" --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR

# Sync (shell command):
cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT -c "<command>" --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR

# Async:
cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT -m "<message>" --async --task-id $TASK_ID --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR

# SSE Streaming (needs A2A gateway):
curl -N -X POST http://localhost:8080/message/stream -H 'Content-Type: application/json' -d '{"role":"user","parts":[{"type":"text","text":"<message>"}]}'

# A2A HTTP Sync:
curl -X POST http://localhost:8080/message/send -H 'Content-Type: application/json' -d '{"role":"user","parts":[{"type":"text","text":"<message>"}]}'
```

## Subscribe-Before-Send (async only)

**CRITICAL:** NATS is fire-and-forget. Start watcher BEFORE sending, or fast tasks lose their results.

```
Step 1 → Bash: TASK_ID=$(python3 -c "import uuid; print(uuid.uuid4())")
Step 2 → Bash(run_in_background=true): cd $AGENTBUS_DIR && python3 -m agentbus.watch_result --task-id $TASK_ID --count 1 --timeout 600 --nats-url "$AGENTBUS_NATS_URL"
Step 3 → Bash: cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT -m "<message>" --async --task-id $TASK_ID --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR
```

Result auto-arrives via `<task-notification>`. Use `Read` on the output file path. No polling needed.

**Safety net:** `cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT <task_id>`

## Present result with stats

```
### Stats
- Duration: Xs, N turns, [thinking/shell] mode
- Session: [session_id] (reusable)
```

| Mode | How result arrives |
|------|-------------------|
| Sync | Blocks, show directly |
| Async | Background watcher catches via `<task-notification>` |
| SSE | Events stream: submitted → working → completed |
| A2A | JSON response |
