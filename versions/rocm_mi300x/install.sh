#!/bin/bash
# Install vLLM 0.17.1 specifically for ROCm 7.2
pip install vllm==0.17.1 --no-deps
pip install pydantic fastapi uvicorn[standard] openai langchain langchain-community faiss-cpu pypdf
echo "✅ ROCm Optimized environment ready!"
