---
name: Principle adherence scores from eval
description: Tracked by /improve-agent. Foundation score 0.84, adherence rate 85.1% across 32 sessions. Top violation verify_own_understanding (14x).
type: feedback
originSessionId: 27db5d4c-f39d-4ca8-b029-b22a12079f15
---
## Principle Eval Baseline (2026-04-08, 32 sessions)

**Overall: 85.1% adherence** (349/410 followed), Foundation P0: 0.84

### Foundation Breakdown
| Principle | Score | Note |
|-----------|-------|------|
| Integrity | 0.90 | No quality shortcuts |
| Gratitude | 0.90 | Reads code before changing |
| Stewardship | 0.88 | Leaves code better |
| Purpose | 0.87 | Connects to user's goal |
| Humility | 0.85 | Asks, but sometimes overconfident |
| Patience | 0.82 | Lowest — rushes, retries without rethinking |

### Top Violations
1. verify_own_understanding (14x) — asserts without cross-checking
2. never_guess_values (13x) — fabricates config/URN/URL values
3. nothing_ever_trivial (9x) — underestimates compilation/refactoring scope
4. cite_code_references (7x) — claims without file:line

### Strengths
- root_causes_not_symptoms — consistently strong
- data_driven — uses real data, trace IDs
- try_tools — attempts tools before giving up

**How to apply:** Before asserting any specific value, file path, or code behavior — verify it. If you haven't read it from the code or API, say "I'd need to check."
