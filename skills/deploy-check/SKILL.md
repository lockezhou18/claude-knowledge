# Deploy Check

Check deployment status for an HP service across all fabrics.

## Usage
`/deploy-check <service-name>` (e.g., `/deploy-check mcm-mt`)

## Steps

1. **Check current prod versions** across all fabrics:
   ```bash
   go-status -f prod-ltx1 -a <service>
   go-status -f prod-lva1 -a <service>
   go-status -f prod-lor1 -a <service>
   ```
   Run these in parallel.

2. **Check recent deployments** in CRT:
   Use `mcp__captain__fetch_application_events` to find recent deployment events for the service.

3. **Check EKG status** — look for any active EKG evaluations or rollbacks:
   Use observe-agent to check: "Show me EKG status for <service> in the last 24 hours"

4. **Check for deployment pauses**:
   Report if any CRT pauses exist for the product.

5. **Summarize** in a table:
   | Fabric | Version | EKG Status | Last Deploy |
   |--------|---------|------------|-------------|

If the user provides a version, also compare what commits are in that version vs what's currently deployed.
