---
name: JIRA Investigation Reply Format
description: Standard format for CSE/oncall JIRA comments — structured RCA with error chain, fix details, verification curli, and next steps
type: feedback
---

When adding investigation comments to JIRA tickets, use this structure:

**1. Title line** — State the outcome clearly
- "Root Cause Identified and Fixed"
- "Investigated — Redirecting to [team]"
- "Data Fix Applied — Please Re-trigger"

**2. Context** (1-2 sentences) — What was investigated and scope
- "Investigated the repeated MOVE_APPLICATION_DATA failures across all 5 transfers (Mar 16, Mar 23, Mar 24 retries)."

**3. Root Cause** — Clear explanation of WHY, not just WHAT
- Name the specific service, method, and error
- Explain the data/code issue in plain language
- Mention if it's persistent vs transient

**4. Error Chain** — Technical trace showing the full call path
- Use arrow notation: `service A → service B → service C → FAILS: "error message"`
- Include service names, method names, specific error strings

**5. Fix Applied** — What was done, when, and how
- Date of fix
- Exact action taken (data fix, code fix, config change)
- Specific values changed

**6. Verification** — Proof the fix worked
- Always include the full curli command and raw output in a {code} block
- Show before/after if possible

**7. Next Step** — Clear action item for the reader
- Who needs to do what
- "Please re-trigger the transfers"
- "Redirecting to [team] — cc @person"

**Why:** Structured RCA comments close tickets faster, reduce back-and-forth, and serve as documentation for future similar issues. The curli verification is critical — it proves the fix worked and gives others a command to verify themselves.

**How to apply:** Every CSE ticket comment, oncall investigation update, and incident post-mortem note. Skip sections that don't apply (e.g., no "Fix Applied" if redirecting to another team).

**IMPORTANT: Always draft the comment and show it to the user for approval BEFORE posting to JIRA. Never post directly.**

**Anti-patterns to avoid:**
- Don't just say "investigating" without findings
- Don't skip the error chain — it's the most useful part for future oncall
- Don't forget the verification curli — "trust but verify" in writing
- Don't use {code} blocks — they don't render properly. Use triple backticks with language hint instead: ```sql ... ``` or ```java ... ```
- JIRA supports markdown-style formatting: **bold**, bullet points, numbered lists, and triple backtick code blocks
