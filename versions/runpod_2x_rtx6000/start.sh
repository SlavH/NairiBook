#!/bin/bash
export CUDA_VISIBLE_DEVICES=0,1
python -m vllm.entrypoints.openai.api_server --model mistralai/Mistral-7B-Instruct-v0.3 --tensor-parallel-size 2 --port 8000 --host 0.0.0.0 --dtype bfloat16 --gpu-memory-utilization 0.5 &
python3 run.py
