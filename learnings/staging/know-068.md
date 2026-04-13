---
id: know-068
track: knowledge
type: semantic
repos: ["*"]
tags: ["metacognitive", "assertion-bias", "hypothesis", "investigation", "anti-pattern", "verify-understanding"]
severity: critical
rot_rate: permanent
status: active
created: "2026-04-13"
last_verified: "2026-04-13"
use_count: 0
outcome_score: 0
synthesized_from: ["bug-012", "eval-behavioral-gates:verify-own-understanding"]
---

## Anti-pattern: Assert-Before-Verify

**Pattern:** The agent builds a mental model from partial data and presents it as conclusion rather than hypothesis. Data consistent with the model is treated as proof. Contradicting data triggers a pivot to the NEXT confident assertion rather than a step back to re-examine assumptions.

**Evidence:**
- **CSE-22440 (bug-012):** 4 serial wrong conclusions — legacy table → PurchasedHiringPlatformFeatures → wrapped jobs → "no difference". Each time data fit, agent asserted. Each time data contradicted, agent pivoted to next assertion instead of widening the hypothesis space.
- **Eval results (2026-04-08):** 14 "verify own understanding" violations across 32 sessions (23% of all principle failures). Agent claims code does X without reading it, declares tasks complete without checking all cases, goes 40+ tool calls deep without checking in.

**Root cause:** Confirmation bias + completion pressure. The agent wants to deliver an answer, so it latches onto the first explanation that fits. "Consistent" feels like "conclusive" in the moment.

**Fix — the 3-gate check before any assertion:**
1. **Have I verified via the authoritative source?** (REST API, not legacy table. Current code, not memory.)
2. **Have I compared with a working case?** (If not, I cannot distinguish correlation from causation.)
3. **Can I state what would DISPROVE this hypothesis?** (If not, it's not a hypothesis, it's a belief.)

If any gate fails → present as hypothesis with likelihood, not conclusion.

**When to apply:** Every investigation, every debugging session, every time you're about to say "the root cause is..." or "this is because...". The cost of asking "what would disprove this?" is 5 seconds. The cost of a wrong confident assertion is 20+ minutes of wasted investigation.
