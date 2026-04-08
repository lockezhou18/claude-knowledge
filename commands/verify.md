# Verify — Confirm a Hypothesis Against Internal Sources

Trace through code, company knowledge, and internal systems to confirm or disprove a specific claim, hypothesis, or assumption. Not exploring — verifying.

**Usage:**
- `/verify [hypothesis or claim to check]`
- `/verify the Euler secondary index for FIND_HIRE_ENTITY_REQUEST was added after entity creation`
- `/verify ts-api finder returns empty because staging fabric mismatch`

If no argument, ask: "What do you want to verify?"

## What Makes Verify Different

- `/research` = "What are the options?" (broad, exploratory)
- `/scope` = "How does this system work?" (mapping)
- `/investigate` = "Why is this broken?" (root cause)
- **`/verify`** = "Is this specific thing true?" (confirmation/disproval)

Verify is surgical. You start with a claim and end with: confirmed, disproved, or inconclusive + what's needed to resolve.

## Step 1: Parse the Claim

Break the hypothesis into verifiable sub-claims. For example:
```
Claim: "Euler secondary index for FIND_HIRE_ENTITY_REQUEST_BY_CANDIDATE_AND_STATUS_DISMISSED 
        was added after the entity was created"

Sub-claims:
  1. The secondary index exists in the code → check Espresso schema / entity definition
  2. When was it added → git log / blame on the index definition
  3. When was the entity created → check data timestamp or creation PR
  4. Was there a backfill → search Jira/Slack for backfill tickets
```

## Step 2: Trace Through Code

For each sub-claim, go to the source of truth:

### Code-level verification
- **Read the actual code** — don't rely on docs or memory. `grep`, `Glob`, `Read` the files.
- **Git blame / git log** — when was this line added? By whom? What PR?
- **Check tests** — does a test exercise this code path? What does it assert?
- **Trace the call chain** — follow the code from entry point to the specific behavior
- **Check config** — feature flags, LiX, application.src, deployment config

### Cross-repo verification
- **jarvis_codesearch** — search for the symbol/pattern across repos (see search-guides/code-search.md for filter syntax)
- **unified_context_search** — broad search across code + wiki + Slack + Jira when unsure where evidence lives
- **search_semantic_code** — semantic search for related code
- **Check dependent services** — if the claim involves cross-service behavior, read both sides

### Runtime verification
- **observe-agent** — check logs/metrics to verify runtime behavior matches the claim
- **grpcurli / curli** (via `linkedin-cli-tools:cli-tools`) — make actual API calls to verify behavior
- **analyze_single_trace** — trace a specific request to verify the call chain matches the claim
- **go-status** (via `linkedin-cli-tools:cli-tools`) — verify deployed version matches expectations

## Step 3: Check Company Sources

### Jira
- `search_jira_issues` — search for tickets about this feature/index/migration
- Look for: creation tickets, backfill tickets, known issues, deployment tickets
- Check ticket status: was the backfill completed or still pending?

### Confluence
- `search_confluence_content` — search for design docs, runbooks, migration guides
- Look for: schema change docs, index documentation, deployment procedures

### Slack
- `search_slack` — search for discussions about this topic
- Look for: deployment announcements, troubleshooting threads, team decisions
- Pay attention to timestamps — when did people first mention this?

### GitHub / PRs
- `gh pr list --search "keyword" --state all` — find PRs that added/modified this
- Read the PR description and review comments — often has context not in the code

### Observability
- `observe-agent` — check metrics, logs for evidence of the behavior
- Check if the index is actually being queried, returning results, or empty
- Check deployment timestamps vs data creation timestamps

## Step 4: Build an Evidence Chain

For each sub-claim, document:
```
Sub-claim: [what you're checking]
Evidence: [what you found, with source links]
  - Code: [file:line, what it shows]
  - Git: [commit hash, date, PR link]
  - Jira: [ticket, status]
  - Slack: [thread link, key quote]
  - Metrics: [dashboard/query, what it shows]
Verdict: CONFIRMED / DISPROVED / INCONCLUSIVE
```

## Step 5: Present Verdict

```
## Verification: [original claim]

### Verdict: CONFIRMED / DISPROVED / PARTIALLY TRUE / INCONCLUSIVE

### Evidence Chain
1. [Sub-claim 1]: CONFIRMED
   - [evidence with sources]
2. [Sub-claim 2]: DISPROVED  
   - [evidence showing why it's wrong]
   - [what's actually true instead]

### What This Means
[Practical implication — what should be done based on this finding]

### If Inconclusive
[What additional information is needed to resolve]
[Who to ask: specific person/team with context]
[What to check: specific system/dashboard/log]
```

## Step 6: Auto-Learn

If the verification revealed something non-obvious:
- Confirmed claim that others might not know → `/learn` it
- Disproved a common assumption → `/learn` the correction (high value — prevents others from making the same wrong assumption)
- Connected to a broader pattern → suggest `/aha`

## Examples

```
/verify the D2 client retries are handled by parseq, not D2 native retry
  → traces RetryPolicy in code
  → finds TaskRetryUtils.java using BackoffPolicy.noBackoff()
  → checks D2 client config for retry settings
  → CONFIRMED: parseq handles retries, D2 retry is disabled

/verify GDPR purge affects HireAccessControlDB
  → checks Trino CDC tables for deletion events
  → checks Espresso cluster mapping (HireAccessControlDB → MD-2)
  → searches Jira for GDPR scope documentation
  → DISPROVED: HireAccessControlDB not in scope, only ResumesSearchDB

/verify the Kafka export event topic was renamed in Q1
  → git log on topic configuration
  → finds PR that changed from old topic name
  → checks Slack for migration announcement
  → CONFIRMED: renamed 2026-03-20, PR #528
```
