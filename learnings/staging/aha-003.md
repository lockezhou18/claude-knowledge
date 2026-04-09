---
id: aha-003
track: knowledge
type: semantic
repos: ["*"]
tags: ["meta", "skills", "architecture", "tier-system", "capability-tools", "playwright-cli", "observe-agent", "linkedin-cli-tools", "pattern"]
severity: high
rot_rate: permanent
status: active
created: "2026-04-03"
last_verified: "2026-04-03"
use_count: 0
outcome_score: 0
visibility: team
origin_skill: aha
synthesized_from: ["eureka-002", "know-030"]
---

## Pattern

The skill ecosystem has three distinct categories, not two. **Tier 1.5 = capability tools** — they provide a *capability* (browser eyes, production eyes, production hands) rather than a *workflow* (Tier 1 skills that require judgment) or a *checklist* (Tier 3 recipes that follow steps mechanically).

The key distinction: **capabilities are the "how" that workflows and checklists invoke — they're not workflows themselves.**

## Evidence

- **playwright-cli** emerged as "browser eyes" — `/investigate` uses it to reproduce UI issues, `/recipe ui-smoke-test` uses it for post-deploy verification, `/recipe capture-ui-state` uses it for PR evidence. It doesn't have its own workflow — it's invoked BY workflows.
- **observe-agent** follows the same pattern — "production eyes." Skills like `/investigate`, `/triage-alert`, `/hp-pipeline-pem` all invoke it for logs/metrics, but it's not a workflow itself.
- **linkedin-cli-tools** = "production hands." `/ship`, `/deploy-check`, `/implement` all invoke it for build/deploy/gRPC, but it provides capability, not workflow.

## Implication

When adopting new tools into the ecosystem, first ask: **is this a workflow (requires judgment), a capability (provides eyes/hands), or a checklist (mechanical steps)?**

- Workflows → Tier 1 skill (`~/.claude/commands/`)
- Capabilities → Tier 1.5 tool (`~/.claude/skills/`) — then wire it into existing Tier 1 skills and Tier 3 recipes
- Checklists → Tier 3 recipe (`~/.claude/commands/recipes/`)

The adoption pattern for Tier 1.5 is: install the tool → create recipes that use it → update existing skills to invoke it → add to auth-preflight if it has auth state.

## When to Apply

When adding any new tool to the ecosystem: classify it as workflow/capability/checklist first. If it's a capability, the work is wiring it INTO existing tiers, not creating a new standalone workflow.
