#!/bin/bash
pip install vllm --no-deps
pip install pydantic pydantic-settings fastapi uvicorn[standard] prometheus-client openai langchain langchain-community langchain-text-splitters faiss-cpu pypdf sentence-transformers huggingface-hub diffusers accelerate transformers bitsandbytes ray
