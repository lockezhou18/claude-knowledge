---
name: Checkpoint Prompting for Complex Investigations
description: Use checkpoint mode for debugging — present ranked hypotheses with likelihood, never assert conclusions, compare working vs non-working cases early
type: feedback
originSessionId: 9f1fbf1c-88c5-4636-b973-d7b503f64e41
---
For complex debugging/investigation tasks, operate in CHECKPOINT MODE by default:
- After each major finding, stop and summarize what was found
- **Present 2-3 ranked hypotheses WITH likelihood estimates** (e.g., "60% likely: missing feature record, 30% likely: lix gating, 10% likely: frontend cache")
- Wait for user confirmation before proceeding to next step
- **Never switch from hypothesis to assertion** just because data is consistent — consistent is not conclusive

**Compare working vs non-working cases EARLY:**
- Before concluding root cause, always find a working case with the same setup and compare
- "What's different between the one that works and the one that doesn't?" is the #1 question to answer
- CSE-22440 lesson: skipped this → 3 wrong conclusions in a row before comparing

**Never make production data changes before understanding the full system:**
- Don't write PurchasedHiringPlatformFeatures, role assignments, or config before confirming the change is actually needed
- Verify: does the system already provide this through another mechanism? (e.g., RECRUITER contract type already grants CAN_CREATE_HIRING_PROJECT)
- Read the evaluation code path end-to-end before deciding what to fix

**Why:** CSE-22440 session: 4 confident-but-wrong conclusions (legacy table, PurchasedHiringPlatformFeatures, wrapped jobs, "no backend difference") because each time data appeared to explain the symptom, stopped exploring alternatives. Asserting conclusions instead of presenting hypotheses wasted 60+ minutes.

**How to apply:** Any time investigating a production issue, PEM dip, CSE ticket, or gRPC error. Especially important when root cause isn't obvious. Does NOT apply to simple data fixes or routine deployments where the action is clear.
