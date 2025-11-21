# Local Training Guide & Hardware Requirements

Yes, you can train these models locally, but it depends heavily on your **GPU VRAM (Video RAM)**.

## 1. SOP Agent (LLM)
Target Models: **Llama 3 (8B)** or **Mistral (7B)**.

| Training Method | Precision | Required VRAM | Performance |
| :--- | :--- | :--- | :--- |
| **Full Fine-Tuning** | 16-bit (FP16) | > 24 GB | Best |
| **LoRA** (Low-Rank Adaptation) | 16-bit | ~16 GB | Excellent |
| **QLoRA** (Quantized LoRA) | 4-bit | **6 - 8 GB** | Very Good (Recommended) |

> **Recommendation**: Use **QLoRA** with the `unsloth` library. It allows you to fine-tune Llama 3 8B on a standard consumer GPU (like an RTX 3060/4060 with 8GB+ VRAM) 2-5x faster.

## 2. Vision Model (SOTA)
Target Models: **Grounding DINO**, **SAM 2**, or **RT-DETR**.

| Task | Model Size | Required VRAM |
| :--- | :--- | :--- |
| **Pre-training** (Transfer Learning) | Base / Large | 12 GB - 24 GB |
| **Fine-Tuning** (Few-Shot) | Base | **8 GB - 12 GB** |
| **Inference** (Running it) | Base | 4 GB - 6 GB |

> **Recommendation**: For the "Pre-training" phase on the massive iFixit dataset, you might need a stronger GPU (RTX 3090/4090 with 24GB) or use a cloud run for just that step. Fine-tuning on your specific data can easily be done on smaller cards (8GB+).

## 3. Logic Agent (The Judge)
*   **Type A: Deterministic Engine (Recommended)**
    *   **What it is**: Pure Python code that compares numbers.
    *   **Logic**: `if detected_screws (3) == required_screws (4): return False`
    *   **Hardware**: **CPU Only**. No GPU needed. No training needed.
*   **Type B: VLM Reasoner (Advanced)**
    *   **What it is**: A small Vision-Language Model (e.g., PaliGemma 3B, Phi-3 Vision) that looks at the image to answer "Is the battery fully removed?"
    *   **Hardware**: **Low VRAM (4-6 GB)**.
    *   **Training**: Fine-tune on "State" examples (Connected vs Disconnected).

## 4. Recommended Local Stack
If you are on Windows, use **WSL2 (Windows Subsystem for Linux)** for the best compatibility.

### Libraries
*   **LLM Training**: [`unsloth`](https://github.com/unslothai/unsloth) (Fastest, low memory) or [`axolotl`](https://github.com/OpenAccess-AI-Collective/axolotl) (Config based).
*   **Vision Training**: [`supervision`](https://github.com/roboflow/supervision) + [`transformers`](https://github.com/huggingface/transformers).

### Example: Checking your GPU
Run this in your terminal to see your VRAM:
```bash
nvidia-smi
```
Look for the **Memory-Usage** (e.g., `4000MiB / 12288MiB`).
