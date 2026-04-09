#!/usr/bin/env python3
"""
Agent Eval Pipeline — Cross-session quality measurement and improvement.

Modeled after the Oracle eval system (candidate-quality-oracle).
Measures agent behavior quality across sessions using an LLM judge,
classifies failures, simulates improvements, and generates HTML reports.

Usage:
    python pipeline.py run --sessions <dir>              # Full pipeline
    python pipeline.py run --sessions <dir> --skip-judge # Metrics only (fast)
    python pipeline.py report --results <file>           # Regenerate HTML report
    python pipeline.py simulate --results <file>         # Run improvement simulation
"""

import argparse
import json
import os
import sys
import glob
import datetime
from pathlib import Path
from collections import Counter, defaultdict

# ── Paths ──────────────────────────────────────────────────────────────────────

EVALS_DIR = Path(__file__).parent
RESULTS_DIR = EVALS_DIR / "results" / "agent-quality"
TAXONOMY_PATH = EVALS_DIR / "failure_taxonomy.md"
JUDGE_PROMPT_PATH = EVALS_DIR / "judge_prompt.md"
LEARNINGS_DIR = Path.home() / "claude-knowledge" / "learnings"
MANIFEST_PATH = LEARNINGS_DIR / "manifest.jsonl"
BRIEFING_PATH = LEARNINGS_DIR / "agent-briefing.md"
MEMORY_DIR = Path.home() / "claude-knowledge" / "rules"

# ── Constants ──────────────────────────────────────────────────────────────────

FAILURE_TYPES = [
    "wrong_approach",
    "skill_deficiency",
    "skill_gap",
    "context_miss",
    "over_engineering",
    "tool_misuse",
    "user_ambiguity",
]

SEVERITY_WEIGHTS = {
    "wrong_approach": 3.0,
    "context_miss": 2.5,
    "skill_deficiency": 2.0,
    "over_engineering": 1.5,
    "tool_misuse": 1.0,
    "skill_gap": 1.0,
    "user_ambiguity": 0.0,
}

FIX_ROUTES = {
    "wrong_approach": "review_rules",
    "context_miss": "review_retrieval",
    "skill_deficiency": "review_skills",
    "over_engineering": "review_rules",
    "tool_misuse": "review_rules",
    "skill_gap": "create_skill",
    "user_ambiguity": "no_fix",
}


# ── Stage 1: Load Sessions ────────────────────────────────────────────────────

def load_sessions(sessions_dir: str) -> list[dict]:
    """Load exported session transcripts from a directory.

    Expected format: each session is a .jsonl file (one JSON object per message)
    or a .json file with the full session array.
    """
    sessions = []
    session_files = sorted(
        glob.glob(os.path.join(sessions_dir, "*.json"))
        + glob.glob(os.path.join(sessions_dir, "*.jsonl"))
    )

    for fpath in session_files:
        try:
            with open(fpath, "r") as f:
                if fpath.endswith(".jsonl"):
                    messages = [json.loads(line) for line in f if line.strip()]
                else:
                    messages = json.load(f)

            session = {
                "session_id": Path(fpath).stem,
                "file_path": fpath,
                "messages": messages if isinstance(messages, list) else [messages],
                "metadata": _extract_metadata(messages),
            }
            sessions.append(session)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  WARN: Skipping {fpath}: {e}", file=sys.stderr)

    print(f"Loaded {len(sessions)} sessions from {sessions_dir}")
    return sessions


def _extract_metadata(messages) -> dict:
    """Extract session metadata from message content."""
    if isinstance(messages, dict):
        return messages.get("metadata", {})

    # Try to extract from first/last messages
    metadata = {}
    if messages:
        first = messages[0] if isinstance(messages[0], dict) else {}
        metadata["start_time"] = first.get("timestamp", "unknown")
        if len(messages) > 1:
            last = messages[-1] if isinstance(messages[-1], dict) else {}
            metadata["end_time"] = last.get("timestamp", "unknown")
        metadata["message_count"] = len(messages)
    return metadata


# ── Stage 2: Load Context (Insights + Memories) ───────────────────────────────

def load_insight_snapshot() -> dict:
    """Load the current manifest as the insight snapshot.

    In production, this should load the manifest as it was at session time.
    For now, uses the current manifest (assumes sessions are recent).
    """
    insights = {}
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    iid = entry.get("id", entry.get("file", "unknown"))
                    insights[iid] = entry
                except json.JSONDecodeError:
                    continue
    print(f"  Loaded {len(insights)} insights from manifest")
    return insights


def load_feedback_memories() -> list[dict]:
    """Load all feedback-type memory files."""
    memories = []
    memory_dir = Path.home() / ".claude" / "projects" / "-Users-bizhou" / "memory"

    if not memory_dir.exists():
        return memories

    for fpath in memory_dir.glob("feedback*.md"):
        try:
            content = fpath.read_text()
            memories.append({
                "id": fpath.stem,
                "file": str(fpath),
                "content": content,
            })
        except Exception:
            continue

    print(f"  Loaded {len(memories)} feedback memories")
    return memories


def load_agent_briefing() -> str:
    """Load the agent briefing content."""
    if BRIEFING_PATH.exists():
        return BRIEFING_PATH.read_text()
    return ""


# ── Stage 3: Judge ─────────────────────────────────────────────────────────────

def build_judge_input(session: dict, insights: dict, memories: list, briefing: str) -> str:
    """Construct the full input for the LLM judge.

    This builds a prompt that includes:
    1. The judge instructions (from judge_prompt.md)
    2. The session transcript
    3. The insight snapshot
    4. The feedback memories
    5. The agent briefing
    """
    judge_instructions = JUDGE_PROMPT_PATH.read_text()

    # Truncate session to avoid token limits — keep first/last N messages
    messages = session["messages"]
    MAX_MESSAGES = 200
    if len(messages) > MAX_MESSAGES:
        half = MAX_MESSAGES // 2
        messages = messages[:half] + [{"role": "system", "content": f"... {len(messages) - MAX_MESSAGES} messages truncated ..."}] + messages[-half:]

    # Build insight summary (not full content — just IDs, tags, summaries)
    insight_summary = []
    for iid, entry in insights.items():
        insight_summary.append({
            "id": iid,
            "tags": entry.get("tags", []),
            "summary": entry.get("summary_tokens", entry.get("summary", "")),
            "status": entry.get("status", "active"),
            "outcome_score": entry.get("outcome_score", 0),
        })

    prompt = f"""
{judge_instructions}

---

## SESSION TRANSCRIPT

```json
{json.dumps(messages, indent=2, default=str)[:100000]}
```

## SESSION METADATA

```json
{json.dumps(session.get('metadata', {}), indent=2, default=str)}
```

## AGENT BRIEFING (what the agent knew at session start)

```
{briefing[:5000]}
```

## INSIGHT SNAPSHOT ({len(insight_summary)} insights available at session time)

```json
{json.dumps(insight_summary, indent=2, default=str)[:20000]}
```

## FEEDBACK MEMORIES ({len(memories)} active rules)

```json
{json.dumps([{"id": m["id"], "content": m["content"][:500]} for m in memories], indent=2, default=str)[:10000]}
```

---

Now evaluate this session. Return a single JSON object matching the schema in Step 3.
"""
    return prompt


def run_judge_on_session(session: dict, insights: dict, memories: list, briefing: str) -> dict:
    """Run the LLM judge on a single session.

    This function is designed to be called by the /improve-agent skill,
    which handles the actual LLM API call. The pipeline script prepares
    the input; the skill orchestrates the execution.

    Returns: judge verdict dict matching the Step 3 schema.
    """
    judge_input = build_judge_input(session, insights, memories, briefing)

    # Write the judge input to a temp file for the skill to consume
    input_path = RESULTS_DIR / f"judge_input_{session['session_id']}.txt"
    input_path.parent.mkdir(parents=True, exist_ok=True)
    input_path.write_text(judge_input)

    print(f"  Judge input written to: {input_path}")
    print(f"  Size: {len(judge_input):,} chars")

    # Return placeholder — the skill will fill this with actual LLM output
    return {
        "session_id": session["session_id"],
        "status": "pending_judge",
        "judge_input_path": str(input_path),
    }


# ── Stage 4: Classify & Aggregate ─────────────────────────────────────────────

def aggregate_verdicts(verdicts: list[dict]) -> dict:
    """Aggregate judge verdicts across sessions into a quality report.

    Input: list of per-session verdict dicts (output of judge Step 3).
    Output: cross-session quality metrics including behavioral loop and compound learning.
    """
    total_tasks = 0
    total_correct = 0
    total_redirections = 0
    failure_counts = Counter()
    severity_total = 0.0
    insight_stats = {
        "total_hits": 0,
        "total_misses": 0,
        "total_wrong": 0,
        "total_violations": 0,
    }

    # Behavioral loop aggregation
    behavioral_signals_detected = 0
    behavioral_signals_total = 0
    adaptation_speeds = Counter()
    proactive_appropriate = 0
    proactive_pushy = 0
    proactive_missed = 0

    # Compound learning aggregation
    compound_insights_generated = 0
    compound_duplicates = 0
    compound_loops_closed = 0
    compound_sessions = 0
    all_graduation_candidates = set()
    all_prune_candidates = set()
    all_stale_candidates = set()

    # Session scores
    session_scores = []
    session_summaries = []

    for verdict in verdicts:
        if verdict.get("status") == "pending_judge":
            continue

        n_tasks = verdict.get("total_tasks", 0)
        n_correct = verdict.get("correct_first_approach", 0)
        total_tasks += n_tasks
        total_correct += n_correct
        total_redirections += verdict.get("total_redirections", 0)

        for ftype, count in verdict.get("failure_distribution", {}).items():
            failure_counts[ftype] += count
            severity_total += SEVERITY_WEIGHTS.get(ftype, 0) * count

        # Aggregate insight stats
        isummary = verdict.get("insight_summary", {})
        for key in insight_stats:
            insight_stats[key] += isummary.get(key, 0)

        # Aggregate behavioral loop
        bloop = verdict.get("behavioral_loop", {})
        behavioral_signals_detected += bloop.get("signals_detected", 0)
        behavioral_signals_total += bloop.get("signals_total", 0)
        for speed, count in bloop.get("adaptation_speed_distribution", {}).items():
            adaptation_speeds[speed] += count
        psug = bloop.get("proactive_suggestions", {})
        proactive_appropriate += psug.get("appropriate", 0)
        proactive_pushy += psug.get("pushy", 0)
        proactive_missed += psug.get("missed", 0)

        # Aggregate compound learning
        clearn = verdict.get("compound_learning", {})
        compound_insights_generated += clearn.get("insights_generated", 0)
        compound_duplicates += clearn.get("duplicates_created", 0)
        if clearn.get("loop_closed"):
            compound_loops_closed += 1
        compound_sessions += 1
        all_graduation_candidates.update(clearn.get("graduation_candidates", []))
        all_prune_candidates.update(clearn.get("prune_candidates", []))
        all_stale_candidates.update(clearn.get("stale_candidates", []))

        # Session score
        if "session_score" in verdict:
            session_scores.append(verdict["session_score"])

        session_summaries.append({
            "session_id": verdict.get("session_id"),
            "session_date": verdict.get("session_date"),
            "agreement_rate": verdict.get("agreement_rate", 0),
            "dominant_failure": verdict.get("dominant_failure_type"),
            "session_score": verdict.get("session_score"),
            "tasks": n_tasks,
            "correct": n_correct,
        })

    agreement_rate = (total_correct / total_tasks * 100) if total_tasks > 0 else 0
    max_severity = 3.0 * total_tasks if total_tasks > 0 else 1
    severity_score = 1 - (severity_total / max_severity)
    signal_detection_rate = (behavioral_signals_detected / behavioral_signals_total) if behavioral_signals_total > 0 else 1.0

    return {
        "run_date": datetime.datetime.now().isoformat(),
        "sessions_evaluated": len([v for v in verdicts if v.get("status") != "pending_judge"]),
        "total_tasks": total_tasks,
        "total_correct": total_correct,
        "agreement_rate": round(agreement_rate, 1),
        "avg_redirections": round(total_redirections / max(total_tasks, 1), 2),
        "severity_weighted_score": round(severity_score, 3),
        "failure_distribution": dict(failure_counts.most_common()),
        "dominant_failure_type": failure_counts.most_common(1)[0][0] if failure_counts else None,
        "insight_stats": insight_stats,
        "behavioral_loop": {
            "signal_detection_rate": round(signal_detection_rate, 3),
            "signals_detected": behavioral_signals_detected,
            "signals_total": behavioral_signals_total,
            "adaptation_speeds": dict(adaptation_speeds),
            "proactive_suggestions": {
                "appropriate": proactive_appropriate,
                "pushy": proactive_pushy,
                "missed": proactive_missed,
            },
        },
        "compound_learning": {
            "insights_generated": compound_insights_generated,
            "duplicates_created": compound_duplicates,
            "loops_closed": compound_loops_closed,
            "sessions_total": compound_sessions,
            "loop_closure_rate": round(compound_loops_closed / max(compound_sessions, 1), 2),
            "graduation_candidates": sorted(all_graduation_candidates),
            "prune_candidates": sorted(all_prune_candidates),
            "stale_candidates": sorted(all_stale_candidates),
        },
        "avg_session_score": round(sum(session_scores) / max(len(session_scores), 1), 3) if session_scores else None,
        "session_summaries": session_summaries,
    }


# ── Stage 5: Simulate Improvements ────────────────────────────────────────────

def simulate_improvements(report: dict) -> list[dict]:
    """For each failure type, simulate what agreement rate would be if all
    failures of that type were fixed.

    Mirrors Oracle's delta-kappa simulation — answers: "What should we fix first?"
    """
    total = report["total_tasks"]
    correct = report["total_correct"]
    current_rate = report["agreement_rate"]

    if total == 0:
        return []

    simulations = []
    for ftype in FAILURE_TYPES:
        count = report["failure_distribution"].get(ftype, 0)
        if count == 0 or ftype == "user_ambiguity":
            continue

        simulated_correct = correct + count
        simulated_rate = round(simulated_correct / total * 100, 1)
        delta = round(simulated_rate - current_rate, 1)

        simulations.append({
            "failure_type": ftype,
            "current_count": count,
            "fix_route": FIX_ROUTES[ftype],
            "simulated_agreement_rate": simulated_rate,
            "delta_agreement": delta,
            "severity_weight": SEVERITY_WEIGHTS[ftype],
            "priority_score": round(delta * SEVERITY_WEIGHTS[ftype], 1),
        })

    # Sort by priority score (highest first)
    simulations.sort(key=lambda x: x["priority_score"], reverse=True)
    return simulations


# ── Stage 6: Generate Report ───────────────────────────────────────────────────

def generate_html_report(report: dict, simulations: list[dict], output_path: str) -> str:
    """Generate an HTML report summarizing agent quality metrics."""

    failure_rows = ""
    for ftype in FAILURE_TYPES:
        count = report["failure_distribution"].get(ftype, 0)
        pct = round(count / max(report["total_tasks"], 1) * 100, 1)
        weight = SEVERITY_WEIGHTS[ftype]
        route = FIX_ROUTES[ftype]
        failure_rows += f"""
        <tr>
          <td><code>{ftype}</code></td>
          <td>{count}</td>
          <td>{pct}%</td>
          <td>{weight}</td>
          <td><code>{route}</code></td>
        </tr>"""

    simulation_rows = ""
    for sim in simulations:
        simulation_rows += f"""
        <tr>
          <td><code>{sim['failure_type']}</code></td>
          <td>{sim['current_count']}</td>
          <td>{sim['simulated_agreement_rate']}%</td>
          <td style="color: green;">+{sim['delta_agreement']}%</td>
          <td>{sim['priority_score']}</td>
          <td><code>{sim['fix_route']}</code></td>
        </tr>"""

    session_rows = ""
    for s in report.get("session_summaries", []):
        color = "green" if (s.get("agreement_rate", 0) or 0) >= 70 else "orange" if (s.get("agreement_rate", 0) or 0) >= 50 else "red"
        session_rows += f"""
        <tr>
          <td>{s.get('session_id', 'unknown')}</td>
          <td>{s.get('session_date', 'unknown')}</td>
          <td>{s.get('tasks', 0)}</td>
          <td>{s.get('correct', 0)}</td>
          <td style="color: {color};">{s.get('agreement_rate', 0)}%</td>
          <td><code>{s.get('dominant_failure', 'none')}</code></td>
        </tr>"""

    istats = report.get("insight_stats", {})
    bloop = report.get("behavioral_loop", {})
    clearn = report.get("compound_learning", {})
    avg_score = report.get("avg_session_score")

    html = f"""<!DOCTYPE html>
<html>
<head>
  <title>Agent Quality Report — {report['run_date'][:10]}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; background: #f8f9fa; }}
    h1 {{ color: #1a1a2e; }}
    h2 {{ color: #16213e; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 32px; }}
    .metrics {{ display: flex; gap: 16px; flex-wrap: wrap; margin: 20px 0; }}
    .card {{ background: white; border-radius: 8px; padding: 20px; min-width: 160px;
             box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }}
    .card .value {{ font-size: 2em; font-weight: bold; }}
    .card .label {{ color: #666; font-size: 0.9em; margin-top: 4px; }}
    .card.green .value {{ color: #16a34a; }}
    .card.orange .value {{ color: #ea580c; }}
    .card.red .value {{ color: #dc2626; }}
    table {{ border-collapse: collapse; width: 100%; background: white; border-radius: 8px;
             box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin: 16px 0; }}
    th, td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
    th {{ background: #f1f5f9; font-weight: 600; }}
    code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
    .priority {{ background: #fef3c7; font-weight: bold; }}
    .section-note {{ color: #666; font-style: italic; margin-bottom: 16px; }}
  </style>
</head>
<body>
  <h1>Agent Quality Report</h1>
  <p>Generated: {report['run_date']} | Sessions: {report['sessions_evaluated']} | Tasks: {report['total_tasks']}</p>

  <h2>Overall Metrics</h2>
  <div class="metrics">
    <div class="card {'green' if report['agreement_rate'] >= 70 else 'orange' if report['agreement_rate'] >= 50 else 'red'}">
      <div class="value">{report['agreement_rate']}%</div>
      <div class="label">Agreement Rate</div>
    </div>
    <div class="card">
      <div class="value">{report['total_correct']}/{report['total_tasks']}</div>
      <div class="label">Correct First Approach</div>
    </div>
    <div class="card">
      <div class="value">{report['avg_redirections']}</div>
      <div class="label">Avg Redirections/Task</div>
    </div>
    <div class="card {'green' if report['severity_weighted_score'] >= 0.7 else 'orange' if report['severity_weighted_score'] >= 0.5 else 'red'}">
      <div class="value">{report['severity_weighted_score']}</div>
      <div class="label">Severity Score (1.0 = perfect)</div>
    </div>
    <div class="card">
      <div class="value"><code>{report.get('dominant_failure_type', 'none')}</code></div>
      <div class="label">Dominant Failure</div>
    </div>
  </div>

  {'<h2>Partnership Score</h2>' + f'<div class="metrics"><div class="card {"green" if avg_score and avg_score >= 0.7 else "orange" if avg_score and avg_score >= 0.5 else "red"}"><div class="value">{avg_score if avg_score else "N/A"}</div><div class="label">Avg Session Score (0-1)</div></div></div>' if avg_score else ''}

  <h2>Human Behavioral Loop</h2>
  <div class="metrics">
    <div class="card {'green' if bloop.get('signal_detection_rate', 0) >= 0.8 else 'orange' if bloop.get('signal_detection_rate', 0) >= 0.6 else 'red'}">
      <div class="value">{bloop.get('signal_detection_rate', 'N/A')}</div>
      <div class="label">Signal Detection Rate</div>
    </div>
    <div class="card">
      <div class="value">{bloop.get('signals_detected', 0)}/{bloop.get('signals_total', 0)}</div>
      <div class="label">Signals Detected</div>
    </div>
    <div class="card green">
      <div class="value">{bloop.get('proactive_suggestions', {{}}).get('appropriate', 0)}</div>
      <div class="label">Good Suggestions</div>
    </div>
    <div class="card orange">
      <div class="value">{bloop.get('proactive_suggestions', {{}}).get('pushy', 0)}</div>
      <div class="label">Pushy Suggestions</div>
    </div>
    <div class="card red">
      <div class="value">{bloop.get('proactive_suggestions', {{}}).get('missed', 0)}</div>
      <div class="label">Missed Opportunities</div>
    </div>
  </div>

  <h2>Compound Learning System</h2>
  <div class="metrics">
    <div class="card">
      <div class="value">{clearn.get('insights_generated', 0)}</div>
      <div class="label">Insights Generated</div>
    </div>
    <div class="card red">
      <div class="value">{clearn.get('duplicates_created', 0)}</div>
      <div class="label">Duplicates Created</div>
    </div>
    <div class="card {'green' if clearn.get('loop_closure_rate', 0) >= 0.8 else 'orange'}">
      <div class="value">{clearn.get('loops_closed', 0)}/{clearn.get('sessions_total', 0)}</div>
      <div class="label">Loops Closed</div>
    </div>
    <div class="card green">
      <div class="value">{len(clearn.get('graduation_candidates', []))}</div>
      <div class="label">Graduation Candidates</div>
    </div>
    <div class="card orange">
      <div class="value">{len(clearn.get('prune_candidates', []))}</div>
      <div class="label">Prune Candidates</div>
    </div>
  </div>

  <h2>Insight System Health</h2>
  <div class="metrics">
    <div class="card green">
      <div class="value">{istats.get('total_hits', 0)}</div>
      <div class="label">Insight Hits</div>
    </div>
    <div class="card red">
      <div class="value">{istats.get('total_misses', 0)}</div>
      <div class="label">Insight Misses</div>
    </div>
    <div class="card orange">
      <div class="value">{istats.get('total_wrong', 0)}</div>
      <div class="label">Misleading Insights</div>
    </div>
    <div class="card red">
      <div class="value">{istats.get('total_violations', 0)}</div>
      <div class="label">Rule Violations</div>
    </div>
  </div>

  <h2>Failure Distribution</h2>
  <p class="section-note">Classified using the 7-type failure taxonomy. Priority chain: wrong_approach > context_miss > skill_deficiency > over_engineering > tool_misuse > skill_gap > user_ambiguity</p>
  <table>
    <tr><th>Failure Type</th><th>Count</th><th>% of Tasks</th><th>Severity Weight</th><th>Fix Route</th></tr>
    {failure_rows}
  </table>

  <h2>Improvement Simulation</h2>
  <p class="section-note">What would agreement rate be if ALL failures of each type were fixed? Sorted by priority score (delta x severity).</p>
  <table>
    <tr><th>Failure Type</th><th>Count</th><th>Simulated Rate</th><th>Delta</th><th>Priority Score</th><th>Fix Route</th></tr>
    {simulation_rows}
  </table>

  <h2>Per-Session Breakdown</h2>
  <table>
    <tr><th>Session</th><th>Date</th><th>Tasks</th><th>Correct</th><th>Agreement</th><th>Dominant Failure</th></tr>
    {session_rows}
  </table>
</body>
</html>"""

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Report written to: {output_path}")
    return output_path


# ── CLI ────────────────────────────────────────────────────────────────────────

def cmd_run(args):
    """Full pipeline: load sessions → build judge inputs → classify → simulate → report."""
    print("=" * 60)
    print("Agent Quality Pipeline")
    print("=" * 60)

    # Stage 1: Load sessions
    print("\n[Stage 1] Loading sessions...")
    sessions = load_sessions(args.sessions)
    if not sessions:
        print("ERROR: No sessions found. Export sessions first with /export-session.")
        sys.exit(1)

    # Stage 2: Load context
    print("\n[Stage 2] Loading context...")
    insights = load_insight_snapshot()
    memories = load_feedback_memories()
    briefing = load_agent_briefing()

    # Stage 3: Judge
    if not args.skip_judge:
        print(f"\n[Stage 3] Preparing judge inputs for {len(sessions)} sessions...")
        judge_results = []
        for session in sessions:
            print(f"  Judging: {session['session_id']}")
            result = run_judge_on_session(session, insights, memories, briefing)
            judge_results.append(result)

        # Save judge input manifest
        manifest_path = RESULTS_DIR / "judge_manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, "w") as f:
            json.dump(judge_results, f, indent=2)
        print(f"\n  Judge manifest: {manifest_path}")
        print(f"  Run /improve-agent to execute the judge and complete the pipeline.")
    else:
        print("\n[Stage 3] Skipped (--skip-judge)")

    # If we have existing verdicts, aggregate them
    verdicts_path = RESULTS_DIR / "verdicts.json"
    if verdicts_path.exists():
        print(f"\n[Stage 4] Aggregating existing verdicts from {verdicts_path}...")
        with open(verdicts_path) as f:
            verdicts = json.load(f)

        report = aggregate_verdicts(verdicts)

        # Stage 5: Simulate
        print("\n[Stage 5] Simulating improvements...")
        simulations = simulate_improvements(report)
        for sim in simulations:
            print(f"  Fix {sim['failure_type']}: +{sim['delta_agreement']}% agreement (priority: {sim['priority_score']})")

        # Save structured results
        results_path = RESULTS_DIR / f"structured_results_{datetime.date.today()}.json"
        full_results = {"report": report, "simulations": simulations, "verdicts": verdicts}
        with open(results_path, "w") as f:
            json.dump(full_results, f, indent=2, default=str)
        print(f"\n  Results: {results_path}")

        # Stage 6: HTML report
        print("\n[Stage 6] Generating HTML report...")
        report_path = RESULTS_DIR / f"agent_quality_report_{datetime.date.today()}.html"
        generate_html_report(report, simulations, str(report_path))
    else:
        print(f"\n  No verdicts yet. Run the judge first, then re-run the pipeline.")


def cmd_report(args):
    """Regenerate HTML report from existing results."""
    with open(args.results) as f:
        data = json.load(f)
    report = data["report"]
    simulations = data.get("simulations", simulate_improvements(report))
    output = args.output or str(RESULTS_DIR / f"agent_quality_report_{datetime.date.today()}.html")
    generate_html_report(report, simulations, output)


def cmd_simulate(args):
    """Run improvement simulation on existing results."""
    with open(args.results) as f:
        data = json.load(f)
    report = data["report"]
    simulations = simulate_improvements(report)
    print("\nImprovement Simulation")
    print("=" * 60)
    print(f"Current agreement rate: {report['agreement_rate']}%\n")
    for sim in simulations:
        print(f"  Fix {sim['failure_type']:20s} → {sim['simulated_agreement_rate']}% (+{sim['delta_agreement']}%) [priority: {sim['priority_score']}]")
    print(f"\n  Fix route priority: {simulations[0]['fix_route'] if simulations else 'none'}")


def main():
    parser = argparse.ArgumentParser(description="Agent Quality Eval Pipeline")
    subparsers = parser.add_subparsers(dest="command")

    # run
    run_parser = subparsers.add_parser("run", help="Run full pipeline")
    run_parser.add_argument("--sessions", required=True, help="Directory containing session exports")
    run_parser.add_argument("--skip-judge", action="store_true", help="Skip judge stage (metrics only)")

    # report
    report_parser = subparsers.add_parser("report", help="Regenerate HTML report")
    report_parser.add_argument("--results", required=True, help="Path to structured_results.json")
    report_parser.add_argument("--output", help="Output HTML path")

    # simulate
    sim_parser = subparsers.add_parser("simulate", help="Run improvement simulation")
    sim_parser.add_argument("--results", required=True, help="Path to structured_results.json")

    args = parser.parse_args()
    if args.command == "run":
        cmd_run(args)
    elif args.command == "report":
        cmd_report(args)
    elif args.command == "simulate":
        cmd_simulate(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
