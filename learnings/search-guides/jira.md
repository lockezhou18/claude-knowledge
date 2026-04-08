# Jira Search Guide

## Tools
- **search_jira_issues** — search for tickets across projects
- **get_jira_issue** — get full details of a specific ticket
- **get_jira_issue_comments** — read ticket comments (often has the real context)
- **unified_context_search** with `sources=["jira"]`

## When to Search Jira
- **Before building**: Has someone already proposed or built this?
- **Before debugging**: Is this a known issue with a ticket?
- **Before designing**: Are there design decisions or RFCs as tickets?
- **During investigation**: Link your findings to existing tickets

## Search Strategy

**For finding existing solutions:**
1. Search with error message or feature name
2. Check **Resolved/Done/Completed** tickets — not just open ones
3. Read the **linked PRs** in resolved tickets — that's the actual code fix
4. Read **comments** — often more useful than the description

**For finding design context:**
1. Search for RFC or design doc tickets in the project
2. Check **Epic** tickets — they link to sub-tasks with implementation details
3. Look at ticket **labels** — teams often tag with feature names

## Search Patterns

```
# Find resolved tickets about a specific error
"ConfigCompilationException" project = HPCP status in (Resolved, Done, Closed)

# Find all tickets for a feature area
"connected projects" OR "phase 2" project = HPCP

# Find tickets assigned to a team
project = HPCP AND assignee in membersOf("hp-backend")

# Find recent bugs
project = HPCP AND type = Bug AND created >= -30d

# Find tickets with linked PRs (likely has a solution)
project = HPCP AND status = Resolved AND "Pull Request" is not EMPTY

# Find design/RFC tickets
project = HPCP AND (type = "Design Review" OR labels = "rfc" OR summary ~ "design")
```

## Which Projects to Check
- **Your team's project** first (HPCP for hiring platform)
- **Related teams** — upstream/downstream service teams
- **Platform teams** — Espresso (ESPENG), Kafka, D2, infrastructure

## Tips
- When searching for "closed" tickets, always include Resolved/Done/Completed — different teams use different terminal statuses.
- Ticket **comments** often have debugging steps, workarounds, and root cause analysis that didn't make it into the description.
- **Linked issues** connect related problems across teams — follow the links.
- If you solve something that had no Jira ticket, consider creating one — future you (or teammates) will search for it.
- Old tickets (> 1 year) may reference code that's been refactored — verify against current codebase before following their solution.
