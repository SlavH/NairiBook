# NairiBook (AI World Gen)

NairiBook is a sophisticated AI-driven engine designed to transform static PDF documentation into interactive, explorable 3D knowledge worlds. It leverages Large Language Models (LLMs) for content synthesis, Retrieval-Augmented Generation (RAG) for knowledge retrieval, and generative pipelines to map information into 3D environments.

## Architecture

```
[PDF Input] 
    → [LangChain RAG Engine] 
        → [vLLM / Llama 3.1] (Semantic World Logic)
            → [SDXL / GenAI] (Concept Imagery)
                → [InstantMesh] (3D Reconstruction)
                    → [Three.js Web UI] (Visualization)
```

## Prerequisites

- **Compute**: NVIDIA GPU(s) with at least 48GB VRAM (for 8B models) or 192GB VRAM (for 70B models).
- **Environment**: Ubuntu 22.04+, CUDA 12.4+, Python 3.11+.
- **Credentials**: A valid [Hugging Face Access Token](https://huggingface.co/settings/tokens) with permission to access Llama 3.1 models.

## Deployment on RunPod

### 1. Initialize Container
Select the `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04` template. Ensure sufficient GPU VRAM is allocated for your target model size.

### 2. Installation
Clone the repository and install the stack:

```bash
git clone git@github.com:SlavH/NairiBook.git
cd NairiBook
pip install -r requirements.txt
```

### 3. Environment Setup
Configure your Hugging Face authentication to allow the vLLM server to pull the required models:

```bash
# Add your HF token to your environment
export HUGGING_FACE_HUB_TOKEN="your_hf_token_here"
```

### 4. Running the Engine
The engine is consolidated into a single entry point `src/main.py` which manages the vLLM lifecycle, vector indexing, and the API server.

**For standard (8B) usage:**
```bash
python3 src/main.py --port 9000
```

**For high-performance (70B) usage (Requires 192GB VRAM):**
```bash
python3 src/main.py --70b --port 9000
```

## API Documentation

The system exposes a REST API via FastAPI:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Serves the interactive 3D frontend |
| `/gen` | `POST` | Triggers a new world generation job |
| `/job/{id}` | `GET` | Polls the status and progress of a generation job |

### Example Request
```bash
curl -X POST http://localhost:9000/gen \
     -H "Content-Type: application/json" \
     -d '{"topic": "Quantum Physics", "pdf_paths": ["/workspace/physics.pdf"]}'
```

## Component Overview

- `src/main.py`: The core orchestrator. It manages process lifecycles (vLLM), vector indexing (FAISS), and the FastAPI application.
- `requirements.txt`: Curated dependency list optimized for the specified CUDA/Torch environment.
- `uploads/`: Directory for incoming PDF documents.
- `faiss_index/`: Persistence layer for RAG knowledge embeddings.

## Troubleshooting

- **vLLM Fails to Load**: Check `vllm.log`. Often caused by incorrect `TENSOR_PARALLEL` settings relative to available VRAM.
- **Out of Memory (OOM)**: Reduce `gpu-memory-utilization` in `src/main.py` or switch from `70b` to `8b` model.
- **Port Conflicts**: Ensure ports 8000 (vLLM) and 9000 (API) are available on your host/pod.
EOF
