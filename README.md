# NairiBook (AI World Gen)

NairiBook is part of the **Nairi Ecosystem** — a suite of AI-powered tools designed to bridge human knowledge and digital transformation.
- [Nairi GitHub](https://github.com/SlavH/Nairi)
- [Nairi Website](https://nairi-seven.vercel.app/)

NairiBook is a sophisticated AI-driven engine designed to transform static PDF documentation into interactive, explorable 3D knowledge worlds. It leverages Large Language Models (LLMs) for content synthesis, Retrieval-Augmented Generation (RAG) for knowledge retrieval, and generative pipelines to map information into 3D environments.

## The Vision
NairiBook is more than an engine; it is a platform for **Generative Knowledge Expedition**. We believe that static PDF documents belong to the past. Our mission is to transform dense, linear knowledge bases into immersive, explorable 3D spaces. By mapping complex concepts into physical dimensions, we enable users to "walk through" technical documentation, making information intuitive, memorable, and interactive.

## How it works: Knowledge-to-Space Mapping
NairiBook follows a multi-stage pipeline:
1.  **Ingestion**: Parses PDF documents into semantic chunks.
2.  **Synthesis**: Uses LLMs to distill core concepts into 3D world descriptions.
3.  **Visualization**: Generates concept imagery and reconstructs them into 3D assets.
4.  **Expedition**: Visualizes the knowledge space in the browser.

## Examples
*   **Physics Manuals**: "Quantum Physics" -> A space where particles are floating spheres, and forces are represented by gravitational wells.
*   **Historical Archives**: "Ancient Rome" -> A reconstructed forum where historical documents appear as interactive scrolls and artifacts.
*   **Technical Documentation**: "System Architecture" -> A city-like map where servers are towers and data streams are glowing highways.

## Deployment Options

NairiBook is architected for cross-platform hardware support:

| Environment | Architecture | Key Features |
| :--- | :--- | :--- |
| **NVIDIA (CUDA)** | `nvidia_cu1281` | Full support for `InstantMesh`, highest performance. |
| **AMD (ROCm)** | `amd_rocm610` | Optimized for **MI300X**, uses `Stable Fast 3D`. |
| **Cloud (DO)** | `digitalocean_vllm` | Lightweight, managed vLLM endpoint integration. |

## Quick Start
1.  **Clone the repo**: `git clone git@github.com:SlavH/NairiBook.git`
2.  **Navigate to your version folder**: `cd versions/nvidia_cu1281/` (or your hardware choice)
3.  **Install dependencies**: `pip install -r requirements.txt`
4.  **Start**: `python3 run.py`

## API Usage
Generate your first knowledge space:
```bash
curl -X POST http://localhost:9000/gen \
     -H "Content-Type: application/json" \
     -d '{"topic": "Quantum Physics", "pdf_paths": ["/workspace/physics.pdf"]}'
```

## Troubleshooting
- **Memory**: If hitting VRAM limits on smaller GPUs, switch from the 70B model to the 8B model.
- **AMD/ROCm**: Ensure `HSA_OVERRIDE_GFX_VERSION` matches your GPU (11.0 for MI300X).
EOF
