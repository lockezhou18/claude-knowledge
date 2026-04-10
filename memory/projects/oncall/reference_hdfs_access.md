---
name: HDFS Access Reference
description: Working steps for grid gateway SSH, ksudo, HDFS commands, and common permission issues
type: reference
---

## HDFS Access via Grid Gateway

### Working Steps (verified 2026-03-24)
```bash
# 1. Remove stale host key if needed
ssh-keygen -R ltx1-holdemgw01.grid.linkedin.com

# 2. SSH to grid gateway
ssh -K ltx1-holdemgw01.grid.linkedin.com

# 3. Switch to proxy user
ksudo -e mcmhp
```

### Common Permission Issues
- Files owned by `metrics:ump033349` (or other users) → `mcmhp` gets "Permission denied"
- Fix: `hdfs dfs -chmod -R 777 /jobs/<path>` (must run as owner or use SentinelGuard)
- `-skipTrash` triggers **SentinelGuard** approval → approve at https://nuage.prod.linkedin.com/workflowApprovalRequestViews#filter=role%3DREQUESTER then re-run same command

### Gotchas
- `ksudo` only works on grid gateway machines, NOT on laptop
- `dali --gridproxy` needs interactive MFA — can't run non-interactively from Claude
- Azkaban HDFS Browser is useful for browsing: `https://ltx1-holdemaz03.grid.linkedin.com:8443/hdfs/<path>` (set proxy user via "Change User" button)
- Host key changes are common — always `ssh-keygen -R` first if SSH fails

**Why:** HDFS access is needed for OA tickets (Pinot segment cleanup), DSR data deletion, and mcm-offline operations.

**How to apply:** Use grid gateway SSH + ksudo for HDFS operations. For OA-812 type issues (Pinot segment mismatch), delete the stale output segment directories, not the input data.
