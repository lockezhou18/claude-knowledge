---
name: delegate
description: "Delegate tasks to the VM agent. Just describe what you want in natural language — the skill figures out the mode, transport, and flags automatically."
allowed-tools: Bash(bash -c "ssh vm*), Bash(bash -c "scp*), Bash(bash -c "rsync*), Bash(bash -c "cd * && vm-run*), Bash(bash -c "vm-run*), Bash(export PATH*vm-run*), Bash(~/bin/vm-agent*), Monitor
inputs: ["task"]
---

# Delegate — Send Work to the VM Agent

Just say what you want. The skill figures out the rest.

```
/delegate review the latest PR for hp-ats-integration-mt
/delegate run mint build
/delegate check go-status for hp-ats-integration-mt
/delegate investigate why the pipeline is stuck
/delegate run the full test suite in the background
/delegate build, test, fix failures, and re-test until green
/delegate what are the last 5 commits in hp-ats-integration-mt
```

## Step 1: Understand the Request

Read the user's natural language and determine:

**A. What mode?**

| Signal in user's words | Mode | How to execute |
|------------------------|------|----------------|
| "in the background", "async", "don't wait", "fire and forget" | **Async** | `vm-agent --async` + Monitor |
| "keep going until", "fix and re-test", "loop until green" | **Auto** | `vm-agent --auto` + Monitor |
| Everything else | **Sync** | Block until result |

**B. Shell or thinking?**

| Signal | Type | How to execute |
|--------|------|----------------|
| Exact command: `mint build`, `mint test`, `gradlew`, `go-status`, `grpcurli`, `curli`, `echo`, `ls`, `cat`, `grep` | **Shell** | `~/bin/vm-agent "<command>"` |
| Needs reasoning: "review", "investigate", "explain", "analyze", "what", "why", "how", "check", "find", "compare" | **Think** | `~/bin/vm-agent -t "<message>"` |
| Ambiguous | **Think** | Safer — VM Claude can run shell commands itself |

**C. Which repo?**

If the user mentions a repo name (e.g., "hp-ats-integration-mt", "mcm-mt"), add `--repo <name>`.
If working in a repo directory, infer from cwd.
If unclear, omit — VM agent uses ~/workspace.

**D. Fresh or continue?**

If "fresh", "new", "start over" → add `--new`
If follow-up to previous delegate → omit (auto-resumes)

## Step 2: Build and Run the Command

Assemble the `~/bin/vm-agent` command from the classification:

```bash
# Shell sync:
~/bin/vm-agent "<shell command>"

# Think sync:
~/bin/vm-agent -t "<message>"

# Think sync with repo:
~/bin/vm-agent -t --repo <repo> "<message>"

# Async (any):
~/bin/vm-agent --async "<message>"

# Auto (multi-round):
~/bin/vm-agent --auto "<message>"

# Fresh session:
~/bin/vm-agent --new -t "<message>"
```

## Step 3: For Async/Auto — Start Monitor

After firing an async or auto task, start the Monitor to watch for results:

```bash
# Get the task_id from the async response, then:
# (run from ~/projects/compound-learning-ecosystem/agentbus)

# Async (one result):
Monitor: python3 -m agentbus.watch_result --task-id <task_id> --count 1 --timeout 600

# Auto (stream checkpoints):
Monitor: python3 -m agentbus.watch_result --task-id <task_id> --count 0 --timeout 1800
```

Tell the user: "Task delegated. I'm watching for results — keep working."

## Step 4: Present Result

- **Sync**: show the result directly
- **Async**: Monitor catches result → present it when it arrives
- **Escalation**: if VM agent returns "ESCALATE:", show the escalation to the user with the suggested action

## Examples

| User says | Classification | Command |
|-----------|---------------|---------|
| "run mint build" | shell, sync | `~/bin/vm-agent "mint build"` |
| "build hp-ats-integration-mt" | shell, sync | `~/bin/vm-agent "cd ~/workspace/connected_project_phase2/hp-ats-integration-mt && mint build"` |
| "review the latest PR" | think, sync | `~/bin/vm-agent -t "review the latest PR"` |
| "what are the last 5 commits" | think, sync | `~/bin/vm-agent -t "what are the last 5 commits"` |
| "investigate why the build failed in hp-ats" | think, sync, repo | `~/bin/vm-agent -t --repo hp-ats-integration-mt "investigate why the build failed"` |
| "run the test suite in the background" | shell, async | `~/bin/vm-agent --async "mint test"` + Monitor |
| "build, test, fix, re-test until green" | think, auto | `~/bin/vm-agent --auto "build, test, fix failures, re-test"` + Monitor |
| "check go-status for hp-ats" | shell, sync | `~/bin/vm-agent "go-status hp-ats-integration-mt"` |
| "run grpcurli to get HireEntityRequest 123" | think, sync | `~/bin/vm-agent -t "run grpcurli to get HireEntityRequest with requestId 123 from ManagedEntityCrudHireEntityRequest on ei-ltx1"` |
| "start fresh — analyze the test failures" | think, sync, new | `~/bin/vm-agent --new -t "analyze the test failures"` |

**Note on grpcurli/curli with complex JSON**: Always use **think mode** (`-t`). The VM Claude builds the command locally with correct escaping. Don't try to pass complex JSON through shell mode — quoting mangles it.

## Session Management

```
/delegate check active sessions       → ~/bin/vm-agent --sessions
/delegate end the current session      → ~/bin/vm-agent --end-session
/delegate health check                 → ~/bin/vm-agent --health
```

## Fallback Chain
1. **AgentBus unreachable** → fall back to SSH (`bash -c "ssh vm '...'"`)
2. **VM unreachable** → run locally
3. **VM agent escalates** → present escalation to user

## Troubleshooting
- **NATS tunnel down**: vm-agent auto-creates. If fails → check VPN, `klist`
- **Listener not running**: `bash -c "ssh vm 'tmux attach -t agentbus'"`
- **Claude -p auth expired**: `! ssh -t vm 'claude auth login'`
- **Health check**: `~/bin/vm-agent --health`
