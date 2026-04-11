# Watch Deps — Track Upstream/Downstream Changes

Monitor changes in dependencies and consumers since last check.

**Usage:**
- `/watch-deps` — check what changed
- `/watch-deps add [repo]` — add to watchlist
- `/watch-deps list` — show watched deps

## Config

`~/.claude/learnings/dependencies.jsonl` — one entry per dependency:
```json
{"repo": "talent-solutions-api", "relationship": "upstream", "what_we_use": "GetCandidateHiringState gRPC", "last_checked": "2026-04-01"}
```

## Check Flow

1. Read `dependencies.jsonl` for watched deps
2. For each dep: check recent commits to proto/API files via `jarvis_codesearch` or `gh api`
3. Check `go-status` for recent deploys
4. Report: action-required vs awareness vs no-change

## Auto-Detection (first time in a repo)

Scan for: `GrpcClient`, `@ServiceClient`, Kafka topic names, `@EspressoTable`, `@RestClient`, lix keys. Present findings, ask which to watch.

## Integration

- Session start: compound agent checks dependencies, adds to briefing if stale
- Before PR: flag if changes affect downstream API contracts
- During /investigate: check if upstream deployed recently
