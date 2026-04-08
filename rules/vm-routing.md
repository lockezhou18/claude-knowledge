# VM Routing Rule

## VM: bizhou-ld2.linkedin.biz

When running on the local machine (macOS), route heavy commands to the VM via SSH.

### Route to VM (prefix with `ssh bizhou-ld2.linkedin.biz '...'`):
- **Build**: `mint build`, `mint test`, `./gradlew`, compilation commands
- **gRPC/REST calls**: `grpcurli`, `curli` against internal services
- **Docker**: any `docker` or `docker-compose` commands
- **Long-running tests**: E2E tests, integration test suites
- **Service operations**: `go-status`, `go-deploy`, KSAP commands
- **Heavy processing**: large file operations, data transforms

### Keep local (run directly):
- **File reads/edits**: Read, Edit, Write, Glob, Grep tools
- **Git operations**: commit, push, PR creation, branch management
- **Planning/thinking**: no compute needed
- **Claude knowledge**: memory, learnings, insights writes
- **Light scripts**: short bash one-liners, jq, etc.
- **Browser tools**: playwright, observe-agent queries

### SSH command format:
```bash
# Simple command
ssh bizhou-ld2.linkedin.biz 'cd ~/workspace/<repo> && mint build'

# Multi-command
ssh bizhou-ld2.linkedin.biz 'cd ~/workspace/<repo> && mint build && mint test'

# With env vars
ssh bizhou-ld2.linkedin.biz 'export JAVA_HOME=/path && cd ~/workspace/<repo> && ./gradlew compileJava'
```

### Important:
- Code must be synced via mutagen before running remote builds
- If SSH fails, check: VPN connected? Kerberos valid (`klist`)?
- For interactive commands, use `linkedin-cli-tools:interactive-cli` with SSH
