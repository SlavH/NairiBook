#!/bin/bash
# Production start script
export HSA_OVERRIDE_GFX_VERSION=11.0.0
export VLLM_USE_ROCM_PAGED_ATTENTION=1

echo "🚀 Starting NairiBook 3D Pipeline..."
# Start vLLM in the background
python -m vllm.entrypoints.openai.api_server \
  --model mistralai/Mistral-7B-Instruct-v0.3 \
  --port 8000 \
  --host 0.0.0.0 \
  --dtype bfloat16 \
  --gpu-memory-utilization 0.95 \
  --max-model-len 32768 &

# Wait for vLLM to be ready
echo "⏳ Waiting for vLLM..."
sleep 45

# Start API
python3 run.py
