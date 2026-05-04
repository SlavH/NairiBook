#!/usr/bin/env python3
"""
World Engine - DigitalOcean vLLM 0.17.1 Optimized
Runs on DO Marketplace Image (vLLM pre-configured)
"""

import os, sys, subprocess, time, json, uuid
from pathlib import Path
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
import uvicorn
from src.engine import WorldEngine

# DO Marketplace vLLM usually comes pre-exposed on standard ports
VLLM_URL = os.getenv("VLLM_URL", "http://localhost:8000/v1")
SERVER_PORT = 9000

app = FastAPI(title="NairiBook - DigitalOcean Edition")
jobs = {}
engine = WorldEngine(vllm_url=VLLM_URL)

@app.get("/")
async def root():
    return HTMLResponse("<html><body><h1>NairiBook (DO Edition)</h1></body></html>")

@app.post("/gen")
async def generate(req: dict, bg: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}
    bg.add_task(run_do_pipeline, job_id, req.get("topic", ""))
    return {"id": job_id}

async def run_do_pipeline(job_id, topic):
    try:
        # DO Marketplace images have vLLM as a service, just query it
        data = await engine.generate_description(topic, "Knowledge context extracted from DO Marketplace env", "meta-llama/Meta-Llama-3.1-8B-Instruct")
        jobs[job_id] = {"status": "done", "data": data}
    except Exception as e:
        jobs[job_id] = {"status": "error", "error": str(e)}

@app.get("/job/{job_id}")
async def get_job(job_id: str):
    return jobs.get(job_id, {"status": "not_found"})

if __name__ == "__main__":
    print("Starting NairiBook on DigitalOcean vLLM...")
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
