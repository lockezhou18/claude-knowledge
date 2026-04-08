# Code Search Guide

## Tool Priority
1. **Current repo**: `grep`, `Glob`, `Read` — always search locally first
2. **Cross-repo (Jarvis)**: `jarvis_codesearch` — LinkedIn's primary code search. Supports advanced filters.
3. **Unified search**: `unified_context_search` — searches code + Confluence + Slack + Jira in one call
4. **Semantic search**: `search_semantic_code` — when keyword search returns noise. Understands meaning, not just text matching. Use for: "find retry logic", "find error handling for timeouts", "find authentication flow"
4b. **Service dependencies**: `fetch_call_graph` — service-level dependency graph (who calls who)
5. **Get file**: `jarvis_get_file` — fetch full source of a specific file found via Jarvis
6. **Git history**: `git log`, `git blame` — when was this added, by whom, what PR?
7. **PR context**: `gh pr list --search`, `gh pr view` — review comments often have the WHY

## Jarvis Code Search — Advanced Syntax (go/code)

Since we follow convention (mp name, file path, class/method names), combining filters finds exactly what you need.

**Filters (combinable with AND/OR/NOT):**

| Filter | Syntax | Example |
|--------|--------|---------|
| File name | `f:` `file:` `name:` | `f:ContractResource.java` `f:*ServiceImpl` |
| File path | `p:` `path:` | `p:hp-ats*processor` |
| Multiproduct | `mp:` | `mp:hp-ats-integration-mt` `mp:^hp*` |
| Package | `pkg:` | `pkg:com.linkedin.talent*` |
| Method/function | `m:` `method:` | `m:processPhase2` `m:get*Mapping` |
| Function usage | `fu:` `func:` | `fu:createOrUpdateHistory` |
| Class declaration | `c:` `class:` | `c:ApplicationProcessor` `c:*ServiceImpl` |
| Class usage | `cu:` | `cu:HireEntityRequest` |
| Super class | `sc:` | `sc:AbstractProcessor` |
| Imports | `i:` `import:` | `i:com.linkedin.talent*grpc` |
| File type | `type:` | `type:java` `type:proto` `type:py` |
| Repo name | `reponame:` | `reponame:hiring-platform/*` |
| Case sensitive | `case:()` | `case:("HireEntity")` |
| File initials | `fi:` | `fi:wa` (for WebApps.java) |
| Package initials | `pkgi:` | `pkgi:clgc` (for com.linkedin.galene.codesearch) |
| Non-MP files | `ismpfile:false` | Find files not in any MP |
| Repo type | `repotype:` | `repotype:github` `repotype:git` |

**Boolean operators** (case-sensitive): `AND`, `OR`, `NOT`
- No operator between terms = implicit AND
- Precedence: Brackets > NOT > AND > OR
- Multiple values for same filter: `mp:seas|galene` (OR) or `mp:seas mp:galene` (also OR)

**Regex** (limited): `^` (start), `$` (end), `*` (wildcard)
- `mp:^hp$` — exact match for "hp"
- `c:^Application*Processor$` — class starting with Application, ending with Processor
- For code field: regex must contain at least 3 characters (trigram index)

**Phrase search**: Use double quotes
- `"hello world"` — exact phrase match
- `"^hello world$"` — exact phrase with word boundaries

**Special characters**: Escape with backslash
- `mp\:hello` — searches for literal "mp:hello" in content
- `\^hello\$` — searches for literal "^hello$"

## Common Search Patterns

```
# Find how peer services implement a pattern
mp:^talent* AND c:*Processor AND m:process* NOT p:test

# Find all gRPC service implementations in HP
mp:^hp* AND c:*GrpcService NOT p:test

# Find who uses our proto/API (downstream consumers)
cu:HireEntityRequest NOT mp:hp-ats-integration-mt

# Find config for a specific service
f:application.src AND mp:talent-solutions-api

# Find how a shared library is used across repos
i:com.linkedin.d2.balancer* AND m:retry*

# Find all Kafka topic references
"IntegrationExportRequestStatusEvent" type:java

# Find test examples for a class
c:ApplicationProcessorTest mp:hp-ats-integration-mt

# Find service implementations without tests
mp:^hp AND c:*ServiceImpl NOT p:test

# Find who extends a base class
sc:AbstractProcessor mp:^talent*

# Find all proto files in a project area
type:proto mp:^hp*
```

## unified_context_search — Multi-Source in One Call

When you need to search code + docs + Slack + Jira simultaneously:
```
sources: ["jarvis", "mp_knowledge", "semantic_code", "slack", "jira", "wiki"]
```
- Supports full Jarvis syntax when `sources=["jarvis"]`
- Auto-fetches full content for top 2 results (configurable via `jarvis_full_content_limit`)
- Skips non-code files (config, generated) for full-content fetch

## What to Look For in Code
- **Patterns**: How do other services in the same org handle this? Don't invent — follow existing patterns.
- **Business logic**: Config values, retry settings, feature flags, routing rules — these live in code, not docs.
- **Test cases**: Tests document expected behavior. Read tests before reading implementation.
- **Shared libraries**: Check if a utility/pattern already exists before building your own.
- **Error handling**: How do peer services handle the same failure modes?

## Tips
- Changes reflect in ~1-2 min after pre-commit for SVN, ~2 hours for Git
- Config file changes may have additional delay
- `go/code QUERY` in Chrome searches directly
- IntelliJ plugin and CLI interface also available
- When code contradicts docs — **code wins**
- **IMPORTANT: `jarvis_codesearch` is an MCP tool, NOT a CLI command.** Use `mcp__captain__jarvis_codesearch` or `unified_context_search` with `sources=["jarvis"]`. Do NOT run `captain jarvis_codesearch` in Bash — it will fail with "No such command."
- Use `jarvis_get_file` (MCP tool) to fetch full file content after finding it via search. Do NOT try to `cat` or `curl` Jarvis URLs.
