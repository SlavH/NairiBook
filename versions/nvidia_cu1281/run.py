#!/usr/bin/env python3
import os, sys, subprocess, time, threading
from pathlib import Path
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
import uvicorn
from src.engine import WorldEngine

VLLM_PORT = 8000
SERVER_PORT = 9000
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"
processes = []

app = FastAPI(title="NairiBook Engine")
jobs = {}
engine = WorldEngine(vllm_url=f"http://localhost:{VLLM_PORT}/v1")

# ... (HTML UI and API endpoints similar to run.py) ...
# I will implement a minimal robust version of the server logic here

@app.post("/gen")
async def generate(req: dict, bg: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}
    bg.add_task(run_pipeline, job_id, req.get("pdf_paths", []), req.get("topic", ""))
    return {"id": job_id}

async def run_pipeline(job_id, paths, topic):
    try:
        vs = engine.build_index(paths, f"idx_{job_id}")
        ctx = "\n\n".join([d.page_content for d in vs.similarity_search(topic, k=5)])
        data = await engine.generate_description(topic, ctx, MODEL_NAME)
        jobs[job_id] = {"status": "done", "data": data}
    except Exception as e:
        jobs[job_id] = {"status": "error", "error": str(e)}

if __name__ == "__main__":
    # Start vLLM process here
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
