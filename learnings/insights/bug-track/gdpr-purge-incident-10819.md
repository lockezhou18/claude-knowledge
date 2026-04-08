---
id: bug-004
track: bug
type: episodic
repos: ["*"]
tags: [incident, sev1, gdpr, espresso, data-deletion, oncall]
severity: critical
created: 2026-03-28
last_verified: 2026-03-28
use_count: 1
outcome_score: 1.0
status: active
rot_rate: medium
---

## When GDPR purge spikes cause widespread Espresso deletions, check HP impact via Trino CDC tables

### Situation
incident-10819 (SEV1): GDPR purger bug stripped URN type when extracting owner IDs, causing company URNs to be treated as member deletions. ~10M+ records deleted across 64 data stores. $170K/day revenue loss.

### HP Impact Assessment Method
1. Run Trino queries against `prod_dbchanges_<db>.<table>` filtering for `operation = 'DELETE'`
2. Compare delete counts across 2-3 week window to identify surge
3. Filter by `auditheader.appname = 'brooklin-service'` for purge-specific deletes
4. Also check WITHOUT the appname filter to catch all deletion sources

### HP Results
- MultichannelManagement.SourcingChannelCandidatesV2: NOT impacted (0 deletes after 3/24)
- HireAccessControlDB.RoleAssignment: NOT impacted (6 total, all on 3/23)
- ResumesSearchDB.UniqueResumeVisibilities: IMPACTED (17.8x surge, 42.6M net new deletes)
- ResumesSearchDB.UniqueResumes: IMPACTED (15.7x surge, 2.9M net new deletes)

### Key Learnings
- ResumesSearchDB is on ESPRESSO_STICKYROUTING cluster, not MD-2
- ResumesSearchDB tables are actively used by recruiter-search-mt, hire-federated-search-backend, resumes-search-dedup-jobs
- Recovery via Espresso bulk PUT restore from Lumos snapshots (incident team handles centrally)
- Check the incident spreadsheet for assigned tables — may be different from core HP tables
