---
description: "6-phase engineering pipeline with gates — loaded on demand for non-trivial tasks"
---

# Engineering Pipeline (Research > Clarify > Plan > Execute > Review > Compound)
Every non-trivial task follows this pipeline. Match ceremony to scope — small tasks can be lightweight, but never skip phases entirely. Each phase has a GATE: do not proceed until satisfied.

## Phase 1: Research (CRITICAL — spend 80% of effort here)
Before writing ANY code, conduct thorough research across all available sources. Work through these layers, stopping when you have enough context. For simple tasks, layers 1-2 may suffice. For complex work, go deeper.

**Layer 1: Local Knowledge (always check)**
1. **Search past learnings.** Check memory files, documented solutions, outcome logs for related patterns, gotchas, or prior fixes. Don't repeat solved mistakes.
2. **Look to the code for business logic.** The connection between business logic and code is very tight — many systems have business logic hard-coded right in. If documentation doesn't exist, look to the code. Know your code broadly and deeply.
3. **Understand why systems were built the way they are.** "While it may be easy to identify the 10% that is broken, it is much harder to identify the 90% that isn't broken." Prefer targeted refactoring over full rewrites.
4. **Read PR histories.** Find related/previous PRs for the same feature area. Understand what patterns were used, what reviewers expected, what the established approach is.
5. **Search LinkedIn codebase (Source of Truth).** The code is the ultimate authority. Search the current repo first (`grep`, `Glob`, `Read`), then cross-repo (`jarvis_codesearch`, `search_semantic_code`). Check how peer services handle the same problem. Read tests — they document expected behavior. When code contradicts docs, code wins.
6. **Check logs & metrics (Runtime Source of Truth).** Code tells you what SHOULD happen; logs tell you what ACTUALLY happened. Use observe-agent for any service's logs/metrics/dependencies. Check: is this code path actually being hit? What errors are occurring? When did behavior change? Correlate with deploys. For debugging: logs first, code second. For architecture: code first, logs to verify.

**Layer 2: Company Knowledge (check for non-trivial work)**
**LinkedIn plugins have priority here — they have deeper context than raw MCP tools.**
7. **Search Jira.** Find related tickets — open, resolved, and closed. Check for prior art, design decisions, known issues, and rejected approaches. Look at both your team's project and related teams' projects. Use search_jira_issues or get_jira_issue tools.
8. **Search Confluence/Wiki.** Look for design docs, architecture decisions, runbooks, and onboarding guides relevant to the area you're changing. Use search_confluence_content or get_confluence_page tools.
9. **Search Slack.** Recent discussions often contain context that isn't documented anywhere else — debugging sessions, design debates, decisions made in threads. Use search_slack tool.
8. **Search GitHub Pages / internal docs.** READMEs, architecture docs, API references. Use search_github_pages tool.

**Layer 3: External Knowledge (check when entering unfamiliar territory)**
See ~/.claude/learnings/authority-sources.md for the research strategy and source examples.
9. **Official documentation first.** The technology's own docs are ground truth. Always start here.
10. **Engineering blogs from companies running it at scale.** Production-proven > theoretical. Search for "[technology] best practices [company]" or "[problem] architecture [scale]". Don't limit to a fixed list — any company running the technology at scale is worth reading.
11. **Research papers and journals.** For cutting-edge, novel, or theoretically deep problems. Search arXiv, Semantic Scholar, Google Scholar by keyword. Especially valuable for AI/ML, distributed systems, and security. Check publication dates — this field moves fast.
12. **Standards and RFCs.** For protocol-level decisions: IETF RFCs, OWASP, W3C, OpenAPI specs. These are canonical — don't rely on blog summaries when the spec itself is available.
13. **Cross-reference.** Don't trust a single source. Verify across 2-3 authoritative sources before making architecture or security decisions.
14. **Check library specs.** Use the library-specs plugin for dependencies in your multiproduct.
15. **Grow the source registry.** When you discover a valuable new source during research, add it to authority-sources.md so future sessions benefit.

**Layer 4: Synthesis (always do)**
11. **Explore alternatives before committing.** Consider 2-3 approaches. What's the simplest? What are the trade-offs? Is there a higher-upside alternative worth mentioning? Don't lock onto the first approach.
12. **Summarize findings to the user.** Don't silently absorb research — present what you found, what the options are, and what you recommend. The user may have context that changes the picture.

**GATE:** Can you explain the existing system, why it was built that way, what the business logic is, what prior work and decisions exist, and what external best practices apply? If not, keep researching.

**BEHAVIORAL GATES** > See `behavioral-gates.md` for full eval-driven rules (approach, tool selection, compound learning, over-engineering). Key reminders:
- Ask which component FIRST. Present hypotheses. Wait for confirmation.
- 3-strike rule: same error 3x > switch strategy or ask.
- "Compare with our system" = lead with mapping. "Check" = read-only.
- curli LOCAL first. observe-agent for logs. Built-in tools > external.
- Every 3+ task session > generate >= 1 insight.

## Phase 2: Clarify Requirements
Before planning implementation, ensure the requirements are clear:
1. **Ask one question at a time.** Don't dump 10 questions — prioritize the most blocking one.
2. **Resolve product decisions here, not during coding.** Scope boundaries, user behavior, success criteria — nail these down before writing code.
3. **Challenge assumptions.** Is this the real problem? Is there a better framing? Suggest alternatives when you see them.
4. **Match ceremony to scope.** Simple bug fix = one quick question. New feature = structured requirements. Large initiative = recommend a design doc first.

**GATE:** Do you and the user agree on WHAT to build, WHY, and what's OUT of scope? If not, keep clarifying.

## Phase 3: Plan (produce a durable artifact for non-trivial work)
For anything beyond a simple fix, produce a plan before coding:
1. **Break work into implementation units.** Each unit should be atomic, focused, and independently testable. Order by dependency.
2. **Specify file paths and test scenarios.** Each unit needs: which files to modify, what to test (specific inputs > expected outputs), what patterns to follow.
3. **Identify the riskiest task first.** Ask: "What is the most risky task?" and "What am I missing?" Address high-risk items early.
4. **Flag unknowns explicitly.** Separate what you know from what you'll discover during execution. Don't fake certainty.
5. **Present the plan to the user before executing.** One question can save an entire rework cycle.

**GATE:** Does the user approve the plan? Are risks identified? Are test scenarios specific (not generic)? If not, iterate.

## Phase 4: Execute
Now write the code, following the plan:
1. **Work in incremental pieces.** Each unit should be a shippable chunk. Don't accumulate a massive uncommitted diff.
2. **Test as you go.** Write tests for each unit before moving to the next. Don't batch all testing to the end.
3. **Track deviations from plan.** If you discover something that changes the approach, surface it to the user before continuing. Don't silently diverge.
4. **Log outcomes.** If a memory/learning influenced your approach, note whether it helped or led astray (for the outcome-log).
5. **Use LinkedIn dev workflow for git operations.** `linkedin-dev-workflow:start` for branch creation, `linkedin-dev-workflow:submit` for commit+push+PR creation. These follow LinkedIn conventions automatically — don't reinvent.
6. **Use LinkedIn CLI tools for build/test/deploy.** `linkedin-cli-tools:cli-tools` knows `mint build`, `mint test`, `grpcurli`, `go-status`, etc. Check available LinkedIn skills before writing raw bash commands.

**GATE:** Does the code match the plan? Do tests pass? Are there deviations the user should know about?

## Phase 5: Review (automated + manual)
Before considering work complete:
1. **Verify against plan.** If there was a plan from Phase 3, check: does the implementation match it? Any units missing? Any scope drift? Any deviations that need documenting?
2. **Self-review the diff.** Read through all changes as if you're a reviewer seeing them for the first time.
3. **Check for the common sins:** security issues (injection, auth bypass, credential leaks), performance issues (N+1 queries, unbounded loops), maintainability issues (unclear names, missing comments on non-obvious logic), dependency issues (breaking upstream contracts).
4. **Run tests.** All existing tests must still pass. New tests must cover the changes.
5. **The PostToolUse hook on `gh pr create` automatically runs multi-persona review** — but don't rely solely on it. Review before creating the PR, not only after.
6. **Use `linkedin-dev-workflow:pr-check`** to check CI status and address PR review comments.

## Phase 6: Compound (close the loop — make the next cycle better)
After significant work (feature, bug fix, debugging session, refactor), run a structured retrospective before moving on. The SessionEnd hook automates part of this, but for substantial work, do it explicitly.

**COMPOUND GATE** > See `behavioral-gates.md` for full compound learning rules.

**6a. Plan vs Reality Diff** — What did you plan? What happened? Where did you deviate and why?

**6b. What Went Well / What Didn't** — Reinforce good patterns, apply 5 Whys to bad ones.

**6c. Generate Actionable Insights** — Format: **When [situation], do [action] because [reason learned]**. Save to memory/staging with Bug-track or Knowledge-track categorization.

**6d. Feed Forward** — Insight lifecycle: create > score > graduate (use_count>=3 + score>=2.0) > or prune (score<-2) > or flag stale (>90 days). See `compound-learning.md` for full spec.

**GATE:** Did you document at least one actionable insight? Did you check if this work revealed stale/wrong existing insights?
