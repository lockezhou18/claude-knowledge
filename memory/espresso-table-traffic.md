---
name: Espresso Table Traffic Metrics
description: How to find per-table read/write traffic for any Espresso table using server-side router metrics
type: reference
---

## How to Find Espresso Table-Level Traffic

**Use server-side Espresso Router metrics** — no client config changes needed.

### Observe Metrics Explorer
- **URL**: https://observe.prod.linkedin.com/metrics-explorer
- **Application**: `espresso-router`
- **Fabric**: `prod`, **Multifabric**: `Yes`

### RRD Naming Pattern
```
espresso-router/espresso-router.i001.Traffic_Checker_Table_Stats.TrafficCheckerTableStats_ESPRESSO_<CLUSTER>.<DB>-<TABLE>_<MetricType>.rrd
```

**IMPORTANT**: Note the `.` (dot) between cluster and DB name, and `-` (dash) between DB and table name.

### Metric Types
- `TableTotalCallCount` — total calls (internal + external)
- `TableExternalTotalCallCount` — external calls only

### Example
For table `SourcingChannelCandidatesV2` in DB `MultichannelManagement` on cluster `MT-LD-2`:
```
espresso-router.i001.Traffic_Checker_Table_Stats.TrafficCheckerTableStats_ESPRESSO_MT-LD-2.MultichannelManagement-SourcingChannelCandidatesV2_TableTotalCallCount.rrd
```

### Search Tip
In Metrics Explorer, search for:
```
TrafficCheckerTableStats_ESPRESSO_<CLUSTER>.<DB>-<partial-table-name>
```

### Client-Side Alternative (requires code change)
If you need client-side per-table metrics (latency, RCU/WCU), enable `emitTableCallStats` in the Espresso client config. This is opt-in and requires espresso-pub >= 55.0.12. But for traffic volume, the router-side metrics above are sufficient and require no code changes.

### Gotcha: Cluster naming
- Client-side metrics use `_` separator: `ESPRESSO_MT-LD-2_MultichannelManagement`
- Router-side metrics use `.` separator: `ESPRESSO_MT-LD-2.MultichannelManagement`
- The earlier attempt with `_` returned null — the `.` is critical.

### Related
- Espresso DB-level metrics are under `Espresso_Client_Sensor` on the client app (e.g., `mcm-mt`)
- HireAccessControlDB metrics are under cluster `MD-2` (not the DB name)
