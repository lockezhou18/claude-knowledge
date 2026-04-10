# Espresso Schema Change Workflow for talent-partner-integrations-mt

## The Key Pattern: Local Espresso Config Override

For E2E testing schema changes on rdev **before** they're in nuage, temporarily point the app at the local Espresso storage node:

Edit `config/app/talent-partner-integrations-mt/groups/qei.src` (**don't commit**):
```xml
<property name="espressoProtoClient.espressoClient.uriPrefix" value="http://localhost:11936"/>
```

This bypasses the D2/router path and connects directly to the storage node where manually registered schemas are available. Reference: [hp-collaboration-mt README](https://github.com/linkedin-multiproduct/hp-collaboration-mt/blob/master/README.md#how-to-deploy-against-the-local-espresso).

## Deploy Order (Critical)
1. Deploy Espresso standalone **first** (`mint deploy --product espresso-stand-alone`)
2. Register schemas via curl to port 11936
3. Deploy app **after** (`mint undeploy` then `mint deploy`) — app crashes if Espresso isn't running

## Schema Notes
- Forward-compatibility requires ALL older avsc versions to have the same enum symbols as the latest
- The `reinit` Gradle task is blocked by `IntegrationEvaluation` view type mismatch — use manual curl
- PR description format: use `# Problem & Solution Overview` / `# Testing Done` (h1, not h2)

### PR Pattern (following PR #129)
1. **PR 1 (Schema-only)**: Proto changes only (`IntegrationEntityType.proto`, key proto files)
   - Gets merged first, triggers nuage schema registration
   - Example: PR #586
2. **PR 2 (API changes)**: Java code + tests, based on PR 1 branch
   - Merged after schema is deployed to nuage
   - E2E write-path testing can happen after PR 1 is in nuage
   - Example: PR #587

## Rdev Deployment Steps

### 1. Set up rexec
```bash
rexec --assign-rdev talent-partner-integrations-mt/<rdev-name> echo "hello"
```

### 2. Build and deploy app
```bash
rexec 'cd ~/talent-partner-integrations-mt && ./gradlew build -x check'
rexec 'cd ~/talent-partner-integrations-mt && mint deploy --debug-app -f qei-ltx1'
```

### 3. Deploy Espresso standalone (separate step!)
```bash
rexec 'mint deploy --product espresso-stand-alone --version $(mint describe espresso-stand-alone --latest)'
```
App deploy does NOT deploy Espresso standalone. Must be done separately.

### 4. Register schemas (if nuage doesn't have them yet)
Order: DB → Document (all versions) → Table
```bash
rexec 'cd ~/talent-partner-integrations-mt/grpc-database/database/UnifiedIntegrationsDB && \
  curl -s -X PUT http://localhost:11936/schemata/db/UnifiedIntegrationsDB/1 --data-binary @schemata/db/UnifiedIntegrationsDB/1.json && \
  for v in 1 2 3 4 5 6; do curl -s -X PUT http://localhost:11936/schemata/document/UnifiedIntegrationsDB/IntegrationEntityToClientEntityMap/$v --data-binary @schemata/document/UnifiedIntegrationsDB/IntegrationEntityToClientEntityMap/$v.avsc; done && \
  curl -s -X PUT http://localhost:11936/schemata/table/UnifiedIntegrationsDB/IntegrationEntityToClientEntityMap/1 --data-binary @schemata/table/UnifiedIntegrationsDB/IntegrationEntityToClientEntityMap/1.json'
```

**IMPORTANT**: If adding new enum symbols, you must backfill ALL older avsc versions (v1-v5) with the full symbol set before registering. The `./gradlew build` step regenerates avsc from proto, overwriting patches. So:
1. Build first (regenerates avsc)
2. Patch avsc locally with Python
3. Sync to rdev
4. Register via curl

### 5. Set up gRPC tunnel
```bash
# In a separate terminal/tmux
rexec --tunnel 28288 -- 'cat'
```

### 6. Run grpcurli tests
```bash
# Proto reflection
grpcurli localhost:28288 describe <proto.message.Type>

# Read path
grpcurli --dv-auth SELF localhost:28288 <service>/FindBy... -d '{...}'

# Write path (requires schemas in nuage or successfully registered)
grpcurli --dv-auth SELF localhost:28288 <service>/Update -d '{...}'
```

## Key Ports (Espresso Standalone)

| Port  | Service          | Use                                    |
|-------|------------------|----------------------------------------|
| 11936 | Storage Node REST | Schema registration (`curl -X PUT`)   |
| 11965 | D2/Jetty admin   | Health check only (404 for schemas)    |
| 12924 | Router           | Data operations (app connects here)    |
| 12930 | MySQL            | Internal storage                       |

## Known Blockers

### `reinit` blocked by IntegrationEvaluation
The `IntegrationEvaluation` table has a pre-existing view type mismatch (`STRING` vs `UNION` for `integrationEvaluationUrn`). This blocks `./gradlew :grpc-database:database:UnifiedIntegrationsDB:reinit` from completing. Use manual curl registration instead.

### Local Espresso standalone (macOS)
Blocked by OpenSSL 1.1 dependency — the bundled MySQL binary requires `libssl.1.1.dylib` which is no longer available via Homebrew. Use rdev instead.

### `mint-integration testrun`
Requires `integ-test-config.json` which doesn't exist in this repo.

## Forward-Compatibility Patch Script
When adding new enum symbols, patch older avsc versions:
```python
import json
base = 'grpc-database/database/UnifiedIntegrationsDB/schemata/document/UnifiedIntegrationsDB/IntegrationEntityToClientEntityMap'
with open(f'{base}/6.avsc', 'r') as f:
    v6 = json.load(f)
for field in v6['fields']:
    if field['name'] == 'integrationEntityType':
        enum_type = field['type'][1]
        full_symbols = enum_type['symbols']
        full_symbolDocs = enum_type.get('symbolDocs', {})
        full_enumValueNumbers = enum_type.get('li.data.proto.enumValueNumbers', {})
        break
for v in [1, 2, 3, 4, 5]:
    path = f'{base}/{v}.avsc'
    with open(path, 'r') as f:
        schema = json.load(f)
    for field in schema['fields']:
        if field['name'] == 'integrationEntityType':
            et = field['type'][1]
            et['symbols'] = full_symbols
            et['symbolDocs'] = full_symbolDocs
            et['li.data.proto.enumValueNumbers'] = full_enumValueNumbers
    with open(path, 'w') as f:
        json.dump(schema, f, indent=2)
```
