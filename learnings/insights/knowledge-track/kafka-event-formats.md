---
id: know-012
track: knowledge
type: semantic
repos: [hp-ats-integration-mt]
tags: [kafka, avro, event, testing, phase2, connected-projects]
severity: medium
created: 2026-03-31
last_verified: 2026-03-31
use_count: 0
outcome_score: 0
status: active
rot_rate: medium
---

**When** producing Kafka test events for Phase 2 processors, **follow the exact Avro format conventions** because subtle format differences cause silent deserialization failures.

## Context

Two event types with different formats and clusters:

### IntegrationEntityReadyEvent (queuing cluster)
- Cluster: `queuing` (requires LDAP password — use tmux on shell host)
- `treeId`: can be `null` (unlike ExportStatusEvent)
- `operationType`: `avro.com.linkedin.events.unifiedintegration.IntegrationEntityOperationType` (note `avro.` prefix, NOT `proto.`)
- `guid`: fixed_16, exactly 16 bytes (e.g., `abcdefghijklmnop`)
- `messageId` in `KafkaAuditHeader`: also 16 bytes
- `memberIdV2`: present but usually `null`
- Has `EventHeader` wrapper with all standard tracking fields

### IntegrationExportRequestStatusEvent (tracking cluster)
- Cluster: `tracking` (no password, uses `kafka.tracking-local`)
- `treeId`: fixed_16, required (exactly 16 bytes)
- `guid`: fixed_16, exactly 16 bytes
- `messageId`: exactly 16 bytes (`0123456789abcdef`)
- `requestType`: `APPLICATION_STAGE` or `APPLICATION_DISPOSITION`
- `clientEntityUrn`: in `requestMetadata` (not top-level)
- Enum values: short form (`FAILURE`, not `ExportRequestRecommendedStatus_FAILURE`)
- `actor`: `null` — processor reads actor from HireEntityRequest

## Guidance

1. **Always consume 1 real event first** to verify the Avro format before producing test events:
   ```bash
   kafka-tool topic consume -f prod-ltx1 -c queuing -t IntegrationEntityReadyEvent --max-messages 1 --pretty-print
   ```
2. **Must SSH to shell host** for Kafka production (e.g., `ltx1-shell07.prod.linkedin.com`). Cannot produce from local Mac.
3. **Single-line JSON**: `echo '...' | kafka-tool topic produce -f prod-ltx1 -c queuing -t TOPIC`
4. **EI uses queuing cluster** for IntegrationEntityReadyEvent: `-c queuing -f ei-ltx1` (NOT tracking — tracking is for cross-fabric events like ExportStatusEvent)

## QEI Local Testing (Verified 2026-04-07)

1. **Cluster**: `IntegrationEntityReadyEvent` uses **queuing** cluster, NOT tracking. Use `-c queuing -f ei-ltx1`.
2. **`memberIdV2: null`** must be included in EventHeader after `actorUrn` — missing this causes `"Expected start-union. Got END_OBJECT"`.
3. **Kafka produce from Mac to EI works** — `kafka-tool topic produce -f ei-ltx1 -c queuing -t IntegrationEntityReadyEvent` (auth via Yubikey, cached after first use).
4. **Consumer starts at LATEST offset** — produce AFTER QEI deploy, not before.
5. **Middleware-created stages lack parent linkage** — stages created via `jobRequisitionStagesApi/update` with `RequestSource_MERGED` don't have `integrationJobRequisitionUrn` in IP's entity store. The processor rejects them. Only stages created via IP's internal sync flow have proper parent linkage.

### Working event template (EI queuing cluster)
```bash
python3 -c "
import json
event = {
    'header': {'com.linkedin.events.EventHeader': {
        'memberId': 0, 'viewerUrn': None, 'applicationViewerUrn': None, 'csUserUrn': None,
        'time': TIMESTAMP_MS, 'server': '', 'service': 'kafka-tool',
        'environment': {'string': 'ei-ltx1'},
        'guid': 'abcdefghijklmnop',
        'treeId': {'com.linkedin.events.fixed_16': 'ABCDEFGHIJKLMNOP'},
        'requestId': {'int': 0},
        'impersonatorId': None, 'version': None, 'instance': None, 'appName': None,
        'testId': None, 'testSegmentId': None,
        'auditHeader': {'com.linkedin.events.KafkaAuditHeader': {
            'time': TIMESTAMP_MS, 'server': 'test', 'instance': {'string': 'test'},
            'appName': 'kafka-tool', 'messageId': '0123456789abcdef',
            'auditVersion': {'int': 1},
            'fabricUrn': {'string': 'urn:li:fabric:ei-ltx1'},
            'clusterConnectionString': {'string': 'kafka.tracking.kafka.ei-ltx1.atd.disco.linkedin.com:16637'}
        }},
        'pageInstance': None, 'clientApplicationInstance': None, 'originSource': None,
        'sessionUrn': None, 'traceData': None,
        'clientMonitoringInstanceId': None, 'clientMonitoringInstanceEventNumber': None,
        'originalClientTime': None, 'clientGlobalSequenceNumber': None,
        'clientTopicLocalSequenceNumber': None, 'viewHierarchy': None,
        'isShadowEvent': None, 'actorUrn': None, 'memberIdV2': None
    }},
    'integrationEntityUrn': {'string': 'urn:li:integrationJobRequisitionStage:STAGE_ID'},
    'operationType': {'avro.com.linkedin.events.unifiedintegration.IntegrationEntityOperationType': 'UPDATE'},
    'integrationContext': {'string': 'urn:li:organization:1000'},
    'dataProvider': {'string': 'urn:li:developerApplication:1592055'}
}
print(json.dumps(event))
" > /tmp/event.json
cat /tmp/event.json | kafka-tool topic produce -f ei-ltx1 -c queuing -t IntegrationEntityReadyEvent
```

## When to Apply

When E2E testing any Phase 2 processor by producing Kafka events manually. Also when debugging "no events consumed" — the event may have been produced with wrong Avro format and silently dropped.
