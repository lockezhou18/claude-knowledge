# Recipe — Create or Run Lightweight Automation

Create, run, or manage recipes — mechanical checklists that don't need judgment.

**Usage:**
- `/recipe run [name] [inputs...]` — run an existing recipe
- `/recipe create [name]` — create a new recipe interactively
- `/recipe list` — list all available recipes
- `/recipe from-history` — create a recipe from steps you just performed

## Run a Recipe

1. Find the recipe in `~/.claude/commands/recipes/[name].md`
2. If recipe has `project:` field, check we're in the right repo
3. Substitute `{{input}}` placeholders with provided values
4. Execute steps sequentially
5. At each step, check for success/failure
6. **On failure**: check the recipe's `## On Failure` section
7. **Chain condition met**: if `chain_when` condition matches, suggest the chained skill:
   "Recipe detected [condition]. Escalating to `/[chain_to]`."
8. Present results

## Create a Recipe

Ask the user:
1. **What does it do?** (one sentence)
2. **What inputs does it need?** (parameters)
3. **What are the steps?** (walk through them — can demonstrate by doing)
4. **What does success look like?**
5. **What should happen on failure?** (chain to a skill? retry? alert?)
6. **Is it project-specific?** (which repo, or global?)

Write to `~/.claude/commands/recipes/[name].md` using the recipe format from README.md.

After creation, ask: "Run `/integrate [name]` to wire it in?"

## Create from History (`/recipe from-history`)

This is the power move. When the user just performed a multi-step task manually:

1. Look at the recent conversation — what commands were run? What files were read/edited?
2. Extract the mechanical steps (skip the thinking/judgment parts)
3. Identify which values should become `{{input}}` parameters
4. Identify where things could fail and what skill should handle it
5. Generate the recipe and present it for approval

Example:
```
User just ran:
  go-status -f prod-ltx1 -a hp-ats-integration-mt
  git log --oneline -5
  gh pr list --state merged --limit 5
  
Agent: "Looks like a deploy check pattern. Create a recipe?"

Recipe generated:
  name: deploy-check-hp-ats
  inputs: [fabric]
  steps:
    1. go-status -f {{fabric}} -a hp-ats-integration-mt
    2. git log --oneline -5
    3. gh pr list --state merged --limit 5
  chain_to: investigate
  chain_when: "deployed version doesn't include latest merged PR"
```

## List Recipes

Scan `~/.claude/commands/recipes/*.md` (excluding README.md):
```
## Available Recipes

### Global
- deploy-check — Check deploy status across fabrics
- sync-test-data — Refresh test data from Greenhouse sandbox

### Project: hp-ats-integration-mt
- check-stages — Verify stage mapping for a connected project
- candidate-status — Check candidate sync status end-to-end
```

## Chaining Rules

### Recipe → Skill (escalation)
When a recipe detects something that needs judgment, it chains UP:
```yaml
chain_to: investigate      # which skill to suggest
chain_when: "error found"  # when to chain (pattern match on step output)
```
The agent says: "Recipe found [issue]. Want me to `/investigate`?"

### Skill → Recipe (delegation)
Any Tier 1 skill can call a recipe for mechanical sub-tasks:
- `/investigate` needs deploy info → runs deploy-check recipe inline
- `/scope` needs service topology → runs service-topology recipe inline
- `/verify` needs to check metrics → runs check-metrics recipe inline

The skill doesn't need to know the recipe's steps — just call it and use the output.

### Recipe → Recipe (chaining)
Recipes can chain to other recipes for multi-step automation:
```yaml
chain_to: recipe:notify-team    # chain to another recipe (prefix with "recipe:")
chain_when: "success"
```
