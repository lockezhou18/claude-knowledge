# Explore — Build a Mental Model of an Unfamiliar Domain

Learn a new domain from scratch. Not investigating a bug, not scoping a feature — just building understanding of an area you know nothing (or little) about.

**Usage:**
- `/explore euler` — what is Euler, how does it work, how does it relate to my systems
- `/explore venice` — what is Venice, when would I use it vs Espresso
- `/explore d2 service mesh` — how does D2 routing work
- `/explore kafka streams vs samza` — compare two technologies in the LinkedIn context
- `/explore agent-lifecycle-mt to compare with agentbus` — side-by-side with gap analysis

## What Makes Explore Different

| Skill | When to use | Source priority |
|---|---|---|
| `/scope` | "Map THIS system for a feature I'm building" | **Local-first** — I'm in the repo |
| `/investigate` | "Find root cause of THIS bug" | **Local-first** — logs, code, config |
| `/research` | "Answer THIS question with evidence" | **Mixed** — depends on question |
| `/find` | "Has someone already solved this?" | **External-first** — company knowledge |
| **`/explore`** | "I don't know enough to ask the right questions" | **External-first** — I'm learning, not debugging |

Explore is the skill you use BEFORE you can use the others. It builds the mental model that makes scope, research, and find effective.

**Key principle: /explore is for things you DON'T know yet.** If it's local and familiar, use /scope or /investigate. /explore goes external-first because the whole point is discovering the unfamiliar.

## Step 0: Detect Mode

Parse the user's argument to determine the exploration mode:

- **Single system**: `/explore euler` → build mental model of one system
- **Comparison**: `/explore X to compare with Y` or `/explore X vs Y` → side-by-side analysis with gap analysis, what each can learn from the other
- **URL**: `/explore https://...` → fetch and analyze external documentation

Also detect the **source type** to determine Layer ordering (see Step 2):
- LinkedIn internal service → Captain MCP tools first
- LinkedIn infra component → infra-specs-expert first
- External/open-source → WebFetch + WebSearch first
- Industry protocol/standard → WebFetch the spec first
- General concept → WebSearch first, then LinkedIn examples
- Local repo module → redirect to `/scope` ("this looks local — want /scope instead?")

## Step 1: Assess Current Knowledge

Ask the user (if not clear from context):
- What do you already know about this? (could be nothing — that's fine)
- Why are you exploring this now? (upcoming work, curiosity, dependency question)
- How deep do you need to go? (awareness / working knowledge / deep expertise)

Depth levels:
- **Awareness**: "What is it, when would I encounter it, who owns it" (~5 min)
- **Working knowledge**: "How does it work, how do I interact with it, what are the gotchas" (~15 min)
- **Deep expertise**: "Internals, edge cases, configuration, operational patterns" (~30+ min)

## Step 2: Discovery Phase (Context-Dependent Layers)

**The layer ordering depends on what you're exploring.** The goal of Layer 1 is the fastest orientation signal — not the most thorough. Use the source routing table to pick the right tools for each layer.

### Source Routing Table

| Exploring... | Layer 1 (orient — fastest signal) | Layer 2 (depth — read the code) | Layer 3 (context — who/why/friction) |
|---|---|---|---|
| **LinkedIn service** (agent-lifecycle-mt, mcm-mt) | `search_github_pages` (CLAUDE.md, README) + `search_confluence_content` | `jarvis_codesearch` + `jarvis_get_file` (key impl files, protos) | `search_slack` + `search_jira_issues` + `search_oncall` |
| **LinkedIn infra** (Espresso, Kafka, D2, Venice) | `linkedin-framework:infra-specs-expert` (has deepest indexed context) | `jarvis_codesearch` (client usage across repos) | `search_confluence_content` (architecture pages) |
| **LinkedIn library** (li-pegasus, ligradle) | `library-specs:download` + `search_github_pages` | `jarvis_codesearch` (usage patterns) + `jarvis_get_file` | `search_jira_issues` (known issues) |
| **External open-source** (NATS, LangGraph, React) | `WebFetch` (official docs/README) | `WebSearch` (tutorials, comparisons) | `jarvis_codesearch` (how LinkedIn uses it internally) |
| **Industry protocol** (A2A, MCP, gRPC, OAuth) | `WebFetch` (spec site / RFC) | `WebSearch` (reference implementations) + GitHub | `jarvis_codesearch` (LinkedIn adoption) |
| **General concept** (event sourcing, CQRS, RAFT) | `WebSearch` (authoritative articles) | `WebFetch` (best resource found) | `jarvis_codesearch` (LinkedIn examples) |
| **Customer/partner product** (Greenhouse, Workday) | `WebFetch` (their docs) / `Playwright` (interactive site) | `WebSearch` (API docs, integration guides) | `search_confluence_content` (internal integration docs) |
| **Comparison** (X vs Y) | Route X and Y independently through this table, **in parallel** | Code deep-dive on both | Gap analysis between findings |

### Running the Layers

**Layer 1 — Orient** (run in parallel, pick tools from routing table):
Goal: understand what this IS in one round of tool calls. After Layer 1, you should be able to write the "What It Is" paragraph of the mental model.

**Layer 2 — Depth** (informed by Layer 1 findings):
Goal: read the actual source code / spec / implementation. Find the core classes, protos, entry points. This is where Claim vs Reality verification happens.

**Layer 3 — Context** (only if depth level is working-knowledge or deep-expertise):
Goal: understand the social/operational context — who owns it, what breaks, what's the backlog.

**Layer 4 — Local Cross-Reference** (only if the explored system touches your repo):
- Check `dependencies.jsonl`, imports, config references
- If no connection found: skip entirely

## Step 3: Code Deep-Dive (Verify Claims)

**Don't trust documentation at face value.** Read the actual source code for key claims.

For each major architectural claim from the docs:
1. Find the implementation via `jarvis_codesearch` or `jarvis_get_file`
2. Verify: does the code match what the docs say?
3. Note discrepancies — these are the most valuable findings

Build a **Claim vs Reality** table:

```markdown
### Claim vs Reality
| What docs/marketing say | What code actually shows | Evidence (file:line) |
|---|---|---|
| "Orchestration platform" | Message router + RPC proxy | SkillInvoker.java:142 |
| "Multi-agent coordination" | Star topology, sync calls only | agent_router.py:28 |
```

This section is often the most valuable output of /explore — it cuts through marketing to ground truth.

## Step 4: Build the Mental Model

Synthesize findings into a structured mental model:

```
## Mental Model: [domain]

### What It Is (one paragraph)
[Explain like the user has never heard of it]

### Core Concepts (3-5 key terms)
- **[Concept 1]**: [what it means, why it matters]
- **[Concept 2]**: [what it means, why it matters]

### How It Works (the mechanics)
[Data flow / architecture / key components]
[Diagram if it helps — ASCII art]

### Claim vs Reality
| Claimed | Verified | Evidence |
[Fill from Step 3 — skip if no discrepancies found]

### How It Connects To Your Work
- [Your system] uses/resembles [this domain] for [purpose]
- Interface: [API/protocol/format]
- Key touchpoints: [specific classes, configs, endpoints]

### Common Gotchas
- [Thing that trips people up #1]
- [Thing that trips people up #2]

### Who Owns It
- Team / Oncall / Slack / Confluence

### What To Explore Next
- [Specific sub-topic worth going deeper on]
- [Related domain that connects to this one]
```

### Comparison Mode (when `/explore X to compare with Y`)

Add these sections:

```
### Side-by-Side Comparison
| Dimension | X | Y | Delta |
[Concrete, evidence-based comparison]

### What X Can Learn From Y
[Specific patterns/features to adopt]

### What Y Can Learn From X
[Reverse direction]

### Gap Analysis
| Capability | X | Y | Priority |
[Actionable roadmap items]
```

## Step 5: Checkpoint — Ask Before Going Deeper

After presenting the initial mental model, **pause and ask**:
- "Want to go deeper on [specific area]?"
- "The claim vs reality on [X] is interesting — want me to verify further?"
- "I see a connection to [your system] — want to explore that angle?"

Don't try to cover everything in one pass. Let the user steer the depth.

## Step 6: Auto-Learn

Save the mental model as knowledge-track insights:
- One high-level insight for the overall domain (`rot_rate: slow`)
- Separate insights for specific gotchas or verified findings (`rot_rate: medium`)
- Tag with the domain name so future sessions find them
- If comparison mode: save the gap analysis as an `/aha`-level insight

## Step 7: Suggest Next Steps

Based on why the user is exploring:
- "Ready to `/scope` a feature in this area?"
- "Want to `/explore` a related domain? ([suggested domain])"
- "Want to go deeper? I can explore [specific sub-topic]."
- "Want to `/find` existing patterns for working with [domain]?"
- "Want to `/aha` to synthesize a pattern from this comparison?"
- "Want to `/learn` a specific finding?"

## Integration

```
/explore agent-lifecycle-mt to compare with agentbus
  → external discovery (GitHub Pages, Confluence, Jarvis)
  → code deep-dive (SkillInvoker.java, AgentApi.proto)
  → claim vs reality verification
  → side-by-side comparison + gap analysis
  → checkpoint: "want to go deeper on inter-agent comms?"
  → saves as insights (/learn, /aha)
  → user now has enough context to:
    → /scope a feature inspired by the comparison
    → /implement items from the gap analysis roadmap
    → /verify specific claims about either system
```

Explore feeds all other skills — it's the knowledge bootstrap.
