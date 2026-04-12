---
id: know-048
track: knowledge
type: semantic
repos: [mcm-mt, hp-ats-integration-mt, talent-solutions-api, *]
tags: [entity-routing, curli, multi-colo, contract, fabric, money-entity-routing, d2]
severity: high
rot_rate: slow
status: active
created: 2026-04-08
last_verified: 2026-04-08
use_count: 1
outcome_score: 0
origin_skill: learn
---

# Entity Routing (ERS) — Contract to Colo Lookup

## Context
LinkedIn uses Entity Routing Service (ERS, aka `money-entity-routing`) to determine which colo/fabric owns a given entity (contract, ad account, etc.). For Hiring Platform, contracts are routed with context `RECRUITER`.

## Guidance

**When you need to find which colo a contract routes to**, use this curli command:

```bash
curli --force-insecure-d2 -f prod-ltx1 -H 'X-RestLi-Protocol-Version: 2.0.0' -XGET \
  'd2://entityRoutes/(context:RECRUITER,entity:urn%3Ali%3Acontract%3A<CONTRACT_ID>)'
```

Key details:
- **D2 cluster**: `MoneyEntityRoutingService`
- **D2 services**: `entityRoutes` (route lookup), `entityRouteBuckets` (bucket management), `internalEntityRoutes`
- **LPS config**: `money-entity-routing/config/public/lps-d2-MoneyEntityRoutingService.src`
- **Rest.li resource**: `EntityRoutesResource` — ComplexKey with `EntityRouteKey(context, entity)`
- **Context enum** (`EntityRouteContext`): `RECRUITER`, `ADS`, `PAYMENTS`, `SALES`
- **Route tables** (Espresso): `recruiter`, `recruiterBucket`, etc. per context
- **Response fields**: `current.fabric` (e.g., `urn:li:fabric:prod-lor1`), `entity`, `context`, `autoReassignable`
- **404 = no route assigned** — typical for sandbox/test contracts when queried from wrong fabric. Use `-f prod-ltx1` to hit a prod fabric that has the data.
- **RestLi v2 header required** — without `X-RestLi-Protocol-Version: 2.0.0`, the ComplexKey `(key:value,key:value)` format isn't parsed correctly.

## When to Apply
- Debugging cross-colo issues (e.g., "why is this contract's data not syncing in this fabric?")
- Understanding which fabric owns a Connected Project's contract
- Pre-flight check before running fabric-specific curli commands
- Verifying test data setup for sandbox contracts
