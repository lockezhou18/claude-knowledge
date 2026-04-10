---
name: Proactive commit suggestions
description: Suggest committing after completing logical units of work, don't wait for user to ask
type: feedback
---

After completing a logical unit of work (e.g., fixing a bug, adding a feature, updating tests), proactively suggest committing instead of waiting for the user to ask.

**Why:** User's commit rate is low relative to work done — logical checkpoints often pass without being captured, leading to large mixed commits later.

**How to apply:** After finishing a code change that passes build/tests, say something like "This is a good checkpoint to commit. Want me to commit these changes?" Don't force it — just suggest.
