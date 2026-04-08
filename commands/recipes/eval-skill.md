---
name: eval-skill
description: Scaffold, run, and report eval cases for skills and recipes — regression protection for agent behavior
inputs: ["action", "skill_name"]
chain_to: learn
chain_when: "eval reveals unexpected behavior worth remembering"
---

## Usage

```
/recipe eval-skill scaffold [skill-name]   # Generate eval cases from skill definition
/recipe eval-skill run [skill-name]        # Run evals for a specific skill
/recipe eval-skill run-all                 # Run all available evals
/recipe eval-skill report [skill-name]     # Show latest results
```

## Steps: scaffold

Generate eval cases for a skill by reading its definition and inferring test scenarios.

1. **Read the skill definition** at `~/.claude/commands/{{skill_name}}.md` or `~/.claude/commands/recipes/{{skill_name}}.md`
2. **Read the eval schema** at `~/.claude/evals/SCHEMA.md`
3. **Identify test scenarios** from the skill:
   - **Happy path**: Invoke with valid arguments, check expected workflow
   - **Missing arguments**: Invoke without required inputs, check it asks for clarification
   - **Error/edge cases**: Based on the skill's `## On Failure` or error handling sections
   - **Chain triggers**: If skill has `chain_to`, verify chaining behavior
   - **Tool usage**: Which tools the skill SHOULD use (Read, Grep, Agent, etc.)
   - **Tool avoidance**: Which tools the skill should NOT use (e.g., destructive tools for read-only skills)
4. **Generate 3-6 eval cases** with 2-5 expectations each, mixing programmatic and LLM-judge
5. **Write** to `~/.claude/evals/{{skill_name}}.json`
6. **Present** the generated evals to the user for review before finalizing
7. User can edit/approve, then the file is ready for `run`

### Scaffolding Heuristics

- Skills that **read/analyze** (explore, scope, investigate) should test: `tool_called: Read`, `tool_called: Grep`, `tool_not_called: Edit`, `tool_not_called: Write`
- Skills that **write files** (learn, aha, eureka) in `dry_run` mode should test: `would_call_tool: Write`, `would_create_file` with path glob. In `live` mode: `file_created`, `file_contains` with expected frontmatter
- Skills that **modify code** (implement, recipe:test-first-fix) in `dry_run` mode should test: `would_call_tool: Edit`, `output_contains` for expected changes. In `live` mode: `tool_called: Edit`, `output_contains` for test results
- Skills with **chain_to** should have an eval case that triggers the chain condition
- All skills should have a **missing-argument** eval that checks for graceful handling

## Steps: run

Execute eval cases for a skill and grade results.

1. **Read** `~/.claude/evals/{{skill_name}}.json`
2. **Determine mode** — resolve `mode` per case (case-level overrides file-level, default `dry_run`)
3. **For each eval case**, in order:
   a. **Set up** — If `setup` exists, create any required files or state
   b. **Execute** — Spawn a sub-agent (Agent tool) with the eval's `prompt`
      - **`dry_run` mode**: Prepend to prompt: "Do NOT actually write any files. Instead, SIMULATE the full workflow and report what you WOULD do. Output an '## Eval Trace' section listing: (1) every tool called, (2) full text output, (3) every file you would have written."
      - **`live` mode**: Use `isolation: "worktree"` to keep writes sandboxed. Execute the skill fully.
      - Set a timeout matching the eval's `timeout_seconds` (default 120s)
      - Capture the agent's full output text and tool call history
   c. **Grade programmatic expectations**:
      - `tool_called` / `tool_not_called`: Check the agent's tool call log (read-side tools work in both modes)
      - `would_call_tool`: Check agent's Eval Trace for the tool name (dry_run only)
      - `would_create_file`: Check agent's Eval Trace for a file path matching the glob (dry_run only)
      - `output_contains` / `output_not_contains` / `output_matches`: Check agent output text
      - `file_created` / `file_contains` / `file_not_modified`: Check filesystem
      - Score: PASS or FAIL (binary)
   d. **Grade LLM-judge expectations**:
      - Present the agent's output + the criteria to your own judgment
      - Score: PASS / PARTIAL / FAIL with a one-line rationale
   e. **Clean up** — Remove any setup files/state
3. **Compile results** into a report:

```
Skill Eval Results: {{skill_name}}
===================================
Run: 2026-04-07T17:00:00Z

Eval: happy-path-with-argument (id: 1)
  [PASS] tool_called: Read                          (programmatic)
  [PASS] tool_called: Write                         (programmatic)
  [PASS] file_created: ~/.claude/learnings/...      (programmatic)
  [PASS] llm_judge: Classifies insight correctly    (qualitative)
  Result: 4/4 passed

Eval: missing-argument (id: 2)
  [PASS] output_contains: "what did you learn"      (programmatic)
  [PASS] tool_not_called: Write                     (programmatic)
  [FAIL] llm_judge: Asks exactly one clarifying Q   (qualitative)
    Reason: Asked two questions instead of one
  Result: 2/3 passed

Summary: 1/2 evals fully passed | 6/7 expectations passed
OVERALL: PARTIAL
```

4. **Save results** to `~/.claude/evals/results/{{skill_name}}-{{date}}.json`:
```json
{
  "skill": "skill-name",
  "run_date": "ISO timestamp",
  "overall": "PASS|PARTIAL|FAIL",
  "evals_passed": 1,
  "evals_total": 2,
  "expectations_passed": 6,
  "expectations_total": 7,
  "cases": [
    {
      "id": 1,
      "name": "happy-path",
      "result": "PASS",
      "expectations": [
        { "type": "tool_called", "tool": "Read", "result": "PASS" },
        { "type": "llm_judge", "criteria": "...", "result": "PASS", "rationale": "..." }
      ]
    }
  ]
}
```

5. **Present** the report to the user

## Steps: run-all

1. **List** all eval files: `~/.claude/evals/*.json` (excluding SCHEMA.md and results/)
2. **Run** each eval suite sequentially (using the `run` steps above)
3. **Compile** a cross-skill summary:

```
Eval Summary: All Skills
========================
Run: 2026-04-07

Skill            Evals    Expectations    Status
learn            3/3      12/12           PASS
investigate      2/3      8/10            PARTIAL
explore          3/3      9/9             PASS
test-first-fix   1/2      4/6             PARTIAL

Overall: 9/11 evals passed | 33/37 expectations passed
```

4. **Save** summary to `~/.claude/evals/results/summary-{{date}}.json`

## Steps: report

1. **Find** the latest result file for `{{skill_name}}` in `~/.claude/evals/results/`
   - If no skill specified, show the latest `summary-*.json`
2. **Read** and present the results
3. If previous runs exist, show **trend**: "Last 3 runs: PASS → PARTIAL → PASS"

## Expected Output

- `scaffold`: A well-structured evals.json file with 3-6 test cases per skill
- `run`: Executed evals with pass/fail results and LLM-judge rationale
- `run-all`: Cross-skill summary showing overall health
- `report`: Latest results with optional trend

## On Failure

- Skill file not found → list available skills and ask user to pick
- Eval file not found → suggest `scaffold` first
- Sub-agent timeout → mark that eval as TIMEOUT, continue with next
- Sub-agent error → mark as ERROR with message, continue with next
- All evals fail → chain to `/investigate` the skill definition
