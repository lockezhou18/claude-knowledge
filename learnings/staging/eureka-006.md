---
id: eureka-006
track: knowledge
type: semantic
repos: [*]
tags: [eureka, mental-model, cross-boundary, design, frontend, backend, infrastructure, figma, playwright, e2e-testing, system-thinking, paradigm]
severity: critical
created: '2026-04-03'
last_verified: '2026-04-03'
use_count: 67
outcome_score: 0.0
rot_rate: permanent
status: active
origin_skill: eureka
emerged_from: 'eureka-004,eureka-005'
graduation_candidate: True
visibility: team
---

## Breakthrough

An AI agent with the right tool connections can see across ALL boundaries simultaneously — designer intent (Figma), frontend implementation (ts-web components + selectors), API contracts (ts-api), backend orchestration (mcm-mt, hp-ats), integration protocols (IP), external systems (Greenhouse), infrastructure (Kafka, Espresso, realtime), and production state (logs, metrics) — and synthesize them into a single coherent picture that no individual role or team can see alone.

## The Old Way

Each role sees their slice:
- **Designer**: Figma screens with states and flows. Doesn't know if backend supports all states.
- **Frontend engineer**: ts-web components and API calls. Doesn't know how the data flows through 5 backend services.
- **Backend engineer**: Service code and Kafka topics. Doesn't know how the UI renders the states or what selectors exist.
- **IP engineer**: Entity mappings and partner adapters. Doesn't know what the recruiter sees.
- **Infra engineer**: Kafka clusters, Espresso tables, realtime events. Doesn't know the business flow.
- **QA/Testing**: Writes test cases from design docs. Can't verify across all layers simultaneously.
- **PM**: Sees the PRD. Can't trace from requirement to running code to production behavior.

Everyone is right about their slice. Nobody sees the whole picture. Bugs live in the gaps.

## The New Way

One session with connected tools produces what no individual can:

```
Figma MCP/API          →  "The design has 3 states: Pending, Confirmed, Failed"
                            + exact UI elements, badge colors, copy text
                            
ts-web code search     →  "ConnectedProjectPipeline renders these states"
                            + [data-test-pipeline-state] selectors
                            + moveProfilesToState() triggers the chain
                            
ts-api exploration     →  "TalentHireEntityRequestResource is the new API"
                            + realtime push event on status change
                            
Backend task list      →  "50+ tasks across 7 services, here's what each does"
                            + ActionWriteBackApi → IP → Greenhouse

HP service knowledge   →  "3 pipelines + shared mapping layer"
                            + every bug maps to one pipeline
                            
Greenhouse API         →  "POST /applications/{id}/move, GET /jobs/{id}/stages"
                            + sandbox verified, API key working
                            
Kafka/Infra knowledge  →  "queuing cluster (inbound), tracking cluster (feedback)"
                            + ExportStatusEventProcessor consumes confirmation
                            
Frontend scope doc     →  "55 days, 9 tasks, all blocked on Pipeline 3 output"
                            + URL patterns, notification copy, banner behavior
```

Combine all of this → **one test case matrix** where each row verifies:
- Design spec (Figma screenshot) matches
- UI renders correctly (Playwright + selectors)
- Backend state is correct (grpcurli)
- ATS state is correct (Greenhouse API)
- Async feedback arrives (Kafka → realtime → UI refresh)

No human can hold all of this in their head simultaneously. But with the right tool connections, the agent CAN — and can produce artifacts (test matrices, system maps, debug traces) that make the full picture accessible to everyone.

## Impact

- **Testing**: Goes from "each team tests their layer" to "one test verifies all layers"
- **Debugging**: Goes from "which service broke?" to "which pipeline, which layer, which mapping?"
- **Onboarding**: Goes from "read 7 READMEs" to "here's the 3-pipeline model with all connections"
- **Communication**: Goes from "designer says X, backend says Y" to "here's the unified view, what's the gap?"
- **Bug bash**: Goes from "manual exploration" to "design-driven cross-system test matrix"

This is not specific to Connected Projects. Any multi-service feature with a design spec can use this pattern:
1. Pull design from Figma (what SHOULD happen)
2. Map to frontend components (how it's IMPLEMENTED)
3. Trace through backend services (how data FLOWS)
4. Connect to external systems (where data LANDS)
5. Verify end-to-end (does REALITY match INTENT?)

## Risks & Caveats

- Tool access is the bottleneck — Figma MCP rate limits, API tokens, ACLs
- The unified view is a snapshot — systems evolve, the model needs refreshing
- Over-reliance risk: the agent sees connections but may miss domain nuance that specialists catch
- Works best for integration-heavy features; less valuable for purely single-service changes

## The Meta-Insight

The value isn't in any single tool. It's in the **connections between tools**. Figma alone is just pictures. Playwright alone is just clicks. grpcurli alone is just data. But Figma + ts-web selectors + Playwright + grpcurli + Greenhouse API = a cross-boundary verification system that didn't exist before.

The agent is the connective tissue between organizational silos.
