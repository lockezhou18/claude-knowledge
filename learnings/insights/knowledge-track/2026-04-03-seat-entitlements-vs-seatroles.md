---
id: know-seat-entitlements-vs-seatroles
track: knowledge
repos: [ssr-data-service, hp-ep-mt, hp-ep-api]
tags: [seatsV2, entitlements, seatRoles, aperture, recruiter-plus, hp-ep-api, proto, permission-check]
severity: high
created: 2026-04-03
last_verified: 2026-04-03
use_count: 0
outcome_score: 0
status: active
rot_rate: slow
paths: ["**/datafetchers/**", "**/hire/**"]
---

## When checking HP feature entitlements (e.g., CAN_ACCESS_RECRUITER_PLUS_FEATURES), use `seatEntitlements` on Seat, not `seatRoles`

**Context:** In ssr-data-service, we needed to check if a seat has `CAN_ACCESS_RECRUITER_PLUS_FEATURES` (Aperture/Recruiter Plus). Initial approach was to check `Seat.seatRoles` for `HP_RECRUITER_PLUS_SEARCHER_SEAT` as a proxy.

**Guidance:** `seatRoles` and `seatEntitlements` are different concepts:
- `seatRoles` = what the seat IS (HP_ADMIN_SEAT, HP_SOURCER_SEAT, HP_RECRUITER_PLUS_SEARCHER_SEAT)
- `seatEntitlements` = what the seat CAN DO (CAN_ACCESS_RECRUITER_PLUS_FEATURES, CAN_POST_JOB, etc.)

Entitlements are the canonical way to check permissions. When you need a permission check, use the actual entitlement — not a seat role as a proxy. The mapping between roles and entitlements is managed by the platform (hp-ep-mt/SeatEntitlementsService) and can change.

**Key pattern:** If the `Seat` proto doesn't have the field you need, the right move is to add it to `hp-ep-api` (Seat.proto) as a first-class field. See hp-ep-api PR #916 which added `seatEntitlements` as `repeated HiringPlatformEntitlement` to Seat.proto.

**Reusability principle:** When adding data to a model, prefer exposing it broadly (e.g., `seatEntitlements: [String!]` on `HireSeat` GraphQL type) rather than a single boolean for one use case. The SME added both `canAccessAperture` on the email type AND `seatEntitlements` on `HireSeat` for reuse.

**When to apply:** Any time you're checking HP permissions from a data fetcher — look for the entitlement on `seatEntitlements`, don't try to reverse-engineer it from `seatRoles` or `contractType`.

**Reference PRs:**
- hp-ep-api #916: Added `seatEntitlements` to Seat.proto
- ssr-data-service #7032: Consumed it in HireSeatDataFetcher + EmailHireProjectCollabInviteDataFetcher
- hire-comms-ssr-frontend #3495: Used `canAccessAperture` to drive email terminology
