---
name: IP sync cadence throttled
description: IP (talent-partner-integrations-mt) reduced Greenhouse sync cadence due to QPS issues — job req stages every 1hr, app stages every 15min, webhooks disabled
type: project
---

IP team (EDS) has throttled Greenhouse sync cadence due to QPS rate limit issues with Greenhouse:

- **Job requisition stages**: pulled every **1 hour** (was 15 min)
- **Application stages**: refreshed every **15 min** (webhooks disabled)
- **Webhooks**: disabled temporarily to clear Kafka lag

**Why:** Greenhouse rate limits being hit as more customers activate. IP negotiating higher limits with Greenhouse.

**How to apply:**
- During E2E testing, expect **up to 1 hour delay** for new Greenhouse jobs/stages to appear in IP
- App stage changes take **~15 min** instead of instant (webhook disabled)
- Testing may need to pause or use pre-existing synced data
- Tracking ticket: HPLT-115585
- **Target resolution: April 15, 2026** — cadence will be restored before bi-di sync charter ramp
- Team asked for test account exception but not currently possible

**Contacts:** svohra (IP), gchandak (IP config), rikar (Greenhouse rate limits)
