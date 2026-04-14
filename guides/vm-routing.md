# VM Routing Rule

## VM: bizhou-ld2.linkedin.biz

Route work to the VM via the `/delegate` skill. Two transports:
- **SSH/vm-run**: shell commands (builds, tests, deploys)
- **AgentBus**: thinking tasks via claude -p on VM (review, investigate, analyze)

### Use /delegate (preferred — handles routing automatically):
```bash
~/bin/vm-agent "mint build hp-ats-integration-mt"      # shell on VM
~/bin/vm-agent -t "review the latest PR changes"       # thinking on VM
~/bin/vm-agent --async "run full test suite"            # async + Monitor notification
~/bin/vm-agent --auto "build, test, fix, re-test"      # autonomous multi-round
```

### Route to VM (shell via SSH/vm-run):
- **Build**: `mint build`, `mint test`, `./gradlew`, compilation commands
- **Long-running tests**: E2E tests, integration test suites
- **Service operations**: `go-status`, `go-deploy`, KSAP commands
- **Heavy processing**: large file operations, data transforms

### Route to VM (thinking via AgentBus):
- **Code review**: `vm-agent -t "review the changes in ..."`
- **Investigation**: `vm-agent -t "investigate why ..."`
- **Analysis**: `vm-agent -t "analyze the test failures"`
- **Eval/dream**: `vm-agent --async "run eval pipeline"`

### Try LOCAL FIRST, fall back to VM:
- **gRPC/REST calls**: `grpcurli`, `curli` — run locally first (local DV auth usually active)
- Only route to VM if local call fails with auth error
- If VM call fails with DV auth error, tell the user to run `! ssh vm 'dv-auth'`

### Keep local (run directly):
- **File reads/edits**: Read, Edit, Write, Glob, Grep tools
- **Git operations**: commit, push, PR creation, branch management
- **Planning/thinking**: no compute needed
- **Claude knowledge**: memory, learnings, insights writes
- **Light scripts**: short bash one-liners, jq, etc.
- **Browser tools**: playwright, observe-agent queries

### Fallback: direct SSH/vm-run (when AgentBus is down)
```bash
bash -c "cd /path/to/local/repo && vm-run mint build"
bash -c "ssh vm 'go-status hp-ats-integration-mt'"
bash -c "scp vm:~/workspace/<repo>/file.txt /tmp/"
```

### Important:
- Use `bash -c "..."` wrapper — direct `ssh` is blocked by Claude Code permissions
- `vm` is an SSH alias in `~/.ssh/config.custom` (ports 8080, 4222 forwarded)
- SSH tunnel for NATS (port 4222) — vm-agent auto-creates if needed
- If SSH fails: check VPN connected? Kerberos valid (`klist`)?
- VM services: tmux `nats` (NATS server), tmux `agentbus` (Claude listener)
