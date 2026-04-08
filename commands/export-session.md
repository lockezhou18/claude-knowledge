# Export Session — Package a Conversation for Sharing

Export the current or a past conversation as a shareable artifact — with the system files it produced.

**Usage:**
- `/export-session` — export current session
- `/export-session [session-id or path]` — export a specific past session

## Step 1: Gather the Conversation

Use `/export` to get the raw conversation transcript, or read the provided file.

## Step 2: Gather Associated Artifacts

Identify all files created or modified during the session:
- Check `~/.claude/learnings/logs/commit-log.jsonl` for commits made
- Check git diff for files changed
- Check timestamps on files in `~/.claude/commands/`, `~/.claude/rules/`, `~/.claude/hooks/`, `~/.claude/learnings/`
- List all artifacts created/modified with their purpose

## Step 3: Create the Package

Build a shareable package at `~/shared/sessions/YYYY-MM-DD-[topic]/`:

```
~/shared/sessions/YYYY-MM-DD-[topic]/
├── README.md                    # What this session accomplished, key takeaways
├── conversation.md              # The full conversation, cleaned up
├── artifacts/                   # All files created/modified
│   ├── commands/                # Skills created
│   ├── rules/                   # Rules created/updated
│   ├── hooks/                   # Hook scripts
│   ├── learnings/               # Knowledge base files
│   └── tests/                   # Test files
├── highlights.md                # Key decision points and insights extracted
└── adoption-guide.md            # How someone else can adopt these patterns
```

## Step 4: Clean the Conversation

Process the raw transcript:
1. **Remove sensitive data** — credentials, internal URLs, personal info, test data IDs
2. **Keep the thinking** — the WHY behind decisions is more valuable than the WHAT
3. **Mark key moments** — where did the design pivot? Where was a breakthrough?
4. **Add section headers** — break the conversation into logical phases

## Step 5: Write Highlights

Extract the most valuable moments into `highlights.md`:
```markdown
# Session Highlights

## Key Decisions
1. [Decision]: [Why this was chosen over alternatives]

## Breakthroughs (/eureka moments)
1. [Insight]: [Why this changed the approach]

## Patterns Discovered (/aha moments)
1. [Pattern]: [What it connects]

## Evolution of the Design
1. Started with: [initial approach]
2. Evolved to: [what changed and why]
3. Final form: [what we ended up with]
```

## Step 6: Write Adoption Guide

Help others adopt the patterns from this session:
```markdown
# Adoption Guide

## Prerequisites
- [What you need before starting]

## Quick Start (30 minutes)
1. [Minimal viable setup]

## Full Setup (2 hours)
1. [Complete implementation]

## Customization
- [What to change for your context]
- [What's generic vs domain-specific]

## FAQ
- [Anticipated questions from reading the conversation]
```

## Step 7: Sanitize and Package

Before final export:
- Strip LinkedIn-specific: internal URLs, team names, service names (or replace with generic equivalents)
- Strip credentials and test data
- Keep the architecture and decision-making intact
- Zip with optional encryption: `openssl enc -aes-256-cbc -salt -pbkdf2`

## Step 8: Log Feedback Signal

`/export-session` = +1.5 signal (session worth preserving). Append to `~/.claude/learnings/logs/feedback-log.jsonl`:
```json
{"ts": "ISO timestamp", "signal": 1.5, "act": "SKILL_INVOCATION", "dimension": "other", "agent_action": "session being exported", "user_context": "/export-session invoked", "skill": "export-session"}
```

## Step 9: Suggest Distribution

Based on the content, suggest where to share:
- **GitHub repo** — if it's a reusable system (like the compound learning system)
- **Blog post** — if the journey/thinking is the value
- **Team wiki** — if it's team-specific knowledge
- **Claude Code marketplace** — if it's a plugin
- **Twitter/LinkedIn thread** — if it's a concise insight chain
