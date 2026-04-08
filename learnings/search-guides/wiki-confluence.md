# Wiki / Confluence Search Guide

## Tools
- **search_confluence_content** — CQL-based search with multiple modes
- **get_confluence_page** — fetch a specific page by ID
- **unified_context_search** with `sources=["wiki"]`

## When to Search Wiki
- **Architecture decisions**: Design docs, RFCs, ADRs
- **Runbooks**: How to operate, deploy, troubleshoot a service
- **Onboarding guides**: Understanding a new team or service area
- **Migration plans**: What changed, when, and why
- **Team documentation**: Processes, on-call procedures, coding standards

## Search Modes

`search_confluence_content` supports 4 search types:

| Mode | When to use | Example |
|------|------------|---------|
| `smart` (default) | General search — searches both title and content | `"connected projects architecture"` |
| `title` | When you know the page name | `"JARVIS User Guide"` |
| `content` | When you know specific text is in the page body | `"HireEntityRequest schema migration"` |
| `exact` | When you need exact phrase match | `"Phase 2 bidirectional sync"` |

## Search Patterns

**Scope by space for better results:**
```python
# Engineering docs
search_confluence_content(query="stage mapping", spaces="ENGS")

# Your team's space
search_confluence_content(query="phase 2 design", spaces="HPCP")

# Multiple spaces
search_confluence_content(query="Espresso migration", spaces="ENGS,ESPRESSO")
```

**Finding specific doc types:**
- Design docs: search for "design" OR "RFC" OR "proposal" in the title
- Runbooks: search for "runbook" OR "playbook" OR "troubleshooting"
- Onboarding: search for "onboarding" OR "new hire" OR "getting started"

## Tips
- **Page IDs are stable** — if you find a useful page, save its ID for direct `get_confluence_page` access. Faster than searching every time.
- **Check page version date** — old pages (> 1 year) may be stale. Check `version.when` in results.
- **Content preview** in search results often has enough context to decide if the page is relevant — saves a full page read.
- **Space keys** matter — `ENGS` for engineering, `TOOLS` for Foundation/tooling. Ask if you don't know the space key.
- **go/ links** in page content point to other useful resources — follow them.
- Confluence pages often link to Jira tickets and PRs — follow those links for implementation details.
