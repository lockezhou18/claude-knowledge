# Dashboard, Who, Health, Sessions

## Dashboard (default — no args)

Run in parallel, present as unified view:

```bash
# 1. Tunnel
lsof -i :$NATS_PORT 2>/dev/null | grep -c LISTEN

# 2. Health
cd $AGENTBUS_DIR && python3 -m agentbus.cli health --port $NATS_PORT

# 3. Agents
cd $AGENTBUS_DIR && python3 -m agentbus.cli agents --agents-dir $AGENTS_DIR

# 4. Sessions
cd $AGENTBUS_DIR && agentbus sessions --target $TARGET_AGENT 2>/dev/null || echo "    (VM unreachable)"

# 5. Unread results
cd $AGENTBUS_DIR && python3 -m agentbus.cli results 2>/dev/null || echo "    (no results)"

# 6. Tasks summary
cd $AGENTBUS_DIR && agentbus tasks --target $TARGET_AGENT 2>/dev/null | tail -1 || echo "    (unreachable)"

# 7. A2A gateway
lsof -i :8080 2>/dev/null | grep -c LISTEN && echo "    OK (port 8080)" || echo "    not running"
```

Present as:
```
=== AgentBus Comms ===
  Tunnel:    OK / DOWN
  NATS:      OK / DOWN
  Agents:    N registered
  Sessions:  ...
  Results:   N new
  Tasks:     N total (M working, K completed)
  A2A:       OK (port 8080) / NOT RUNNING
```

## Who

```bash
cd $AGENTBUS_DIR && python3 -m agentbus.cli agents --agents-dir $AGENTS_DIR
```

## Health

```bash
lsof -i :$NATS_PORT 2>/dev/null | grep LISTEN && echo "Tunnel: OK" || echo "Tunnel: DOWN"
cd $AGENTBUS_DIR && python3 -m agentbus.cli health --port $NATS_PORT
~/bin/vm-agent --health 2>&1 || echo "(VM unreachable)"
```

## Sessions

```bash
cd $AGENTBUS_DIR && agentbus sessions --target $TARGET_AGENT 2>&1 || echo "(VM unreachable)"
```
