# Development Process Notes

## PR Descriptions
- Always include full grpcurli commands and raw output in E2E testing sections
- Use `# Problem & Solution Overview` / `# Testing Done` (h1 headers) for talent-partner-integrations-mt PRs

## Rdev Deployment
- Run `mint undeploy` before `mint deploy` to avoid `boot-listeners.txt` classpath issues
- Deploy Espresso standalone **before** the app when using local Espresso config
- Use `rexec --assign-rdev <mp>/<rdev-name>` to point rexec at a specific rdev

## Local Espresso Testing on Rdev
- Point app at storage node directly: `espressoProtoClient.espressoClient.uriPrefix` → `http://localhost:11936` in `qei.src` (don't commit)
- Register schemas via curl: DB → Document versions → Table, in order
- Reference: [hp-collaboration-mt README](https://github.com/linkedin-multiproduct/hp-collaboration-mt/blob/master/README.md#how-to-deploy-against-the-local-espresso)

## Avro Schema Forward-Compatibility
- When adding new enum symbols, backfill ALL older avsc versions with the full symbol set before registering
- `./gradlew build` regenerates avsc from proto, overwriting patches — re-patch after build, before sync
