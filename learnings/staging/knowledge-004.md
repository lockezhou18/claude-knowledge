---
id: knowledge-004
track: knowledge
type: semantic
repos: ["*"]
tags: [espresso, metrics, observe, monitoring, oncall]
severity: medium
created: 2026-03-28
last_verified: 2026-03-28
use_count: 1
outcome_score: 1.0
status: active
rot_rate: medium
---

## When checking Espresso table metrics, search by cluster name not just DB name

### Context
Espresso metrics are keyed by cluster name (e.g., ESPRESSO_MT-MD-2, ESPRESSO_STICKYROUTING), not database name. Different databases live on different clusters.

### Guidance
- HireAccessControlDB → cluster `ESPRESSO_MT-MD-2`
- ResumesSearchDB → cluster `ESPRESSO_STICKYROUTING`
- RRD pattern: `espresso-router/espresso-router.i001.Traffic_Checker_Table_Stats.TrafficCheckerTableStats_<CLUSTER>.<DB>-<Table>_TableTotalCallCount.rrd`
- Base document tables may not have their own metrics — traffic is tracked on versioned secondary index tables (e.g., RoleAssignmentsV3 not RoleAssignment)
- Read/Write trackers: `EspressoRouterSensor_<CLUSTER>_<DB>_ReadCallTracker.CallCountTotal.rrd`
- Use observe-agent to discover the correct cluster: "Search for ALL available Espresso metrics containing '<DB>' in the RRD name"

### When to Apply
- Verifying Espresso table health during incidents
- Checking RCU/WCU for quota monitoring
- Investigating data deletion impact (e.g., GDPR purge incidents)
