# Ralph for Claude Code — Case Study of Harness Engineering

**Source:** https://github.com/frankbria/ralph-claude-code
**Stars:** 8.7K | **Version:** v0.11.5 | **Language:** Shell
**Fetched:** 2026-04-15

## Overview

Ralph is an autonomous AI development framework that enables continuous development cycles using Claude Code. Named after Geoffrey Huntley's "Ralph technique," it automates iterative project improvement with built-in safeguards against infinite loops and API overuse.

Core concept: "give Claude Code a task list, let it loop autonomously until done, with safety rails."

## Architecture

Three essential files per project:
- **`.ralph/PROMPT.md`** — Development instructions (what to build)
- **`.ralph/fix_plan.md`** — Prioritized task list (what's next)
- **`.ralph/AGENT.md`** — Build/run instructions (how to build)

Five-step loop:
1. Read instructions from PROMPT.md
2. Execute Claude Code with current context
3. Track progress (file changes, task completion)
4. Evaluate completion (dual-condition exit gate)
5. Repeat until done or limits hit

## Key Engineering Patterns

### Dual-Condition Exit Gate
Requires BOTH conditions before terminating:
- `completion_indicators >= 2` (heuristic pattern matching from output)
- AND Claude's explicit `EXIT_SIGNAL: true` in RALPH_STATUS block

Prevents both premature exit (heuristic false positive) and runaway looping (Claude never says done). Neither condition alone is sufficient.

### Circuit Breaker (Stagnation Detection)
- Opens after 3 loops with no file changes (ground truth, not self-report)
- Opens after 5 loops with identical errors
- Opens if output declines >70%
- 30-minute cooldown → HALF_OPEN → CLOSED recovery
- Two-stage error filtering eliminates false positives

### Rate Limiting
- 100 API calls/hour (configurable)
- Optional token budget (MAX_TOKENS_PER_HOUR)
- 5-hour API limit detection with wait-or-exit prompt

### Session Continuity
- Preserves Claude context across loop iterations
- 24-hour TTL prevents stale context accumulation
- Auto-reset on: circuit breaker open, project completion, manual interrupt
- Last 50 transitions logged for debugging

### Tool Permission Scoping
```bash
ALLOWED_TOOLS="Write,Read,Edit,Bash(git *),Bash(npm *),Bash(pytest)"
```
Explicit allowlist constrains the probabilistic core's action space.

## Test Coverage
566 tests, 100% pass rate. 477 unit + 136 integration across 18 test files.

---

## Cybernetic Analysis

Ralph is a minimal viable ultrastability loop for software development — same pattern as Karpathy's autoresearch but for code instead of ML experiments.

### Cybernetic Mapping

| Cybernetic Concept | Ralph Implementation |
|---|---|
| **Deterministic shell** | `ralph_loop.sh`, `.ralphrc` config, rate limits, circuit breaker, timeout |
| **Probabilistic core** | Claude Code executing against PROMPT.md + fix_plan.md |
| **Ultrastability L1** | Current working codebase (passes tests) |
| **Ultrastability L2** | Claude exploring modifications each loop iteration |
| **Crystallization** | Task marked complete in fix_plan.md → code committed |
| **Variety attenuation** | ALLOWED_TOOLS, timeout (15min), rate limit (100/hr), single focus (task list) |
| **Variety amplification** | Full tool access within bounds, session continuity preserving context |
| **Circuit breaker** | Beer's algedonic signal — bypass normal loop when system is stuck |
| **Exit detection** | Dual-condition gate = eigenform test — heuristic AND explicit signal must agree |
| **Session continuity** | Memory across loops — prevents context loss between iterations |
| **POSIWID** | "Did files change?" is ground truth, not "did Claude say it's done" |

### What Ralph Gets Right

1. **Dual-condition exit gate** — Both heuristic + explicit signal required. Prevents premature crystallization AND runaway exploration. A stability proof in miniature.

2. **Circuit breaker as S3* audit** — Doesn't trust Claude's self-report. Checks file changes (ground truth). This is Goodhart's Law protection — the audit metric (file changes) is uncorrelated with the agent's self-assessment.

3. **Rate limiting as variety attenuation** — Hard constraint forces efficient exploration. Like autoresearch's 5-min budget.

4. **Session continuity with expiration** — 24h TTL prevents stale context. This is decay/staleness management.

5. **POSIWID enforcement** — The system measures what Claude DOES (files changed, tests pass) not what it SAYS (completion signals). Beer's principle applied.

### What Ralph Lacks

| Gap | Ralph | Compound Learning Ecosystem |
|---|---|---|
| **Learning across runs** | None — each project starts fresh | Graduated insights, outcome scoring |
| **S4 (Intelligence)** | None — no research/adaptation | Scout, /research, authority-sources |
| **S5 (Identity)** | Just PROMPT.md — no persistent principles | Principle 0, engineering principles, MEMORY.md |
| **Outcome scoring** | Binary (task done / not done) | Multi-signal (use_count, outcome_score, freshness) |
| **Cross-session memory** | Session continuity within one project only | Memory architecture across all projects |
| **Self-improvement** | None — the harness never gets better | Eval pipeline, /improve-agent, compound learning |
| **Multi-agent** | Single Claude instance looping | Agent teams, parallel sub-agents, agentbus |
| **Depth calibration** | Fixed loop — same approach every iteration | Adaptive (quick/standard/deep/exhaustive) |

### Bateson Learning Level Classification

Ralph operates at **Learning I** — changing behavior based on feedback within a single project. Each loop iteration adjusts based on what Claude did last iteration, but the process itself never changes.

The compound learning ecosystem targets **Learning II** — changing the process of learning across projects. Insights graduate, principles evolve, the eval system improves the improvement process.

### Design Patterns Worth Borrowing

1. **Dual-condition exit gate** — Apply to insight graduation: both quantitative score AND qualitative review before promoting. Neither alone sufficient.

2. **Circuit breaker with ground truth** — Apply to compound learning: if N sessions pass with no measurable behavior change, the improvement process is stagnant. Halt and investigate.

3. **Session continuity with TTL** — Apply to memory: context should expire. 90-day staleness audit in dream.py serves this purpose.

4. **File changes as POSIWID metric** — Apply to eval: measure what the agent DOES (code changes, correct investigations, insight quality) not what it REPORTS (scores, self-assessments).

### Comparison: Three Harness Case Studies

| Dimension | autoresearch | Ralph | Compound Learning |
|---|---|---|---|
| **Domain** | ML experiments | Software development | Agent self-improvement |
| **Loop unit** | 5-min training run | Claude Code execution (~15 min) | One session (hours) |
| **Metric** | val_bpb (single, precise) | Task completion + file changes | outcome_score (multi-signal) |
| **Exit condition** | Improvement over baseline | Dual-condition gate | Graduation threshold (score >= 2.0) |
| **Shell complexity** | 3 files, ~500 lines | ~3K lines Shell + lib/ | 20+ skills, 8 hooks, eval pipeline |
| **Memory** | Current best only | Session continuity (24h) | Persistent across sessions/projects |
| **Learning level** | L0-L1 (no adaptation) | L1 (within-project adaptation) | L2 (meta-learning) |
| **What persists** | Best train.py | Completed code + tasks | Graduated insights, skills, principles |
| **Stars** | ~10K | 8.7K | N/A (internal) |

All three prove the same cybernetic pattern: deterministic shell + probabilistic core + crystallization-on-improvement = stable progress through uncertainty.
