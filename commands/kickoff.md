# Kickoff — Smart Orchestrator

Assess what the user needs and guide them through the right skills in the right order. NOT a rigid pipeline — adapts to context, skips what's unnecessary, loops back when needed.

**Usage:**
- `/kickoff [anything]` — describe what you want to do, the orchestrator figures out the path

## Step 1: Assess Intent

Read the user's input and classify:

| Intent | Signals | Start With |
|--------|---------|------------|
| **New feature** | "add", "build", "create", "implement", PRD, Jira ticket | `/scope` → clarify → plan (or `mae-core:architect` for complex) → execute |
| **Complex design** | "architect", "design system", "plan large", multi-service | `mae-core:architect` (parallel Claude + Codex planners) |
| **Bug fix** | "fix", "broken", "error", "bug", specific symptom | `/investigate` → fix → test |
| **Debugging** | "why", "failing", "not working", alert, PEM | `/investigate` |
| **Oncall** | "alert", "pager", "incident", "sev" | `/oncall` |
| **Exploration** | "how does", "understand", "what is", "map" | `/scope` |
| **Find existing** | "is there", "has anyone", "existing", "already", "reuse" | `/find` |
| **Research** | "best practice", "should we", "compare", "options" | `/research` |
| **Refactor** | "clean up", "simplify", "refactor", "migrate" | `/scope` → plan → execute |
| **Continue** | "resume", "where was I", "continue" | Read `active-work.md` → resume at last phase |

If unclear, ask ONE question: "Are you building something new, fixing something broken, or exploring?"

## Step 2: Run the Appropriate Skill

Don't re-implement skills — invoke them. Each skill already has its full workflow defined.

## Step 3: At Each Skill's Completion, Suggest What's Next

This is the key integration point. When a skill finishes, the orchestrator suggests (not forces) the natural next step:

```
After /scope completes:
  → "Found 3 unknowns. Want to /research them?"
  → "This looks like something others may have solved. /find existing solutions?"
  → "Requirements clear? Ready to plan?"
  → "Need to clarify with PM first? Here are the open questions."

After /find completes:
  → Found solution → "Adapt this? I'll plan the implementation."
  → Nothing found → "/research to design from scratch?"
  → Partial match → "/scope the found solution's codebase to understand it better?"

After /research completes:
  → "Ready to plan the implementation?"
  → "Want to /find if someone's built this already?"
  → "Want to /scope a related area first?"

After /investigate completes:
  → "Root cause found. Should I save it? (/learn)"
  → "This connects to [past incident]. Capture the pattern? (/aha)"
  → "Ready to fix? I'll plan the fix."

After plan is approved:
  → "Starting execution. I'll work through units and check in."
  → "Create a branch first? Use `linkedin-dev-workflow:start` for LinkedIn naming convention."
  → Use `linkedin-cli-tools:cli-tools` for build/test commands (mint build, mint test)

After execution completes:
  → "Ready for review? I'll self-review the diff."
  → "Run `mint build` to verify?" (linkedin-cli-tools)
  → "Want to create the PR? Use `linkedin-dev-workflow:submit` — multi-persona review will auto-run."

After PR is created/merged:
  → "Check CI status? Use `linkedin-dev-workflow:pr-check`"
  → "Run /compound to close the loop?"

At ANY point:
  → If agent notices a pattern → "I see a connection to [X]. Capture it? (/aha)"
  → If agent discovers something big → "This is significant — save as /eureka?"
  → If agent hits unfamiliar territory → "I need to /research [topic] before continuing."
  → If user wants to stop → Save progress to active-work.md, suggest /compound
```

## Step 4: Context Preservation

If work spans multiple sessions:
- Save current phase + progress to `active-work.md`
- Next session, briefing shows: "In progress: [feature] — last at [phase]. Resume?"
- `/kickoff resume` or `/kickoff continue` picks up where you left off

## The Principle

**The orchestrator is a router, not a rail.** 

It knows the full map of skills and suggests the right one based on context. But the user can jump to any skill at any time. The pipeline phases (Research → Clarify → Plan → Execute → Review → Compound) are a default path, not a mandatory sequence.

```
    /scope ←──────────────────────────────────────┐
      ↓ (suggests)                                 │
    /research ←── loop back if unknowns found ────┘
      ↓ (suggests)
    Clarify (inline)
      ↓ (suggests)
    Plan (inline)
      ↓ (suggests)
    Execute (inline)
      ↓ (suggests)
    Review (auto via hook)
      ↓ (suggests)
    /compound

    At any point: /learn, /aha, /eureka, /investigate, /research
    At any point: pause → active-work.md → resume next session
```
