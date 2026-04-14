# Rules Derived from Usage Insights (2026-04-07)

## Debugging & Investigation

- **Prefer curli/REST APIs over Trino/SQL for data lookups.** Unless the user explicitly asks for SQL/Trino, use `curli` or `grpcurli` for data retrieval. REST APIs are faster and more reliable in this environment. Multiple sessions showed wasted time on Trino when curli would have resolved issues in one call.

- **Use observe-agent as the primary log investigation tool.** Do not grep local files or manually construct Kusto queries for production log analysis. observe-agent has the context and access. Always reuse session IDs for multi-step investigations.

- **Trust user direction on which component to check.** When the user specifies a file, processor, service, or API to investigate, go there FIRST. Do not investigate alternative components before checking the one the user pointed to. The user has architectural knowledge — their hints are not suggestions, they're directions.

## Code Changes & PRs

- **Target the minimal correct layer.** Prefer fixes in shared service methods over processor-level changes. Start with the simplest approach (e.g., fire-and-forget over complex retry logic, contains-check over pagination abstraction). Do not over-engineer. Only add complexity when the user explicitly requests it.

- **Verify Java compilation after every code change.** After editing Java files, run the build (`./gradlew compileJava` or `mint build`) and fix ALL compilation errors (wrong types, unused imports, Java version incompatibilities like `Set.of()`) before presenting the change. Do not declare a fix complete until it compiles.

- **PR descriptions must be complete.** CI will fail without a full description section. Always include one. When using curli for E2E verification in PRs, verify URL encoding (especially for URNs with colons and special characters).
