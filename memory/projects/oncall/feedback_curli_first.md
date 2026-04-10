---
name: Curli First for Data Lookups
description: Use mcm-mt curli/grpcurli REST APIs directly for sourcing channel and hiring project lookups instead of Trino queries
type: feedback
---

When investigating CSE tickets involving sourcing channels, hiring projects, or other MCM entities, go straight to curli REST API calls against mcm-mt instead of Trino queries.

**Why:** Trino tables often have permission issues (e.g., sourcingchannelsv2 access denied) or stale snapshots. The REST APIs return live data and are faster to iterate on. The hiring-platform skill commands are useful references but shouldn't need explicit invocation — just use the curli patterns directly.

**How to apply:**
- For entity lookups (sourcingChannels, hiringProjects, hiringProjectCandidates), use `curli --dv-auth SELF -f prod-ltx1 "d2://..."` directly
- Only fall back to Trino when you need aggregate queries across many records
- Keep curli/grpcurli commands as single lines for easy copy-paste
