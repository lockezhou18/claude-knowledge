# PR #584 E2E Testing Progress

## PR Info
- **PR**: https://github.com/linkedin-multiproduct/talent-partner-integrations-mt/pull/584
- **Branch**: `bizhou/add-hiring-project-candidate-history-urn-support`
- **Repo**: `/Users/bizhou/workspace/talent-partner-integrations-mt`
- **Reviewer request**: `svohra_LinkedIn` asked for curli testing details

## What the PR Does
Adds `HiringProjectCandidateHistoryUrn` support to `ClientEntityUrn` in talent-partner-integrations-mt. New enum `INTEGRATION_APPLICATION_STAGE_HISTORY = 9` in `IntegrationEntityType.proto`. Key maxsize bumped 150→300.

## What's Already Done

### Unit Tests: PASSING (100% coverage on changed lines)

### Read-path E2E (on old rdev rustic-mars): DONE
- Proto reflection: `hiringProjectCandidateHistoryUrn` field confirmed
- `FindUrnMappingByClientEntityUrn`: returned `{}` — full E2E success
- Production-sized URN finder: confirmed KEY_TOO_LONG at old maxsize, works at 300

### Write-path E2E: NOT YET COMPLETED
- Blocked by Espresso standalone schema issues (see below)

### Local avsc file patches: DONE
- v1-v5 avsc files patched with all 10 enum symbols for forward-compatibility
- Verified: all 6 versions have identical enum symbol sets
- **These patches are NOT committed** — they're local-only for Espresso standalone registration
- Files at: `grpc-database/database/UnifiedIntegrationsDB/schemata/document/UnifiedIntegrationsDB/IntegrationEntityToClientEntityMap/{1-6}.avsc`

## Key Technical Discoveries

### Espresso Standalone Ports (rdev)
- **11936** = Correct REST API port for schema registration (`curl -X PUT`)
- **11965** = D2/Jetty port (returns 404 for schema ops — WRONG for registration)
- **12924** = Router port
- **12930** = MySQL port

### Schema Registration via curl
Schemas must be registered in order: DB → Document (all versions) → Table
```bash
# DB schema
curl -s -X PUT http://localhost:11936/schemata/db/UnifiedIntegrationsDB/1 --data-binary @schemata/db/UnifiedIntegrationsDB/1.json

# Document schemas (v1-v6)
for v in 1 2 3 4 5 6; do
  curl -s -X PUT http://localhost:11936/schemata/document/UnifiedIntegrationsDB/IntegrationEntityToClientEntityMap/$v \
    --data-binary @schemata/document/UnifiedIntegrationsDB/IntegrationEntityToClientEntityMap/$v.avsc
done

# Table schema
curl -s -X PUT http://localhost:11936/schemata/table/UnifiedIntegrationsDB/IntegrationEntityToClientEntityMap/1 \
  --data-binary @schemata/table/UnifiedIntegrationsDB/IntegrationEntityToClientEntityMap/1.json

# Also register ClientEntityToIntegrationEntityMap (view table)
for f in schemata/document/UnifiedIntegrationsDB/ClientEntityToIntegrationEntityMap/*.avsc; do
  v=$(basename $f .avsc)
  curl -s -X PUT http://localhost:11936/schemata/document/UnifiedIntegrationsDB/ClientEntityToIntegrationEntityMap/$v --data-binary @$f
done
curl -s -X PUT http://localhost:11936/schemata/table/UnifiedIntegrationsDB/ClientEntityToIntegrationEntityMap/1 \
  --data-binary @schemata/table/UnifiedIntegrationsDB/ClientEntityToIntegrationEntityMap/1.json
```

### Why `reinit` Fails
1. `-x :grpc-database:build` causes sync step to silently skip (delete runs but sync doesn't)
2. Without `-x`, build regenerates avsc from proto, overwriting enum backfill patches
3. `IntegrationEvaluation` table has pre-existing view type mismatch that blocks `reinit` entirely

### The Update grpcurli (write-path test)
Must include `mappingMetadata` to bypass pre-existing NPE in `upsertWithInferredContextAndProvider()`:
```bash
grpcurli --dv-auth SELF localhost:28288 \
  proto.com.linkedin.talent.partner.integrations.IntegrationEntityUrnToClientEntityUrnMappingApi/Update \
  -d '{"value":{"integrationEntityUrn":{"integrationApplicationStageUrn":{"integrationApplicationStageId":"6501"}},"clientEntityUrn":{"hiringProjectCandidateHistoryUrn":{"hiringProjectCandidateUrn":{"hiringProjectUrn":{"hiringContext":"urn:li:contract:93003909","hiringProjectId":"9123204"},"hireIdentityUrn":{"hireIdentityId":"50106475"}},"historyId":111}},"mappingMetadata":{"integrationMetadata":{"integrationContext":{"organizationUrn":{"organizationId":"1000"}},"dataProvider":{"developerApplicationUrn":{"applicationId":"1592055"}}},"contractUrn":{"contractId":"93003909"}}}}'
```

## Current Rdev State
- **rustic-mars**: DELETED (schemas were wiped, rdev was deleted to allow rexec to switch)
- **curious-silver**: RUNNING but not yet deployed
  - Created ~5 hours before last session
  - State: RUNNING, Cluster: rdev-aks-wus3-11
  - Exposed ports: 28287→44012 (https), 80→43566 (file-server)
  - No gRPC tunnel set up yet
- **rexec**: Was pointing to rustic-mars. After `--reset`, tried to create new rdev (cancelled). Needs reconfiguration to point to curious-silver.

## Next Steps to Complete E2E Testing

1. **Configure rexec to use curious-silver**
   - May need `rexec --reset --rdev` and select curious-silver during onboarding
   - Or the auto-provisioned rdev from the cancelled reset may work

2. **Build and deploy on the rdev**
   ```bash
   rexec 'cd ~/talent-partner-integrations-mt && ./gradlew build -x check'
   rexec 'cd ~/talent-partner-integrations-mt && mint deploy --debug-app -f qei-ltx1'
   ```

3. **Manually register schemas via curl** (port 11936, see commands above)
   - The patched avsc files will be synced from local by rexec
   - Must register on a FRESH Espresso standalone (no pre-existing schemas)

4. **Set up gRPC tunnel**
   ```bash
   rexec --tunnel 28288 -- 'cat'
   ```

5. **Run all 5 grpcurli tests** (proto reflection, read finder, write Update, verify write, prod-sized finder)

6. **Update PR description** with complete E2E results

## Test Data (from EI_DATA_SUMMARY.md)
- Contract: `93003909`, Org: `1000`, DataProvider: `1592055`
- HiringProject: `9123204`, HireIdentity: `50106475`
- IntegrationApplicationStage: `6501`
- Seat: `97831119`
