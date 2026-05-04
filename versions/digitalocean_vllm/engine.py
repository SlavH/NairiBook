import os, json, httpx, re
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

class WorldEngine:
    def __init__(self, vllm_url="http://localhost:8000/v1"):
        self.vllm_url = vllm_url

    def build_index(self, pdf_paths, index_path):
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        all_chunks = []
        for p in pdf_paths:
            if os.path.exists(p):
                all_chunks.extend(splitter.split_documents(PyPDFLoader(p).load()))
        vs = FAISS.from_documents(all_chunks, embeddings)
        vs.save_local(index_path)
        return vs

    async def generate_description(self, topic, context, model_name):
        prompt = f"Create a JSON world map for {topic} based on: {context[:4000]}. JSON ONLY.\n" + \
                 '{"world_name": "Name", "description": "Brief", "objects": [{"name": "Obj1", "description": "What it is", "appearance": "Visual"}], "environment": {"sky_color": "#1a1a2e"}}'
        
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(f"{self.vllm_url}/chat/completions",
                json={"model": model_name, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7})
            content = r.json()["choices"][0]["message"]["content"]
            match = re.search(r'\{.*\}', content, re.DOTALL)
            return json.loads(match.group()) if match else json.loads(content)
