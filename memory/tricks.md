# Tricks & Handy Shortcuts

## PR CI Checks

- **Rerun a stuck/pending CI check**: `rerun-check -c "<check name>"` (e.g., `rerun-check -c "Owner Approval"`)
- Common use case: "Owner Approval" stays pending after force-push/rebase — rerun it to re-trigger

## Tmux (prefix: Ctrl-a)

- Config: `~/.tmux.conf`
- **Close window**: `Ctrl-a` + `&` (prompts y/n)
- **Close pane**: `Ctrl-a` + `x` (prompts y/n)
- **Split horizontal**: `Ctrl-a` + `|`
- **Split vertical**: `Ctrl-a` + `-`
- **Navigate panes**: `Ctrl-a` + arrow keys
- **Resize panes**: `Ctrl-a` + `H/J/K/L` (5 cells, repeatable)
- **Copy mode**: vi keys, `v` to select, `y` to copy (pbcopy)
- **Paste**: `Ctrl-a` + `p`
- **Reload config**: `Ctrl-a` + `r`
