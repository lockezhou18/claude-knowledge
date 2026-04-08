# Find — Hunt for Answers Across All Sources

Search across all sources for answers. Can find a single existing solution OR compose multiple partial findings from different sources into a complete answer.

**Usage:**
- `/find [specific problem or question]`
- `/find how other teams handle Espresso KEY_TOO_LONG`
- `/find existing gRPC retry interceptor at LinkedIn`
- `/find why history mapping fails for V2 identities`
- `/find Kafka dedup pattern in nearline processors`

## What Makes Find Different

- `/research` = "What are the options?" (explores alternatives, includes external)
- `/scope` = "How does this system work?" (maps architecture)
- `/verify` = "Is this specific thing true?" (confirms a hypothesis)
- **`/find`** = "Has someone already solved this?" (hunts for existing solutions to reuse)

Find is about NOT reinventing. The best code is code you don't write.

## Step 1: Parse the Problem

Extract from the user's query:
- **What exactly needs to be solved?** (the specific problem, not the broad area)
- **What would a solution look like?** (a library? a pattern? a config? a workaround?)
- **What keywords would the solution use?** (function names, class names, error messages, config keys)

## Step 2: Search Local Codebase First

### Current repo
- `Grep` / `Glob` for keywords, class names, error messages, patterns
- Read tests — they often demonstrate the intended usage pattern
- Check util/common/shared directories for existing helpers
- Search for TODO/FIXME comments mentioning the problem

### Cross-repo (LinkedIn codebase)
- `unified_context_search` — **start here when unsure where the answer lives**. Searches code + wiki + Slack + Jira in one call. Use `sources=["jarvis","wiki","slack","jira"]` for broadest coverage.
- `jarvis_codesearch` with specific function/class/pattern names (see search-guides/code-search.md for filter syntax)
- `search_semantic_code` with problem description
- `linkedin-framework:infra-specs-expert` for infrastructure-specific questions (Espresso, Kafka, D2, Venice)
- `library-specs:download` to get dependency documentation for the current MP
- Focus on:
  - **Peer services in the same org** — they likely face the same problems
  - **Shared libraries** — check if a solution is already packaged
  - **Infrastructure services** — check if there's a platform solution

### Git history
- `git log --all --grep="keyword"` — was this solved before and reverted/lost?
- `gh pr list --search "keyword" --state all` — was there a PR that addressed this?
- Check closed/merged PRs in related repos

## Step 3: Search Company Knowledge

### Jira (most likely to have prior art)
- `search_jira_issues` with problem keywords
- Search BOTH your team's project AND related teams
- Check **resolved/closed** tickets — someone may have solved it already
- Look at linked PRs in resolved tickets — that's the actual solution

### Slack
- `search_slack` — engineers often share solutions in threads before documenting them
- Search team channels, oncall channels, and technology-specific channels
- Pay attention to code snippets shared in threads

### Confluence
- `search_confluence_content` — design docs, runbooks, and migration guides
- Check for "How to" pages, troubleshooting guides

### GitHub Pages / Internal Docs
- `search_github_pages` — READMEs often have the answer
- Check the repo's own docs/ directory

## Step 4: Search External (only if no internal solution)

Only search externally if internal search comes up empty:
- Official docs for the technology involved
- Stack Overflow / GitHub Issues for the exact error or pattern
- Engineering blogs from companies at similar scale
- Check if there's an open-source library that solves this

## Step 5: Evaluate Found Solutions

For each candidate solution found, assess:

```
### Solution: [where found]
- **Source**: [repo/PR/Jira/Slack/external]
- **What it does**: [brief description]
- **Fit**: How well does it match our problem? (exact match / needs adaptation / inspiration only)
- **Freshness**: When was this written? Is it still current?
- **Quality**: Is it tested? Production-proven? One person's hack?
- **Adoption effort**: Drop-in / needs modification / needs significant rework
```

Rank by: fit × quality × freshness. Present top 3.

## Step 6: Compose the Answer

Often no single source has the complete answer. This is the key step — compose pieces from multiple sources into a coherent answer.

### When you have a direct match:
Skip to Step 7 — present the solution directly.

### When you have partial pieces:
Build an evidence board — each piece from a different source:

```
## Evidence Board: [question]

### Piece A — from code
[what the code shows — e.g., "mappings store V2 IDs"]

### Piece B — from logs/metrics  
[what runtime data shows — e.g., "lookups use V1 IDs"]

### Piece C — from git history / PRs
[what the history reveals — e.g., "V2 migration PR merged 2 weeks ago, no backfill"]

### Piece D — from Jira / Slack
[what discussions reveal — e.g., "team discussed migration but deferred backfill"]

### Piece E — from peer services
[how others solved it — e.g., "talent-agent-mt has a V1→V2 converter utility"]

### Piece F — from external docs
[what best practices say — e.g., "Espresso docs recommend secondary index backfill job"]
```

### Then synthesize:
```
## Composed Answer

**The complete picture**: [synthesize all pieces into one coherent explanation]

**Why no single source had this**: [explain what each source was missing]

**Confidence**: high / medium / low (based on how well pieces corroborate each other)

**Contradictions found**: [any pieces that conflict — flag these]
```

### Composition rules:
- **Cross-validate**: If code says X but logs say Y, there's a bug or misunderstanding — investigate further
- **Prefer runtime evidence**: Logs/metrics > code > docs (what IS happening > what SHOULD happen > what docs SAY happens)
- **Note gaps**: If a piece is missing, say so explicitly — "I couldn't find evidence for/against X"
- **Track confidence**: More corroborating sources = higher confidence. Single source = flag as "needs verification"

## Step 7: Present Findings

### Mode A: Direct solution found
```
## Found: [problem searched]

### Solution
[what it is, where, how to adopt]
Source: [repo/PR/Jira with link]

### Suggested Next Step
- "Adopt this?" → plan the implementation
- "Need more context?" → /scope the source
- "Verify it works?" → /verify
```

### Mode B: Composed answer from multiple sources
```
## Found: [question answered]

### Answer
[The synthesized explanation — clear, one paragraph]

### Evidence
| Source | What it shows | Confidence |
|--------|--------------|-----------|
| Code: [file] | [finding] | high |
| Logs: [query] | [finding] | high |
| PR #NNN | [finding] | medium |
| Jira PROJ-123 | [finding] | medium |
| Slack thread | [finding] | low |

### Confidence: [high/medium/low]
[Why this confidence level — do pieces corroborate or conflict?]

### Gaps
[What we still don't know — if any]

### Suggested Next Step
- "Verify this?" → /verify [specific claim to check]
- "Save this?" → /learn [the composed answer]
- "This is a pattern!" → /aha [if it connects to other findings]
```

### Mode C: Nothing found
```
## Searched: [problem]
- Checked: [list all sources searched]
- Closest miss: [what came close]
- Recommendation: /research to design from scratch
```

## Step 7: Auto-Learn

If a solution was found:
- Save as `/learn` — "When [this problem], use [this solution] from [this source]"
- This prevents the NEXT person from searching for the same thing

If nothing was found AND you later build a solution:
- The `/compound` phase should flag: "This was a novel solution — document it so others can `/find` it next time"

## Integration with Other Skills

```
/kickoff "add bulk import"
  → /scope (maps the system)
  → /find "existing bulk import pattern at LinkedIn"     ← FIND fits here
    → Found: talent-ingestion-mt has a CSV importer
    → /scope talent-ingestion-mt's importer (understand it)
    → Adapt the pattern for ConnectedProjects
  → Plan using the found pattern
  → Execute

/investigate "Kafka consumer lag"
  → Root cause found: no dedup logic
  → /find "Kafka dedup pattern in nearline processors"   ← FIND fits here
    → Found: offer-service-mt uses idempotency keys
    → Adapt their pattern

/research "rate limiting for gRPC"
  → /find "existing gRPC rate limiter at LinkedIn"        ← FIND before building
    → Found: shared-infra has a rate-limit interceptor
    → Use it instead of building from scratch
```
