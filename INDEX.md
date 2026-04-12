# Knowledge Graph

**191** files across **6** layers, **543** connections, **4** topic clusters.

## Layers
- **memory/** (59 files)
- **staging/** (79 files)
- **rules/** (8 files)
- **guides/** (3 files)
- **commands/** (24 files)
- **skills/** (18 files)

## Topic Clusters

### Cluster 1: context + agent + check
- ["ApplicationProcessor race condition — stage mapping missing on CREATE"](memory/insights/bug-002-application-race.md) (memory)
- [bug-007](learnings/staging/bug-007.md) (staging)
- [Bug 002](memory/insights/bug-002.md) (memory)
- [know-012-2](learnings/staging/know-012-2.md) (staging)
- [know-010](learnings/staging/know-010.md) (staging)
- [know-002](learnings/staging/know-002.md) (staging)
- [know-010-2](learnings/staging/know-010-2.md) (staging)
- [Eval-driven behavioral gates](memory/eval/eval-behavioral-gates.md) (memory)
- [know-014-2](learnings/staging/know-014-2.md) (staging)
- [know-016-2](learnings/staging/know-016-2.md) (staging)
- ... and 158 more

### Cluster 2: xlsx + docs + read
- [markitdown converts DOCX/XLSX/PPTX to clean markdown for LLM consumption](learnings/staging/know-055.md) (staging)
- [markitdown](skills/markitdown/SKILL.md) (skills)

### Cluster 3: package + usage + system
- [/share](commands/share.md) (commands)
- [/export-session](commands/export-session.md) (commands)

### Cluster 4: track + show + what
- [/worklog](commands/worklog.md) (commands)
- [watch-deps](skills/watch-deps/SKILL.md) (skills)

## Strongest Connections

- **Plugin Auto-Trigger Rules** ↔ **Plugin Auto-Trigger Rules** — 30 shared: auto, configs, consumers, context, creator
- **hp-contract-chooser-pem** ↔ **hp-pipeline-pem** — 22 shared: access, alerts, analyzes, availability, control
- **"ApplicationProcessor race condition — stage mapping missing on CREATE"** ↔ **Bug 002** — 19 shared: applicants, because, candi, candidate, check
- **Eval-driven behavioral gates** ↔ **Behavioral Gates** — 18 shared: 2026, agent, approach, behavioral, component
- **Claude Native Memory Research** ↔ **Migration Decision — Option B** — 15 shared: auto, broken, dream, first, flagged
- **markitdown converts DOCX/XLSX/PPTX to clean markdown for LLM consumption** ↔ **markitdown** — 15 shared: claude, clean, consumption, convert, design
- **knowledge-003** ↔ **hp-pipeline-pem** — 15 shared: availability, candidate, change, dips, features
- **Claude Native Memory Research** ↔ **Claude Auto Dream is broken — own the maintenance** — 14 shared: auto, behind, broken, claude, consolidation
- **Ats Bi Directional Sync Principles** ↔ **Ip Interface App Stage Sync ** — 13 shared: aditya, author, bhandari, comments, directional
- **"know-058"** ↔ **"know-056"** — 13 shared: agent, agentbus, agents, context, dynamic
- **"know-059"** ↔ **"know-058"** — 12 shared: context, e2e, identities, mock, participant
- **oncall-daily-digest** ↔ **oncall-trunk-health** — 12 shared: backend, check, daily, digest, directly
- **Engineering Principles** ↔ **Memory** — 11 shared: admit, answers, dont, engineering, faith
- **Front-load context to avoid wrong-approach friction** ↔ **know-031** — 11 shared: across, approach, claude, context, friction
- **Self-improving eval system architecture** ↔ **know-049-2** — 11 shared: architecture, auto, compound, findings, knowledge
- **aha-003** ↔ **Skill Tiers** — 11 shared: capability, eyes, hands, judgment, provide
- **know-010-2** ↔ **know-016-2** — 11 shared: architecture, because, connected-projects, context, event
- **Insights Report Findings (April 2026)** ↔ **aha-005** — 10 shared: agent, approach, claudemd, friction, insights
- **Inlogs** ↔ **search-inlogs** — 10 shared: cluster, database, inlogs, integration, kusto
- **Migration Decision — Option B** ↔ **Claude Auto Dream is broken — own the maintenance** — 10 shared: auto, autodreamenabled, broken, disable, dream
- **Plan — Migrate ecosystem to Claude-native memory architecture** ↔ **Self-improving eval system architecture** — 10 shared: anthropic, architecture, auto, compound, consolidates
- **Plan — Migrate ecosystem to Claude-native memory architecture** ↔ **know-049-2** — 10 shared: architecture, auto, claude, compound, foundation
- **know-030** ↔ **know-048-2** — 10 shared: across, agent, architecture, building, compound
- **know-030** ↔ **know-033** — 10 shared: agent, architecture, building, compound-learning, context
- **know-040** ↔ **eureka-005** — 10 shared: architecture, connected-projects, phase, phase2, pipeline-sync
- **know-012-2** ↔ **know-010-2** — 10 shared: because, clusters, connected-projects, context, different
- **"know-059"** ↔ **"know-056"** — 10 shared: auth, because, context, fails, mock
- **iTerm2 required for VM clipboard** ↔ **know-046** — 9 shared: apple, clipboard, iterm2, over, support
- **Insights Report Findings (April 2026)** ↔ **know-031** — 9 shared: agent, approach, claude, friction, insights
- **know-030** ↔ **know-037** — 9 shared: compound-learning, context, hooks, knowledge, meta
- ... and 513 more connections

## Cross-Layer Connections
*(connections between different knowledge types)*

- [memory] **Eval-driven behavioral gates** ↔ [rules] **Behavioral Gates** — 2026, agent, approach, behavioral
- [staging] **markitdown converts DOCX/XLSX/PPTX to clean markdown for LLM consumption** ↔ [skills] **markitdown** — claude, clean, consumption, convert
- [staging] **knowledge-003** ↔ [skills] **hp-pipeline-pem** — availability, candidate, change, dips
- [memory] **Claude Native Memory Research** ↔ [staging] **Claude Auto Dream is broken — own the maintenance** — auto, behind, broken, claude
- [memory] **Engineering Principles** ↔ [rules] **Memory** — admit, answers, dont, engineering
- [memory] **Front-load context to avoid wrong-approach friction** ↔ [staging] **know-031** — across, approach, claude, context
- [memory] **Self-improving eval system architecture** ↔ [staging] **know-049-2** — architecture, auto, compound, findings
- [staging] **aha-003** ↔ [guides] **Skill Tiers** — capability, eyes, hands, judgment
- [memory] **Insights Report Findings (April 2026)** ↔ [staging] **aha-005** — agent, approach, claudemd, friction
- [memory] **Inlogs** ↔ [skills] **search-inlogs** — cluster, database, inlogs, integration
- [memory] **Migration Decision — Option B** ↔ [staging] **Claude Auto Dream is broken — own the maintenance** — auto, autodreamenabled, broken, disable
- [memory] **Plan — Migrate ecosystem to Claude-native memory architecture** ↔ [staging] **know-049-2** — architecture, auto, claude, compound
- [memory] **iTerm2 required for VM clipboard** ↔ [staging] **know-046** — apple, clipboard, iterm2, over
- [memory] **Insights Report Findings (April 2026)** ↔ [staging] **know-031** — agent, approach, claude, friction
- [staging] **know-048-2** ↔ [commands] **/improve-agent** — across, agent, eval, improvement
- [memory] **Research Pipeline Pattern** ↔ [staging] **eureka-003-2** — dashboard, executive, intelligence, level
- [memory] **Engineering Principles** ↔ [rules] **Engineering Principles** — amazon, engineering, guide, insiders
- [memory] **Plugin Auto-Trigger Rules** ↔ [rules] **Proactive Suggestions** — during, invoke, proactively, right
- [memory] **Plan — Migrate ecosystem to Claude-native memory architecture** ↔ [staging] **autoMemoryDirectory unifies Claude memory read/write** — architecture, auto, claude, complex
- [memory] **Eval-driven behavioral gates** ↔ [commands] **/improve-agent** — agent, eval, failures, improve
