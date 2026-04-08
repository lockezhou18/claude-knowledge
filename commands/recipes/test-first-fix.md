---
name: test-first-fix
description: Fix a bug using test-driven workflow — write failing test FIRST, then implement minimal fix
inputs: ["bug_description"]
chain_to: investigate
chain_when: "root cause unclear"
---

## Steps

1. **Read** the relevant source files and understand current behavior
2. **Write a failing unit test** that reproduces the exact bug
3. **Run** the test to confirm it fails for the right reason:
   - `mint test` or `./gradlew test --tests '*TestClassName*'`
4. **Implement the minimal fix** — simplest change that makes the test pass
   - No new abstractions, no retry logic, no extra error handling unless asked
   - Check master for existing patterns before inventing new ones
5. **Re-run** the test — if it fails, read the error and iterate (don't ask the user)
6. **Run the full module build** to catch compilation errors:
   - `mint build` or `./gradlew build`
7. **Present** the final diff and test results only when everything passes

## Expected Output
- One new test that would have caught the bug
- One minimal code fix
- Passing build

## On Failure
- Test can't be written (no test framework?) → ask user which test approach
- Build fails 3+ times on same error → stop and explain the blocker
- Root cause unclear → chain to `/investigate`
