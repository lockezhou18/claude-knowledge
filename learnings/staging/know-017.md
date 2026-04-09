---
id: know-017
track: knowledge
type: semantic
repos: ["hp-ats-integration-mt", "*"]
tags: ["espresso", "nosql", "database", "infrastructure", "mysql", "partitioning", "replication", "schema"]
severity: high
created: "2026-04-02"
last_verified: "2026-04-02"
use_count: 0
outcome_score: 0
rot_rate: slow
status: active
---

## Espresso Mental Model — LinkedIn's Distributed NoSQL Database

**When** working with Espresso-backed services (hp-ats-integration-mt, mcm-mt, or any LinkedIn service), understand these fundamentals.

### What It Is

Distributed, fault-tolerant NoSQL document store **built on MySQL/InnoDB**. Stores JSON documents with hash-based partitioning and automatic failover. Powers most LinkedIn online data — user profiles, messaging, hiring data.

### Architecture

```
App → Espresso Client (espresso-pub)
  → Router (port 12921, stateless, hash-routes by partition key)
  → Storage Nodes (MySQL/InnoDB per partition)
  → Apache Helix (cluster management, master election, failover)
```

### Core Concepts

| Concept | What it means |
|---------|---------------|
| **Database** | Logical container (like MySQL DB). Created via Nuage. |
| **Table** | Collection of documents within a DB |
| **Partition Key** | Determines which shard stores the document. Hash-based. |
| **SCN** | System Change Number — monotonic clock per partition for ordering |
| **Router** | Stateless proxy — hashes key, routes to correct storage node |
| **Helix** | Cluster manager — partition assignment, master election, auto-failover |

### Consistency Model

| Scope | Guarantee |
|-------|-----------|
| Within partition | **ACID** (MySQL transactions). `TxMultiPut` = all-or-nothing. |
| Cross-partition | **No transactions** — each partition independent |
| Cross-datacenter | **Eventual** — async replication via Kafka CDC |

### Day-to-Day Working Patterns

**Create a database:**
```
Nuage UI → + Create → Espresso → DEV fabric first
Then promote: DEV → EI → PROD
```

**Schema changes:** Avro-based evolution. Safe: add fields with defaults, remove optional fields. Breaking: remove required, narrow types → needs new version.

**Client usage (Java):**
```java
// Sync
GetRequest req = new GetRequest.Builder()
    .setDatabase("myDb").setTable("myTable").setKey("key-123").build();
client.get(req, callback);

// Async (ParSeq)
Task<GetResponse> task = parseqClient.execute(getRequest);

// Multi-colo write
client.putMultiColo(putRequest, Set.of("ltx1", "lor1", "lva1"), callback);

// Transactional batch (WITHIN same partition only)
client.execute(new TxMultiPutRequest(putA, putB));
```

**Testing:**
```java
@ExtendWith(EspressoTestExtension.class)
class MyTest {
    @Test
    void test(EspressoTestClient client) {
        client.put("testDb", "users", "user-1", document);
        byte[] result = client.get("testDb", "users", "user-1");
    }
}
```

### Common Gotchas (from real experience)

1. **KEY_TOO_LONG** — InnoDB index key length limit. Composite keys with long URNs exceed it. hp-ats-integration-mt hit this: CandidateHiringState mapping can't persist via UPDATE → processor always takes CREATE path.

2. **Transactions are partition-scoped** — `TxMultiPut` only works within ONE partition. Cross-partition = no transaction guarantee.

3. **Materialized Views being decommissioned** — ALL MV use cases must migrate to Euler GLAI. No new MVs accepted.

4. **HikariCP maxLifetime** — LinkedIn defaults to 150s (vs HikariCP default 30m). Pool sizing: `connections × RPS × avg_query_time × safety_factor`.

5. **Promotion workflow stuck** — Nuage promotions can hang. Check workflow status at Nuage UI, escalate via #nuage-experience-team.

6. **Schema validation 422** — Validate Avro locally before registering. Common: invalid Avro, incompatible evolution, missing version.

### HP Services Espresso Usage

| Service | Database | What's stored |
|---------|----------|---------------|
| hp-ats-integration-mt | HiringPlatformIntegrationDB | Entity mappings (HP ↔ IP), stage mappings |
| mcm-mt | HiringContextDB | HiringProjects, HiringProjectCandidates, CandidateHiringStates |
| hire-access-control | HireAccessControlDB | Entitlements, HiringProjectPreferences |
| Euler (HireEntityRequest) | EDB managed by Euler | HireEntityRequest entities (write-back tracking) |

### Operational Tools

| Tool | Purpose |
|------|---------|
| Nuage UI | Create/promote DBs, manage schemas |
| Espresso Athena | Partition health dashboards |
| `espresso-gui` | macOS GUI client for browsing data |
| `espresso-utilities` | SRE toolbox |
| Espresso Pretzel | Database migrations (replaces Flyway) |

### Espresso vs Alternatives — When to Use What

| | **Espresso** | **Venice** | **TiDB** | **MongoDB** | **DynamoDB** | **Cassandra** |
|--|-------------|-----------|---------|------------|-------------|--------------|
| **Model** | Document (JSON) | Key-value | Relational SQL | Document (BSON) | Key-value/Document | Wide-column |
| **Built on** | MySQL/InnoDB | Kafka+RocksDB | TiKV (Raft) | WiredTiger | Proprietary (AWS) | LSM-tree |
| **Consistency** | ACID per partition | Eventual | Full ACID distributed | Single-doc atomic | Configurable | Tunable (QUORUM) |
| **Best for** | Online CRUD, user data | ML feature serving, read-heavy | Complex SQL, distributed txn | Flexible schema, rapid dev | Serverless, AWS-native | Write-heavy, time-series |
| **Latency** | Low (online) | Sub-ms (DaVinci) | Medium (distributed) | Low-medium | Low (single-digit ms) | Low-medium |
| **Query** | Key + secondary idx | Key only | Full SQL | Rich query language | Key + GSI + PartiQL | CQL (SQL-like) |
| **Transactions** | Partition-scoped | None | Cross-shard ACID | Multi-doc (4.0+) | Single-item or txn API | Lightweight txn (LWT) |
| **Scaling** | Hash partition | Kafka partitions | Auto-shard (TiKV) | Sharding (manual/auto) | Auto (on-demand) | Ring-based |
| **LinkedIn use** | Primary online store | Derived data, recommendations | GLAI indexes (Euler) | Not used | Not used | Not used |

### For Personal Infra — Key Takeaways

| Espresso Pattern | Self-hosted Equivalent |
|-----------------|----------------------|
| Hash partitioning | MongoDB sharding or CockroachDB auto-sharding |
| MySQL/InnoDB underneath | Vitess (MySQL-compatible distributed) or PlanetScale |
| Avro schema evolution | MongoDB schema validation or Protobuf + schema registry |
| Nuage for DB management | Terraform + Helm charts for DB provisioning |
| Espresso CDC → Kafka | MongoDB Change Streams or Debezium CDC |
| Partition-scoped txn | CockroachDB or TiDB for distributed transactions |

**If starting fresh for personal infra:**
- **Simple CRUD + flexibility**: MongoDB or PostgreSQL (most versatile)
- **Need distributed transactions**: CockroachDB or TiDB
- **Write-heavy + time-series**: ScyllaDB (Cassandra-compatible, better performance)
- **Serverless/managed**: DynamoDB (AWS) or Firestore (GCP)
- **MySQL-compatible + distributed**: Vitess or PlanetScale

### Ownership
- **Team**: DDS (Distributed Data Systems)
- **Slack**: #espresso
- **Nuage**: https://nuage.prod.linkedin.com
