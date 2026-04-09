---
name: improve-agent
description: "Cross-session quality eval and improvement loop for the AI Partner ecosystem"
inputs: ["action"]
chain_to: compound
chain_when: "improvement loop completes with accepted fixes"
---

# Improve Agent — Systematic Quality Improvement

Run the self-improving evaluation loop: measure AI Partner quality across sessions,
classify failures, simulate which fixes have highest impact, apply fixes, re-measure.

Modeled after the Oracle eval system (candidate-quality-oracle PRs #265, #300).

## Usage

```
/improve-agent run           # Full pipeline: export → judge → classify → simulate → report
/improve-agent judge         # Judge pre-exported sessions (resumes from judge_manifest.json)
/improve-agent report        # Regenerate report from existing verdicts
/improve-agent fix           # Apply highest-priority fix from latest report
/improve-agent loop [N]      # Run N improvement iterations (default: 3)
```

## Steps: run

### 1. Gather Session Data

Export recent sessions if not already exported:

```bash
ls ~/.claude/evals/sessions/
```

If empty or stale, export the last 5-10 sessions:
- Check `~/.claude/sessions/` for recent session IDs
- For each, read the session transcript
- Save to `~/.claude/evals/sessions/{session_id}.json`

Minimum 5 sessions for meaningful signal. Warn if fewer.

### 2. Run the Pipeline (Metrics + Judge Preparation)

```bash
python3 ~/claude-knowledge/evals/pipeline.py run --sessions ~/.claude/evals/sessions/
```

This loads sessions, builds judge inputs, and saves them to
`~/.claude/evals/results/agent-quality/judge_input_{session_id}.txt`.

### 3. Execute the Judge

For each judge input file in the manifest:

1. Read the judge input
2. Send to an LLM (use yourself — read the input and produce the verdict JSON)
3. Follow the judge_prompt.md instructions exactly
4. Save the verdict to `~/.claude/evals/results/agent-quality/verdict_{session_id}.json`

**Important**: The judge is YOU reading the session transcripts and producing structured
verdicts. This is the "LLM-as-judge" pattern from the Oracle system. Be rigorous.
Follow the taxonomy. Don't be generous — honest assessment drives real improvement.

After all sessions are judged:
- Collect all verdict files into `~/.claude/evals/results/agent-quality/verdicts.json`
- Re-run the pipeline to aggregate: `python3 ~/claude-knowledge/evals/pipeline.py run --sessions ~/.claude/evals/sessions/ --skip-judge`

### 4. Present Results

Open the generated HTML report and present to the user:
- Overall agreement rate (% of correct first approaches)
- Partnership score (weighted composite)
- Dominant failure type and fix route
- Signal detection rate (behavioral loop)
- Compound learning health
- Improvement simulation (what to fix first)

Ask the user: "The dominant failure type is `{type}`. The simulation shows fixing it
would improve agreement by +{delta}%. Should I apply the fix?"

### 5. Apply Fixes (with user approval)

Based on the dominant failure type, route to the appropriate fix:

| Fix Route | Action |
|-----------|--------|
| `review_rules` | Read the counterfactuals from verdicts. Identify the rule/gate that should have prevented the failures. Edit CLAUDE.md, memory files, or behavioral gates. |
| `review_skills` | Read the skill file(s) cited in fix_targets. Compare current instructions against the counterfactuals. Edit the skill .md to address the gap. |
| `review_retrieval` | Check scout hooks, manifest search logic, briefing content. Are the right insights being surfaced? Edit hooks or re-tag insights. |
| `create_skill` | Draft a new skill .md based on the workflow pattern. Follow existing skill conventions. Run `/integrate` after creation. |
| `no_fix` | No agent-side fix. Report `user_ambiguity` cases to the user for awareness. |

**Before applying any fix:**
- Snapshot the current state of the file being changed
- Present the proposed change to the user
- Only apply with explicit approval

### 6. Re-Measure (Regression Detection)

After applying a fix:
1. Re-run the judge on the SAME session corpus
2. Compare before/after metrics
3. Present delta to the user:

```
Before: agreement 62%, severity 0.72, signal detection 0.8
After:  agreement 68%, severity 0.78, signal detection 0.8
Delta:  +6% agreement, +0.06 severity, +0.0 signal detection
```

If any metric regressed, flag it. Ask user whether to keep or revert.

### 7. Feed Compound Learning + Auto Memory Integration

After the improvement loop, write findings to THREE places:

**A. Compound Learning System** (our insights):
- Write outcome-log entries for insights the judge identified as helpful/wrong
- Update insight scores based on the judge's insight audit
- Graduate insights that passed threshold (use_count >= 3, outcome_score >= 2.0)
- Prune insights the judge flagged as misleading
- Update agent-briefing.md with new quality metrics

**B. Auto Memory** (Anthropic's system — so Auto Dream can consolidate):
- Update `~/.claude/projects/-Users-bizhou/memory/eval-behavioral-gates.md` with latest gates
- Update `~/.claude/projects/-Users-bizhou/memory/eval-principle-scores.md` with latest scores
- Keep frontmatter format (name, description, type: feedback) so Auto Dream recognizes them
- Update MEMORY.md index if new memory files are added
- Auto Dream will then consolidate these with other memories between sessions

**C. Behavioral Gates** (our rules file, loaded by scout hook):
- Update `~/claude-knowledge/rules/behavioral-gates.md` with eval-driven gates
- This is the detailed version; the memory files are the summary Auto Dream maintains

**Why three places:** Auto Memory is what Auto Dream sees and consolidates. Behavioral gates are what the scout hook loads for detail. Compound learning is the cross-session intelligence. They serve different roles but must stay in sync. The eval system is the single source of truth — it writes to all three.

## Steps: judge

Resume judging from an existing `judge_manifest.json`:

1. Read `~/.claude/evals/results/agent-quality/judge_manifest.json`
2. For each entry with `status: "pending_judge"`:
   - Read the judge input file
   - Produce the verdict
   - Save to verdict file
3. Aggregate all verdicts
4. Generate report

## Steps: report

1. Read `~/.claude/evals/results/agent-quality/verdicts.json`
2. Run: `python3 ~/claude-knowledge/evals/pipeline.py report --results <latest_structured_results>`
3. Present the HTML report

## Steps: fix

1. Read the latest `structured_results_*.json`
2. Look at the improvement simulation — pick the highest priority_score
3. Read all verdicts with that failure type
4. Collect counterfactuals and fix_targets
5. Propose and apply the fix (with user approval)
6. Re-run judge for regression detection

## Steps: loop

Run N improvement iterations (default 3):

```
for i in 1..N:
  1. Run full pipeline (or reuse existing verdicts after iteration 1)
  2. Identify dominant failure type
  3. Apply fix (with user approval per iteration)
  4. Re-measure
  5. Present cumulative before/after
  6. If no improvement or user stops → break
```

After all iterations, present a cumulative report:
```
Loop Summary
============
Iteration 1: Fixed wrong_approach rules → +4% agreement
Iteration 2: Fixed investigate skill → +3% agreement
Iteration 3: Fixed scout retrieval → +2% agreement

Cumulative: 62% → 71% agreement (+9%)
```

## Key Design Decisions

1. **The judge is the AI Partner itself** — Reading its own session transcripts and
   producing structured verdicts. This is self-evaluation, not external review. The
   rigor comes from the structured taxonomy and the requirement to cite evidence.

2. **Insights are first-class citizens** — Every verdict includes an insight audit.
   The improvement loop directly feeds graduation, pruning, and outcome tracking.
   This closes the compound learning loop.

3. **Human behavioral awareness is 25% of the score** — This isn't just a code quality
   eval. The partnership dimension (signal detection, adaptation speed, proactive
   suggestions) matters as much as technical correctness.

4. **Fix one type per iteration** — Like the Oracle system, fix the highest-priority
   failure type, re-measure, then move to the next. Don't try to fix everything at once.

5. **Always re-measure** — No fix is accepted without regression detection. The Oracle
   team found that targeted improvements can cause overall regression due to stochasticity.
   Always check.

## On Failure

- No sessions exported → guide user through export
- Judge produces invalid JSON → retry with stricter instructions
- Fix causes regression → revert and try a different approach
- All failure types are `user_ambiguity` → nothing to fix; suggest the user improve prompt specificity
- < 5 sessions → warn about insufficient data, run anyway but flag low confidence

## Expected Output

- `~/.claude/evals/results/agent-quality/verdicts.json` — all session verdicts
- `~/.claude/evals/results/agent-quality/structured_results_YYYY-MM-DD.json` — aggregated metrics
- `~/.claude/evals/results/agent-quality/agent_quality_report_YYYY-MM-DD.html` — visual report
- Updated skills, rules, or hooks (depending on fix route)
- Outcome-log entries for the compound learning system
