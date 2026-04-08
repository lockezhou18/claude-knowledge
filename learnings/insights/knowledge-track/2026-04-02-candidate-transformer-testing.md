---
id: know-014
track: knowledge
type: semantic
repos: ["hp-ats-integration-mt"]
tags: ["ei", "testing", "candidate", "identity", "v2", "member", "transformer", "connected-projects"]
severity: medium
created: "2026-04-02"
last_verified: "2026-04-02"
use_count: 0
outcome_score: 0
rot_rate: slow
status: active
paths: ["**/CandidateProcessor.java", "**/CandidateTransformer.java"]
---

## Candidate Transformer Test Scenarios (from EI E2E Testing)

**When** testing candidate sync (CandidateProcessor/CandidateTransformer), verify these scenarios:

### Test Scenarios

1. **Create candidate without member** — New IntegrationCandidate with no `manualMatchedMember`
   - Creates: candidateProfile hireIdentityV2
   - Does NOT create member identity
   - Verify: `hireIdentitiesV2?q=relatedHireIdentity` shows 1 identity (candidateProfile only)

2. **Create candidate with member** — IntegrationCandidate with `manualMatchedMember` set
   - Creates: candidateProfile hireIdentityV2 + member hireIdentityV2 in same group
   - Verify: group has 2 identities (candidateProfile + member)

3. **Add member to existing candidate** — `$set manualMatchedMember` on existing atsCandidates
   - Adds member identity to existing group
   - CandidateProfile identity unchanged
   - Verify: group now has 2 identities

4. **Remove member** — `$delete manualMatchedMember`
   - Removes member from group
   - CandidateProfile identity persists (NOT deleted)
   - Verify: group back to 1 identity

5. **Re-add different member** — Set new `manualMatchedMember`
   - Old member removed, new member added
   - CandidateProfile identity unchanged
   - Verify: group has 2 identities (candidateProfile + new member)

6. **Unmatched member** — Member ID that doesn't resolve
   - Logs warning but doesn't fail
   - CandidateProfile still created

### Key Insight for Phase 2

The V2 identity group structure is critical for ActionWriteBack:
- **ApplicationProcessor** creates entity mappings using `candidateProfileIdentityUrn` (V2)
- **ConnectedProjectCandidateService** resolves V1 → V2 to find the mapping
- If the candidate has multiple V2s in the group, the fallback logic (PR #524) tries each V2

**When debugging "No IntegrationApplicationStage mapping found":**
1. Check the V2 group: `hireIdentitiesV2?q=relatedHireIdentity`
2. Check which V2 has the mapping: try each V2 in `FindByHiringEntity`
3. The mapping is always on the `candidateProfile` V2, not the member V2
