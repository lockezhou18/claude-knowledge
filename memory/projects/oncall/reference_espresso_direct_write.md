---
name: Espresso Direct Write via Router
description: How to read/write Espresso records directly via the router REST API using curli from prod shell hosts
type: reference
---

**When to use:** When the service's REST API can't handle the update (e.g., partial update NPEs on null fields), you can write directly to Espresso.

**D2 service naming convention:** `EDB-{DatabaseName}`
- Example: `EDB-HireIdentity` for the HireIdentity database

**REST API format:** `https://{router-host}:11937/{DatabaseName}/{TableName}/{key}`
- Example: `https://router-mt-ld-3.prod-lor1.pqd.prod.linkedin.com:11937/HireIdentity/HireIdentity/254318478`

**Finding the router host:** Use curli verbose output — check `x-espresso-cluster` header to identify the cluster (e.g., `ESPRESSO_MT-LD-3` → `router-mt-ld-3`)

**Steps:**
1. SSH to prod shell: `ssh ltx1-shell07.prod.linkedin.com`
2. Get certs: `id-tool grestin -f {fabric} sign` (needs Yubikey tap)
3. READ: `curli -X GET 'https://{router}:11937/{db}/{table}/{key}' -k --key ./identity.key --cert ./identity.cert -H 'Accept:application/json'`
4. WRITE: `curli -X PUT 'https://{router}:11937/{db}/{table}/{key}' -k --key ./identity.key --cert ./identity.cert -H 'Content-Type:application/json' -H 'X-Espresso-Schema-Version:{version}' -d '{json}'`
5. Verify with another GET

**Gotchas:**
- Must run from prod shell host, not laptop (ACL)
- grestin needs interactive Yubikey auth — can't fully automate
- Always READ before WRITE to confirm current state
- Include X-Espresso-Schema-Version header on writes
- Confluence wiki for router DNS: go/espresso-router-d2-names (page ID 525205209)
