# Karpathy's autoresearch — Concrete Case Study of Harness Engineering

**Source:** https://github.com/karpathy/autoresearch
**Fetched:** 2026-04-15

## Overview

Autoresearch is a framework that enables AI agents to conduct machine learning research autonomously. As described in the project: "give an AI agent a small but real LLM training setup and let it experiment autonomously overnight."

The system allows autonomous agents to modify code, train models, evaluate results, and iterate on improvements without human intervention, creating a fully automated research cycle.

## Core Architecture

The project maintains intentional simplicity with three essential files:

**1. prepare.py** — Handles fixed constants, one-time data preparation (downloading datasets, training tokenizers), and runtime utilities like dataloaders and evaluation functions. This file remains unchanged during agent iterations.

**2. train.py** — The single file agents modify. Contains the complete GPT model implementation, optimizer configurations (Muon + AdamW), and the training loop. Agents can adjust architecture, hyperparameters, batch sizes, and optimizer settings.

**3. program.md** — Baseline instructions guiding agent behavior. Humans edit this file to refine the research objectives and agent constraints.

## Key Design Principles

**Fixed Time Budget**: Training runs for exactly 5 minutes (wall clock, excluding startup/compilation), making experiments directly comparable regardless of architectural changes. This design enables approximately 12 experiments per hour, or roughly 100 overnight runs.

**Single Metric**: Validation bits per byte (val_bpb) determines success — lower scores indicate improvement. This metric remains vocabulary-size-independent, allowing fair comparison across architectural variations.

**Self-Contained**: No distributed training complexity, no external dependencies beyond PyTorch and minimal packages. Single GPU, single file, one metric.

## Workflow

The agent iteratively:
1. Modifies train.py based on program.md instructions
2. Executes 5-minute training runs
3. Evaluates whether val_bpb improved
4. Retains successful changes or discards unsuccessful ones
5. Repeats autonomously

## Implementation Details

The training setup builds on simplified nanochat architecture. Agents have complete freedom to modify:
- Model depth and width
- Attention patterns
- Batch sizes and learning rates
- Optimizer configurations
- Any other hyperparameters within train.py

## Requirements

- Single NVIDIA GPU (tested on H100)
- Python 3.10+
- uv project manager

## Quick Start Commands

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Prepare data and tokenizer (one-time, ~2 min)
uv run prepare.py

# Single training experiment (~5 min)
uv run train.py
```

## Operating the Agent

Users interact by directing Claude or similar AI models to examine program.md and initiate experiments:

> "Hi have a look at program.md and let's kick off a new experiment!"

The markdown file serves as a lightweight skill specification for the autonomous agent.

## Platform Considerations

Currently requires NVIDIA GPUs. Notable forks extend support to macOS, Windows, and AMD platforms by adjusting hyperparameters and dataset choices for smaller compute environments.

## Language Composition

83.4% Python, 16.6% Jupyter Notebook.

---

## Cybernetic Analysis — Why This Is a Textbook Harness

autoresearch is a minimal viable ultrastability loop. Every cybernetic principle maps cleanly:

| Cybernetic Concept | autoresearch Implementation |
|---|---|
| **Deterministic shell (Level 1)** | `prepare.py` (immutable), 5-min wall clock, val_bpb metric, retain-on-improvement rule |
| **Probabilistic core (Level 2)** | LLM agent freely modifying `train.py` |
| **Crystallization** | Successful changes kept as new baseline; failed changes discarded |
| **Ultrastability** | When current best (L1) is beaten, new config becomes L1. When not beaten, L2 tries again |
| **Everything-as-feedback** | val_bpb goes up? Information. Goes down? Also information. Both drive next iteration |
| **Variety attenuation** | Single file scope, single metric, single GPU, fixed time budget — massively constrains the exploration space |
| **Variety amplification** | Full architectural freedom within train.py — agent can change anything inside the constraint box |
| **Good Regulator** | val_bpb IS the model of the system — one number that captures "did this help?" |
| **POSIWID** | The system's purpose is literally what it does: lower val_bpb or don't |
| **Eigenform** | `prepare.py` and `program.md` survive all iterations — they ARE the fixed points |

### Key Design Insight

**Fixed time budget + single metric + retained-on-improvement** is the minimum viable harness for turning probabilistic exploration into deterministic progress.

The 5-minute wall clock is the crystallization temperature — short enough for rapid exploration (100 experiments/night), long enough for meaningful signal. The retain-on-improvement rule is binary ultrastability: beat the current best or the change is discarded.

### Comparison with Compound Learning Ecosystem

| Dimension | autoresearch | Compound Learning |
|---|---|---|
| **Exploration unit** | 5-min training run | One Claude session |
| **Metric** | val_bpb (single, precise) | outcome_score (multi-signal, approximate) |
| **Crystallization threshold** | Any improvement over baseline | use_count >= 3 AND score >= 2.0 |
| **Shell complexity** | 3 files, ~500 lines | 20+ skills, 8 hooks, eval pipeline |
| **Feedback latency** | 5 minutes | Days (cross-session) |
| **What persists** | Best train.py | Graduated insights, skills, rules |
| **What's discarded** | Failed modifications | Pruned insights (score < -2) |
| **Human role** | Edit program.md | Correct approach, approve plans, /compound |
| **S5 (Identity)** | program.md constraints | Principle 0 + engineering principles |

autoresearch proves the pattern works at the simplest scale. The compound learning ecosystem applies it at the complex end — longer feedback loops, richer signals, more diverse crystallization targets. Same cybernetic architecture.
