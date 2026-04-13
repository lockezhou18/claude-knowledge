# Pipe, A2A, Trust, Input Required, Webhooks, Agent Cards

## Pipe (Bidirectional Channel)

```bash
cd $AGENTBUS_DIR && agentbus pipe \
  --agent $LOCAL_AGENT --to $TARGET_AGENT \
  --nats-url "$AGENTBUS_NATS_URL" --agents-dir $AGENTS_DIR
```

- Bidirectional: both sides send/receive simultaneously
- context_id: auto-generated, links all tasks during the pipe
- Task events appear inline (working → completed)
- Shell commands auto-detected; questions route as thinking

After closing: `agentbus tasks --target $TARGET_AGENT --context <session-id>`

## A2A Gateway

```bash
# Check status:
lsof -i :8080 2>/dev/null | grep -c LISTEN && echo "OK" || echo "NOT RUNNING"
curl -s http://localhost:8080/.well-known/agent-card 2>/dev/null | python3 -m json.tool

# SSE Streaming:
curl -N -X POST http://localhost:8080/message/stream \
  -H 'Content-Type: application/json' \
  -d '{"role":"user","parts":[{"type":"text","text":"<message>"}]}'

# Sync:
curl -X POST http://localhost:8080/message/send \
  -H 'Content-Type: application/json' \
  -d '{"role":"user","parts":[{"type":"text","text":"<message>"}]}'

# Start gateway:
cd $AGENTBUS_DIR && agentbus a2a-server --agent $TARGET_AGENT --port 8080
```

## Trust (TOFU)

Approve untrusted agent (when Guardian rejects with "Agent 'X' not trusted"):

```bash
cd $AGENTBUS_DIR && agentbus trust <agent_name> --target $TARGET_AGENT
```

One-time — persistent across restarts.

## Input Required

When a task pauses for user input:

```bash
# Find paused tasks:
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT --state input_required

# Resume:
echo '{"resume_task_id":"<id>","message":"<answer>"}' | cd $AGENTBUS_DIR && agentbus send --to $TARGET_AGENT --stdin
```

## Webhooks

```bash
# Register:
curl -X POST http://localhost:8080/tasks/<id>/pushNotificationConfigs \
  -H 'Content-Type: application/json' -d '{"url":"<callback-url>"}'

# List:
curl http://localhost:8080/tasks/<id>/pushNotificationConfigs

# Remove:
curl -X DELETE http://localhost:8080/tasks/<id>/pushNotificationConfigs
```

## Agent Card Setup

Personal cards go in `agents/local/` (gitignored):
```bash
cp $AGENTBUS_DIR/agents/examples/$TARGET_AGENT.json $AGENTBUS_DIR/agents/local/my-vm.json
```
