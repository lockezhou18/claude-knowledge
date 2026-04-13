# Task Lifecycle, Pipe, A2A, Input Required

## Task Tracking

Tasks are persistent (FileTaskStore) — survive listener restarts.

```bash
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT                    # all
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --state working    # in flight
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --state completed  # done
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --state failed     # errors
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT <task_id>          # specific
cd $AGENTBUS_DIR && agentbus cancel <task_id> --target $TARGET_AGENT         # cancel
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --context <ctx>    # by context
```

| User says | Action |
|-----------|--------|
| "is it done", "status", "check on that" | tasks + last task_id |
| "cancel", "stop", "kill", "abort" | cancel + last task_id |
| "what's running" | tasks --state working |
| "what failed" | tasks --state failed |

Remember the last task_id so follow-ups work without repeating it.

## Interactive Pipe

```bash
cd $AGENTBUS_DIR && agentbus pipe \
  --agent $LOCAL_AGENT --to $TARGET_AGENT \
  --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR
```

- Generates context_id linking all tasks in the conversation
- Task state events appear inline
- After closing: `agentbus tasks --context <session-id>`

## A2A Streaming

```bash
# SSE (real-time):
curl -N -X POST http://localhost:8080/message/stream \
  -H 'Content-Type: application/json' \
  -d '{"role":"user","parts":[{"type":"text","text":"<message>"}]}'

# Sync:
curl -X POST http://localhost:8080/message/send \
  -H 'Content-Type: application/json' \
  -d '{"role":"user","parts":[{"type":"text","text":"<message>"}]}'
```

Gateway must be running: `agentbus a2a-server --agent $TARGET_AGENT --port 8080`

## Input Required

When a task pauses for user input:

```bash
# Find paused:
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --state input_required

# Resume:
echo '{"resume_task_id":"<id>","message":"<answer>"}' | cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT --stdin
```

## Workflow Delegation

| User says | Approach |
|-----------|----------|
| "build then test then deploy" | Use `--auto` (simpler) |
| "run these 3 in order" | Consider workflow for independent commands |
