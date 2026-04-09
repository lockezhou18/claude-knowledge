# Memory Index

## Workflow Preferences
- [Workflow Rules](workflow-rules.md) - Two-phase explore-then-implement pattern, interaction preferences

## Tricks
- [Tricks & Handy Shortcuts](tricks.md) - rerun-check, CI tips, useful commands

## Engineering Principles
- [Engineering Principles](engineering-principles.md) - 13 principles: estimation, 5 Whys, data-driven decisions, own dependencies, design for failure, no throwaway code, logs

## Espresso
- [Espresso Metrics](espresso-metrics.md) - HireAccessControlDB metrics are under cluster name MD-2, not the DB name
- [Espresso Table Traffic](espresso-table-traffic.md) - Per-table traffic via espresso-router `Traffic_Checker_Table_Stats` (note `.` not `_` between cluster and DB)

## Graduated Insights
- [V2 Identity findFirst()](v2-identity-findFirst.md) - Never use findFirst() on V2 identity streams; try all V2s with fallback
- [Research Pipeline Pattern](research-pipeline-pattern.md) - 5-step exploration: simple question → pull threads → map ecosystem → cross-validate → combine dimensions

## Feedback
- [Front-load Context](feedback-frontload-context.md) — Always specify service/file/tool upfront to avoid wrong-approach friction (28 instances)

## Eval-Driven (updated by /improve-agent)
- [Behavioral Gates](eval-behavioral-gates.md) — Approach, tool, principle, compound gates from 35-session eval
- [Principle Scores](eval-principle-scores.md) — 85.1% adherence, top violations: verify (14x), guess values (13x)
- [System Architecture](eval-system-architecture.md) — How eval, compound learning, and Auto Dream integrate

## Troubleshooting
- [Build & Config Troubleshooting](build-troubleshooting.md) - mint build-cfg errors, local deploy issues
