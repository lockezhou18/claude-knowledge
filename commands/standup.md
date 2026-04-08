Generate my daily standup summary:

1. Check recent git commits from the last 24 hours across all repos in ~/workspace/connected_project_phase2/ (use `git log --all --author=bizhou --since="24 hours ago" --oneline` in each MP directory)
2. List any open PRs I have (use `gh pr list --author @me --state open` in each repo)
3. Check for any PRs merged in the last 24 hours (`gh pr list --author @me --state merged --search "merged:>=$(date -v-1d +%Y-%m-%d)"`)
4. Summarize what was accomplished and what's in progress

Format as markdown:

## Done
(Merged PRs and completed work from commits)

## In Progress
(Open PRs and uncommitted work)

## Blockers
(Any CI failures, pending reviews, or environment issues noticed)
