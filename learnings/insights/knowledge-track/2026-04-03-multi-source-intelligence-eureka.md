---
id: eureka-003
track: knowledge
type: semantic
repos: ["*"]
tags: ["eureka", "meta", "research", "data-synthesis", "ai-usage", "productivity", "pattern"]
severity: critical
rot_rate: permanent
status: active
created: "2026-04-03"
last_verified: "2026-04-03"
use_count: 0
outcome_score: 0
visibility: team
origin_skill: eureka
emerged_from: "aha-003"
graduation_candidate: true
---

## Breakthrough

Combining multiple internal data sources (Trino tables + APIs + Confluence + MP knowledge + live console) through systematic cross-validation produces executive-level intelligence that no single dashboard provides.

## The Old Way

Each data source is queried in isolation:
- go/aiide/usage for adoption dashboards
- Anthropic Console for individual cost
- Confluence for program status
- Crew API for org structure
- Each tells a partial story. No one — not even directors — has the combined picture.

## The New Way

**Multi-source data synthesis pattern:**
1. **Identify all data sources** — don't stop at the first table. Map the full ecosystem (supertable, cost tables, crew API, console, wiki, MP knowledge).
2. **Cross-validate units and accuracy** — check one source against another (Trino estimated_cost vs Anthropic Console SoT). This caught the cents-vs-dollars ambiguity.
3. **Combine dimensions** — adoption (supertable) + cost (claude_code + cursor_usage_events) + org structure (crew API) + strategy (AI Constellation wiki) = full picture.
4. **Surface insights no individual system reveals** — e.g., "100% adoption, $27K/month Claude, 90/10 Claude-to-Cursor ratio, enterprise pricing at 40% opus discount, per-person cost tiers, model usage breakdown, dual-tool usage patterns."

The result: a view that surpasses what any existing dashboard provides, assembled on-demand from raw data.

## Impact

- **Replaces**: manual dashboard-hopping and spreadsheet assembly
- **Scope**: any team wanting AI usage intelligence — the pattern is reusable
- **What changes**: instead of asking "where's the dashboard?", ask "what are all the data sources?" and synthesize

## Risks & Caveats

- Data freshness: Trino tables lag real-time (ETL delay). Console is SoT for current state.
- Enterprise pricing in estimated_cost may change — re-verify periodically.
- The pattern requires knowing which tables exist — the developer-productivity-analysis MP knowledge is the rosetta stone.

## Next Steps

- This pattern could become a `/recipe ai-usage-report` for any crew
- The Trino queries are reusable — parameterize by crew_id
- Consider proposing a combined dashboard to the DPX team that does what we did manually
