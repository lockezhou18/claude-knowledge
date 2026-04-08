# Share — Export Our Patterns for Others

Package our system (or parts of it) into shareable formats that others can adopt.

**Usage:**
- `/share skill [skill-name]` — export a single skill as a standalone file
- `/share system` — export the full system as a documented package
- `/share template [component]` — export a component as a reusable template
- `/share insight [insight-id]` — export a specific insight for team sharing

## Mode 1: Share a Skill

Export a skill from `~/.claude/commands/` as a standalone, documented file:

1. Read the skill file
2. Strip any LinkedIn-specific details (credentials, internal URLs, team names)
3. Add a header explaining: what it does, when to use it, dependencies, setup
4. Write to `~/shared/skills/[skill-name].md`

## Mode 2: Share the Full System

Generate a complete documentation package of our compound learning system:

### What to Include
```
~/shared/compound-learning-system/
├── README.md                  # Overview, philosophy, setup guide
├── setup/
│   ├── settings-hooks.json    # Hook configuration (sanitized)
│   ├── rules-template.md      # Pipeline rules template (no personal data)
│   └── install.sh             # Script to set up the directory structure
├── skills/
│   ├── compound.md            # /compound skill
│   ├── learn.md               # /learn skill
│   ├── aha.md                 # /aha skill
│   ├── eureka.md              # /eureka skill
│   ├── research.md            # /research skill
│   ├── investigate.md         # /investigate skill
│   ├── scope.md               # /scope skill
│   └── scout.md               # /scout skill
├── knowledge-base/
│   ├── SCHEMA.md              # Knowledge base schema
│   ├── authority-sources.md   # External research guide
│   └── directory-structure.md # Folder layout explanation
├── hooks/
│   ├── score-insights.py      # Scoring engine
│   ├── compound-learning-commit.py
│   └── compound-learning-pr.py
└── tests/
    └── test-rules-e2e.sh      # E2E test suite template
```

### Sanitization Rules
Before exporting, strip:
- LinkedIn-specific system tags, test credentials, internal URLs
- Personal memory content (insights, briefing, manifests)
- Project-specific rules (captain.md, test-environments.md)
- Allowlist entries from settings.json

Keep:
- The pipeline structure and philosophy
- Hook configuration patterns (with placeholder values)
- Skill definitions (they're generic)
- Schema and scoring logic
- Test framework

### README.md Content
```markdown
# Compound Learning System for Claude Code

A self-improving knowledge management system for AI coding agents.

## Philosophy
Each unit of engineering work makes subsequent units easier.
The agent learns around you — you work, it captures, scores, promotes, and prunes knowledge.

## The Pipeline
Research → Clarify → Plan → Execute → Review → Compound

## Skills
- /scope — Understand the system before designing
- /research — Deep investigation across all knowledge layers  
- /investigate — Find root cause with hypothesis-first debugging
- /learn — Quick-save a fact
- /aha — Capture a pattern connecting observations
- /eureka — Capture a breakthrough
- /compound — Full retrospective + rebuild briefing
- /scout — Learn from other agent systems

## Knowledge Base
Agent-optimized with tiered loading, three-signal scoring, 
episodic/semantic memory types, and automated lifecycle management.

## Setup
[installation instructions]
```

## Mode 3: Share a Template

Export a specific component as a reusable template:

- `/share template schema` — the SCHEMA.md as a starter template
- `/share template hooks` — hook configuration patterns
- `/share template pipeline` — the 6-phase pipeline rules
- `/share template scoring` — the scoring engine
- `/share template tests` — the e2e test framework

Each template includes:
- The file(s) with placeholders for customization
- A brief explaining what it does and how to adapt it
- Example usage

## Mode 4: Share an Insight

Export a specific insight for team sharing (future team scaling):

1. Read the insight file
2. Strip personal context, keep the generalizable pattern
3. Format for the team knowledge repo (when it exists)
4. Suggest which team members would benefit

## Feedback Signal

`/share` = +1.5 signal (session-level value — work worth packaging). Append to `~/.claude/learnings/logs/feedback-log.jsonl`:
```json
{"ts": "ISO timestamp", "signal": 1.5, "act": "SKILL_INVOCATION", "dimension": "other", "agent_action": "session work being shared", "user_context": "/share invoked", "skill": "share"}
```

## Output Location

All exports go to `~/shared/` with clear naming. The user can then:
- Copy to a repo and PR it
- Share via Slack
- Upload to Confluence
- Contribute to the Claude Code plugin marketplace
