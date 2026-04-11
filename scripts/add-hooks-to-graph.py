#!/usr/bin/env python3
"""Add hooks + evals layer to the knowledge graph HTML."""
import json
import re
import sys
from pathlib import Path

GRAPH_HTML = Path(__file__).parent.parent / "docs" / "knowledge-graph.html"

# ── Hook definitions: id, name, trigger, reads, writes, invokes ──────────────

HOOK_NODES = [
    {
        "id": "hooks/knowledge-scout.py",
        "name": "Knowledge Scout",
        "layer": "hooks",
        "trigger": "UserPromptSubmit",
        "desc": "Fast knowledge retrieval + auth preflight on every prompt. Reads manifest, scores insights, logs retrievals.",
    },
    {
        "id": "hooks/compound-learning-commit.py",
        "name": "Commit Logger",
        "layer": "hooks",
        "trigger": "PostToolUse (git commit)",
        "desc": "Logs commit metadata to commit-log.jsonl for compound learning.",
    },
    {
        "id": "hooks/compound-learning-pr.py",
        "name": "PR Logger",
        "layer": "hooks",
        "trigger": "PostToolUse (gh pr create)",
        "desc": "Logs PR metadata to pr-log.jsonl for compound learning.",
    },
    {
        "id": "hooks/score-insights.py",
        "name": "Insight Scorer",
        "layer": "hooks",
        "trigger": "Standalone (called by scout)",
        "desc": "Three-signal scoring: recency + relevance + importance. Ranks insights without LLM tokens.",
    },
    {
        "id": "hooks/vm-route-builds.py",
        "name": "VM Build Router",
        "layer": "hooks",
        "trigger": "PreToolUse (Bash)",
        "desc": "Intercepts mint/gradle build commands and redirects to VM via vm-run.",
    },
    {
        "id": "hooks/auto-allowlist.py",
        "name": "Auto Allowlist",
        "layer": "hooks",
        "trigger": "PostToolUse",
        "desc": "Auto-adds approved Bash commands to global allowlist. Syncs project rules to global.",
    },
    {
        "id": "hooks/post-edit-java-compile.py",
        "name": "Java Compile Check",
        "layer": "hooks",
        "trigger": "PostToolUse (Edit)",
        "desc": "Auto-compiles after Java file edits. Debounces multi-file batches. Catches type errors immediately.",
    },
    {
        "id": "hooks/pre-commit-build-check.py",
        "name": "Pre-Commit Build Gate",
        "layer": "hooks",
        "trigger": "PreToolUse (git commit)",
        "desc": "Verifies Java compilation before allowing git commit. Blocks on build failure.",
    },
    {
        "id": "hooks/async-results-check.py",
        "name": "Async Results Check",
        "layer": "hooks",
        "trigger": "UserPromptSubmit",
        "desc": "Checks for new VM delegate results in agentbus/results/. Surfaces notifications.",
    },
    {
        "id": "hooks/session-end-compound.agent",
        "name": "SessionEnd Compound Agent",
        "layer": "hooks",
        "trigger": "SessionEnd (agent)",
        "desc": "Full compound learning loop: context → diff → insights → memory → briefing → feedback → worklog.",
    },
    {
        "id": "evals/pipeline.py",
        "name": "Eval Pipeline",
        "layer": "evals",
        "trigger": "Manual (/improve-agent)",
        "desc": "Cross-session quality measurement. LLM judge, failure taxonomy, improvement simulation, HTML reports.",
    },
]

# ── Edges: hook → file it reads/writes/invokes ──────────────────────────────
# Format: (source, target, relation, keywords)

# ── Data layer nodes (logs, manifest, settings) that hooks connect through ────

DATA_NODES = [
    {
        "id": "learnings/manifest.jsonl",
        "name": "Manifest (search index)",
        "layer": "staging",
        "desc": "JSONL search index for all insights. 62 entries with scoring fields (use_count, outcome_score).",
    },
    {
        "id": "learnings/logs/commit-log.jsonl",
        "name": "Commit Log",
        "layer": "staging",
        "desc": "Append-only log of git commits. SessionEnd compound reads this for pattern extraction.",
    },
    {
        "id": "learnings/logs/pr-log.jsonl",
        "name": "PR Log",
        "layer": "staging",
        "desc": "Append-only log of PR creations. Captures branch, commits, PR URL.",
    },
    {
        "id": "learnings/logs/outcome-log.jsonl",
        "name": "Outcome Log",
        "layer": "staging",
        "desc": "Event stream of insight retrievals and outcomes. Tracks when insights help or mislead.",
    },
    {
        "id": "learnings/SCHEMA.md",
        "name": "Insight Schema",
        "layer": "staging",
        "desc": "334-line schema defining insight file format, manifest structure, scoring algorithm, graduation criteria.",
    },
    {
        "id": "settings/base.json",
        "name": "Settings (hooks config)",
        "layer": "rules",
        "desc": "Base settings defining all hook triggers (UserPromptSubmit, PostToolUse, PreToolUse, SessionEnd).",
    },
]

HOOK_EDGES = [
    # knowledge-scout reads
    ("hooks/knowledge-scout.py", "learnings/manifest.jsonl", "reads", ["manifest", "insights", "search-index"]),
    ("hooks/knowledge-scout.py", "learnings/SCHEMA.md", "reads", ["schema", "format"]),
    ("hooks/knowledge-scout.py", "commands/dream.md", "triggers", ["dream", "notifications", "lazy-dream"]),
    # knowledge-scout writes
    ("hooks/knowledge-scout.py", "learnings/logs/outcome-log.jsonl", "writes", ["retrieval", "use-count", "tracking"]),
    # knowledge-scout invokes
    ("hooks/knowledge-scout.py", "hooks/score-insights.py", "invokes", ["scoring", "ranking", "manifest"]),

    # commit logger writes
    ("hooks/compound-learning-commit.py", "learnings/logs/commit-log.jsonl", "writes", ["commit", "metadata", "logging"]),

    # PR logger writes
    ("hooks/compound-learning-pr.py", "learnings/logs/pr-log.jsonl", "writes", ["pr", "metadata", "logging"]),

    # score-insights reads
    ("hooks/score-insights.py", "learnings/manifest.jsonl", "reads", ["manifest", "scoring", "ranking"]),

    # vm-route-builds connects to delegate
    ("hooks/vm-route-builds.py", "skills/delegate/SKILL.md", "gates", ["vm", "build", "routing"]),

    # auto-allowlist reads/writes settings
    ("hooks/auto-allowlist.py", "settings/base.json", "reads+writes", ["permissions", "allowlist", "settings"]),

    # java compile connects to pre-commit
    ("hooks/post-edit-java-compile.py", "hooks/pre-commit-build-check.py", "related", ["java", "compile", "build-gate"]),

    # async results connects to delegate
    ("hooks/async-results-check.py", "skills/delegate/SKILL.md", "reads", ["agentbus", "results", "notifications"]),

    # SessionEnd compound agent reads everything
    ("hooks/session-end-compound.agent", "learnings/logs/commit-log.jsonl", "reads", ["commits", "context"]),
    ("hooks/session-end-compound.agent", "learnings/logs/pr-log.jsonl", "reads", ["prs", "context"]),
    ("hooks/session-end-compound.agent", "learnings/logs/outcome-log.jsonl", "reads+writes", ["outcomes", "scoring"]),
    ("hooks/session-end-compound.agent", "learnings/manifest.jsonl", "reads+writes", ["manifest", "graduation", "use-count"]),
    ("hooks/session-end-compound.agent", "commands/compound.md", "implements", ["compound", "learning", "loop"]),
    ("hooks/session-end-compound.agent", "learnings/SCHEMA.md", "follows", ["schema", "format", "frontmatter"]),
    # SessionEnd writes insights
    ("hooks/session-end-compound.agent", "hooks/knowledge-scout.py", "feeds", ["briefing", "next-session"]),

    # Eval pipeline reads
    ("evals/pipeline.py", "learnings/manifest.jsonl", "reads", ["manifest", "insights", "snapshot"]),
    ("evals/pipeline.py", "commands/improve-agent.md", "implements", ["eval", "judge", "quality"]),
    ("evals/pipeline.py", "rules/behavioral-gates.md", "reads+writes", ["gates", "failures", "improvements"]),
    ("evals/pipeline.py", "memory/eval/eval-behavioral-gates.md", "writes", ["eval", "findings", "gates"]),

    # Cross-hook connections
    ("hooks/knowledge-scout.py", "hooks/session-end-compound.agent", "cycle", ["feedback-loop", "read-write-cycle"]),
    ("hooks/compound-learning-commit.py", "hooks/session-end-compound.agent", "feeds", ["commit-log", "input"]),
    ("hooks/compound-learning-pr.py", "hooks/session-end-compound.agent", "feeds", ["pr-log", "input"]),
    ("evals/pipeline.py", "hooks/session-end-compound.agent", "evaluates", ["quality", "improvement"]),
]


def main():
    html = GRAPH_HTML.read_text()

    # Extract data between markers
    start_marker = "// ==GRAPH_DATA_START==\n"
    end_marker = "\n// ==GRAPH_DATA_END=="
    start_idx = html.index(start_marker) + len(start_marker)
    end_idx = html.index(end_marker)
    data_line = html[start_idx:end_idx]

    # Parse: "const GRAPH_DATA = {...};"
    json_str = data_line.replace("const GRAPH_DATA = ", "").rstrip(";")

    # The JSON may have issues with embedded file contents. Try to parse.
    # If it fails, use a regex approach to extract nodes and links separately.
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        print("JSON parse failed — trying repair approach...", file=sys.stderr)
        # Extract nodes array and links array separately
        # Find the nodes array
        nodes_start = json_str.index('"nodes"') + len('"nodes"') + 2  # skip ": ["
        # This is too fragile. Let's try a different approach.
        # Since the file was generated, let's regenerate from scratch.
        print("ERROR: Cannot parse existing graph data. Aborting.", file=sys.stderr)
        sys.exit(1)

    existing_ids = {n["id"] for n in data["nodes"]}

    # Add data layer nodes first
    for dnode in DATA_NODES:
        if dnode["id"] not in existing_ids:
            node = {
                "id": dnode["id"],
                "name": dnode["name"],
                "layer": dnode["layer"],
                "path": dnode["id"],
                "connections": 0,
                "content": dnode["desc"],
            }
            data["nodes"].append(node)
            existing_ids.add(dnode["id"])
            print(f"  + data: {dnode['name']} ({dnode['layer']})")

    # Add hook/eval nodes
    for hook in HOOK_NODES:
        if hook["id"] not in existing_ids:
            node = {
                "id": hook["id"],
                "name": hook["name"],
                "layer": hook["layer"],
                "path": hook["id"],
                "connections": 0,  # will be recalculated
                "content": f"**{hook['trigger']}**\n\n{hook['desc']}",
            }
            data["nodes"].append(node)
            existing_ids.add(hook["id"])
            print(f"  + node: {hook['name']} ({hook['layer']})")

    # Add edges (only where both source and target exist)
    existing_links = {(l["source"], l["target"]) for l in data["links"]}
    added = 0
    skipped_targets = set()
    for source, target, relation, keywords in HOOK_EDGES:
        if source not in existing_ids:
            continue
        if target not in existing_ids:
            skipped_targets.add(target)
            continue
        if (source, target) in existing_links or (target, source) in existing_links:
            continue
        link = {
            "source": source,
            "target": target,
            "strength": 8,  # moderate default
            "shared": [relation] + keywords,
        }
        data["links"].append(link)
        existing_links.add((source, target))
        added += 1

    if skipped_targets:
        print(f"  Skipped edges to missing nodes: {skipped_targets}", file=sys.stderr)

    # Recalculate connection counts
    conn_counts = {}
    for link in data["links"]:
        conn_counts[link["source"]] = conn_counts.get(link["source"], 0) + 1
        conn_counts[link["target"]] = conn_counts.get(link["target"], 0) + 1
    for node in data["nodes"]:
        node["connections"] = conn_counts.get(node["id"], 0)

    # Add colors for new layers
    print(f"\n  Added {len(HOOK_NODES)} hook/eval nodes, {added} edges")
    print(f"  Total: {len(data['nodes'])} nodes, {len(data['links'])} links")

    # Add hook/eval/data descriptions to contents dict
    if "contents" not in data:
        data["contents"] = {}
    for hook in HOOK_NODES:
        data["contents"][hook["id"]] = f"Trigger: {hook['trigger']}\n\n{hook['desc']}"
    for dnode in DATA_NODES:
        if dnode["id"] not in data["contents"]:
            data["contents"][dnode["id"]] = dnode["desc"]

    # Rebuild data line
    new_json = json.dumps(data, ensure_ascii=False)
    new_data_line = f"const GRAPH_DATA = {new_json};"

    # Replace in HTML
    new_html = html[:html.index(start_marker) + len(start_marker)] + new_data_line + html[end_idx:]

    # Add colors for hooks and evals layers
    old_colors = "memory: '#3fb950', staging: '#d29922', rules: '#f85149',\n  guides: '#a371f7', commands: '#58a6ff', skills: '#f778ba'"
    new_colors = "memory: '#3fb950', staging: '#d29922', rules: '#f85149',\n  guides: '#a371f7', commands: '#58a6ff', skills: '#f778ba',\n  hooks: '#ff7b72', evals: '#ffa657'"
    new_html = new_html.replace(old_colors, new_colors)

    GRAPH_HTML.write_text(new_html)
    print(f"\n  Written to {GRAPH_HTML}")


if __name__ == "__main__":
    main()
