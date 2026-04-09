---
name: Espresso Metrics — HireAccessControlDB Cluster Name
description: HireAccessControlDB Espresso metrics are indexed under cluster name MD-2, not the database name
type: reference
---

Espresso metrics for **HireAccessControlDB** are published under the cluster name **MD-2**, not the database name.

**Why:** Espresso metrics are organized by cluster, not by logical database name. The cluster name and the database name differ for this DB.

**How to apply:** When querying Espresso metrics dashboards (Observability, Grafana, etc.) for HireAccessControlDB, filter/search by cluster `MD-2` rather than `HireAccessControlDB`.
