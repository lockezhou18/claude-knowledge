---
name: Research Pipeline Pattern
description: Validated 5-step exploration pattern that produces executive-level intelligence from scattered data sources
type: reference
id: know-research-pipeline
status: graduated
tags: [research, methodology, exploration, data-driven, cross-validate]
---

When exploring an unfamiliar domain with scattered data, follow this 5-step pipeline:

1. **Start with a simple question** — don't over-scope. "Where can we see AI usage?" is better than "give me everything about AI metrics."
2. **Don't stop at the first answer** — the first result (a dashboard, a doc) is the entry point, not the answer. Keep pulling threads to discover what's behind it.
3. **Map the full ecosystem** — identify ALL data sources, owners, and relationships. The value is in the connections between systems, not any single system.
4. **Cross-validate against SoT** — before presenting data, verify units, accuracy, and freshness against the source of truth. This caught a cents-vs-dollars error that would have produced a 100x wrong report.
5. **Combine dimensions no single dashboard combines** — the breakthrough insight comes from joining data across systems that weren't designed to talk to each other (adoption + cost + org structure + model breakdown + pricing tiers).

**Why:** This pattern was validated with the strongest feedback signal (+2.0 x3) across 24 research_depth signals. User said "even my director doesn't have such full picture." The data was always there — nobody had assembled it.

**How to apply:** Any time the user asks an open-ended "where/how/what" question about a domain. Don't answer with the first link found — run the full pipeline. The recipe `/recipe ai-usage-report` is a concrete example of the output this pattern produces.
