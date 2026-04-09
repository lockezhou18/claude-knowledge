---
id: know-015
track: knowledge
type: semantic
repos: ["hp-ats-integration-mt", "talent-solutions-api", "linkedin-entities"]
tags: ["euler", "glai", "managed-entity", "tidb", "espresso", "indexing", "infrastructure", "hireEntityRequest"]
severity: critical
created: "2026-04-02"
last_verified: "2026-04-02"
use_count: 0
outcome_score: 0
rot_rate: slow
status: active
paths: ["**/HireEntityRequest*", "**/EulerConfigurations*", "**/hire-entity-request-uc/**"]
---

## Euler Mental Model — Entity Management and GLAI Indexing

**When** working with HireEntityRequest or any Euler managed entity, understand these fundamentals to avoid silent query failures and deployment confusion.

### get vs find — The Critical Difference

```
get(urn)   → Espresso (SOT) directly → ALWAYS works
find(where) → GLAI (TiDB) via index → FAILS if entity not indexed
```

**If GLAI indexing fails for ANY reason, ALL finders return empty for that entity — no error.**

### Why GLAI Indexing Fails

The GLAI pipeline: Espresso write → Brooklin CDC → euler-index-builder (Samza) → TiDB upsert.

**Common failure: queryField value exceeds column maxSize** (default ~255 chars).
- One bad field poisons the WHOLE entity — it's dropped entirely from GLAI
- The entity still exists in Espresso (get works), but invisible to all finders
- No error logged in the consuming service — finders silently return empty

### queryField Configuration

```protobuf
// In HireEntityRequestEulerConfigurations.proto
option (.euler.entityOptions) = {
  queryField: {path: "hiringProjectUrn"}
  queryField: {path: "hiringProjectCandidateRequestDetails.candidate"}
  queryField: {path: "hiringProjectCandidateRequestDetails.historyUrn", maxSize: 300}
  queryField: {path: "status"}
  queryField: {path: "isDismissed"}
  queryField: {path: "lastModifiedAt"}
  queryField: {path: "hiringProjectCandidateRequestDetails.targetPipelineStateValue"}
};
```

- `maxSize` controls TiDB varchar column width for compound URN fields
- Without it, defaults to ~255 — easily exceeded by nested proto URNs
- Set explicitly for any compound URN field (especially HiringProjectCandidateHistoryUrn)

### Deployment Pipeline

```
linkedin-entities repo (PR merged)
  → Post-merge CI builds version (e.g., v1.0.423)
  → Deploys to vertical (euler-managed-entities-common-pool)
  → Dark cluster first (canary on one host per fabric)
  → Main fleet promotion (manual or auto after bake time)
```

- HireEntityRequest lives in **common-pool** vertical
- Check deployment: `go-status -f prod-ltx1 -a euler-managed-entities-common-pool`
- Dark cluster shows as separate line with `.dark-cluster` suffix
- Main fleet promotion can lag days behind PR merge

### Debugging Checklist

When `find` returns empty but `get` works:
1. **Check if entity is in GLAI** — there's no direct way; the symptom IS the diagnosis
2. **Check queryField sizes** — does any indexed field exceed maxSize?
3. **Check deployment** — is the entity model version deployed to main fleet?
4. **Check GLAI CDC lag** — entity created < 30s ago? Indexing might not be done
5. **Check Euler vertical health** — `go-status` for the vertical

### Key Services and Ports

| Service | Prod | Local |
|---------|------|-------|
| Query Server | port 22823 | — |
| Control Plane | port 16665 | — |
| hp-ats-integration-mt | — | 28465 |
| talent-partner-integrations-mt | — | 28288 |

### Ownership

- **Team**: Euler Crew (ID: 3834)
- **Slack**: #euler
- **Entity definitions repo**: linkedin-multiproduct/linkedin-entities
- **Vertical**: euler-managed-entities-common-pool
