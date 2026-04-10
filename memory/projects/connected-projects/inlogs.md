# InLogs / Kusto Query Reference

## hp-ats-integration-mt
- **Cluster**: `lilogsusprod05`
- **Database**: `hp-ats-integration-mt`
- **Table**: `hp_ats_integration_mt_logs`

### Common Query Patterns

**Search by treeId:**
```kql
hp_ats_integration_mt_logs
| where treeId has "YOUR_TREE_ID"
```

**Search by time range (last 1 hour):**
```kql
hp_ats_integration_mt_logs
| where timestamp > ago(1h)
| order by timestamp desc
| take 100
```

**Search by error level:**
```kql
hp_ats_integration_mt_logs
| where level == "ERROR"
| where timestamp > ago(1h)
| order by timestamp desc
| take 50
```

**Search by message content:**
```kql
hp_ats_integration_mt_logs
| where message has "keyword"
| where timestamp > ago(1h)
| order by timestamp desc
| take 50
```

### Timestamp Conversion (Unix ms to PST)
```bash
TZ="America/Los_Angeles" date -r $((TIMESTAMP_MS/1000)) "+%Y-%m-%d %H:%M:%S %Z"
```

### How to Execute
Use the `execute_kusto_query` MCP tool:
- `cluster_name`: "lilogsusprod05"
- `database`: "hp-ats-integration-mt"
- `query`: your KQL query

Or use `target` parameter for auto-discovery:
- `target`: "hp-ats-integration-mt"
