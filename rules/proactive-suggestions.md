---
description: "When to proactively suggest skills — loaded on demand, not every session"
---

# Proactive Skill Suggestions (always-on, no skill invocation needed)
The agent should suggest skills when the moment is right, even if the user didn't invoke `/kickoff`:
- Found a root cause during debugging > "Save this? (`/learn`)"
- Noticed a pattern across incidents > "This connects to [X]. Capture it? (`/aha`)"
- Discovered a fundamentally better approach > "This is a breakthrough. Save as `/eureka`?"
- Hit unfamiliar territory mid-implementation > "I need to `/research` this before continuing."
- Entering a completely new domain (Euler, Venice, D2, etc.) > "Want to `/explore` this first to build a mental model?"
- About to start a big feature > "Want to `/scope` the area first?"
- About to build something that might already exist > "Let me `/find` if someone's solved this before."
- Starting work after a few days away > "Run `/watch-deps` to check what changed in your dependencies?"
- PR changes a public API/proto > "This affects downstream consumers. Run `/watch-deps` to check who's impacted?"
- Session wrapping up with significant work done > "Run `/compound` to close the loop?"
- Just finished a task or switching context > "Run `/checkpoint` to sync?" (lightweight, 30s)
- Long session (3+ hours) without a compound > "It's been a while. Run `/compound` for full retrospective?"
- Something broken > "Let me `/investigate` this systematically."
- Just created a new skill file > "Run `/integrate [name]` to wire it into the ecosystem?"
- Refactored a skill's instructions > "Run `/recipe eval-skill run [name]` to verify behavior didn't regress?"
- Just integrated a new skill > "Scaffold evals with `/recipe eval-skill scaffold [name]`?"
- Just did a manual UI test > "Record it with `/recipe ui-session record` so you can replay it instantly next time?"
- About to create a PR with UI changes > "Run `/recipe ui-session compare` on before/after sessions for PR evidence?"
- Running the same E2E test again > "Replay the saved session with `/recipe ui-session replay` — near-instant vs re-discovering elements"
- Need to confirm a hypothesis with evidence > "Let me `/verify` this against internal sources."
- Just performed a repetitive multi-step task > "That looked mechanical. Create a `/recipe` from those steps?"
- A recipe hit something unexpected > escalate to the appropriate skill (investigate, verify, etc.)
- Complex multi-service design task > "This spans multiple services. Use `mae-core:architect` for parallel planning?"
- First time scoping a new repo > "Run `linkedin-framework:map-infrastructure` to auto-detect infra systems?"
- Plan approved, ready to build > "Use `/implement` to work through units systematically?"
- About to run mint build/test or gradlew locally > delegate auto-intercepts, but if it doesn't: "This should run on the VM. Use `bash -c \"cd <repo> && vm-run mint build\"`"
- Code ready, need to ship > "Use `/ship` for the full PR > prod pipeline?"
- PR created, waiting on CI/deploy > "Use `/wait-for` to poll across sessions?"
Don't be pushy — suggest once, move on if the user doesn't engage.
