# Scope — Understand the System Before Designing

Map the existing system, trace data flows, and understand constraints before proposing a design. Use when starting a new project, getting a PRD, or entering an unfamiliar codebase area.

**Usage:** `/discover [feature/project/area to understand]`

If no argument, ask: "What area or feature do you need to understand?"

## Step 0: Understand the WHY

Before mapping the system, understand what the user/PM actually wants:
1. **What's the goal?** Not the feature — the business outcome. Why does this matter?
2. **Who's the customer?** End user? Internal team? Another service?
3. **What does success look like?** How will we know this worked?
4. **What's the scope?** What's explicitly in and out?
5. **Are there constraints?** Timeline, dependencies, tech limitations, team bandwidth?

If a PRD/doc exists, read it first. Challenge assumptions: "Is this the right problem to solve?"

## Step 1: Map the Current State

**Lead with substance, not plumbing.** For every component you discover, explain WHAT the data represents and WHY it exists before describing HOW it flows. "Espresso table X" is plumbing — "candidate hiring state transitions tracked for real-time pipeline display" is substance.

### 1a. Code-Level Discovery
- Trace a single piece of data end-to-end through the relevant feature area (follow the data, not the architecture)
- Identify entry points (API endpoints, Kafka consumers, cron jobs)
- Follow the code path: controller → service → processor → storage
- Map the data model: what entities exist, how they relate, where they're stored
- Identify the business logic — where are the rules? What are the invariants?
- **Mine commit history**: `git log --oneline -20 <key file>` and `git blame` on non-obvious code. When something looks complex, the commit message often explains why.

### 1b. Service-Level Discovery
- Which services are involved? Who owns them?
- What are the interfaces between services? (gRPC, REST, Kafka, Espresso)
- What are the dependencies? Upstream (who calls us) and downstream (who we call)
- Are there shared libraries or common patterns?
- **Disambiguate naming**: When the same term appears in different services, check if it means the same thing. Call out naming collisions explicitly — they cause the worst cross-team misunderstandings.

### 1c. Infrastructure Discovery
- Where does data live? (Espresso tables, Kafka topics, Venice stores)
- What monitoring exists? (PEM surfaces, Grafana dashboards, InGraphs metrics)
- What's the deployment model? (Kubernetes, fabric-aware, canary strategy)
- What LiX/feature flags gate this area?

**Auto-invoke LinkedIn infra plugins:**
- **First time in a new repo?** Run `linkedin-framework:map-infrastructure` to auto-detect infrastructure systems (Espresso, Kafka, D2, Venice, etc.) and generate skill files under `.claude/skills/infrastructure/`. This only needs to run once per repo.
- **Infra questions?** Use `linkedin-framework:infra-specs-expert` — it has deep knowledge about Espresso key constraints, Kafka topic configs, D2 routing, Venice store patterns that our system doesn't replicate. Ask it directly rather than guessing.
- **Dependencies unknown?** Run `library-specs:download` to auto-download dependency docs for the current MP. Then use `library-specs:skills` to understand how to use them.

### Tools for Scope
- **Code**: Read local, `jarvis_codesearch` cross-repo, `unified_context_search` for broad search
- **Infrastructure**: `linkedin-framework:infra-specs-expert` for infra questions (Espresso, Kafka, D2 deep knowledge), `linkedin-framework:map-infrastructure` for auto-detection, `observe-agent` for runtime topology and service dependencies
- **Docs**: `search_github_pages`, `search_confluence_content` for architecture docs
- **Dependencies**: `library-specs:download` (auto-download for current MP), then `library-specs:skills` for usage docs

## Step 2: Check Prior Knowledge

1. Search `~/.claude/learnings/manifest.jsonl` for existing insights in this area
2. Search company knowledge:
   - **Jira**: Related tickets, design decisions, known issues (`search_jira_issues`)
   - **Confluence**: Design docs, architecture docs, runbooks (`search_confluence_content`)
   - **Slack**: Recent design discussions (`search_slack`)
3. Search git history: `git log --oneline --all --grep="keyword" -30` for related PRs
4. Check if team members have worked on this before: `gh pr list --search "keyword" --state all`

## Step 3: Document the Negative Space

Before moving to constraints, explicitly document what does NOT happen:
- "Service A does NOT call Service B directly — it goes through Kafka"
- "This entity does NOT get updated on the read path — only on write"
- "The V2 migration does NOT backfill existing records"

These are often more valuable than documenting what DOES happen — they prevent wrong assumptions.

## Step 4: Verify Your Own Understanding

After building your mental model, actively try to break it:
- "Does X really not include Y?" — test your boundaries
- "Are these two things actually separate?" — check for hidden connections
- "Is this name the same thing in both services?" — check for naming collisions
- "Am I sure about this count/value?" — verify against actual code, not memory

If any of these questions reveal a mistake, fix it before presenting to the user.

## Step 5: Identify Constraints and Risks

Map out what shapes the solution:
- **Hard constraints**: Things that cannot change (API contracts with external partners, data model limits, compliance requirements)
- **Soft constraints**: Things that are expensive to change (shared libraries, cross-team dependencies, established patterns)
- **Risks**: What could go wrong? (Data migration complexity, backward compatibility, performance at scale)
- **Open questions**: What do you still not know? What needs clarification from PM/team?

## Step 6: Produce Discovery Artifacts

### Architecture Map
```
## Discovery: [feature/area]

### What This System Does (substance first)
- [Plain language: what problem it solves, what data it handles, why it exists]
- [NOT "it uses Kafka and Espresso" — that's plumbing]

### Business Context
- Goal: [why this exists]
- Customer: [who benefits]
- Success criteria: [how we measure]

### Current Architecture
- [Service A] → [Service B] → [Service C]
- Data flow: [entry] → [processing] → [storage] → [output]
- Key entities: [Entity1 — what it REPRESENTS (stored in X), Entity2 — what it REPRESENTS (stored in Y)]

### What Does NOT Happen (negative space)
- [Service A does NOT call Service C directly — goes through B]
- [Entity X is NOT updated on reads — only on writes]
- [This flow does NOT handle [edge case] — that's a separate path]

### Naming Watch (disambiguation)
- "[term]" means [X] in [Service A] but [Y] in [Service B]

### Service Ownership
| Service | Team | Interface | Notes |
|---------|------|-----------|-------|
| ... | ... | ... | ... |

### Data Model
| Entity | What it Represents | Storage | Key Fields | Relationships |
|--------|-------------------|---------|------------|---------------|
| ... | ... | ... | ... |

### Existing Patterns to Follow
- [Pattern from the codebase that new code should match]

### Constraints
- Hard: [cannot change]
- Soft: [expensive to change]

### Risks
- [Risk 1]: likelihood, impact, mitigation
- [Risk 2]: ...

### Open Questions
- [Questions for PM / team / upstream owners]

### Recommended Next Steps
- [What to research externally, what to plan, what to clarify]
```

## Step 5: Auto-Learn

Save key architectural insights as `knowledge-track` entries:
- Data flows → `rot_rate: slow` (architecture changes slowly)
- Entity mappings → `rot_rate: slow`
- Service ownership → `rot_rate: medium` (teams reorganize)
- Test data references → `rot_rate: fast` (data changes)

These become the foundation for future sessions working in this area — exactly how `know-010` through `know-016` were created for Phase 2.

Tell the user: "Saved N architectural insights. Future sessions will have this context automatically."

## Step 6: Handoff

Present the discovery to the user and suggest next action:
- "Ready to plan?" → proceed to Phase 3 (Plan) of the pipeline
- "Need external research?" → `/research [specific topic]`
- "Questions for PM?" → list the open questions clearly
- "Need to investigate something specific?" → `/investigate [symptom]`
