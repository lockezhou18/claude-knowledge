---
id: know-049
track: knowledge
type: semantic
repos: [*]
tags: [curli, rest-li, d2, debugging, process, code-search, lps, complex-key]
severity: high
rot_rate: permanent
status: active
created: 2026-04-08
last_verified: 2026-04-08
use_count: 9
outcome_score: 0
origin_skill: learn
---

# How to Compose a curli Command for an Unfamiliar Rest.li Service

## Context
When you need to call a Rest.li service you've never used before (no existing curli in REFERENCE.md), you need to discover the D2 service name, resource path, key format, and encoding. This process was refined while building the entity routing curli.

## Guidance

**When composing a curli for an unfamiliar service, follow this 6-step process:**

### Step 1: Find the Resource Class
- Jarvis codesearch: `c:ResourceName` or `code:resourceName filetype:java`
- Look for `@RestLiCollection(name = "resourceName")` annotation — this gives the resource path
- Check the class extends: `ComplexKeyResourceTemplate<K, EmptyRecord, V>` = ComplexKey, `CollectionResourceTemplate<K, V>` = simple key

### Step 2: Find the D2 Service Name (NOT in Java code)
- The D2 service name lives in **LPS config**, NOT in Java source
- Search: `f:lps-d2-* reponame:<mp-name>` in Jarvis
- The LPS file maps: cluster name → services → paths
- Each `<entry key="serviceName">` with `<entry key="path" value="/resourcePath"/>` is a D2 service
- The curli URL is `d2://serviceName/...` (the path is already baked into the service definition)

### Step 3: Determine Key Format
- **Simple key** (`CollectionResourceTemplate<Long, V>`): `d2://service/123`
- **ComplexKey** (`ComplexKeyResourceTemplate<K, EmptyRecord, V>`): needs Rest.li v2 protocol
  - Add header: `-H 'X-RestLi-Protocol-Version: 2.0.0'`
  - URL format: `d2://service/(field1:value1,field2:value2)`
- **Compound key**: `d2://service/key1=val1&key2=val2`

### Step 4: Find Enum/Model Values
- Read the key/model PDL or Java class for enum values
- Jarvis: `c:EntityRouteContext` or `f:EntityRouteContext.pdl`
- Also check `RouteTable` or similar mapping classes for context → internal mapping

### Step 5: URL Encoding
- URN colons: `urn:li:contract:123` → `urn%3Ali%3Acontract%3A123`
- ComplexKey parentheses: literal `(` and `)` in the URL
- Ampersands in ComplexKeys: use `,` not `&` between fields

### Step 6: Fabric & Auth
- **`-f prod-ltx1`**: Specify fabric if local D2 proxy can't resolve the service
- **`--force-insecure-d2`**: Use when `--dv-auth SELF` gives SSL errors locally. Works for read-only lookups on services that don't enforce DV auth.
- **`--dv-auth SELF`**: Use when the service requires DV auth (most prod services)
- **Don't route curli to VM** when DV auth is needed — `authn-cli` SSO times out over non-interactive SSH, password fallback hits EOFError (no TTY). Use `--force-insecure-d2` locally instead.
- Test with `-f` pointing to different prod fabrics if you get 404 (data may be in a different colo)

### Step 7: Protocol Version (CRITICAL for Associations)
- **`@RestLiAssociation`** (extends `AssociationResourceAsyncTemplate`): Do NOT use `X-RestLi-Protocol-Version:2.0.0`. Assoc keys go in path: `d2://resource/key1=val1&key2=val2?q=finder`. No URL encoding needed for URN values.
- **`@RestLiCollection` with ComplexKey** (extends `ComplexKeyResourceTemplate`): Use v2 protocol with `(field1:val1,field2:val2)` format.
- See know-050 for detailed examples and error patterns.

## When to Apply
- Any time you need to call a Rest.li service you haven't used before
- When building curli commands from code inspection rather than copying existing examples
- When debugging "Invalid D2 service name" or "context field not present" errors
- When debugging "not a Compound key" errors (likely v2 protocol on an Association)
