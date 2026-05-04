#!/usr/bin/env python3
import os, uuid, uvicorn, httpx
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Configuration
VLLM_URL = "http://localhost:8000/v1"
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3" 
NAIRIBOOK_PORT = 9000

app = FastAPI(title="NairiBook Engine - Web Interface")
jobs = {}
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

HTML_UI = """
<!DOCTYPE html>
<html>
<head><title>NairiBook 3D Expedition</title></head>
<body>
    <h1>NairiBook Generative Knowledge Expedition</h1>
    <input type="text" id="topic" placeholder="Enter topic (e.g. Quantum Physics)">
    <button onclick="gen()">Generate World</button>
    <div id="status"></div>
    <div id="output" style="white-space: pre-wrap; background: #f0f0f0; padding: 10px;"></div>
    <script>
        async function gen() {
            const topic = document.getElementById('topic').value;
            document.getElementById('status').innerText = 'Generating...';
            const resp = await fetch('/gen', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({topic: topic, pdf_paths: []})
            });
            const data = await resp.json();
            poll(data.id);
        }
        async function poll(id) {
            const resp = await fetch('/status/' + id);
            const data = await resp.json();
            if (data.status === 'done') {
                document.getElementById('output').innerText = data.data;
                document.getElementById('status').innerText = 'Ready';
            } else {
                document.getElementById('status').innerText = 'Processing...';
                setTimeout(() => poll(id), 2000);
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return HTML_UI

@app.post("/gen")
async def generate(req: dict, bg: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}
    bg.add_task(run_pipeline, job_id, req.get("pdf_paths", []), req.get("topic", ""))
    return {"id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    return jobs.get(job_id, {"status": "not_found"})

async def run_pipeline(job_id, pdf_paths, topic):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{VLLM_URL}/chat/completions", json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": f"Generate a detailed 3D world description for the topic: {topic}. Structure it as an explorable simulation map."}],
                "temperature": 0.7,
                "max_tokens": 2000
            })
            result = resp.json()
        jobs[job_id] = {"status": "done", "data": result['choices'][0]['message']['content']}
    except Exception as e:
        jobs[job_id] = {"status": "error", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=NAIRIBOOK_PORT)
