---
id: bug-003
track: bug
type: episodic
repos: [cap, talent-agent-mt]
tags: [error-handling, 4xx-to-5xx, grpc, restli, oncall, monitoring]
severity: high
created: 2026-03-25
last_verified: 2026-03-28
use_count: 1
outcome_score: 2.0
status: active
rot_rate: slow
paths: ["**/SearchResponseUtils.java", "**/TalentDigitalDoubleMessageService.java", "**/TalentDigitalDoubleCommonService.java", "**/SearchResource.java"]
---

## When downstream 4xx errors get wrapped as 5xx, investigate the error handling chain end-to-end

### Situation
Two separate services (cap-services, talent-agent-mt) were wrapping downstream 400/429 errors as INTERNAL/500, inflating error rate SLOs and triggering false alerts.

### Incidents
1. **cap-services (incident-10696)**: `SearchResponseUtils.handleRestLiResponseException()` used `startsWith("Exceeds the pagination limit")` which didn't match seas-cloud-server's message format `"Pagination context start + count: (25675) exceeds request limit: (20000)"`. Fix: case-insensitive `contains("pagination")` and `contains("limit")`. PR: cap#4428 (merged).

2. **talent-agent-mt (alerts 46883146, 59431434)**: `IllegalArgumentException` for OJP contracts wrapped as INTERNAL/500 by gRPC layer. Also `log.error()` for expected business conditions ("No hiring workflow found") inflated gRPC error rate. Fix: `StatusRuntimeException(INVALID_ARGUMENT)` + downgrade log.error→log.warn. PR: talent-agent-mt#1682.

### Resolution
- Always trace the full exception chain: downstream response → catch block → re-throw → what status the caller sees
- Check error message matching is robust (case-insensitive, contains not startsWith)
- Business-logic checks that return false (not failures) should log at WARN, not ERROR
- Use proper gRPC status codes (INVALID_ARGUMENT for bad input, PERMISSION_DENIED for auth, RESOURCE_EXHAUSTED for rate limits)

### Prevention
- When reviewing error handling code, verify all downstream 4xx codes are propagated, not just 429
- Check if `log.error()` calls are for actual errors vs expected business conditions
