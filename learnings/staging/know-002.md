---
id: know-002
track: knowledge
repos: [hp-ats-integration-mt, talent-partner-integrations-mt]
tags: [espresso, key-size, workaround, mapping, history]
severity: medium
created: 2026-03-25
last_verified: 2026-03-25
use_count: 1
outcome_score: 1
status: active
rot_rate: medium
---

**When** IP Espresso KEY_TOO_LONG blocks entity mapping writes for HiringProjectCandidateHistoryUrn (~175 chars, maxsize 150), **use** shortened URN with placeholder zeros for contractId/projectId/identityId **because** historyId is globally unique and the other fields are redundant for the mapping key.

## Key Details
- Full URN: 175-178 chars (over 150 limit)
- Shortened URN with zeros: exactly 150 chars
- Lix-gated: `talent.shortened.history.urn.mapping.key.enabled`
- ESPENG-57173 pending — remove workaround once maxsize bumped to 300
- Write AND read paths verified with prod IP Espresso grpcurli calls
