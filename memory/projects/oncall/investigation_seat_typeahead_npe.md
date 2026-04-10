---
name: CSE Seat Typeahead NPE Investigation
description: NPE in hire group typeahead caused by seatsV2 migration lix — traced from ts-web GraphQL through SeatServiceImpl to SeatsV2Client
type: project
---

## CSE-22367: Unable to Add Member to Project (Typeahead NPE)

**NOT the same as ENT-35609** (stale HS index). ENT-35609 was a cross-colo HS index inconsistency fixed by index rebuild on Feb 12.

**Actual root cause:** NPE in `SeatsV2Client.findByAttributes()` at line 167 — a null element in the seatsV2 response causes `DirectArrayTemplate.add()` → `ArgumentUtil.notNull()` to throw.

**Call chain:**
```
ts-web GraphQL: hireGroupTypeaheadResultsByText
  → ts-api HireGroupTypeaheadResultResource (finder: text)
    → HireGroupTypeaheadResultServiceImpl.findByText()
      → SeatServiceImpl.findBySearch()
        → SeatServiceImpl.fetchSeatsFromSeatsV2TextQuery() ← NEW PATH
          → SeatsV2Client.findByAttributes() ← NPE here
```

**Regression:** Error went from 0 to 7,035/day starting 2026-03-23. Caused by lix ramp of `talent-solutions-api.seat.search.direct.seatsv2.enabled` (PR #8492 by tdamera).

**Lix:** `talent-solutions-api.seat.search.direct.seatsv2.enabled`
**PR:** https://github.com/linkedin-multiproduct/talent-solutions-api/pull/8492
**MP:** talent-solutions-api

**Key learning:** Initial investigation went down wrong path (auth/contractUrn null). The actual stacktrace from observe agent with treeId was critical — it showed the NPE was in `SeatsV2Client.findByAttributes` stream processing, not in ViewerService. Always get the full stacktrace before theorizing.

**Why:** Lix cleanups and migrations in ts-api are frequent. When investigating new errors, check error trends first to identify regressions vs chronic issues.

**How to apply:** For typeahead-related CSEs, check if `seat.search.direct.seatsv2.enabled` lix is involved. Deramping the lix is the immediate mitigation.
