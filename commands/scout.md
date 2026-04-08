# Scout — Learn from Other Agent Systems

Evaluate another plugin, repo, rules file, or agent framework and extract patterns worth adopting. Can target a specific repo OR do a broad ecosystem scan.

**Usage:**
- `/scout https://github.com/someone/cool-plugin` — evaluate a specific repo
- `/scout ecosystem` — broad scan for new ideas across the AI coding agent ecosystem
- `/scout trending` — find what's new and popular in Claude Code / AI agent space

## Mode 1: Evaluate a Specific Repo

### Step 1: Read Their System
- Clone or fetch the repo structure (use `gh api` for tree, `WebFetch` for raw files)
- Identify their skills/commands, rules, hooks, agents, knowledge management
- Read their CLAUDE.md, AGENTS.md, README, and key skill files

### Step 2: Compare With Our System
For each component they have, assess:

| Their Component | Do We Have It? | Ours Better / Theirs Better / Different Approach? |
|----------------|----------------|--------------------------------------------------|

Focus on:
- **Skills/commands we don't have** — could they fill a gap?
- **Different approaches to same problem** — is theirs more elegant?
- **Novel patterns** — something we haven't thought of?
- **Knowledge management** — how do they handle memory, learning, retrieval?
- **Hook design** — any clever automation we're missing?
- **Prompt engineering techniques** — better instructions, persuasion, formatting?

### Step 3: Extract Actionable Ideas
For each finding worth adopting:
```
### Idea: [name]
- **Source**: [repo/file]
- **What they do**: [description]
- **What we do now**: [our current approach or "nothing"]
- **Adoption effort**: low / medium / high
- **Impact**: how much better would our system be?
- **Recommendation**: adopt as-is / adapt / skip / watch
```

### Step 4: Present to User
Show findings ranked by impact/effort ratio. User decides what to adopt.

If user approves, create the skill/hook/rule immediately.

### Step 5: Update Watch List
Add the repo to `~/.claude/learnings/watchlist.jsonl` for periodic re-scanning:
```json
{"repo": "owner/name", "last_scanned": "2026-04-01", "key_findings": ["finding1"], "watch_reason": "why this repo matters"}
```

## Mode 2: Ecosystem Scan

### Step 1: Discover What's Out There
Search broadly for new and trending AI coding agent tools:

**GitHub searches:**
- `WebSearch "claude code plugin" site:github.com` — new plugins
- `WebSearch "claude code skills" OR "claude commands" site:github.com` — community skills
- `WebSearch ".cursorrules" best practices 2026` — Cursor community patterns
- `WebSearch "AI coding agent framework" new 2026` — new frameworks
- `WebSearch "claude code hooks" OR "claude code automation"` — hook patterns
- `WebSearch "LLM agent memory" OR "AI agent knowledge management" new` — knowledge systems

**Check known ecosystem sources:**
- GitHub trending (language:markdown, topic:claude-code or ai-agent)
- Claude Code plugin marketplace (check for new entries)
- Awesome lists: awesome-cursorrules, awesome-claude-code, awesome-ai-agents
- Hacker News, Reddit r/ClaudeAI, Reddit r/LocalLLaMA for discussions

### Step 2: Filter for Relevance
From discoveries, filter for:
- **Stars/activity** — is this actually used or just a toy?
- **Recency** — is this actively maintained?
- **Relevance** — does it solve a problem we have or could have?
- **Novelty** — does it do something we haven't seen before?

### Step 3: Deep-Dive Top 3-5
For the most promising finds, run Mode 1 (evaluate specific repo) on each.

### Step 4: Report
```
## Ecosystem Scan: [date]

### New Discoveries
1. [repo] (⭐ stars) — [what it does, why it's interesting]
2. ...

### Worth Adopting
- [Idea from repo X] — [why, effort, impact]

### Worth Watching
- [repo] — [not ready to adopt but interesting direction]

### Our Competitive Advantages
- [Things we have that nobody else does]
```

## Mode 3: Trending

Quick scan of what's gaining traction in the last 30 days:
- Search GitHub for recently created/updated repos with claude-code, ai-agent, coding-assistant topics
- Check Hacker News and Reddit for discussions about AI coding workflows
- Look for new blog posts about Claude Code productivity
- Report top 5 most interesting finds

## Auto-Scout (via Compound Phase)

The `/compound` command's Step 7 (Skill Proposals) should also check:
- Read `~/.claude/learnings/watchlist.jsonl`
- For repos scanned >30 days ago, flag for re-scan in the briefing:
  ```
  ## Watch List Due for Re-Scan
  - EveryInc/compound-engineering-plugin (last scanned: 2026-03-31)
  - obra/superpowers (last scanned: 2026-03-31)
  ```
- The next session can run `/scout [repo]` to check for updates
