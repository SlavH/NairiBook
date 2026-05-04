#!/bin/bash
# Optimization for MI300X
export HSA_OVERRIDE_GFX_VERSION=11.0.0
export VLLM_USE_ROCM_PAGED_ATTENTION=1

echo "🚀 Starting vLLM for MI300X (ROCm 7.2.0)..."
python -m vllm.entrypoints.openai.api_server \
  --model mistralai/Mistral-7B-Instruct-v0.3 \
  --port 8000 \
  --host 0.0.0.0 \
  --dtype bfloat16 \
  --gpu-memory-utilization 0.95 \
  --max-model-len 32768 &

echo "Starting NairiBook API on 7878..."
python3 run.py
