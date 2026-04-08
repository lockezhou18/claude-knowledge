---
name: patent-publication-tracker
description: Track patent and publication process status. Check patent portal, remind of next steps.
inputs: ["patent_id"]
chain_to: research
chain_when: "venue deadline approaching"
---

## Steps

1. **Check patent status**: Visit https://linkedin-patent.anaqua.com/Details.aspx?ID={{patent_id}}
   - Current patent: ID 93827 — "Self-Evolving Knowledge and Behavioral Adaptation System for AI Agents"
   - Filed: 2026-04-04
   - Status: Under CELA review

2. **Check publication readiness**:
   - [ ] Patent filed → ✓ (ID 93827)
   - [ ] Manager discussion → pending
   - [ ] Eng Lead (Sr Director+) identified → pending
   - [ ] Target venue selected → pending (recommend: CHASE or ASE Industry Track)
   - [ ] One-pager written (Google Doc) → pending
   - [ ] Eagle Eye scan (go/EagleEyeAgent) → pending
   - [ ] JIRA ticket #1 (Initial Review) → pending
   - [ ] Full paper draft → pending
   - [ ] JIRA ticket #2 (Final Review) → pending
   - [ ] Submit to venue → pending

3. **Timeline check**: Patent filing → patent application typically takes ~2 months. Publication process can run in parallel after patent team responds.

## Expected Output
Status update on patent + publication progress with next action item.

## On Failure
If patent is declined → can still publish (just remove patentable claims). Chain to /research for alternative venues.
