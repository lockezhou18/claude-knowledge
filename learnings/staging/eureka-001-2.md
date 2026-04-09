---
id: eureka-001-2
track: knowledge
type: semantic
repos: ['connected-project-phase2', '*']
tags: ['eureka', 'figma', 'playwright', 'e2e-testing', 'design-driven', 'bug-bash', 'greenhouse', 'phase2']
severity: high
created: '2026-04-03'
last_verified: '2026-04-03'
use_count: 0
outcome_score: 0.0
rot_rate: slow
status: active
graduation_candidate: true
visibility: team
origin_skill: eureka
---

## Breakthrough

Use Figma designs as the authoritative source of truth to auto-generate cross-system E2E test cases that verify UI state, backend data, and ATS state simultaneously — turning design specs into executable test matrices.

## The Old Way

Testing was done in silos:
- **UI testing**: Manual clicking through Recruiter, eyeballing if it looks right
- **Backend testing**: grpcurli commands verifying data in HP, run separately
- **ATS testing**: Manual checks in Greenhouse sandbox
- **Test case generation**: Someone reads the design doc and manually writes test scenarios
- **Design drift**: No automated way to catch when implementation diverges from Figma spec

Each layer tested independently. Cross-system assertions (did the UI change match what Greenhouse shows?) required manual coordination. Test cases were derived from eng design docs, not the actual design screens.

## The New Way

**Figma REST API → Claude analysis → test case matrix → Playwright + API verification triangle**

1. Figma REST API (`/v1/files/{key}?depth=2`) pulls complete file structure (pages, frames, IDs)
2. Figma image API (`/v1/images/{key}?ids=...`) downloads screenshots of every prototype frame
3. Claude reads screenshots → extracts the **complete UI state machine** (states, transitions, UI elements, expected text, badge colors)
4. Each design state maps to: **Playwright action** (trigger) + **Greenhouse API assertion** (ATS side) + **grpcurli assertion** (HP side) + **Playwright screenshot** (UI verification)
5. Run against real sandbox (Greenhouse Sandbox 2 + prod HP)

The triangle:
```
        Playwright (UI trigger + verify)
       /                               \
      /    each Figma state = one       \
     /     row in the test matrix        \
Greenhouse API  ←——————————————→  HP Backend (grpcurli)
  (verify ATS state)              (verify HP state)
```

Why this is fundamentally better:
- **Design is the spec**: Test cases are derived from actual Figma screens, not someone's interpretation of a doc
- **Cross-system by default**: Every test verifies all three systems, not just one
- **Visual regression**: Playwright screenshots compared against Figma screenshots catch design drift
- **Reproducible**: The Figma file structure is stable — same API call, same screens, same test matrix
- **Scalable**: Any new Figma page/frame automatically becomes a test candidate

## Impact

- Replaces manual test case writing for Connected Projects Phase 2 bug bash
- Pattern generalizable to any feature with Figma designs + multi-system integration
- Scope: team-wide (HP team), potentially org-wide (any team with Figma + ATS/external system)
- Reduces bug bash prep from days to hours

## Proof of Concept (2026-04-03)

- File: `QY9uG0nCKIlqkQr7hsDGQT` (Connected Projects - Pipeline stage sync)
- Extracted 6 prototype states: Stage move start → Pending → Confirmed → Mismatch → Expired → Failed
- Each state has: UI badge color, tooltip text, candidate count changes, conflict banners
- Downloaded all screenshots to `bug-bash/figma-screens/`
- Personal access token bypasses MCP rate limits for bulk operations

## Risks & Caveats

- Figma personal access token needs to be stored securely (not in git)
- MCP rate limit (View seat) is tight — REST API with personal token is the workaround
- Design file must be kept up-to-date — stale Figma = stale test cases
- Figma component names don't map 1:1 to DOM selectors — need `data-testid` or ARIA role bridging
- Prototype flows (transitions) aren't fully extractable from REST API — rely on frame naming convention

## Next Steps

1. Create test case matrix from the 6 extracted states
2. Wire Playwright to trigger stage moves in Recruiter UI
3. Add Greenhouse API + grpcurli assertions after each move
4. Compare Playwright screenshots against Figma screenshots for visual regression
5. Package as a `/recipe` for the bug bash team
