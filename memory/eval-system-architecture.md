---
name: Self-improving eval system architecture
description: How the eval system (/improve-agent), compound learning, and Auto Dream integrate. Three knowledge stores, one source of truth.
type: project
originSessionId: 27db5d4c-f39d-4ca8-b029-b22a12079f15
---
## Architecture: Three Knowledge Stores, One Source of Truth

The eval system (`/improve-agent`) is the source of truth. It writes to three stores:

```
/improve-agent (eval loop)
  │
  ├──▶ Auto Memory (memory/*.md)
  │    Auto Dream consolidates these between sessions.
  │    Files: eval-behavioral-gates.md, eval-principle-scores.md
  │    Format: frontmatter with type: feedback
  │
  ├──▶ Behavioral Gates (rules/behavioral-gates.md)
  │    Scout hook loads these for detailed rules.
  │    Updated each eval iteration.
  │
  └──▶ Compound Learning (learnings/)
       Insights, manifest, outcome tracking.
       Graduation, pruning, briefing updates.
```

**Why:** Auto Dream handles memory hygiene (prune stale, merge overlaps, fix dates). Our eval handles quality improvement (classify failures, simulate fixes, update gates). Compound learning handles cross-session intelligence (insights, outcomes). Each has a role.

**How to apply:** When `/improve-agent` produces findings, always update all three stores. When Auto Dream consolidates, it naturally maintains the eval memory files alongside other memories. When compound learning generates insights, they feed future eval runs.
