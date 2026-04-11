# Session Handoff (Deprecated)

Session continuity is now handled natively by Claude's memory system:
- **Auto Memory** saves key facts, decisions, and context during sessions
- **memory/MEMORY.md** serves as the persistent index
- **Active work** tracked in `memory/project/` files

If you need an explicit handoff note, just ask: "Summarize this session for next time" — Claude will write to memory.

No separate skill needed.
