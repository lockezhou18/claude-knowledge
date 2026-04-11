---
name: V2 Identity findFirst() Bug
description: When multiple V2 candidate-profile identities exist in a group, findFirst() picks the wrong one. Always try all V2s with fallback.
type: reference
id: bug-001
status: graduated
tags: [identity, v2, hp-ats-integration, gotcha, findFirst, mapping]
repos: [hp-ats-integration-mt]
---

## When [situation]
Working with HireIdentity V2 lookups in hp-ats-integration-mt where a candidate has multiple V2 identities in the same identity group.

## Do [action]
Never use `findFirst()` on V2 identity streams. Instead, try ALL V2 identities with fallback — iterate through the group and attempt each one until one succeeds.

## Because [reason]
`findFirst()` is non-deterministic when multiple V2s exist in a group. It can pick a V2 that doesn't have the expected mapping, while another V2 in the same group does. This caused silent failures in stage sync and writeback flows (PR #524).

**Graduated from:** insights/bug-track (bug-001), use_count=3, outcome_score=3
