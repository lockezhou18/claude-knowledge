---
name: Check knowledge/memory BEFORE trial-and-error
description: Agent must search learnings and memory files before attempting unfamiliar operations — especially Kafka, Avro, and infrastructure tasks
type: feedback
---

When facing an unfamiliar operation (Kafka event production, Avro schema, infrastructure config), **search the knowledge files FIRST** before attempting trial-and-error.

**Why:** On 2026-04-07, we spent ~1hr fighting Avro schema issues for IntegrationEntityReadyEvent. The user said "check repo knowledge/memory" and we immediately found `memberIdV2` (the missing field) and the correct cluster (`queuing` not `tracking`). The answer was in `kafka-event-formats.md` and `ei-testing-patterns.md` the entire time.

**How to apply:**
- Before ANY Kafka produce/consume: search learnings for the topic name
- Before ANY Avro event construction: search for existing templates
- Before ANY infrastructure operation: check if there's a knowledge file about it
- When multiple knowledge files conflict: cross-validate against the code (e.g., check which cluster the consumer config actually uses)
- This is Phase 1 Research Layer 1 in the engineering pipeline — "Search past learnings FIRST"
