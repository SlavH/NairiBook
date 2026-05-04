#!/bin/bash
set -e
echo "🚀 Preparing Production Environment for ROCm MI300X..."

# Ensure dependencies are installed correctly within the environment
# We install base requirements for our app
pip install --upgrade pip
pip install fastapi uvicorn[standard] openai langchain langchain-community langchain-text-splitters faiss-cpu pypdf sentence-transformers huggingface-hub diffusers accelerate transformers bitsandbytes ray cbor2

echo "✅ Environment configured. Please ensure you are running this inside a ROCm-enabled container!"
