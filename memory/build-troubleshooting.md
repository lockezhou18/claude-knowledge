# Build & Config Troubleshooting

## ConfigCompilationException: "Cannot resolve app-def default value"

When `mint build-cfg`, `mint run-local`, or `mint qprodRun` fails with errors like:
```
ConfigCompilationException:
Cannot resolve app-def default value missing from <beanName>.<property>
```

**Root cause**: New beans introduced by dependency upgrades that need config values in `application.src`.

**How to resolve**:
1. Search Slack for the key part of the error message. E.g. search: `Unable to compile configs, please fix configs errors: d2`
2. Check team channels (e.g. #talent-solutions-api-dev or relevant infra channels) for recent discussions
3. Example: https://linkedin-randd.slack.com/archives/C08AL2PMGNQ/p1754427593259009
4. Often the fix is `mint update` to pull latest dependency versions that include the config fixes
5. If `mint update` doesn't help, add missing properties to `config/app/<app>/application.src` following existing patterns for similar beans

**Pattern for finding the right config values**:
- For `TrackingProducerFactory` beans: copy pattern from existing `TrackingClient.trackingProducer.*` entries
- For `D2ClientFactory` / `zkHosts`: use `${__r2d2DefaultClient__.r2d2Client.zkHosts}`
- For `VeniceClient`: check existing Venice client entries nearby
