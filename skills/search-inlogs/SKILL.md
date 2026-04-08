---
description: |-
  Search hp-ats-integration-mt production logs in InLogs (Kusto).
  Use when the user wants to search production logs, investigate errors,
  debug issues, or look up requests by treeId, message content, or time range.
user-invocable: true
allowed-tools:
  - execute_kusto_query
inputs:
  - query_type:
      description: "Type of search: treeId, error, message, time-range, or custom KQL"
      example_value: "treeId"
  - search_value:
      description: "The value to search for (treeId, keyword, error message, etc.)"
      example_value: "AAZJaRc834YsFxT8nWDiyQ=="
  - time_range:
      description: "How far back to search (e.g., 1h, 6h, 1d, 7d). Default: 1h"
      example_value: "1h"
  - limit:
      description: "Max number of results to return. Default: 50"
      example_value: "50"
---

# Search InLogs (hp-ats-integration-mt)

Search production logs for **hp-ats-integration-mt** using Kusto (InLogs).

## Cluster Details

- **Cluster**: `lilogsusprod05`
- **Database**: `hp-ats-integration-mt`
- **Table**: `hp_ats_integration_mt_logs`

## Step 1: Determine Query Type

Based on user input, construct the appropriate KQL query:

### Search by treeId
```kql
hp_ats_integration_mt_logs
| where treeId has "{{search_value}}"
| order by timestamp desc
| take {{limit}}
```

### Search for errors (recent)
```kql
hp_ats_integration_mt_logs
| where level == "ERROR"
| where timestamp > ago({{time_range}})
| order by timestamp desc
| take {{limit}}
```

### Search by message content
```kql
hp_ats_integration_mt_logs
| where message has "{{search_value}}"
| where timestamp > ago({{time_range}})
| order by timestamp desc
| take {{limit}}
```

### Search by time range only
```kql
hp_ats_integration_mt_logs
| where timestamp > ago({{time_range}})
| order by timestamp desc
| take {{limit}}
```

### Custom KQL
If the user provides a custom KQL query, use it directly. Ensure the table name `hp_ats_integration_mt_logs` is used.

## Step 2: Execute the Query

Use the `execute_kusto_query` MCP tool with:
- **cluster_name**: `lilogsusprod05`
- **database**: `hp-ats-integration-mt`
- **query**: the constructed KQL query

Alternatively, use the `target` parameter for auto-discovery:
- **target**: `hp-ats-integration-mt`

## Step 3: Present Results

1. Show the **exact KQL query** that was executed
2. Present results in a readable format
3. Highlight key fields: `timestamp`, `level`, `message`, `treeId`, `className`
4. If timestamps are in Unix milliseconds, convert to PST:
   ```bash
   TZ="America/Los_Angeles" date -r $((TIMESTAMP_MS/1000)) "+%Y-%m-%d %H:%M:%S %Z"
   ```
5. Note the number of results returned
6. Flag any ERROR or WARN level entries

## Common Debugging Patterns

### Find all logs for a specific request
```kql
hp_ats_integration_mt_logs
| where treeId has "{{search_value}}"
| order by timestamp asc
```

### Find errors with stack traces
```kql
hp_ats_integration_mt_logs
| where level == "ERROR"
| where timestamp > ago({{time_range}})
| project timestamp, className, message, exceptionMessage, exceptionStackTrace
| order by timestamp desc
| take {{limit}}
```

### Find logs related to a specific entity (e.g., hiringProject, contract)
```kql
hp_ats_integration_mt_logs
| where message has "{{search_value}}"
| where timestamp > ago({{time_range}})
| project timestamp, level, className, message, treeId
| order by timestamp desc
| take {{limit}}
```

### Count errors by class in last N hours
```kql
hp_ats_integration_mt_logs
| where level == "ERROR"
| where timestamp > ago({{time_range}})
| summarize count() by className
| order by count_ desc
| take 20
```

## Preferred Tool: observe agent

The `execute_kusto_query` MCP tool requires Trino MFA auth which often fails. **Prefer `observe agent` CLI instead:**

```bash
# First call requires Okta browser auth
observe agent "Search hp-ats-integration-mt logs for <query>"

# Follow-up queries reuse session
observe agent --session <session-id> "<follow-up query>"
```

`observe agent` can search ANY service, not just hp-ats-integration-mt:
- `talent-partner-integrations-mt`
- `unified-integrations-raw-data-mt`
- `talent-solutions-api-frontend`

**Timeout:** Use 600000ms (10 min) — investigations can be long-running.

## Error Handling

- If the query times out, suggest narrowing the time range or adding more filters
- If no results are found, suggest broadening the search (longer time range, partial match)
- If authentication fails, inform the user they may need to run `az login`
- **InLogs ingestion delay**: ~2-5 minutes after event processing before logs appear
- **observe agent Okta auth**: First call opens browser for Okta login — don't interrupt, let user complete
