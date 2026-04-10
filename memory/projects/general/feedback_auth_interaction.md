---
name: auth-interaction-preference
description: Prefer ! prefix over tmux for auth flows to keep user in conversation context
type: feedback
---

Prefer `!` prefix for auth commands over launching interactive tmux sessions.

**Why:** When tmux is launched for auth, the user loses the ability to interact with Claude — they're in a separate terminal context with no visibility or help. The handoff between "Claude helping" → "user alone in tmux" → "back to Claude" is clunky and breaks flow.

**How to apply:**
- For simple auth commands (kinit, token refresh, single-command logins): suggest `! <command>` so output stays in the conversation
- Only fall back to tmux for truly interactive multi-step flows (e.g., 2FA prompts that need repeated input)
- Always run auth pre-flight checks before workflows that need auth, rather than launching tmux preemptively
- When tmux is unavoidable: give exact instructions, set checkpoints, and verify auth worked after user returns
