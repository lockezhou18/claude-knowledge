# Recipes — Lightweight Automation

Recipes are NOT skills. They don't require judgment — they're checklists the agent follows mechanically.

## Recipe vs Skill

| | Skill | Recipe |
|--|-------|--------|
| **Requires judgment?** | Yes | No — just follow the steps |
| **Ceremony** | Full markdown with phases | Minimal — steps + inputs |
| **Lifetime** | Long-lived, universal | May be disposable or project-specific |
| **Example** | /investigate (requires hypothesis-first thinking) | deploy-check (run these 5 commands) |

## Recipe Format

```yaml
---
name: recipe-name
description: What this recipe does (one line)
inputs: ["param1", "param2"]    # What the user provides
chain_to: investigate            # Optional: which skill to suggest after completion
chain_when: "failure detected"   # Optional: condition for chaining
project: hp-ats-integration-mt   # Optional: project-scoped (blank = global)
---

## Steps
1. [Step with {{param1}} placeholder]
2. [Step]
3. [Step]

## Expected Output
[What success looks like]

## On Failure
[What to do if a step fails — often chains to a skill]
```

## Chaining: Recipes → Skills

Recipes can chain UP to skills when they detect something that needs judgment:

```
Recipe: deploy-check
  Step 1: go-status -f prod-ltx1 → got version
  Step 2: compare with expected → MISMATCH DETECTED
  → Chains to: /investigate "version mismatch in prod"

Recipe: sync-test-data  
  Step 1: query Greenhouse API → got data
  Step 2: compare with HP → DISCREPANCY FOUND
  → Chains to: /verify "Greenhouse data matches HP"

Recipe: check-pem
  Step 1: fetch PEM metrics → availability below SLA
  → Chains to: /hp-pipeline-pem for full investigation
```

The recipe handles the mechanical part. When it hits something that needs thinking, it escalates to a skill.

## Skills can also call DOWN to recipes:

```
/investigate finds root cause → needs to verify deploy state
  → Calls recipe: deploy-check
  → Recipe returns version info
  → /investigate uses it to continue analysis

/scope mapping a system → needs current deploy topology
  → Calls recipe: service-topology
  → Recipe returns which fabrics, which versions
  → /scope uses it in the architecture map
```

This is how tiers chain:
```
Tier 1 (Skills — thinking)
  ↕ calls / chains to
Tier 3 (Recipes — mechanical)
  ↕ escalates when judgment needed
Tier 1 (Skills — thinking)
```
