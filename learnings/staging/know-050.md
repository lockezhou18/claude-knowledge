---
id: know-050
track: knowledge
type: semantic
repos: [mcm-mt, *]
tags: [curli, rest-li, d2, debugging, association, finder, protocol, complex-key]
severity: high
rot_rate: permanent
status: active
created: 2026-04-09
last_verified: 2026-04-09
use_count: 2
outcome_score: 1
origin_skill: learn
related_to: [know-049]
---

# RestLiAssociation Finders Require v1 Protocol (No X-RestLi-Protocol-Version:2.0.0)

## Context
Spent an entire session failing to call `hiringProjectCandidates?q=hiringProject` finder. The `X-RestLi-Protocol-Version:2.0.0` header causes "not a Compound key" errors for `@RestLiAssociation` resources. Removing the header (default v1 protocol) fixes it immediately.

## Guidance

**When calling a finder on a `@RestLiAssociation` resource, do NOT use `X-RestLi-Protocol-Version:2.0.0`.**

### Working pattern (v1 protocol, no version header):
```bash
curli --dv-auth SELF -f prod-ltx1 \
  'd2://hiringProjectCandidates/hiringContext=urn:li:contract:CONTRACT&hiringProject=urn:li:hiringProject:(urn:li:contract:CONTRACT,PROJECT_ID)?q=hiringProject&start=0&count=50' \
  -H 'Accept:application/json'
```

### Key rules:
1. **Assoc keys go in the path** before `?q=`: `d2://resource/key1=val1&key2=val2?q=finder`
2. **No URL encoding needed** for URN colons/parens in assoc key values
3. **No `X-RestLi-Protocol-Version:2.0.0` header** — use default (v1)
4. **v2 protocol misparses** the `&`-separated assoc keys as compound key notation and fails

### How to tell if a resource is an Association:
- Java: `@RestLiAssociation` annotation, extends `AssociationResourceAsyncTemplate`
- PDL/IDL: has `assocKeys` in resource definition
- Multiple `@Key` annotations with `@AssocKeyParam` in finders

### Contrast with ComplexKey resources:
- `@RestLiCollection` with `ComplexKeyResourceTemplate` → uses v2 protocol, `(field1:val1,field2:val2)` format
- `@RestLiAssociation` with `AssociationResourceAsyncTemplate` → uses v1 protocol, `key1=val1&key2=val2` format

### Verified example:
```bash
# hiringProjectCandidates — @RestLiAssociation with assocKeys: hiringContext, candidate, hiringProject
# Finder "hiringProject" uses @AssocKeyParam for hiringContext and hiringProject
curli --dv-auth SELF -f prod-ltx1 \
  'd2://hiringProjectCandidates/hiringContext=urn:li:contract:2011455851&hiringProject=urn:li:hiringProject:(urn:li:contract:2011455851,1686265484)?q=hiringProject&start=0&count=50' \
  -H 'Accept:application/json'
# Returns: 10 HPCs with candidate URNs and candidateHiringState
```

## When to Apply
- Any time you're constructing curli for a `@RestLiAssociation` finder
- When you get "not a Compound key" errors from curli
- When you get "Parameter X is required" despite it being in the URL (v2 protocol misparse)
- Refer to know-049 (6-step curli composition process) for the general approach, then apply this v1 rule for associations
