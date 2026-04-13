---
name: AgentBus shell PATH issue
description: Agentbus -c shell commands use non-login shell with minimal PATH — mint and other LinkedIn tools not found. Use -m (thinking) or prefix PATH.
type: feedback
originSessionId: 4a5c2d5a-af02-4e3e-9323-5e7659721be4
---
AgentBus `-c` (shell) commands run in a non-interactive, non-login shell (`sh -c "..."`), which only gets the base system PATH (`/usr/local/bin:/usr/bin:/bin:/sbin`).

**Why:** The agentbus listener spawns commands via Python `subprocess`, which does not source `.bashrc` / `.bash_profile`. LinkedIn tools like `mint` live in `/usr/local/linkedin/bin` which is added by the profile.

**How to apply:**

| Transport | Shell type | PATH | LinkedIn tools? |
|-----------|-----------|------|-----------------|
| `-c "command"` (shell) | `sh -c` (non-login) | Minimal system PATH | NO — `mint`, `phoenix`, etc. not found |
| `-m "message"` (thinking) | Claude's Bash tool (`bash -l`) | Full login PATH | YES — works correctly |
| Interactive SSH (`ssh -t vm`) | Login shell | Full PATH | YES |

**Workarounds (in order of preference):**
1. **Use thinking mode (`-m`)** for builds — VM Claude runs via login shell
2. **Prefix PATH** in shell commands: `PATH=/usr/local/linkedin/bin:$PATH mint build ...`
3. **Fix the listener** to spawn `bash -l -c "..."` instead of `sh -c "..."` (permanent fix, not yet done)
