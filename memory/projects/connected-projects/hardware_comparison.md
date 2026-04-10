# Hardware Comparison: DGX Spark vs Mac Studio for LLM

## Key Specs

| Spec | DGX Spark (GB10) | Mac Studio M4 Ultra | Mac Studio M3 Ultra |
|---|---|---|---|
| Price | ~$3,999 | ~$4,999-$7,999 | ~$3,999+ |
| Memory | 128GB LPDDR5x | 192GB or 256GB unified | 192GB unified |
| Memory Bandwidth | **273 GB/s** | est. **900+ GB/s** | **819 GB/s** |
| GPU Compute | Blackwell, 1 PFLOP FP4 (sparse) | 80-core GPU | 80-core GPU |
| TDP | 140W | ~200W | ~200W |
| CUDA/Tensor Cores | Yes (5th gen Tensor) | No (Metal/ANE) | No |

## Critical Insight: Memory Bandwidth is the Bottleneck

LLM inference/reasoning is memory-bandwidth bound. DGX Spark's 273 GB/s vs Mac Studio's 819+ GB/s means Mac Studio generates tokens ~3x faster.

## Estimated Performance

| Device | ~tok/s (20B FP16) | ~tok/s (70B Q4) |
|---|---|---|
| DGX Spark | ~8-12 | ~4-6 |
| Mac Studio M3 Ultra | ~25-35 | ~12-18 |
| Mac Studio M4 Ultra | ~30-40 | ~15-22 |

## When to Pick Which

- **Fast inference/reasoning**: Mac Studio (3x bandwidth)
- **Run 70B+ models**: Mac Studio (256GB option)
- **Fine-tuning (LoRA/SFT)**: DGX Spark (CUDA + Tensor Cores)
- **Daily driver + AI**: Mac Studio
- **CUDA research frameworks**: DGX Spark
- **Best bang for buck inference**: Mac Studio M3 Ultra (192GB, ~$4K)

## Nemotron 3 Nano (31.6B total, 3.6B active MoE)

- DGX Spark: Can do LoRA fine-tuning (128GB fits model + optimizer)
- Mac Studio: Better for inference, but no CUDA for training
- RTX 5090 (32GB): QLoRA only for this model size
