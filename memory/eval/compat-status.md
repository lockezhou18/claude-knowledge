---
name: Claude Feature Compatibility Status
description: Tracks which native Claude features are available and adopted
type: eval
last_probed: 2026-04-09
claude_version: 2.1.98 (Claude Code)
---

| Feature | Status | Adoption | Issues | Notes |
|---------|--------|----------|--------|-------|
| Auto Dream /dream command works | not_available | architecture_change | #38461, #42015 | Cannot confirm /dream works without interactive session. Che |
| PreMemoryWrite/PostMemoryWrite hooks available | not_available | auto_replace | #44820 | Checked settings.json for memory hook event references |
| Native memory access tracking metadata | not_available | auto_augment | #40806 | No access metadata found in memory files |
| MEMORY.md truncation preserves newest entries | not_available | auto_augment | #40210 | Cannot confirm fix without controlled test. Bug #40210 statu |
| Dream indexes subdirectory files | available | architecture_change | #40614 | Checked MEMORY.md for subdirectory references (may be our ow |
| Team/org memory sharing available | not_available | architecture_change | #38536 | Checked settings.json for team memory references |
