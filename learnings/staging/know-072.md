---
id: 'know-072'
track: 'knowledge'
type: 'semantic'
repos: ['*']
tags: ['claude-code', 'session', 'recovery', 'tmux', 'jsonl', 'operational']
severity: 'medium'
created: '2026-04-15'
last_verified: '2026-04-15'
use_count: 0
outcome_score: 0.0
status: 'active'
rot_rate: 'permanent'
---

# When a Claude Code session is lost (tmux closed, terminal crash), recover via JSONL files

Sessions are stored as JSONL files in `~/.claude/projects/<project-dir-encoded>/`. Each file is named `<session-id>.jsonl`.

**Recovery steps:**
1. `ls -lt ~/.claude/sessions/*.json` — lists active session metadata (PID, sessionId, cwd)
2. `ps aux | grep claude` — shows which sessions are still running
3. `ls -lt ~/.claude/projects/<project-dir>/*.jsonl` — find recent session files (sorted by modification time)
4. `grep -l "keyword" ~/.claude/projects/<project-dir>/*.jsonl` — search session content for a keyword
5. `claude resume <session-id>` — resume from the correct working directory

**Key details:**
- Session JSONL path encodes the working directory: `/Users/bizhou` → `-Users-bizhou`
- `claude resume` must be run from the same working directory as the original session
- If a tmux session is closed, the Claude process inside it is killed (won't show in `ps`)
- The JSONL file persists even after the process dies — the conversation is recoverable
- First user message can be extracted with: `head -20 <file>.jsonl | python3 -c "import sys,json; ..."`

**Why:** tmux + Claude is a common pattern. Accidental tmux close kills the process but the session data remains on disk. Knowing the file layout saves minutes of searching.
