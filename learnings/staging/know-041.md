---
id: know-041
track: knowledge
type: episodic
repos: [*]
tags: [claude-code, trino, cost, metrics, ai-usage, developer-productivity-analysis]
severity: high
rot_rate: medium
status: active
created: "2026-04-03"
last_verified: "2026-04-03"
use_count: 4
outcome_score: 0
origin_skill: learn
---

## Context

When querying AI tool costs from the developer-productivity-analysis Trino tables.

## Guidance

When querying `openhouse.u_svc_pr_deitools.claude_code`, the `estimated_cost.amount` field inside `model_breakdown` JSON is in **cents** (divide by 100 for USD). This reflects **LinkedIn enterprise pricing**, not public API rates:
- **Opus**: ~40% of public API rate (significant discount)
- **Sonnet**: at par with public pricing (1.0x)
- **Haiku**: ~1.25x of public pricing

For `openhouse.u_svc_pr_deitools.cursor_usage_events`, the `total_cents` field is also in cents (divide by 100). Filter `kind != 'Errored, Not Charged'` to exclude failed requests.

Cross-verified against Anthropic Console SoT (platform.claude.com workspace limits page) — daily rates are consistent.

## When to Apply

Any time you query AI tool cost data from Trino for reporting or analysis. Always divide by 100 for USD. Do not use public API pricing to compute costs — use the `estimated_cost` field which already reflects enterprise rates.
