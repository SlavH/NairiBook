#!/bin/bash
export CUDA_VISIBLE_DEVICES=0,1
python -m vllm.entrypoints.openai.api_server --model meta-llama/Meta-Llama-3.1-8B-Instruct --tensor-parallel-size 2 --port 8000 --host 0.0.0.0 --dtype bfloat16 --gpu-memory-utilization 0.5 &
python3 run.py
