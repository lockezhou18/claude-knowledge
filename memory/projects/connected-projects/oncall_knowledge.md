# Oncall Knowledge

## Deployment Commands

### talent-agent-nearline
Deploy from a prod shell host first:
```bash
ssh ltx1-shell07.prod.linkedin.com
```

Then deploy:
```bash
sp job deploy -p talent-agent-nearline -a <app-name> --nomination-check-skipped -f <fabric> -i i001 -v <version> --skip-cross-fabric-deploy-check
```

Example:
```bash
sp job deploy -p talent-agent-nearline -a hiring-intent-screening-project-question-processor --nomination-check-skipped -f prod-ltx1 -i i001 -v 0.0.1013 --skip-cross-fabric-deploy-check
```

Fabrics: `prod-lor1`, `prod-ltx1`, `prod-lva1`

### mcm-samza (Samza/Flink jobs)
Check version:
```bash
sp job status deploy -p mcm-samza -a <app-name> -f <fabric> -i i001
```

Restart:
```bash
sp job restart -p mcm-samza -a <app-name> -f <fabric> -i i001
```

Redeploy (if restart not available):
```bash
sp job deploy -p mcm-samza -a <app-name> -f <fabric> -i i001 -v <version> --nomination-check-skipped --skip-cross-fabric-deploy-check
```

Common app names:
- `hiring-activity-ingestion-approval-approver-response`
- `hiring-activity-hiringprojectcandidate`

### D2 Update Commands

#### hp-ats-integration-mt
```bash
lps d2 update -c HpAtsIntegrationMt -p hp-ats-integration-mt -f <fabric> --bypass-canary
```

#### mcm-mt
```bash
# REST
lps d2 update -f <fabric> -c McmServices -p mcm-mt --bypass-canary

# gRPC
lps d2 update -f <fabric> -c McmServicesGrpc -p mcm-mt --bypass-canary
```

#### hp-mt
```bash
# REST
lps d2 update -c HiringPlatformServices -p hp-mt -f <fabric> --bypass-canary --no_jetty_http2_check

# gRPC
lps d2 update -c HiringPlatformServicesGrpc -p hp-mt -f <fabric> --bypass-canary --no_jetty_http2_check
```

## EKG Override / Bypass

### Override EKG per deployment (recommended)
```bash
crt nominate -p <product> -v <version> -f <fabric> --promote-canary --policy-override-reason EKG_NON_BLOCKING_FAILURE
```

### Temporarily disable EKG rollback
```bash
crt preferences set -p <product> --ekg-rollback-enabled false
# Re-enable after deployment:
crt preferences set -p <product> --ekg-rollback-enabled true
```

### Pause EKG
```bash
crt pause -p <product> -f <fabric> --reason "reason"
# Resume after:
crt resume -p <product> -f <fabric>
```

### Delete deployment pause (UI)
https://crt.prod.linkedin.com/#/deployment/pauses?products=%5B%22<product>%22%5D

Example for ts-api: https://crt.prod.linkedin.com/#/deployment/pauses?products=%5B%22talent-solutions-api%22%5D

## EKG Rules

### mcm-mt EKG Rules
| Rule | ID | Link |
|------|----|------|
| mcm-mt (default) | 301657 | [View/Edit](https://engx.corp.linkedin.com/assets/urn%3Ali%3AekgRule%3A%28PROD%2C301657%29) |
| mcm-mt_sre (SRE) | 301257 | [View/Edit](https://engx.corp.linkedin.com/assets/urn%3Ali%3AekgRule%3A%28PROD%2C301257%29) |
| mcm-mt_custom (owner) | 330150 | [View/Edit](https://engx.corp.linkedin.com/assets/urn%3Ali%3AekgRule%3A%28PROD%2C330150%29) |

### EKG Management Links
- **CRT EKG Rules**: `https://crt.prod.linkedin.com/#/testing/ekg/rules?active=true&fabric=prod-ltx1&instance=i001&product=<product>`
- **Owner-Defined Rules**: `https://tools.corp.linkedin.com/apps/tools/ekg/ekg2/owner-defined-rules/#/rules?deployable=<product>&container=<product>`
- **EngX EKG Rules**: https://engx.corp.linkedin.com/ekg/rules

### Key rollback thresholds (default canary template)
- Error Rate: P50 > 5%
- Inbound Latency: P90 increase > 50% (200ms floor)
- CPU: avg > 95% or increase > 40%
- Plus: GC stalls, exception rate, warn rate, QPS change, memory

## ACL / Deployment Permissions

### Check who can deploy a multiproduct
```bash
acl-tool role_membership find --resource-urn urn:li:multiProduct:<mp-name>
```

### Grant deployment access (DEVELOPMENT_TEAM)
```bash
acl-tool role_membership create --actor <SGP-ENG-group> --resource-urn urn:li:multiProduct:<mp-name> --role DEVELOPMENT_TEAM
```
- Only `SGP-ENG` or `SGP-TEAM` groups allowed (not individual users)
- Must be `RESOURCE_ADMIN` on the resource to run this
- If 403 Forbidden, try via SSH proxy: `ssh -t eng-portal.corp.linkedin.com ssh lor1-shell01.prod.linkedin.com -t acl-tool ...`

### Check what groups a user belongs to
```bash
acl-tool role_membership find --actor <username>
```

### Check current prod deployment version
```bash
go-status -f prod-ltx1 -a <app-name>
```

### Compare commits between versions
```bash
gh api repos/linkedin-multiproduct/<mp-name>/compare/v<old>...v<new> --jq '.commits[] | {author: .commit.author.name, message: .commit.message | split("\n")[0]}'
```

## Dashboards

### Hiring Platform Pipeline Dashboard (Azure Data Explorer)
- **URL**: https://dataexplorer.azure.com/dashboards/4f5cd8b2-9c1f-4229-9083-236ca49b25d3?p-_startTime=1hours&p-_endTime=now&p-_productName=v-Hiring+Platform+-+Pipeline&p-_clientApplicationUrn=all&p-_platform=v-Web&p-_fabrics=all&p-_aggregationWindow=v-1h&p-_oopsPageKeys=all#810282be-7738-4b74-a48f-1adb3a73f48f
- Shows pipeline metrics for Hiring Platform (errors, latency, QPS)
- Filterable by product, fabric, time range, aggregation window, client app, platform
- Super helpful for oncall triage and investigating pipeline issues

## Shell Hosts
- **Prod**: `ltx1-shell07.prod.linkedin.com`
- Requires VPN connection
