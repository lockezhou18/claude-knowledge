---
name: sync
description: "Manage Mutagen file sync between laptop and VM. Check status, fix broken sessions, create/terminate sessions."
allowed-tools: Bash(mutagen *), Bash(bash -c "ssh vm*), Bash(bash -c "scp*)
inputs: ["subcommand"]
---

# Sync — Mutagen File Sync Management

Manage bidirectional file sync between laptop and VM via Mutagen.

**Usage:**
- `/sync` or `/sync status` — show all session status
- `/sync fix` — diagnose and repair broken sessions
- `/sync create <local> <remote> [--name NAME]` — create a new sync session
- `/sync terminate <name>` — remove a session
- `/sync pause <name>` / `/sync resume <name>` — pause/resume a session

## Architecture

- **Mutagen 0.17.x** syncs local `/Users/bizhou/workspace` to `vm:~/workspace/`
- VM: `bizhou-ld2.linkedin.biz` (SSH alias: `vm`)
- Two primary active sessions:
  - `workspace` — entire workspace directory (covers connected_project_phase2 and all project folders)
  - `hp-ats-integration-mt` — dedicated sync for the main repo checkout
- Several paused `rexec-*` sessions exist for old Rexec containers (ignore unless user asks)

## Status Check (`/sync` or `/sync status`)

```bash
mutagen sync list
```

Report a table:
| Session | Alpha | Beta | Status |
|---|---|---|---|

Flag any session showing:
- "Connecting to beta" — connection broken
- "Last error:" — has an error
- "[Paused]" — intentionally paused (note but don't flag)

## Fix Flow (`/sync fix`)

### Step 1: Diagnose
```bash
mutagen sync list 2>&1
```

Look for:
- **"server magic number incorrect"** — stdout pollution on VM during non-interactive SSH
- **"unexpected EOF"** — stale agent or network drop
- **"Connecting to beta"** — can't reach VM

### Step 2: Check VM connectivity
```bash
bash -c "ssh vm 'echo OK'"
```
If this fails: VPN down or Kerberos expired. Tell user to check.

### Step 3: Check for stdout pollution
```bash
bash -c "ssh vm 'echo MARKER_START; echo MARKER_END'"
```
If ANYTHING appears between MARKER_START and MARKER_END besides blank lines, there's stdout pollution from shell profiles. Common culprits:
- `~/.bashrc` sourcing scripts that echo (e.g., agentbus autostart)
- `/etc/profile.d/` scripts with echo statements

**Fix:** Wrap offending lines in `~/.bashrc` with interactive guard:
```bash
if [[ $- == *i* ]]; then
    source ~/path/to/script.sh
fi
```

### Step 4: Kill stale agents on VM
```bash
bash -c "ssh vm 'pkill -f mutagen-agent 2>/dev/null; echo cleared'"
```
Note: exit code 255 is expected if pkill kills the SSH subprocess.

### Step 5: Terminate and recreate broken sessions
```bash
mutagen sync terminate <name>
mutagen sync create <local-path> vm:<remote-path> --name <name>
```

Primary sessions to restore:
- `mutagen sync create /Users/bizhou/workspace vm:~/workspace/ --name workspace`
- `mutagen sync create /Users/bizhou/workspace/hp-ats-integration-mt vm:~/workspace/hp-ats-integration-mt --name hp-ats-integration-mt`

### Step 6: Verify
```bash
mutagen sync list
```
Confirm "Connected: Yes" on both alpha and beta, status is "Watching for changes" or "Scanning files".

## Create Session (`/sync create`)

```bash
mutagen sync create <local-path> <remote> --name <name>
```

Example:
```bash
mutagen sync create /Users/bizhou/workspace/new-repo vm:~/workspace/new-repo --name new-repo
```

## Known Issues

| Issue | Cause | Fix |
|---|---|---|
| "server magic number incorrect" | Shell profile echoes to stdout on VM | Guard with `[[ $- == *i* ]]` |
| "unexpected EOF" on beta | Stale mutagen-agent process | Kill agent, recreate session |
| Session connects then disconnects | Large `.git` or `build/` dirs | Add `--ignore` patterns |
| Slow initial scan | Huge workspace | Wait; subsequent syncs are incremental |

## Proactive Triggers

This skill should be suggested when:
- User reports files not appearing on VM
- `/delegate` commands show stale files
- After VM reboot or network reconnect
- User asks "is sync working?"
