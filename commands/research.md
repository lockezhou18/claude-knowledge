# Research — Deep Investigation Before Action

Run Phase 1 of the engineering pipeline as a standalone skill. Use when you want thorough research before making decisions, or when investigating without implementing.

**Usage:** `/research [topic or question]`

If no argument provided, ask the user: "What do you want to research?"

## Layer 1: Local Knowledge (always)

1. Read `~/.claude/learnings/agent-briefing.md` for session context and hot insights.
2. Search `~/.claude/learnings/manifest.jsonl` for related insights — filter by tags/repo matching the topic. Read top 3-5 matched insight files.
3. Read relevant memory files from `~/.claude/projects/-Users-bizhou/memory/` (check MEMORY.md index first).
4. Search git history in the current repo: `git log --oneline --all --grep="keyword" -20` and `git log --oneline -30` for recent changes in the area.
5. Search for related PRs: `gh pr list --search "keyword" --state all --limit 10`.
6. Read the code — look for business logic, understand why systems were built the way they are. If documentation doesn't exist, the code is the documentation. Use `jarvis_codesearch` for cross-repo (see search-guides/code-search.md for filter syntax).
7. Check logs/metrics — use `observe-agent` to verify runtime behavior matches code expectations. See search-guides/logs-metrics.md.

## Layer 2: Company Knowledge (for non-trivial topics)

8. **Broad search first**: Use `unified_context_search` to search code + wiki + Slack + Jira in one call when you're not sure where the answer lives.
9. **Jira**: Search for related tickets (open AND resolved/closed). Use `search_jira_issues`. Look for prior art, design decisions, known issues, rejected approaches. See search-guides/jira.md.
10. **Confluence**: Search for design docs, architecture decisions, runbooks. Use `search_confluence_content` or `get_confluence_page`. See search-guides/wiki-confluence.md.
11. **Slack**: Search for recent discussions — use the exception-first pattern for errors. Use `search_slack`. See search-guides/slack.md.
12. **GitHub Pages / internal docs**: READMEs, architecture docs, API references. Use `search_github_pages`.
13. **Infrastructure specs**: Use `linkedin-framework:infra-specs-expert` for questions about LinkedIn infrastructure (Espresso, Kafka, D2, Venice).
14. **Library specs**: Use `library-specs:download` then `library-specs:skills` for dependency documentation.

## Layer 3: External Knowledge (for unfamiliar territory)

11. Check `~/.claude/learnings/authority-sources.md` for research strategy and source examples by domain.
12. **Official documentation first** — the technology's own docs are ground truth.
13. **Engineering blogs from companies at scale** — search for "[technology] best practices" or "[problem] architecture [scale]". Don't limit to a fixed list.
14. **Research papers** — for cutting-edge or novel problems. Search arXiv, Semantic Scholar, Google Scholar.
15. **Standards and RFCs** — for protocol-level decisions. IETF, OWASP, W3C, OpenAPI specs.
16. **Cross-reference** — verify across 2-3 sources before trusting any single one for architecture or security decisions.
17. **Library specs** — use the library-specs plugin for dependency documentation.

## Layer 4: Synthesis (always)

18. **Explore 2-3 alternatives.** What's the simplest approach? What are the trade-offs? Is there a higher-upside alternative? Don't lock onto the first approach.
19. **Identify risks.** Ask: "What is the most risky part?" and "What am I missing?"
20. **Check for contradictions.** Did different sources disagree? Surface this to the user.

## Output

Present findings to the user as a structured brief:

```
## Research: [topic]

### What I Found
- [Key findings from each layer, with source links/references]

### Prior Work
- [Related PRs, Jira tickets, Confluence pages, past insights]

### Options
1. **[Approach A]** — [pros/cons/trade-offs]
2. **[Approach B]** — [pros/cons/trade-offs]
3. **[Approach C]** — [pros/cons/trade-offs]

### Recommendation
[Your recommendation with rationale]

### Risks & Unknowns
- [What could go wrong]
- [What you still don't know]

### Sources
- [List of sources consulted with links]
```

If any new authoritative source was discovered during research, add it to `~/.claude/learnings/authority-sources.md`.
