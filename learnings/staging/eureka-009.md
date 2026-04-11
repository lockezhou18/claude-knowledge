---
id: eureka-009
track: knowledge
type: semantic
status: active
name: Static HTML knowledge graph makes compound learning observable
description: Embedding all knowledge (178 files, 6 layers) into a single D3.js HTML file with clickable nodes, content panels, and connection highlighting — zero server, zero API, regenerated nightly by dream.py
created: 2026-04-11
last_verified: 2026-04-11
repos: [memory-migration, claude-knowledge]
tags: [eureka, visualization, knowledge-graph, d3js, compound-learning, observability]
severity: critical
use_count: 0
outcome_score: 0.0
rot_rate: permanent
origin_skill: eureka
---

## Breakthrough
A single static HTML file with embedded JSON can visualize an entire compound learning ecosystem — 178 files across 6 layers, 479 connections, fully navigable with content preview — with zero infrastructure.

## The Old Way
Knowledge lived in flat files across directories. You could grep, read manifests, or ask Claude about connections. But the relationships between a staging insight, a project memory, a graduated insight, and a skill were invisible. You had to hold the mental model in your head. When someone new (or a future session) arrived, they started from scratch.

## The New Way
`build-knowledge-graph.py` scans all 6 layers (memory, staging, rules, guides, commands, skills), extracts keywords, computes Jaccard overlap, clusters by connected components, and generates:
1. `INDEX.md` — markdown knowledge graph (for Claude/GitHub)
2. `docs/knowledge-graph.html` — interactive D3.js force-directed graph (for humans)

The HTML embeds ALL file contents (truncated to 2000 chars). Click any node → detail panel shows content + connections. No server, no API, no build step. Just `open knowledge-graph.html`.

Regenerated nightly by dream.py's REBUILD phase. Always current.

## Impact
- **Observability**: Can literally see how an oncall investigation connects to a staging insight connects to a graduated memory connects to a skill
- **Onboarding**: New session or new person opens one file, sees everything
- **Debugging**: When knowledge seems stale or disconnected, the graph shows orphaned nodes and weak clusters
- **Pattern**: static HTML + embedded JSON + D3.js is reusable for ANY knowledge system

## Risks & Caveats
- File grows with ecosystem (currently 372KB — manageable, but watch at 500+ files)
- Content truncation (2000 chars) may miss important details in long files
- Keyword-based connections miss semantic relationships (LLM could improve this)

## Next Steps
- Add to dream.py notification: "Knowledge graph updated: N new connections"
- Consider GitHub Pages deployment for team viewing
- Explore LLM-enhanced connection detection (semantic similarity, not just keyword overlap)
