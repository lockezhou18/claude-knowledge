# Slack Search Guide

## Tools
- **search_slack** — search messages across channels
- **read_slack_message** — read a specific message/thread by URL/timestamp
- **unified_context_search** with `sources=["slack"]`

## When to Search Slack
- **Errors/exceptions**: Someone likely hit the same error before and discussed it
- **Recent decisions** not yet documented anywhere
- **Debugging sessions**: Engineers share solutions in threads before documenting
- **Deployment announcements**: "Just deployed X to prod"
- **Design debates**: Decisions made in threads that never made it to Confluence
- **Quick answers**: "How do I do X?" answered by a teammate

## Search Strategy for Debugging

**The exception-first pattern** (most effective for debugging):
1. **Copy the first sentence of the exception/error** — this is what others would have pasted too
2. **Search Slack** with that exact text — find threads where others hit the same error
3. **Read the full thread** — the resolution is usually further down in replies
4. **Check who resolved it** — they may have more context if you need to follow up

Example flow:
```
Error: "ConfigCompilationException: Cannot resolve app-def default value"
  → search_slack: "Cannot resolve app-def default value"
  → Found: 3 threads in #hp-backend where others hit this
  → Thread 1: "Fixed by adding missing bean config to application.src"
  → Thread 2: "This happens after upgrading parseq — run mint update"
  → Resolution found without investigating from scratch
```

## Search Patterns

**For errors:**
- Search the exact error message (first line, quoted)
- Search the exception class name: `NullPointerException hp-ats`
- Search the failing method: `processPhase2 error`

**For design context:**
- Search feature/project name: `"connected projects phase 2"`
- Search the Jira ticket number: `HPCP-1234`
- Search the PR number: `#524` or `PR 524`

**For operational context:**
- Search service + "deploy": `hp-ats-integration-mt deploy`
- Search service + "rollback": `hp-ats rollback`
- Search alert name: `PEM pipeline availability`

**For finding the right person:**
- Search the code area + "help" or "question": `stage mapping question`
- Look at who replied with solutions — they're the domain expert

## Which Channels to Check
- **Team channels**: #hp-backend, #connected-projects (team-specific)
- **Oncall channels**: #hp-oncall, #hiring-platform-oncall (incident context)
- **Tech channels**: #grpc, #espresso, #kafka (technology-specific help)
- **Announcement channels**: #deploys, #incidents (operational context)

## Two-Step Pattern: Search → Read Thread

`search_slack` finds messages but only shows previews. The answer is almost always in the **thread replies**, not the first message. Always follow up with `read_slack_message` to get the full thread:

```
Step 1: search_slack("ConfigCompilationException app-def")
  → Found 3 threads in #hp-backend

Step 2: read_slack_message(thread_url)  ← THIS is where the solution is
  → Reply 3: "Fixed by adding missing bean config to application.src"
```

## Tips
- Slack search is best for **recent** context (< 6 months). Older discussions may be archived.
- Thread replies often have the answer — always `read_slack_message` to get the full thread, not just the first message.
- If you find a solution in Slack, `/learn` it — so next time we find it in the knowledge base instead of searching Slack again.
- Engineers often share code snippets in threads — these are mini-solutions worth capturing.
