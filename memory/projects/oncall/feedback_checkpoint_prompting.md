---
name: Checkpoint Prompting for Complex Investigations
description: Use checkpoint mode for debugging — pause at each finding, present hypotheses, wait for confirmation before deep-diving
type: feedback
---

For complex debugging/investigation tasks, operate in CHECKPOINT MODE by default:
- After each major finding, stop and summarize what was found
- Present 2-3 ranked hypotheses
- Wait for user confirmation before proceeding to next step

**Why:** 5 out of 8 oncall sessions had wrong-approach friction where Claude went too far down a wrong path before user could correct. Presenting hypotheses early lets the user steer the investigation.

**How to apply:** Any time investigating a production issue, PEM dip, CSE ticket, or gRPC error. Especially important when root cause isn't obvious. Does NOT apply to simple data fixes or routine deployments where the action is clear.
