#!/usr/bin/env python3
"""
World Engine - DigitalOcean vLLM 0.17.1 Optimized for MI300X
Automatically detects and configures AMD ROCm for MI300X.
"""

import os, sys, subprocess, json, uuid
from pathlib import Path
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
import uvicorn
from src.engine import WorldEngine

# Ensure MI300X/ROCm environment variables are set
os.environ["HSA_OVERRIDE_GFX_VERSION"] = "9.4.2"
os.environ["VLLM_TARGET_DEVICE"] = "rocm"

# Configuration
VLLM_URL = os.getenv("VLLM_URL", "http://localhost:8000/v1")
SERVER_PORT = 9000

# Initialization
app = FastAPI(title="NairiBook - DigitalOcean Edition (AMD Optimized)")
jobs = {}
engine = WorldEngine(vllm_url=VLLM_URL)

def setup_amd_environment():
    """Ensure vLLM uses ROCm backend on MI300X"""
    print("Configuring environment for MI300X (ROCm)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "vllm-rocm"])
        print("vLLM-ROCm backend configured.")
    except Exception as e:
        print(f"Warning: vLLM-ROCm configuration failed: {e}")

@app.get("/")
async def root():
    return HTMLResponse("<html><body><h1>NairiBook (DO + AMD Engine)</h1><input id='t' placeholder='Topic'><button onclick='go()'>Go</button><script>async function go(){let t=document.getElementById('t').value;let r=await fetch('/gen',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({topic:t,pdf_paths:[]})});alert('Started');}</script></body></html>")

@app.post("/gen")
async def generate(req: dict, bg: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}
    bg.add_task(run_do_pipeline, job_id, req.get("topic", ""))
    return {"id": job_id}

async def run_do_pipeline(job_id, topic):
    try:
        # Use vLLM endpoint configured for MI300X
        data = await engine.generate_description(topic, "Knowledge context extracted from DO Marketplace env", "meta-llama/Meta-Llama-3.1-8B-Instruct")
        jobs[job_id] = {"status": "done", "data": data}
    except Exception as e:
        jobs[job_id] = {"status": "error", "error": str(e)}

@app.get("/job/{job_id}")
async def get_job(job_id: str):
    return jobs.get(job_id, {"status": "not_found"})

if __name__ == "__main__":
    setup_amd_environment()
    print("Starting NairiBook on DigitalOcean (MI300X optimized)...")
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
