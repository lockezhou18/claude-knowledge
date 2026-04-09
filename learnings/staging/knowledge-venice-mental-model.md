---
id: knowledge-venice-mental-model
track: knowledge
repos: [mcm-mt, hp-ats-integration-mt, talent-partner-integrations-mt, talent-solutions-api]
tags: [venice, derived-data, storage, infrastructure, ml-features, embeddings]
severity: low
created: "2026-04-03"
last_verified: "2026-04-03"
use_count: 0
outcome_score: 0
status: active
rot_rate: slow
paths: []
---

# Venice — LinkedIn's Derived Data Store

## What It Is
Venice is LinkedIn's distributed key-value store for serving **precomputed/derived data** with sub-ms read latency. NOT a source of truth — that's Espresso. Venice serves the derived version of truth (ML features, embeddings, recommendations, denormalized views).

## When to use Venice vs Espresso
- **Venice**: Precomputed data, read-heavy (>1000:1), batch+streaming writes via Kafka, eventual consistency
- **Espresso**: Source of truth, CRUD, read-your-writes consistency, direct transactional writes

## Core Concepts
- **Store**: Named key-value dataset (Avro schema). Three types: batch-only, streaming-only, hybrid (most common)
- **Push Job (VPJ)**: Batch write from Hadoop/Spark → Kafka → atomic version swap
- **Hybrid Store**: Merges batch + streaming writes at WRITE time (not read time like Lambda)
- **DaVinci Client**: Local RocksDB, <1ms SSD — makes your app stateful (NSS deployment)
- **Thin Client**: App → Router → Server, ~10ms P99 — simplest setup
- **Fast Client**: App → Server directly, lower latency than thin

## HP Service Usage
| Service | Role | Store(s) |
|---|---|---|
| mcm-mt | READ | `EnterpriseJobSJFEmbeddings`, `HiringPlatformIntegrationJobRequisitionEmbeddings` (job embeddings for similar project matching) |
| talent-solutions-api | READ | Job Distribution Feed store (ATS Job Feed feature) |
| talent-partner-integrations-mt | READ+WRITE | `HsJobRequisitionToHiringProjectBiMap` (bidirectional job req ↔ hiring project mapping) |
| hp-ats-integration-mt | Config only | Changelog consumer config exists but no Java code (unused CDC setup) |
| hire-access-control | Config only | No active usage |

## Key Gotchas
- First push after enabling hybrid MUST be full (not incremental)
- Key schemas are immutable — must delete+recreate store to change
- Partition count immutable once hybrid — plan upfront
- Samza system name must be `"venice-0"` NOT `"venice"` (silent failure)
- Batch get max 150 keys on generic clusters (HTTP 413 if exceeded)
- Online write read-after-write latency ~30 min max — not for consistency
- Stores >250GB need Venice team review + `go/hwforecast`
- ACL save in Nuage is full replacement (not incremental)

## Ownership & Resources
- **Team**: Venice Crew (ODI), Crew ID 1120
- **Slack**: `#venice`
- **Go-links**: `go/venice`, `go/nuage`, `go/venice-store-create`
- **Open Source**: Apache Incubating — venicedb.org
