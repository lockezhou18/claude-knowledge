---
description: "Skill tier definitions — loaded on demand when routing to skills/recipes"
---

# Skill Tiers
- **Tier 1: Skills** (`~/.claude/commands/*.md`) — universal, require judgment, always loaded
- **Tier 1.5: Capability tools** (`~/.claude/skills/`) — provide a capability (eyes, hands) that Tier 1 skills and Tier 3 recipes invoke. Not workflows themselves — they're the "how" behind other tiers' "what".
  - `playwright-cli` — browser eyes. Used by `/investigate` (reproduce UI issues), `/recipe ui-smoke-test` (post-deploy verification), `/recipe capture-ui-state` (PR evidence), `/recipe greenhouse-e2e` (sandbox testing), `/recipe ui-session` (record/replay/compare browser test sessions)
  - `observe-agent` — production eyes. Logs, metrics, dependencies.
  - `linkedin-cli-tools` — production hands. Build, deploy, gRPC calls.
  - `delegate` — remote execution hands. `vm-run` (sync+build on VM), direct SSH, file transfer. Used by `/implement` (builds), `/ship` (pre-PR validation), `/investigate` (remote gRPC/curli), `/pr-fix` (compile after fixes), `/oncall` (service queries). Auto-intercepted by PreToolUse hook for mint/gradlew commands. Always use `bash -c "..."` wrapper.
- **Tier 2: Project skills** (`{repo}/.claude/commands/`) — project-specific, loaded per repo
- **Tier 3: Recipes** (`~/.claude/commands/recipes/*.md`) — mechanical checklists, no judgment needed
- Recipes chain UP to skills when they detect issues needing judgment
- Skills chain DOWN to recipes for mechanical sub-tasks
- Skills and recipes invoke Tier 1.5 capabilities as needed
- The `/recipe from-history` command auto-creates recipes from manual steps just performed
