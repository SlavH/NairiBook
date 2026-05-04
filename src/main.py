#!/usr/bin/env python3
"""
World Engine - Integrated Solution
"""

import os, sys, subprocess, time, json, uuid, threading
from pathlib import Path
import httpx
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
import uvicorn

# Config
VLLM_PORT = 8000
SERVER_PORT = 9000
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Config
VLLM_PORT = 8000
SERVER_PORT = 9000
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"
TENSOR_PARALLEL = 1
processes = []

class WorldEngine:
    async def run(self, job_id, topic, pdf_paths, jobs):
        try:
            # 1. RAG
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            all_chunks = []
            for p in pdf_paths:
                if os.path.exists(p):
                    docs = PyPDFLoader(p).load()
                    all_chunks.extend(RecursiveCharacterTextSplitter(chunk_size=1000).split_documents(docs))
            
            if not all_chunks:
                raise ValueError("No valid PDF content found.")
            
            vs = FAISS.from_documents(all_chunks, embeddings)
            context = "\n\n".join([d.page_content for d in vs.similarity_search(topic, k=5)])
            
            # 2. LLM Description
            prompt = f"Create a JSON world map for {topic} based on: {context[:2000]}. JSON ONLY."
            async with httpx.AsyncClient(timeout=120) as client:
                r = await client.post(f"http://localhost:{VLLM_PORT}/v1/chat/completions", 
                    json={"model": MODEL_NAME, "messages": [{"role": "user", "content": prompt}]})
                import re
                content = r.json()["choices"][0]["message"]["content"]
                match = re.search(r'\{.*\}', content, re.DOTALL)
                world_data = json.loads(match.group())
            
            # 3. Model Placeholder
            for obj in world_data.get("objects", []):
                obj["model"] = "generated_model_for_" + obj["name"]
                
            jobs[job_id] = {"status": "done", "data": world_data}
        except Exception as e:
            jobs[job_id] = {"status": "error", "error": str(e)}

app = FastAPI()
jobs = {}
engine = WorldEngine()

@app.post("/gen")
async def generate(req: dict, bg: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}
    bg.add_task(engine.run, job_id, req["topic"], req.get("pdf_paths", []), jobs)
    return {"id": job_id}

@app.get("/job/{job_id}")
async def get_job(job_id: str):
    return jobs.get(job_id, {"status": "not_found"})

if __name__ == "__main__":
    # Simplified main for integrated run
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
