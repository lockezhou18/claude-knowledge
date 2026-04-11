# Workflow Rules

## Two-Phase Explore-Then-Implement Pattern

For complex tasks that require understanding unfamiliar code (new features, cross-file refactors, business logic changes):

1. **Phase 1 — Explore**: Spawn an Explore sub-agent to research the codebase. Return a concise summary of key classes, methods, patterns, and enums involved. Do NOT start implementing.
2. **Review**: Present the summary to the user for confirmation and course-correction before writing any code.
3. **Phase 2 — Implement**: Only after user confirms the exploration summary, begin implementation with a clear plan.

**Why**: User prefers targeted action over open-ended searching. Avoid spending 20+ tool calls exploring without producing code. Keep the main conversation context clean by offloading exploration to sub-agents.

**Exception**: Skip phase 1 for simple/targeted tasks where the scope is already clear (single-file edits, known file paths, small bug fixes).

## Config File Editing Rule

When editing config files (tmux.conf, shell configs, settings.json, allowlists, etc.):

1. **Read the existing file first** — always understand what's already there.
2. **Make targeted additions/edits** — use the Edit tool to change only what's needed. Never replace the entire file.
3. **Preserve existing settings** — don't overwrite or reorganize the user's existing config.
4. **Confirm before overwriting** — if a full rewrite is truly necessary, ask first.

**Why**: User has been burned by Claude replacing entire configs (tmux, allowlists), requiring rollbacks and wasted time.

## Build & Test Rule

When making code changes in Java projects:

1. **Always run tests** before considering a task complete.
2. **Run from the correct directory** — use `mint build` or the appropriate build command from the correct module directory, not the repo root.
3. **If tests fail, fix them** — don't leave the task in a broken state.

**Why**: Multiple sessions had friction from running builds in the wrong directory or not running tests, leading to incomplete outcomes.

## Visual Artifacts: Open, Don't Suggest

When generating or modifying HTML files (graphs, reports, visualizations, diagrams):

1. **`open` the file immediately** — don't say "you can open this to verify."
2. In cmux, the browser renders in the adjacent pane — zero context switch.
3. For verification, screenshot after opening if needed.

**Why**: User uses cmux split panes. `open file://` renders on the right while terminal stays on the left. Visual verification becomes part of the coding loop, not a manual step.
