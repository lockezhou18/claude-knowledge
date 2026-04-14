---
id: know-036
track: knowledge
type: semantic
repos: 
tags: 
severity: high
rot_rate: slow
status: active
created: "2026-04-03"
last_verified: "2026-04-03"
use_count: 1
outcome_score: 0
---

# Kafka/Xinfra Mental Model — LinkedIn's Streaming Stack

## The Full Stack (7 Layers)
```
TrackerProcessorCallback (your code)
  → TrackerProcessor (callback orchestrator, IC propagation, health sensors)
    → TrackingConsumer (Avro-native, schema registry)
      → Xinfra Consumer (broker-agnostic: Kafka OR Northguard)
        → LiKafkaConsumer (large message chunking >1MB)
          → Apache Kafka Consumer
            → Kafka Brokers OR Northguard Brokers (C++)
```

## Xinfra = Virtualized Pub-Sub
Abstracts Kafka vs Northguard behind unified `Consumer<K,V>` / `Producer<K,V>`.
- **XMD**: global topic namespace
- **Conductor**: consumer group management, offset storage
- Migration is config-only: `kafkaConsumer.useXTrackingConsumer=true`

## Northguard = Kafka Replacement (C++)
- Key-range sharding (not partitions), Raft consensus (no ZK), no GC pauses
- 99.9% SLA, exited Code Yellow June 2023
- Consumer migration active FY25H1

## 5 Cluster Types
| Type | Scope | Use |
|------|-------|-----|
| Queuing | Within-fabric only | Service-to-service (IntegrationEntityReadyEvent) |
| Tracking | Cross-fabric (aggregated) | Analytics, cross-DC (ExportStatusEvent) |
| Data Deployment | CORP→all prod | Offline→online (ML models) |
| Aggregate | All DCs merged | Cross-DC consumption |
| QEI | ACL-free | Testing |

## TrackerProcessor Pattern
Implement `TrackerProcessorCallback<T>`, wire via `TrackerProcessorFactory.Overrides` + `TopicProcessors.createSingleTopicProcessor()`. Boot listener needs `@Import` + `getBean` (NO `registerBean` for consumers). Missing any = silent failure.

## MultiColoFilter — Cross-DC Dedup
Range-based entity partitioning. `isActive(entityId)` = true for exactly one DC. Config-driven via `env.specific.multiColoFilter.rangeAssignments`.

## LiKafka Large Message Support
Producer chunks >1MB into `LargeMessageSegment`s. Consumer `MessageAssemblerImpl` reassembles. Transparent to application code.

## Brooklin = CDC + Cross-DC Mirroring
1. Espresso/MySQL changes → `LiDatastreamEvent` → Kafka topics (`prod_dbchanges_<DB>.<Table>`)
2. Cross-DC: local cluster → aggregate cluster via Brooklin Mirror Maker

## Key Design Decisions
- Log-compacted topics = anti-pattern (being migrated away)
- IC propagation through Kafka via `ServiceCallTrackerProcessorCallback` (treeId, guid)
- Samza for stream processing (dead-end — Flink is future, `flink-li-framework` exists)

## Operational Tooling
- Nuage (topics/ACLs), LagMonitor (lag), Reflection (debug UI), kafka-tool (CLI)
- Oncall: kafka-sre, kafka-services-dev, xinfra-conductor-dev, northguard-dev
- Slack: #kafka, #xinfra-clients, #northguard

## Industry Comparison
- LinkedIn leads: unified ecosystem, Xinfra abstraction, MultiColoFilter, IC propagation
- LinkedIn lags: Samza (use Flink), no cloud elasticity, slow state recovery, basic event-time, no tiered storage, no standard DLQ
- If cloud: AutoMQ > WarpStream (latency). For processing: Flink > Samza (ecosystem 50x).
