# Session Handoff

Generate a handoff note summarizing the current session for continuity.

## Usage
`/session-handoff`

## Steps

1. **Review the conversation** — scan through what was discussed and accomplished in this session.

2. **Generate a structured handoff note** with these sections:

   ### What Was Done
   - Bullet list of completed tasks, investigations, fixes, deployments

   ### What's Pending
   - Open items, PRs awaiting review, tickets still in progress

   ### Key Decisions Made
   - Architecture choices, approaches selected, things ruled out

   ### Blockers
   - Anything waiting on others, permissions needed, external dependencies

   ### Next Steps
   - Exact next action to pick up from

3. **Save to worklog** — append to or create the current week's worklog file at `/Users/bizhou/workspace/oncall/oncall_week_<date>_worklog.md`

4. **Update memory** if any reusable patterns, gotchas, or preferences were discovered during the session.
