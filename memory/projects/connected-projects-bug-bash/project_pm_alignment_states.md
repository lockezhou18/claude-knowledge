---
name: PM Alignment - Candidate Movement History States
description: PM alignment with Tara (2026-02-18) on Phase 2 candidate movement states - only 3 HP states, inbound history dedup, outbound multi-request handling
type: project
---

PM sync with Tara Iyer on 2026-02-18 established these Phase 2 candidate movement behaviors:

1. **Inbound (ATS → LinkedIn)**: Charter release shows ONE history record if the target state is the same. Full movement records is P1, blocked on IP application stage table redesign.

2. **Outbound (LinkedIn → ATS)**: If multiple requests target the same stage movement, once IP confirms success, ALL requests marked successful. Future redesign (with IP) to tie one request to one stage movement.

3. **HP States**: Only 3 states — SUCCESS, TIMEOUT_FAILURE, GENERAL_FAILURE. CONFLICT state removed (intermediate, won't display in UI).

**Why:** Simplifies charter scope. CONFLICT was an intermediate state that added UI complexity without user value. Deduping inbound history avoids confusing duplicate records.

**How to apply:** Test cases should validate these 3 states only. Do not test for CONFLICT/MISMATCH in charter. Inbound sync tests should verify deduplication (one record per target state).
