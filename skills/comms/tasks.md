# Tasks, Results, Inbox, Stop

## Tasks

| User says | Command |
|-----------|---------|
| "tasks", "task list" | `agentbus tasks --target $TARGET_AGENT` |
| "working", "in flight" | `agentbus tasks --target $TARGET_AGENT --state working` |
| "completed", "what finished" | `agentbus tasks --target $TARGET_AGENT --state completed` |
| "failed", "errors" | `agentbus tasks --target $TARGET_AGENT --state failed` |
| specific task ID | `agentbus tasks --target $TARGET_AGENT <task_id>` |
| "cancel", "stop", "kill" | `agentbus cancel <task_id> --target $TARGET_AGENT` |

All commands run from: `cd $AGENTBUS_DIR`

Present as:
```
=== Tasks on $TARGET_AGENT ===
  [>] 2026-04-12T10:30 abc123.. working   mint build...
  [+] 2026-04-12T10:28 def456.. completed echo hello
  [-] 2026-04-12T10:25 ghi789.. failed    grpcurli ...
  3 task(s)
```

## Results

```bash
# Unread only (default):
cd $AGENTBUS_DIR && python3 -m agentbus.cli results

# All: add --all
# Specific task: pass task_id
```

## Ack

```bash
cd $AGENTBUS_DIR && python3 -m agentbus.cli ack          # all
cd $AGENTBUS_DIR && python3 -m agentbus.cli ack <task_id> # specific
```

## Inbox

```bash
cat ~/agentbus-inbox.log 2>/dev/null || echo "(no messages yet)"
```

## Stop Listener

```bash
pkill -f "hook_listener.*$LOCAL_AGENT" 2>/dev/null && echo "Listener stopped" || echo "No listener running"
```
