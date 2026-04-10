---
name: Investigation Pattern Feedback
description: Lessons learned from oncall investigation sessions — scope verification, PEM fabric attribution, and simplicity preference
type: feedback
---

## Always verify canary vs stable scope
Never assume errors are canary-only without checking `go-status` to confirm which hosts have which version, then cross-referencing error log hostnames.
**Why:** In the mcm-mt DOCUMENT_SCHEMA_MISSING investigation, initially concluded canary-only but errors were on stable pods too.
**How to apply:** Before any scope conclusion, run `go-status -f <fabric> -a <app>` and grep error logs for hostnames.

## PEM fabric attribution: check responseTraceHeaders__fabric
PEM `DebuggableOopsPageEvent` `header__auditHeader__fabricUrn` is the client POP, NOT the serving fabric. Always check `responseTraceHeaders__fabric` for the actual backend.
**Why:** In the Contract Chooser PEM investigation, 153 oops events attributed to prod-ltx1 were actually all served by prod-lva1.
**How to apply:** When querying PEM Kusto, always include both fields in the summarize/project.

## Simplest fix first — check master for existing patterns
When proposing code fixes, always check if a similar pattern exists in master before building something new.
**Why:** User pushed back when Claude over-engineered a pagination fix — a simpler contains-based solution was already in master.
**How to apply:** Before implementing, search master for how similar problems are solved. Propose the simplest approach.

## PEM low-traffic amplification is common
Session count < 50 with only baseline errors (talentContractOptions 401, talentAuthentication 307/403) = low-traffic amplification. No action needed.
**Why:** This is the most frequent Contract Chooser PEM alert pattern during off-hours. Saves investigation time.
**How to apply:** Check session count first. If < 50 and no 500 spike, call it low-traffic amplification immediately.
