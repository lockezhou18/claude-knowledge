---
name: ai-usage-report
description: Generate executive-level AI tool usage and cost report for any crew, combining adoption + cost + org data
inputs: ["crew_id", "month"]
chain_to: null
chain_when: null
project: null
---

## Overview

Combines multiple data sources (crew API + developer_supertable + claude_code + cursor_usage_events) to produce a comprehensive AI tool usage report that no single dashboard provides.

## Steps

1. **Get crew members:**
   Use `get_crew_members` MCP tool with `crew_id={{crew_id}}`, `full_time_only=true`.
   Extract all `email` and `username` (ldap) values.

2. **Query adoption from developer_supertable:**
   ```sql
   SELECT
     ldap,
     COUNT(DISTINCT CASE WHEN is_any_ai_tool_user THEN activity_date_pt END) AS ai_active_days,
     COUNT(DISTINCT CASE WHEN is_claude_user THEN activity_date_pt END) AS claude_days,
     COUNT(DISTINCT CASE WHEN is_copilot_user THEN activity_date_pt END) AS copilot_days,
     COUNT(DISTINCT CASE WHEN is_cursor_user THEN activity_date_pt END) AS cursor_days,
     COUNT(DISTINCT CASE WHEN is_windsurf_user THEN activity_date_pt END) AS windsurf_days,
     COALESCE(SUM(num_claude_sessions), 0) AS total_claude_sessions,
     COALESCE(SUM(num_claude_commits), 0) AS total_claude_commits,
     COALESCE(SUM(num_claude_pull_requests), 0) AS total_claude_prs,
     COALESCE(SUM(num_total_ai_completions), 0) AS total_ai_completions
   FROM openhouse.u_svc_pr_deitools.developer_supertable
   WHERE datepartition >= '{{month}}-01'
     AND activity_date_pt >= DATE '{{month}}-01'
     AND activity_date_pt < DATE '{{month}}-01' + INTERVAL '1' MONTH
     AND ldap IN ({{ldap_list}})
   GROUP BY ldap
   ORDER BY ai_active_days DESC
   ```
   - Table: `openhouse.u_svc_pr_deitools.developer_supertable`
   - Server: holdem
   - Note: no crew column — filter by ldap list from step 1

3. **Query Claude Code cost:**
   ```sql
   SELECT
     REPLACE(email_address, '@linkedin.com', '') AS ldap,
     COUNT(DISTINCT CAST(FROM_UNIXTIME(date, 'America/Los_Angeles') AS DATE)) AS active_days,
     ROUND(SUM(
       REDUCE(
         CAST(json_extract(model_breakdown, '$') AS ARRAY(JSON)),
         CAST(0.0 AS DOUBLE),
         (s, x) -> s + COALESCE(CAST(json_extract_scalar(x, '$.estimated_cost.amount') AS DOUBLE), 0.0),
         s -> s
       )
     ) / 100.0, 2) AS claude_cost_usd
   FROM openhouse.u_svc_pr_deitools.claude_code
   WHERE email_address IN ({{email_list}})
     AND model_breakdown IS NOT NULL
     AND model_breakdown != '[]'
     AND CAST(FROM_UNIXTIME(date, 'America/Los_Angeles') AS DATE) >= DATE '{{month}}-01'
     AND CAST(FROM_UNIXTIME(date, 'America/Los_Angeles') AS DATE) < DATE '{{month}}-01' + INTERVAL '1' MONTH
   GROUP BY email_address
   ORDER BY claude_cost_usd DESC
   ```
   - **CRITICAL: divide amount by 100** — field is in cents, not dollars (know-041)
   - Reflects LinkedIn enterprise pricing (Opus ~40% of public API rate, Sonnet at par)

4. **Query Claude model breakdown (crew total):**
   ```sql
   SELECT
     json_extract_scalar(model_entry, '$.model') AS model,
     ROUND(SUM(CAST(json_extract_scalar(model_entry, '$.estimated_cost.amount') AS DOUBLE)) / 100.0, 2) AS cost_usd,
     SUM(CAST(json_extract_scalar(model_entry, '$.tokens.output') AS BIGINT)) AS output_tokens
   FROM openhouse.u_svc_pr_deitools.claude_code
   CROSS JOIN UNNEST(CAST(json_extract(model_breakdown, '$') AS ARRAY(JSON))) AS t(model_entry)
   WHERE email_address IN ({{email_list}})
     AND model_breakdown IS NOT NULL AND model_breakdown != '[]'
     AND CAST(FROM_UNIXTIME(date, 'America/Los_Angeles') AS DATE) >= DATE '{{month}}-01'
     AND CAST(FROM_UNIXTIME(date, 'America/Los_Angeles') AS DATE) < DATE '{{month}}-01' + INTERVAL '1' MONTH
   GROUP BY json_extract_scalar(model_entry, '$.model')
   ORDER BY cost_usd DESC
   ```

5. **Query Cursor cost:**
   ```sql
   SELECT
     REPLACE(email, '@linkedin.com', '') AS ldap,
     COUNT(*) AS cursor_events,
     ROUND(SUM(CAST(total_cents AS DOUBLE)) / 100.0, 2) AS cursor_cost_usd
   FROM openhouse.u_svc_pr_deitools.cursor_usage_events
   WHERE email IN ({{email_list}})
     AND total_cents IS NOT NULL
     AND kind != 'Errored, Not Charged'
     AND CAST(FROM_UNIXTIME(timestamp / 1000, 'America/Los_Angeles') AS DATE) >= DATE '{{month}}-01'
     AND CAST(FROM_UNIXTIME(timestamp / 1000, 'America/Los_Angeles') AS DATE) < DATE '{{month}}-01' + INTERVAL '1' MONTH
   GROUP BY email
   ORDER BY cursor_cost_usd DESC
   ```
   - `total_cents` field — divide by 100 for USD

6. **Assemble the report:**

   ### Section A: Summary
   ```
   ## Crew {{crew_id}} — AI Usage Report ({{month}})

   | Metric | Value |
   |--------|-------|
   | Total FTEs | [from step 1] |
   | AI tool users | [from step 2] |
   | Adoption rate | [users / FTEs]% |
   | Claude users | [count] |
   | Cursor users | [count] |
   | Total Claude cost | $[from step 3] |
   | Total Cursor cost | $[from step 5] |
   | **Grand total** | **$[sum]** |
   ```

   ### Section B: Per-Person Combined
   Join steps 2 + 3 + 5 by ldap. Sort by total cost descending.
   ```
   | Person | AI Days | Claude Cost | Cursor Cost | Total | Sessions | Commits | PRs |
   ```

   ### Section C: Model Breakdown
   From step 4.
   ```
   | Model | Cost | % of Total |
   ```

   ### Section D: Key Insights
   Auto-generate observations:
   - Adoption rate and dominant tool
   - Top spenders and their usage patterns
   - Model mix (% opus vs sonnet vs haiku)
   - Dual-tool vs single-tool users
   - Members not in supertable (likely managers with no coding activity)

## Expected Output

A complete markdown report with 4 sections: summary, per-person, model breakdown, and insights.

## Data Availability

- **Supertable**: Jan 2023 to present (but AI columns: Copilot from Apr 2025, Cursor/Windsurf from Aug 2025, Claude from Jan 2026)
- **claude_code**: Jan 2026+
- **cursor_usage_events**: Aug 2025+
- **ETL lag**: Trino tables lag real-time by ~1-2 days. For current-month data, use Anthropic Console as SoT.

## On Failure

- Auth error on Trino → run `! az login` or check VPN
- No data for month → check data availability windows above
- Cost seems wrong → cross-validate one person against Anthropic Console (platform.claude.com workspace limits page shows MTD per user). Remember: amounts in cents, enterprise pricing.
- Missing crew members → some may not have coding activity (managers). Note them separately.
