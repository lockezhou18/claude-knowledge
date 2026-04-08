# Service Topology Reference — Contract Chooser

## PEM Product Details

| Property | Value |
|----------|-------|
| **Product** | Hiring Platform - Contract Chooser |
| **Platform** | Web |
| **Tracking Service** | samza-pem-degradation-tracking |
| **Enabled Fabrics** | prod-lva1, prod-ltx1, prod-lor1 |

## Session Count Baselines

| Time Period | Expected Session Count |
|-------------|----------------------|
| Weekday peak | 200–428 |
| Off-hours / weekends | 8–50 |
| **Low-traffic threshold** | **< 50 — 1 error can tank availability** |

## Service Dependency Graph

```
PEM (Hiring Platform - Contract Chooser)
  └── talent-solutions-web  (/talent/contract-chooser)
        └── talent-solutions-api-frontend
              ├── /talentContractOptions  ──► hp-ep-mt (contractsV2, finder:activeUser)
              │                                    └── ep-apps-connector-mt (epContracts)
              │                                          └── eis-backend (memberContractSeats)
              │
              ├── /talentAuthentication ──► hp-ep-mt (seatsV2)
              │                                  └── ep-apps-connector-mt (epSeats)
              │                                        └── eis-backend (memberContractSeats)
              │
              ├── /talentMe  ──────────────► hp-ep-mt (contractsV2)  ← #1 CALLER by volume
              │                                    └── ep-apps-connector-mt → eis-backend
              │
              ├── /talentNotificationCards ─► NotificationDecorationService
              │                                    ├── [direct] hp-ep-mt /seatsV2 (1 call, deduped by PR 8393)
              │                                    ├── mcm-mt /sourcingChannels → hp-ep-mt /seatsV2
              │                                    ├── mcm-mt /hiringProjects → hp-ep-mt /seatsV2
              │                                    ├── recruiter-search-mt /hireSavedSearches → hp-ep-mt /seatsV2
              │                                    ├── hire-access-control /hireRoleAssignments → hp-ep-mt /seatsV2
              │                                    └── hire-recommender → hp-ep-mt /seatsV2
              │                                    ⚠️ FAN-OUT: 25-49 seatsV2 calls per page load
              │
              └── /talentSeats  ────────────► hire-access-control (/seatEntitlements)
                                                    └── ats-middleware (/atsIntegrations)
                                                          └── Espresso (MemberContractSeatLookup)
```

## Top Callers to hp-ep-mt (from incident-10781 data)

During overload, the dominant callers to hp-ep-mt seatsV2+contractsV2:

| Rank | Caller | hp-ep-mt Endpoint | % of Traffic | Notes |
|------|--------|-------------------|-------------|-------|
| 1 | `/talentMe` | contractsV2 | **53%** | Every Recruiter page load |
| 2 | `voyager-api-messaging-dash` | contractsV2 | **22%** | Non-Recruiter LinkedIn messaging |
| 3 | `job-posting-flow-mt` | contractsV2+seatsV2 | 5% | Job posting eligibility |
| 4 | `/talentNotificationCards` | seatsV2 | 0.6% | Notification decorations |
| 5 | `/talentContractOptions` | contractsV2 | 0.4% | Contract chooser page |
| 6 | `/talentAuthentication` | seatsV2 | 0.1% | Auth/session |

**Key insight:** The Contract Chooser endpoint itself (`talentContractOptions`) is a tiny fraction of hp-ep-mt traffic. Most overload comes from `/talentMe` (every page load) and voyager messaging.

## Notification Fan-Out Detail (seatsV2)

A single `/talentNotificationCards` page load triggers 25-49 seatsV2 calls because every intermediate service independently resolves seat auth:
- PR 8393 (HPLT-104533) fixed the direct decoration layer (N→1 dedup) ✅
- But mcm-mt, recruiter-search-mt, hire-access-control, hire-recommender each make their own seatsV2 calls ❌
- This is architectural — no single-service fix can deduplicate cross-service calls

## Dark Cluster Configuration

Config location: `config/public/lps-d2-TalentSolutionsApiFrontend.src` in talent-solutions-api repo

| Dark Cluster | Strategy | Config |
|---|---|---|
| `darkTalentSolutionsApiFrontend` | RELATIVE_TRAFFIC | multiplier = 0.05 (5%) |
| `darkTalentSolutionsApiFrontendFaultLine` | RELATIVE_TRAFFIC | multiplier = 0.05 (5%) |
| `darkTalentSolutionsApiFrontend1QPS` | CONSTANT_QPS | 1 QPS (warmup only) |

Deploy changes: `lps d2 update -f <fabric> -c TalentSolutionsApiFrontend --bypass-canary`

## Endpoint Error Baselines (28-day confirmed)

| Endpoint | Max errors/period | Avg errors/period | Notes |
|----------|-------------------|-------------------|-------|
| `talentContractOptions` | 13 | 0.012 | Stable — always present |
| `talentAuthentication` | 5 | 0.013 | Stable |
| `talentContracts` | 1 | 0.00007 | Near-zero |
| `talentSeats` | N/A | N/A | Primary incident endpoint |

## Service Log Tables (Kusto)

| Service | Log Table | Cluster |
|---------|-----------|---------|
| talent-solutions-api-frontend | `talent_solutions_api_frontend_logs` | inlogsliprod |
| hp-ep-mt | `hp_ep_mt_war_logs` | inlogsliprod |
| hire-access-control | Run `get_table_mapping_for_application("hire-access-control")` | inlogsliprod |
| ats-middleware | Run `get_table_mapping_for_application("ats-middleware")` | inlogsliprod |

## PEM Kusto Access

- **Cluster:** `inlogsprodplatform.westus2.kusto.windows.net`
- **Database:** `Pem`
- **Tables:** `FeatureDegradeEvent`, `DebuggableOopsPageEvent`
- **Auth:** `az login --tenant "658728e7-1632-412a-9815-fe53f53ec58b" --scope "https://inlogsprodplatform.westus2.kusto.windows.net/.default"`

## Trace Explorer URL

Format: `https://observe.prod.linkedin.com/trace-explorer/visualize?traceId=<url-encoded-treeId>&environment=prod&viewType=Tree`

URL-encode: `+` → `%2B`, `=` → `%3D`, `/` → `%2F`

Retention: ~7 days. Get trace evidence early. Logs Explorer links have longer retention as backup.
