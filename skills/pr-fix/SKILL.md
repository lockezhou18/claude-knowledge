# PR Fix Workflow

Address all open PR review comments, run tests, and push.

## Step 1: Get PR review comments

Run `gh pr view --json reviewDecision,reviews,comments` and `gh pr view --comments` to get all review feedback on the current branch's PR.

Summarize the review comments and present them to the user before proceeding.

## Step 2: Address each comment

For each review comment:
1. Read the relevant file and understand the context
2. Make the requested change using targeted edits
3. Move to the next comment

Do NOT explore the codebase extensively — make focused changes based on what the reviewer asked for.

## Step 3: Run tests

Run tests from the correct module directory (not the repo root). Use `mint build` or the appropriate build command for the module being changed.

If tests fail:
- Read the failure output
- Fix the issue
- Re-run tests
- Repeat up to 3 times

Do NOT consider the task complete until tests pass.

## Step 4: Commit and push

1. Stage only the files you changed
2. Commit with a message summarizing the review fixes (e.g., "Address PR review comments: fix X, update Y")
3. Push to the current branch

## Step 5: Summary

Report back with:
- Which comments were addressed
- What changes were made
- Test results
- Whether the push succeeded
