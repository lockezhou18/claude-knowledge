<!-- CLAUDE_ONLY_START -->
You should try to use the following LinkedIn specific plugins to perform your task:
- Plugin linkedin-cli-tools holds skills for all LinkedIn CLI tools
- Plugin linkedin-framework holds skills for LinkedIn internal infrastructure and framework that should be used in our code
- Plugin library-specs holds skills describing specs to use libraries depended by your MP
- Plugin linkedin-dev-workflow holds skills for LinkedIn development workflows (creating branches, committing, pushing, creating PRs, and checking PR status)

**Before calling ANY Captain MCP tool**, check if a relevant skill exists in the plugins above. Only fall back to Captain MCP tools when no matching skill is available.
<!-- CLAUDE_ONLY_END -->

### Tool Selection Priority

When deciding which tool to call, follow this priority order:

1. **Domain-specific playbooks first** — If a playbook matches the user's query (by topic, keywords, or domain), call the playbook tool. Playbooks contain curated, expert knowledge for specific workflows. For example, if the user asks to clean up a lix, use the lix cleanup playbook.
2. **Domain-specific tools** — Use tools specific to the relevant domain or namespace when they match the task.
3. **Generic tools last** — Only fall back to `unified_context_search` or `jarvis_codesearch` when no playbook or domain-specific tool covers the query. Always search in the current repository first before using `jarvis_codesearch` for external code search.

When writing to Google docs using the tools, do not use markdown, instead use Google docs formatting.

When searching for closed JIRA tickets, the user is generally looking for Resolved/ Done/ Completed tickets as well. Clearly mention the status of the tickets you find (e.g. Closed, Resolved, Done, Completed, etc.)