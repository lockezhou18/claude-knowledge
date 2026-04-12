---
id: know-063
track: knowledge
type: semantic
repos: ["*"]
tags: ["llm", "fine-tuning", "cost-optimization", "model-selection", "small-models", "qwen", "production", "architecture"]
severity: high
rot_rate: slow
status: active
created: 2026-04-11
last_verified: 2026-04-11
use_count: 0
outcome_score: 0
origin_skill: learn
related_to: ["aha-007"]
---

# When Small Fine-Tuned Models Beat Frontier Models

## Context

LinkedIn LIHA uses a two-tier model strategy: frontier models (GPT-4o, Claude) for recruiter-facing conversation, fine-tuned Qwen-3 8B for high-volume structured tasks. Discovered during /explore of talent-agent-service and CMA codebases.

## Guidance

**When a task is structured, high-volume, and rubric-definable, fine-tune a small model instead of calling a frontier API.**

### The Decision Boundary

Use **frontier model** (GPT-4o, Claude) when:
- Task is conversational / open-ended
- Volume is low (hundreds-thousands/day)
- Quality requirements change frequently
- No training data exists yet

Use **fine-tuned small model** (8B class) when:
- Task is structured / classifiable (scoring, extraction, classification)
- Volume is high (millions/month)
- You can write a rubric for what "correct" looks like
- Training data exists or can be generated
- Data must stay on-prem
- Latency matters (<500ms vs 1-3s API)

### The Rule of Thumb

**If you can write a rubric for it, you can fine-tune a small model for it.**

### Evidence: LIHA's Two-Tier Architecture

| Task | Model | Why |
|---|---|---|
| Recruiter chat | GPT-4o via Proxima | Open-ended, low volume, needs broad knowledge |
| Sub-agent workflows | Claude Agent SDK | Tool use, multi-step reasoning |
| Candidate evaluation | Qwen-3 8B FT (SFT+RL) | Structured rubric, millions/month, 1 GPU, <500ms |
| CMA activity extraction | Qwen-3 8B FT (SFT) | Pattern extraction from trajectories, nearline |
| i18n evaluation | Qwen-3 8B FT (i18n variant) | Same task, non-English profiles |

### Economics

| | Frontier API | Self-hosted 8B FT |
|---|---|---|
| Per-call cost | $0.01-0.03 | ~$0.001 |
| At 1M calls/month | $10K-30K | $1K-3K |
| Fine-tunable | No (API) | Yes (SFT + RL) |
| Data leaves network | Yes | No |
| Latency | 1-3s | <500ms |
| Quality on rubric tasks | Good | Better (domain-trained) |

## When to Apply

- When designing an AI system with mixed task types — split into conversation tier + structured tier
- When cost projections for LLM API calls look high — check if tasks can be rubric-defined
- When evaluating build-vs-buy for AI features — fine-tuning investment pays off above ~100K calls/month
- When data privacy is a constraint — self-hosted small models keep data on-prem
- When latency is critical — 8B inference is 3-6x faster than frontier API roundtrip
