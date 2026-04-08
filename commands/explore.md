# Explore — Build a Mental Model of an Unfamiliar Domain

Learn a new domain from scratch. Not investigating a bug, not scoping a feature — just building understanding of an area you know nothing (or little) about.

**Usage:**
- `/explore euler` — what is Euler, how does it work, how does it relate to my systems
- `/explore venice` — what is Venice, when would I use it vs Espresso
- `/explore d2 service mesh` — how does D2 routing work
- `/explore kafka streams vs samza` — compare two technologies in the LinkedIn context

## What Makes Explore Different

- `/scope` = "Map this system for a specific feature I'm building"
- `/research` = "Answer this question with evidence"
- `/find` = "Has someone already solved this?"
- `/think` = "Let's think together, no structure needed" (see /think)
- **`/explore`** = "I don't know enough to ask the right questions yet. Teach me."

Explore is the skill you use BEFORE you can use the others. It builds the mental model that makes scope, research, and find effective.

## Step 1: Assess Current Knowledge

Ask the user (if not clear from context):
- What do you already know about this? (could be nothing — that's fine)
- Why are you exploring this now? (upcoming work, curiosity, dependency question)
- How deep do you need to go? (awareness / working knowledge / deep expertise)

Depth levels:
- **Awareness**: "What is it, when would I encounter it, who owns it" (~5 min)
- **Working knowledge**: "How does it work, how do I interact with it, what are the gotchas" (~15 min)
- **Deep expertise**: "Internals, edge cases, configuration, operational patterns" (~30+ min)

## Step 2: Gather from Multiple Angles

Search these in parallel — each gives a different perspective:

### What it IS (conceptual)
- `search_confluence_content` — look for overview/intro/onboarding pages
- `search_github_pages` — README, getting started guides
- `linkedin-framework:infra-specs-expert` — if it's LinkedIn infrastructure (Espresso, Kafka, D2, Venice, Euler, etc.), this has the deepest context
- `library-specs:download` + `library-specs:skills` — if it's a library/framework

### How it WORKS (mechanical)
- `jarvis_codesearch` — find the core classes, interfaces, entry points
- Look at tests — they show intended usage patterns
- Look at config — `application.src`, proto files, deployment configs reveal structure

### How it's USED (practical)
- `jarvis_codesearch` — how do peer services use this? Search for imports/usages across repos
- `search_slack` — what questions do engineers ask about it? What problems do they hit?
- `search_jira_issues` — what bugs and features are filed? What's the backlog?

### How it CONNECTS to you (contextual)
- Does your service depend on this? Check `dependencies.jsonl`
- Does this depend on your service?
- What's the interface between your code and this system?
- Who's the team/oncall? Use `search_oncall` or `get_crew_details`

### What can go WRONG (operational)
- `observe-agent` — what does the monitoring look like? What alerts exist?
- `search_jira_issues` — common failure modes, past incidents
- `search_slack` — debugging war stories

## Step 3: Build the Mental Model

Synthesize findings into a structured mental model:

```
## Mental Model: [domain]

### What It Is (one paragraph)
[Explain like the user has never heard of it]

### Core Concepts (3-5 key terms)
- **[Concept 1]**: [what it means, why it matters]
- **[Concept 2]**: [what it means, why it matters]
- ...

### How It Works (the mechanics)
[Data flow / architecture / key components]
[Diagram if it helps — mermaid or ASCII]

### How It Connects To Your Work
- [Your service] uses [this domain] for [purpose]
- Interface: [API/Kafka/Espresso/gRPC]
- Key touchpoints: [specific classes, configs, topics]

### Common Gotchas
- [Thing that trips people up #1]
- [Thing that trips people up #2]

### Who Owns It
- Team: [team name]
- Oncall: [oncall rotation]
- Slack: [channel]
- Confluence: [space/page]

### Key Resources
- [Link to docs]
- [Link to getting started]
- [Link to architecture page]

### What To Explore Next
- [Specific sub-topic worth going deeper on]
- [Related domain that connects to this one]
```

## Step 4: Auto-Learn

Save the mental model as knowledge-track insights:
- One high-level insight for the overall domain (`rot_rate: slow` — core understanding decays slowly)
- Separate insights for specific gotchas (`rot_rate: medium` — details change faster)
- Tag with the domain name so future `/explore`, `/scope`, `/research` sessions find them

The mental model becomes the foundation — next time anyone (you or a future session) touches this domain, the knowledge base already has context.

## Step 5: Suggest Next Steps

Based on why the user is exploring:
- "Ready to `/scope` a feature in this area?"
- "Want to `/explore` a related domain? ([suggested domain])"
- "Want to go deeper? I can explore [specific sub-topic]."
- "Want to `/find` existing patterns for working with [domain]?"

## Integration

```
/explore euler
  → builds mental model (what, how, gotchas, who owns it)
  → saves as insights
  → user now has enough context to:
    → /scope a feature that uses Euler
    → /investigate a bug involving Euler
    → /find how other services interact with Euler
    → /verify a claim about Euler behavior
```

Explore feeds all other skills — it's the knowledge bootstrap.
