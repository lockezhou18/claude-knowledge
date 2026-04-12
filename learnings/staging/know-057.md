---
id: "know-057"
track: "knowledge"
type: "semantic"
repos: ["*"]
tags: ["testing", "mock", "asyncio", "python", "coroutine"]
severity: "medium"
rot_rate: "slow"
created: "2026-04-12"
last_verified: "2026-04-12"
use_count: 1
outcome_score: 1
status: "active"
---

## Context

When testing code that calls `asyncio.run(coroutine_function(...))`, patching `asyncio.run` with a synchronous `MagicMock` creates the coroutine object but never awaits it. Python GC emits `RuntimeWarning: coroutine was never awaited` — but the warning may appear in a completely different test due to GC timing.

## Guidance

Patch the async function itself with `AsyncMock`, not `asyncio.run`:
```python
# WRONG — leaks unawaited coroutine:
with patch("asyncio.run", return_value=mock_reply):

# RIGHT — no coroutine created:
with patch("module.async_func", new_callable=AsyncMock, return_value=mock_reply):
```

## When to Apply

When testing CLI or sync wrapper code that calls `asyncio.run()`. When seeing `RuntimeWarning: coroutine was never awaited` in tests — the source may be in a different test file from where the warning appears.
