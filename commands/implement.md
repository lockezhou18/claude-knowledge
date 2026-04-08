# Implement — Execute a Plan Systematically

Take a plan (from Phase 3, a design doc, a Jira ticket, or an OpenSpec spec) and implement it task by task with tracked progress, incremental commits, and continuous verification.

**Usage:**
- `/implement` — implement the plan from the current conversation
- `/implement [plan file or Jira ticket]` — implement from a specific source
- `/implement continue` — resume implementation from where you left off

## What Makes Implement Different

- `/kickoff` = router — figures out what to do and where to start
- `/scope` / `/research` = understanding — builds context before acting
- **`/implement`** = execution — takes a plan and builds it, tracking progress
- `/compound` = retrospective — captures what was learned after

Implement is the "do the work" skill. It assumes you already know WHAT to build (from /scope + /research + plan). Now build it.

## Step 0: Load the Plan

Find the implementation source:
1. **From conversation**: If Phase 3 just produced a plan, use it directly
2. **From plan file**: `docs/plans/YYYY-MM-DD-*.md` or a path the user provides
3. **From Jira ticket**: Pull the ticket description and acceptance criteria
4. **From OpenSpec**: If an openspec change exists, run `openspec instructions apply --change "<name>" --json` to get the task list and context artifacts (proposal, design, spec)
5. **Resume**: Check `~/.claude/learnings/retrospectives/active-work.md` for in-progress implementation

**Present the plan to the user:**
```
## Implementation Plan: [name]
Source: [plan file / Jira / OpenSpec / conversation]

### Units (N total)
1. [ ] [Unit 1] — [goal, files to modify]
2. [ ] [Unit 2] — [goal, files to modify]
...

### Starting with Unit 1. Confirm?
```

Wait for confirmation before starting. (BEHAVIORAL GATE: don't assume — ask which unit to start with.)

## Step 0.5: Codebase Convention Audit (for non-trivial changes)

Before writing any code, audit the target codebase to prevent naming, structural, and architectural mistakes that are expensive to fix after implementation. Skip this for trivial changes (config tweaks, doc fixes, single-line bug fixes).

### 0.5a. Find 2-3 Similar Examples
Identify existing code that follows the same pattern as the planned change. If adding a new API endpoint, find an existing endpoint. If adding a new table, find an existing table's full stack.

### 0.5b. Trace Naming Conventions End-to-End
Follow one existing example through the full chain relevant to your change:
```
Proto file → Generated stubs → API/Resource class → Service interface → 
Service impl → Client → Factory → Wiring (DI/config) → Test location → 
Build config (coverage excludes, module registration)
```
Record the naming pattern at each layer. Note any prefixes, suffixes, or casing conventions.

### 0.5c. Verify Upstream/Downstream Contracts Field-by-Field
For any proto/API you depend on or expose:
- **Read the latest version** (pull latest, don't rely on stale copies)
- **Enumerate every field** in request and response — for each, trace where it comes from and where it goes
- Check what consumers actually read (not just what the schema defines)
- Check for name collisions (e.g., proto-generated classes vs hand-written classes)

### 0.5d. Document Conventions
Add a brief "Conventions" note to your progress tracking:
```
## Conventions (from audit)
- Class naming: [pattern found, e.g., Hp{Feature}Api, {Feature}Service, {Feature}ServiceImpl]
- Test location: [pattern found, e.g., same module, com.linkedin.{pkg}/]
- Wiring: [pattern found, e.g., OffspringBootListener, @Import, registerBean]
- Proto naming: [pattern found, e.g., file name matches service name inside]
```

If the plan's proposed names or patterns don't match what the audit found, **update the plan before proceeding**.

## Step 0.9: Choose Execution Mode

For the implementation units, choose one of two modes:

### Mode A: Standard (default)
Work through units in this session using the Step 1 cycle below. Best for:
- Small changes (1-3 units)
- Units that are tightly coupled and need shared context
- Exploratory work where the plan may change

### Mode B: Ralph Loop (autonomous batch)
Generate a `ralph-loop.sh` script that spawns a **fresh Claude session per task**. Best for:
- Large changes (4+ well-defined units)
- Independent units that don't need shared context
- Preventing context degradation on long implementations

To use Ralph Loop mode, tell the user:
```
This plan has N units. I can either:
A) Work through them here (good for coupled/exploratory work)
B) Generate a Ralph Loop script — fresh Claude session per task, 
   prevents context degradation (good for well-defined independent units)
```

If the user chooses Mode B, generate the script per the **Ralph Loop Generator** section at the bottom of this file, then hand off.

## Step 1: Work Through Units

For each implementation unit, follow this cycle:

```
Read → Test → Code → Test → Commit
```

### 1a. Read First
- Read the files to modify — understand the current state
- Check for existing patterns in the codebase that match the task
- If the plan specifies patterns to follow, read those examples

### 1b. Test First (when applicable)
- Use the **test-first-fix recipe** approach: write a failing test that defines the expected behavior
- For new features: write the test that will pass when the unit is complete
- For bug fixes: write the test that reproduces the bug
- Run the test to confirm it fails for the right reason
- Skip this step only for config changes, documentation, or scaffolding

### 1c. Code
- **Minimal implementation** — simplest code that makes the test pass
- Follow existing patterns in the codebase — don't invent new approaches
- If you hit something unexpected, surface it to the user before continuing (don't silently diverge from the plan)

### 1d. Verify
- Run the test — it should pass now
- Run the full module build: `mint build` or `./gradlew build` (via `linkedin-cli-tools:cli-tools`)
- If build fails, fix it yourself (don't ask the user for compilation errors)
- If build fails 3+ times on the same issue, stop and explain the blocker

### 1e. Commit
- Commit this unit with a descriptive message using `linkedin-dev-workflow:submit` or `git commit`
- The pre-commit build hook will verify compilation
- One commit per unit — not one massive commit at the end

### 1f. Update Progress
Mark the unit as done and show progress:
```
✓ Unit 1: [done]
→ Unit 2: [starting now]
  Unit 3: [pending]
```

## Step 2: Plan Verification (after each unit)

After completing each unit, check:
- **Does the implementation match the plan?** If drifting, surface it.
- **Are there deviations?** Document why in the commit message.
- **Did completing this unit reveal something that changes the remaining plan?** If so, propose the change to the user before continuing.

This is the OpenSpec "verify" concept applied continuously — don't wait until all units are done to check alignment.

## Step 3: Handle Blockers

When stuck:
- **Build fails repeatedly** → stop, explain, ask for help
- **Plan is ambiguous** → ask ONE clarifying question, don't guess
- **Dependency not available** → check `/watch-deps`, suggest workaround or stub
- **Unfamiliar code area** → run `/explore` or `/find` inline, then continue
- **Test can't be written** → ask user which test approach, or skip with explicit note

## Step 4: Completion

When all units are done:

### 4a. Final Verification
- Run full test suite (not just unit tests)
- Self-review the full diff: `git diff origin/main...HEAD`
- Check against the original plan — anything missing?
- Check for the common sins: unused imports, wrong types, missing error handling, pattern violations

### 4b. PR Creation
- Suggest creating the PR: "All units done. Create PR with `linkedin-dev-workflow:submit`?"
- The multi-persona review hook fires automatically on PR creation
- Include plan reference in PR description

### 4c. Update Active Work
- Update `~/.claude/learnings/retrospectives/active-work.md` with completion status
- Log to worklog: what was implemented, how many units, any deviations

### 4d. Suggest Compound
- "Implementation complete. Run `/checkpoint` to save progress, or `/compound` for full retrospective?"

## Multi-Session Implementation

If the work spans multiple sessions:
- After each session's work, update `active-work.md` with:
  - Which units are done
  - Which unit is next
  - Any blockers or deviations discovered
  - Branch name and last commit
- `/implement continue` picks up from here next session
- The agent briefing will show "Implementation in progress — Unit 3/5 done"

## Integration

```
/kickoff "build bulk import feature"
  → /scope (map the system)
  → /research (check approaches)
  → Plan (Phase 3 — break into units)
  → /implement (this skill — work through units)
    → Unit 1: Read → Test → Code → Verify → Commit
    → Unit 2: Read → Test → Code → Verify → Commit
    → ...
    → Final verification
    → PR creation (linkedin-dev-workflow:submit)
    → Multi-persona review (auto hook)
  → /compound (close the loop)
```

---

## Ralph Loop Generator

When the user selects Mode B, generate a `ralph-loop.sh` script. Place it alongside the plan source (e.g., in the repo root or the openspec change directory).

### Template

Generate the script by filling in `WORKTREE`, `TASKS`, and the per-task prompts from the plan:

```bash
#!/bin/bash
# ralph-loop.sh — Fresh-session-per-task autonomous implementation
# Spawns a new Claude Code session for each task, preventing context degradation.
#
# Usage: ./ralph-loop.sh
# Stop:  Ctrl+C (safe — each task commits before moving on)
# Resume: re-run ./ralph-loop.sh (skips completed tasks via progress file)

set -euo pipefail

WORKTREE="{{absolute_path_to_working_directory}}"
PROGRESS_FILE="$WORKTREE/.ralph-progress.md"
SUMMARY_FILE="$WORKTREE/.ralph-summary.md"

# Initialize progress files if they don't exist
if [ ! -f "$PROGRESS_FILE" ]; then
  echo "# Ralph Loop Progress" > "$PROGRESS_FILE"
  echo "" >> "$PROGRESS_FILE"
fi
if [ ! -f "$SUMMARY_FILE" ]; then
  echo "# Progress Summary" > "$SUMMARY_FILE"
  echo "" >> "$SUMMARY_FILE"
fi

# Task definitions — one per implementation unit
TASKS=(
{{for each unit: "Unit N: one-line description"}}
)

TASK_PROMPTS=(
{{for each unit: the full prompt with context, file paths, what to do, what to test}}
)

completed_count() {
  grep -c '^\- \[x\]' "$PROGRESS_FILE" 2>/dev/null || echo 0
}

TOTAL=${#TASKS[@]}
echo "Total tasks: $TOTAL, Completed: $(completed_count)"

for i in "${!TASKS[@]}"; do
  TASK_NUM=$((i + 1))
  TASK_NAME="${TASKS[$i]}"

  # Skip already-completed tasks
  if grep -q "^\- \[x\] $TASK_NAME" "$PROGRESS_FILE" 2>/dev/null; then
    echo "⏭  Skipping completed: $TASK_NAME"
    continue
  fi

  # Check for [HUMAN] gate
  if echo "$TASK_NAME" | grep -q '\[HUMAN\]'; then
    echo ""
    echo "============================================"
    echo "  STOPPED — Human gate reached"
    echo "  $TASK_NAME"
    echo "  Complete the manual step, then re-run."
    echo "============================================"
    exit 0
  fi

  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  Task $TASK_NUM/$TOTAL: $TASK_NAME"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Build the prompt with inter-iteration context
  CONTEXT="$(cat "$SUMMARY_FILE")"
  FULL_PROMPT="You are implementing task $TASK_NUM of $TOTAL in a multi-task plan.

## Prior Progress
$CONTEXT

## Current Task
${TASK_PROMPTS[$i]}

## Rules
- Work in: $WORKTREE
- Read existing code and follow codebase conventions before writing
- Run build + tests after changes
- Commit with a descriptive message when done
- Write a brief progress entry to $SUMMARY_FILE in this format:
  ## Task $TASK_NUM — $TASK_NAME
  - **Files changed:** [list]
  - **Key decisions:** [any notable choices]
  - **Issues:** [problems and resolutions, or 'None']
  - **Status:** Done
"

  # Spawn a fresh Claude session
  echo "$FULL_PROMPT" | claude --dangerously-skip-permissions -p - \
    --working-directory "$WORKTREE" \
    2>&1 | tee -a "$WORKTREE/.ralph-raw.log"

  EXIT_CODE=${PIPESTATUS[0]}

  if [ $EXIT_CODE -eq 0 ]; then
    # Mark task complete
    echo "- [x] $TASK_NAME" >> "$PROGRESS_FILE"
    echo "✅ Completed: $TASK_NAME"
  else
    echo "- [ ] $TASK_NAME — FAILED (exit $EXIT_CODE)" >> "$PROGRESS_FILE"
    echo "❌ Failed: $TASK_NAME (exit code $EXIT_CODE)"
    echo "   Check .ralph-raw.log for details. Fix and re-run."
    exit 1
  fi
done

echo ""
echo "🎉 All $TOTAL tasks complete!"
echo "   Progress: $PROGRESS_FILE"
echo "   Summary:  $SUMMARY_FILE"
echo "   Run 'git diff origin/main...HEAD' to review all changes."
```

### Generation Rules

When generating the script from a plan:

1. **Extract units** from the plan and create one `TASKS` entry and one `TASK_PROMPTS` entry per unit.
2. **Each task prompt must be self-contained** — include:
   - What to do (the unit goal)
   - Which files to modify (from the plan)
   - Which patterns to follow (from the Convention Audit in Step 0.5)
   - What to test
   - Any dependencies on prior tasks ("Task 2 added X in file Y — you'll need to import it")
3. **Add `[HUMAN]` gates** for tasks requiring manual intervention (deploy steps, credential setup, external system changes).
4. **Set `WORKTREE`** to the actual working directory.
5. **Make the script executable**: `chmod +x ralph-loop.sh`
6. **Tell the user**: "Run `./ralph-loop.sh` to start. Each task gets a fresh Claude session. Ctrl+C to stop safely. Re-run to resume from where you left off."

### Important Notes

- `--dangerously-skip-permissions` is required for non-interactive execution. Warn the user about this.
- Each task should commit its own changes — if a task fails, previous tasks' work is preserved.
- The `SUMMARY_FILE` provides inter-iteration context so each fresh session knows what came before.
- If the user doesn't have `claude` CLI available, fall back to Mode A (standard).
