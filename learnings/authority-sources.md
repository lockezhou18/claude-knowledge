# Research Guide — Agent Reference

This file teaches the agent HOW to find authoritative knowledge, not just WHERE.
The examples below are starting points — always search broadly and follow the evidence.

## Research Strategy

### Priority order (always follow this):
0. **LinkedIn codebase (Source of Truth)** — the code is the ultimate authority for business logic, patterns, and how things actually work. Always check the code FIRST before trusting docs, wikis, or memory.
1. **Official documentation** — the technology's own docs are ground truth for external tech
2. **Engineering blogs from companies running it at scale** — production-proven, battle-tested
3. **Research papers & journals** — for cutting-edge, novel, or theoretically deep problems
4. **Conference talks & proceedings** — distilled practitioner knowledge
5. **High-quality community resources** — Stack Overflow top answers, curated awesome-lists, reputable tutorials
6. **General web search** — last resort, verify credibility before trusting

## What Are You Trying to Answer?

Start here. Pick the question type, follow the recommended path.

### Code & Architecture Questions
| Question | Go-to tool | Deep dive |
|----------|-----------|-----------|
| "What does this code do?" | `grep`/`Glob`/`Read` (local) | — |
| "How do other services handle this?" | `jarvis_codesearch` with `mp:` + `c:` or `m:` | [code-search.md](search-guides/code-search.md) |
| "Who calls our API / uses our class?" | `jarvis_codesearch` with `cu:` or `fu:` | [code-search.md](search-guides/code-search.md) |
| "When was this added and why?" | `git log`, `git blame`, `gh pr view` | — |
| "Does a utility/library for this already exist?" | `jarvis_codesearch` with `mp:` + keywords | [code-search.md](search-guides/code-search.md) |
| "Find code by meaning, not just keywords?" | `search_semantic_code` (when keyword search returns noise) | [code-search.md](search-guides/code-search.md) |
| "What services depend on each other?" | `fetch_call_graph` (service dependency graph) | — |
| "What Espresso tables does this service use?" | `get_table_mapping_for_application` | — |

### Runtime & Debugging Questions
| Question | Go-to tool | Deep dive |
|----------|-----------|-----------|
| "What's actually happening in prod?" | `observe-agent` (natural language) | [logs-metrics.md](search-guides/logs-metrics.md) |
| "Why did this specific request fail?" | `analyze_single_trace` with treeId, or `pb_investigate_trace_id` (Captain playbook) | [logs-metrics.md](search-guides/logs-metrics.md) |
| "What are users seeing?" | PEM Kusto / `fetch_pem_errors` | [logs-metrics.md](search-guides/logs-metrics.md) |
| "PEM alert — what's going on?" | `pb_investigate_pem_alert` (Captain playbook — may be more current than our skills) | [logs-metrics.md](search-guides/logs-metrics.md) |
| "Iris alert — what triggered it?" | `analyze_iris_alerts` (pass the alert link) | — |
| "When did behavior change?" | `fetch_metrics_by_rrd` + `go-status` | [logs-metrics.md](search-guides/logs-metrics.md) |
| "Is this error a spike or baseline?" | PEM Kusto `FeatureDegradeEvent` categorization | [logs-metrics.md](search-guides/logs-metrics.md) |
| "What do the Grafana dashboards show?" | `fetch_grafana_dashboard_panels` or `read_grafana_dashboard` | — |
| "What's the SLO status?" | `fetch_slo_data` | — |
| "Which errors are contributing most to PEM dip?" | `get_server_side_top_contributors` | [logs-metrics.md](search-guides/logs-metrics.md) |
| "Query data in Espresso/HDFS directly?" | `execute_trino_query` (Trino SQL against Holdem cluster) | — |

### Context & History Questions
| Question | Go-to tool | Deep dive |
|----------|-----------|-----------|
| "Has someone hit this error before?" | `search_slack` → `read_slack_message` (search, then read full thread) | [slack.md](search-guides/slack.md) |
| "Was this already decided/designed?" | `search_confluence_content`, or `read_google_docs_document` for Google Docs | [wiki-confluence.md](search-guides/wiki-confluence.md) |
| "Is there a ticket for this?" | `search_jira_issues` → `get_jira_issue` + `get_jira_issue_comments` for full details | [jira.md](search-guides/jira.md) |
| "Who's the expert on this?" | `search_slack` → see who answered, or `get_crew_details` / `search_teams` | [slack.md](search-guides/slack.md) |
| "Who's oncall for this service?" | `get_current_oncall` or `search_oncall` | — |
| "What changed recently that could cause this?" | `fetch_application_events` + `git log` | [logs-metrics.md](search-guides/logs-metrics.md) |

### "I don't know where to start"
| Situation | Tool | Why |
|-----------|------|-----|
| Broad question, no idea where answer lives | `unified_context_search` | Searches code + wiki + Slack + Jira in one call |
| Have a keyword but no context | `unified_context_search` with `sources=["jarvis","wiki","slack"]` | Cast a wide net |
| Need the answer fast, any source | `search_slack` first (most likely to have quick answers) | Engineers answer before documenting |
| PRD is a Google Doc | `read_google_docs_document` | Read it directly, don't ask user to paste |

### LinkedIn Plugins — See captain.md (SoT)
`~/.claude/rules/captain.md` is the source of truth for LinkedIn plugin/tool usage. It's maintained by the LinkedIn plugin team.

Key rule from captain.md: **"Before calling ANY Captain MCP tool, first check if a relevant skill exists in the LinkedIn-specific plugins."**

When doing LinkedIn work, check available LinkedIn plugins/skills before writing raw commands — they have the right guidance and tool-calling built in, saving back-and-forth.

Commonly used:
- `linkedin-dev-workflow` — git operations, PRs, CI checks
- `linkedin-cli-tools` — build, test, deploy, API calls (grpcurli, curli, go-status)
- `linkedin-framework` — infrastructure questions (Espresso, Kafka, D2), infra mapping
- `library-specs` — dependency documentation
- `observe-agent` — logs, metrics, alerts, service dependencies
- `mae-core` — complex multi-service planning

This list is not exhaustive — check the skill list in your current session for the latest available.

### Source of Truth Hierarchy
When sources contradict each other:
```
Logs/Metrics (what IS happening)  >  Code (what SHOULD happen)  >  Docs (what someone WROTE)
```
Code wins over docs. Logs win over code. If you find a mismatch, `/learn` it.

### Detailed Search Guides (syntax reference):
- **[Code Search](search-guides/code-search.md)** — Jarvis filters, patterns, unified search
- **[Logs & Metrics](search-guides/logs-metrics.md)** — observe-agent, KQL, treeId tracing, PEM
- **[Wiki / Confluence](search-guides/wiki-confluence.md)** — CQL modes, space scoping
- **[Slack](search-guides/slack.md)** — exception-first pattern, channel strategy
- **[Jira](search-guides/jira.md)** — JQL, resolved tickets, linked PRs

### How to assess authority:
- **Who wrote it?** Engineers at companies running this at scale > independent bloggers > anonymous posts
- **When?** Recent (< 2 years) for fast-moving tech. Timeless for fundamentals.
- **Citations/stars?** Highly cited papers, highly starred repos indicate community validation
- **Official vs community?** Official docs first, community guides for gaps
- **Does it show production experience?** "We run this at 10M QPS" > "I tried this in a weekend project"

### How to search:
- Use `WebSearch` with specific queries: "[technology] best practices [company]" or "[problem] architecture [scale]"
- Use `WebFetch` to read specific pages from known authoritative sources
- For papers: search arXiv, Semantic Scholar, Google Scholar with technical keywords
- For RFCs: search datatracker.ietf.org with the protocol name
- Don't stop at the first result — cross-reference across 2-3 sources

## Example Authoritative Sources by Domain

These are EXAMPLES to seed your search, not an exhaustive list. Always search beyond these.

### Distributed Systems & Infrastructure
Companies running at massive scale write the best content here:
- Google (research.google), Amazon (aws.amazon.com/builders-library), Netflix (netflixtechblog.com), LinkedIn (engineering.linkedin.com), Meta, Uber, Cloudflare, Stripe, Shopify, Discord, Slack
- Key papers: MapReduce, Spanner, Dynamo, Kafka, Raft, Paxos — search by name on Google Scholar

### AI/ML & LLMs
This field moves fast — always check publication dates:
- Research labs: Anthropic, OpenAI, Google DeepMind, Meta AI (FAIR), Microsoft Research, Cohere, Mistral
- Paper repositories: arXiv (cs.AI, cs.CL, cs.LG, cs.SE), Semantic Scholar, Google Scholar
- Practical engineering: Hugging Face blog, LangChain docs, LlamaIndex docs, Simon Willison's blog, Lilian Weng's blog
- Benchmarks & evals: Papers With Code, HELM, Chatbot Arena

### Software Engineering & Architecture
Timeless principles + modern practices:
- Thought leaders: Martin Fowler, Kent Beck, Uncle Bob, Gregor Hohpe
- Company blogs: any top-tier tech company's engineering blog is likely authoritative for their domain
- Books (search for summaries/key ideas): Designing Data-Intensive Applications, Site Reliability Engineering, A Philosophy of Software Design
- Conferences: Strange Loop, QCon, GOTO, InfoQ (transcripts searchable)

### Security
Always verify against authoritative sources for security decisions:
- OWASP (owasp.org) — the baseline for web security
- CWE/CVE databases — known vulnerabilities
- Vendor security docs — each cloud provider, framework, language has security guidance
- Google Project Zero, Trail of Bits, NCC Group — vulnerability research

### Data & Databases
- Official docs for your specific database are always the first stop
- Performance/scaling: check engineering blogs from companies at similar scale
- Correctness: Jepsen.io for distributed database testing
- Design: search for "[database] internals" or "[database] architecture" blog posts

### Standards & Protocols
- IETF RFCs (datatracker.ietf.org) — HTTP, TLS, OAuth, JWT, gRPC, QUIC
- W3C (w3.org) — web standards, accessibility
- OpenAPI, AsyncAPI, GraphQL — API specification standards
- protobuf.dev, grpc.io — Google's protocol ecosystem

### Emerging / Agent Engineering
Fast-evolving — check dates carefully:
- Anthropic docs (tool use, agents, MCP), OpenAI docs (function calling, assistants)
- MCP specification (modelcontextprotocol.io)
- Agent frameworks: LangChain, LlamaIndex, CrewAI, AutoGen
- Prompt engineering: Anthropic's prompt engineering guide, OpenAI cookbook

## When to Search External Sources

**DO search when:**
- Entering unfamiliar technology or framework
- Problem should have a well-known solution but you can't find one internally
- Security-sensitive decisions (always verify against OWASP/CWE)
- Performance optimization at scale
- Architecture decisions with long-term implications
- Internal code does something unusual — check if there's a better industry pattern
- You're about to make a technology choice (library, framework, protocol)
- The user explicitly asks for best practices or industry standards

**DON'T search when:**
- Answer is clearly in the codebase or internal docs
- Question is specific to internal systems with no external equivalent
- Making a small code change within an established pattern
- You already have high-confidence knowledge about the topic

## Growing This Guide

This file should evolve. When you discover a new authoritative source during research:
- If it proved valuable (cited in an insight, influenced a decision), add it here
- Organize by domain, not alphabetically
- Include a brief note on what makes it authoritative
- Remove sources that consistently provide outdated or low-quality information
