---
name: playwright-cli
description: Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, test web applications, or extract information from web pages.
allowed-tools: Bash(playwright-cli:*), Bash(npx playwright-cli:*), Bash(npx @playwright/cli@latest:*), Bash(npm install -g @playwright/cli*), Bash(which playwright-cli*)
---

# Browser Automation with playwright-cli

**IMPORTANT: Always open the browser in headed mode (`--headed`) so the user can see the browser window and interact with it (e.g., for SSO login). Never use headless mode unless the user explicitly requests it.**

## Auto-install

Before running any playwright-cli command, check if it's installed:

```bash
which playwright-cli 2>/dev/null || echo "not found"
```

If not found, install it:

```bash
npm install -g @playwright/cli@latest
```

Then install skills if `.claude/skills/playwright-cli/` does not exist in the project:

```bash
playwright-cli install --skills
```

## Quick Start

```bash
# open new browser (ALWAYS use --headed)
playwright-cli open --headed
# navigate to a page
playwright-cli goto https://example.com
# interact using refs from the snapshot
playwright-cli click e15
playwright-cli type "search text"
playwright-cli press Enter
# take a screenshot
playwright-cli screenshot
# close the browser
playwright-cli close
```

## Core Commands

```bash
playwright-cli open --headed              # open visible browser
playwright-cli open --headed URL          # open and navigate
playwright-cli goto URL                   # navigate
playwright-cli click REF                  # click element by ref
playwright-cli fill REF "value"           # fill input field
playwright-cli type "text"                # type text
playwright-cli press Enter                # press key
playwright-cli select REF "option"        # select dropdown
playwright-cli snapshot                   # capture page state
playwright-cli screenshot                 # take screenshot
playwright-cli close                      # close browser
```

## Navigation

```bash
playwright-cli go-back
playwright-cli go-forward
playwright-cli reload
```

## Tabs

```bash
playwright-cli tab-list
playwright-cli tab-new URL
playwright-cli tab-select 0
playwright-cli tab-close
```

## Storage & Auth

```bash
playwright-cli state-save auth.json       # save cookies + storage
playwright-cli state-load auth.json       # restore session
playwright-cli cookie-list
playwright-cli cookie-set NAME VALUE --domain=example.com
```

## Persistent Sessions

```bash
# persistent profile retains cookies/auth across sessions
playwright-cli open --headed --persistent
# named session
playwright-cli -s=myapp open --headed --persistent
playwright-cli -s=myapp goto https://app.example.com
playwright-cli -s=myapp close
```

## Network & DevTools

```bash
playwright-cli console                    # view console output
playwright-cli network                    # view network requests
playwright-cli route "**/*.jpg" --status=404  # mock requests
playwright-cli eval "document.title"      # run JS
```

## Snapshots

After each command, playwright-cli provides a snapshot of the current browser state with element refs (e1, e2, etc.) that you can use for interactions.

## Common Workflows

### Form submission
```bash
playwright-cli open --headed https://example.com/form
playwright-cli snapshot
playwright-cli fill e1 "user@example.com"
playwright-cli fill e2 "password123"
playwright-cli click e3
```

### LinkedIn SSO login (interactive)
```bash
playwright-cli open --headed https://www.linkedin.com/login
# User logs in manually in the headed browser
# Then save the auth state for reuse
playwright-cli state-save linkedin-auth.json
```

### Greenhouse sandbox testing
```bash
playwright-cli open --headed https://app.greenhouse.io/users/sign_in
# User logs in, then:
playwright-cli state-save greenhouse-auth.json
# Later sessions:
playwright-cli open --headed
playwright-cli state-load greenhouse-auth.json
playwright-cli goto https://app.greenhouse.io/dashboard
```
