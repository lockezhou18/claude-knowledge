---
id: knowledge-003
track: knowledge
type: semantic
repos: ["*"]
tags: [pem, pipeline, availability, oncall, monitoring, investigation]
severity: medium
created: 2026-03-28
last_verified: 2026-03-28
use_count: 1
outcome_score: 1.0
status: active
rot_rate: medium
---

## When investigating HP Pipeline PEM dips, check change-candidate-stage and pipeline-profile-list features first

### Context
Pipeline PEM (Hiring Platform - Pipeline, Web) monitors availability of the `d_talent_projectsHome` page. Historical error distribution: `change-candidate-stage` (~61%), `pipeline-profile-list` (~37.5%).

### Guidance
1. Fetch PEM errors via `mcp__captain__fetch_pem_errors` with product "Hiring Platform - Pipeline"
2. Check if SERVER_ERROR dominates (>50% = backend issue) vs CLIENT_ERROR
3. Correlate with mcm-mt deployments and LiX ramps — these are the most frequent triggers
4. `change-candidate-stage` path: tsapi → mcm-mt → hp-mt → Espresso (MultichannelManagement)
5. `pipeline-profile-list` path: tsapi → mcm-mt → hire-access-control → Espresso (HireAccessControlDB)
6. Low session count (<50) + only baseline errors = low-traffic amplification, skip investigation

### When to Apply
- PEM availability alert for "Hiring Platform - Pipeline"
- `d_talent_projectsHome` oops page count spike
- Candidate stage change failures reported
- Use `/hp-pipeline-pem` skill for structured investigation
