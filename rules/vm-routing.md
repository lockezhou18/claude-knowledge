# VM Routing Rule

## VM: bizhou-ld2.linkedin.biz

When running on the local machine (macOS), route heavy commands to the VM via SSH.

### Route to VM — use `vm-run` (syncs code + runs remotely):
- **Build**: `mint build`, `mint test`, `./gradlew`, compilation commands
- **Docker**: any `docker` or `docker-compose` commands
- **Long-running tests**: E2E tests, integration test suites
- **Service operations**: `go-status`, `go-deploy`, KSAP commands
- **Heavy processing**: large file operations, data transforms

### Try LOCAL FIRST, fall back to VM:
- **gRPC/REST calls**: `grpcurli`, `curli` against internal services
  - Run locally first — local DV auth is usually active
  - Only route to VM if local call fails with auth error
  - NEVER blindly route all curli/grpcurli to VM — DV auth on VM is often expired
  - If VM call fails with DV auth error, tell the user to run `! ssh vm 'dv-auth'`

### Keep local (run directly):
- **File reads/edits**: Read, Edit, Write, Glob, Grep tools
- **Git operations**: commit, push, PR creation, branch management
- **Planning/thinking**: no compute needed
- **Claude knowledge**: memory, learnings, insights writes
- **Light scripts**: short bash one-liners, jq, etc.
- **Browser tools**: playwright, observe-agent queries

### Preferred: `vm-run` (auto-sync + run)
`~/bin/vm-run` detects the current git repo, rsyncs it to `~/workspace/<repo>` on the VM, then runs the command. Works from ANY local path.

```bash
# From any local repo path (e.g., ~/workspace/connected_project_phase2/hp-ats-integration-mt)
bash -c "cd /path/to/local/repo && vm-run mint build"
bash -c "cd /path/to/local/repo && vm-run mint test"
bash -c "cd /path/to/local/repo && vm-run ./gradlew compileJava"
```

### Direct SSH (for commands not tied to a repo):
```bash
bash -c "ssh vm 'grpcurli ...'"
bash -c "ssh vm 'go-status hp-ats-integration-mt'"
bash -c "scp vm:~/workspace/<repo>/file.txt /tmp/"
```

### Important:
- Use `bash -c "..."` wrapper — direct `ssh` is blocked by Claude Code permissions
- `vm` is an SSH alias defined in `~/.ssh/config.custom` (passwordless via LinkedIn key)
- `vm-run` rsyncs source code (excluding .gradle, build, out, .git) before running
- If SSH fails, check: VPN connected? Kerberos valid (`klist`)?
- For interactive commands, use `linkedin-cli-tools:interactive-cli` with SSH
