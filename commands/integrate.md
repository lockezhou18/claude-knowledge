# Integrate — Wire a New Skill Into the Ecosystem

After creating or modifying a skill, automatically update all connected components so the ecosystem stays coherent.

**Usage:**
- `/integrate [skill-name]` — integrate a specific new/modified skill
- `/integrate all` — re-integrate all custom skills (full ecosystem sync)

## What Gets Updated

When a new skill is created, these components need to know about it:

### 1. Rules (MEMORY.md)

Read `~/.claude/rules/MEMORY.md`. Check if the new skill should be:
- **Referenced in the pipeline phases** — does it belong in Research, Clarify, Plan, Execute, Review, or Compound?
- **Added to proactive suggestions** — when should the agent suggest this skill unprompted?
- **Connected to existing rules** — does it reinforce or extend an existing rule?

If yes, update the relevant section. Don't add bloat — only add if the skill fills a gap.

### 2. Kickoff Orchestrator

Read `~/.claude/commands/kickoff.md`. Check:
- **Intent routing table** — should this skill appear as a starting point for a new intent?
- **Handoff suggestions** — should other skills suggest this one as a next step?
- **Skill map** — update the skill map at the bottom if it exists

### 3. Knowledge Base Schema (SCHEMA.md)

Read `~/.claude/learnings/SCHEMA.md`. Check:
- **New tags needed** — does the skill introduce a new domain that needs tag taxonomy entries?
- **New track type** — does it need a new insight track (like review-track, decision-track)?
- **Task-type router** — should the scoring system recognize a new task type for this skill?

### 4. Agent Briefing Template

The SessionEnd hook generates `agent-briefing.md`. Check if:
- The new skill produces artifacts that should be summarized in the briefing
- The new skill has a watchlist, log, or output file that the briefing should reference

### 5. E2E Tests

Read `~/test-rules-e2e.sh`. Add a test case for the new skill:
- Design a prompt that should trigger the skill's behavior
- Define a grep assertion that verifies the rule is followed
- Append to the test file

### 5b. Skill Evals

Scaffold behavioral evals for the new skill:
- Run the logic from `/recipe eval-skill scaffold [skill-name]`
- Generate 3-6 eval cases covering happy path, missing args, error handling, and chain triggers
- Write to `~/.claude/evals/[skill-name].json`
- See `~/.claude/evals/SCHEMA.md` for the eval format

### 6. Cross-Skill Handoffs

Read all skills in `~/.claude/commands/`. For each existing skill, check:
- Should the existing skill suggest the new skill at its completion?
- Should the new skill suggest existing skills at its completion?
- Update the handoff sections of affected skills

### 7. Compound Phase

Check if `/compound` should track outputs from the new skill:
- Does the skill generate logs that compound should review?
- Does the skill produce insights that compound should score?
- Update compound.md if needed

## Execution

### For `/integrate [skill-name]`:
1. Read the new skill file
2. Understand its purpose, triggers, inputs, outputs
3. Run through checks 1-7 above
4. Make updates (ask user before modifying existing skills)
5. Present a summary of what was integrated

### For `/integrate all`:
1. List all skills in `~/.claude/commands/`
2. Read each one
3. Build a complete skill map with handoffs
4. Check all 7 integration points for consistency
5. Fix any gaps or stale references
6. Present a full ecosystem health report:

```
## Ecosystem Health Report

### Skill Map
[complete map of all skills with handoff connections]

### Integration Status
| Skill | In Rules | In Kickoff | Has Tests | Has Evals | Has Handoffs | Compound Aware |
|-------|----------|------------|-----------|-----------|--------------|----------------|
| ...   | ✓        | ✓          | ✗         | ✓         | ✓            | ✓              |

### Gaps Found
- [skill X] not referenced in kickoff routing
- [skill Y] has no test coverage
- [skill Z] doesn't suggest next steps

### Actions Taken
- Updated [file] to add [what]
```

## Auto-Integration Rule

When ANY new `.md` file is created in `~/.claude/commands/`, the agent should proactively ask:
"New skill created. Run `/integrate [name]` to wire it into the ecosystem?"

This ensures nothing is created in isolation.
