---
name: PEM Kusto Access Reference
description: How to query PEM database directly via Azure Kusto SDK — cluster, database, table names, and key fields
type: reference
---

## PEM Kusto Database Access

**Cluster:** `inlogsprodplatform.westus2.kusto.windows.net`
**Database:** `Pem`
**Auth:** `az login --tenant "658728e7-1632-412a-9815-fe53f53ec58b" --scope "https://inlogsprodplatform.westus2.kusto.windows.net/.default"`
**Token expires every 12 hours** — re-auth when you see AADSTS70043 errors.

### Key Tables

| Table | Purpose |
|-------|---------|
| `DebuggableOopsPageEvent` | Client-side oops pages — the actual user-visible failures |
| `FeatureDegradeEvent` | Feature-level degradation — error counts by endpoint, status code, fabric |
| `ProductAvailabilityPartialSessionScoreEvent` | Session-level availability scores |
| `ServerSidePageLoadEvent` | Server-side page load metrics |

### Key Fields — DebuggableOopsPageEvent
- `pageKey` — e.g., `d_talent_contract_chooser`
- `responseErrorType` — `SERVER_ERROR`, `NETWORK_ERROR`, `UNCLASSIFIED`
- `header__auditHeader__fabricUrn` — **client POP** (NOT serving fabric!)
- `responseTraceHeaders__fabric` — **actual serving fabric**
- `downstreamCallTreeId` — treeId for trace analysis
- `memberId` — affected member

### Key Fields — FeatureDegradeEvent
- `downstreamApiEndpointPath` — e.g., `talent/api/talentContractOptions`
- `downstreamApiResponseCode` — HTTP status code
- `responseErrorType` — `SERVER_ERROR`, `CLIENT_ERROR`, `UNCLASSIFIED`
- `fabric` — serving fabric
- `downstreamApiTreeId` — treeId for trace analysis
- `memberId` — affected member

### Python Snippet
```python
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.identity import AzureCliCredential

cluster = "https://inlogsprodplatform.westus2.kusto.windows.net"
credential = AzureCliCredential()
token = credential.get_token(f"{cluster}/.default")
kcsb = KustoConnectionStringBuilder.with_aad_application_token_authentication(cluster, token.token)
client = KustoClient(kcsb)
response = client.execute("Pem", query)
```

**Why:** The standard `kql_fetch_logs` MCP tool uses inLogs API which doesn't have the PEM database. Direct Kusto SDK is the only way to query PEM data programmatically.
**How to apply:** Use this when investigating PEM alerts and need ground-truth error data beyond what `fetch_pem_errors` and `get_server_side_top_contributors` provide.
