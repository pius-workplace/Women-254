import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
import datetime as dt
import shutil
import time

app = FastAPI(title="SHEBot API", description="API for indexing and querying multiple documents using LlamaIndex and ChromaDB", version="0.1.0")

# ChromaDB setup (persistent)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection(name="shebot_documents")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
embed_model = OpenAIEmbedding(api_key=os.getenv("OPENAI_API_KEY"))  # Set your AP
# Global index (load or create on startup)
try:
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)
except ValueError:
    index = VectorStoreIndex([], storage_context=storage_context, embed_model=embed_model)

MAX_REQUESTS_PER_MINUTE = 100
request_counts = {}

class QueryRequest(BaseModel):
    query: str
    user_lang: str | None = None  # "en", "sw", "sheng"
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    used_provider: str
    retrieved: List[Dict]
    ts: str

SYSTEM_PROMPT = """You are SHEBot: a Kenyan women’s safety assistant.
Follow Safety by Design: privacy-first, trauma‑informed, concise.
If emergency keywords appear, return the emergency contacts first.
Answer in the same language the user uses (English, Swahili, or Sheng) when possible.
If unsure, say so and offer reputable local contacts.
You are supportive and non‑judgmental.
"""

def _llm_answer(prompt: str) -> str:
    from google.generativeai import GenerativeModel  # Assuming Gemini as default provider
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
    genai = GenerativeModel(GEMINI_MODEL, safety_settings={
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_MEDIUM_AND_ABOVE',
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_MEDIUM_AND_ABOVE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_MEDIUM_AND_ABOVE',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_MEDIUM_AND_ABOVE'
    })
    resp = genai.generate_content(prompt)
    return resp.text

def build_prompt(user_msg: str, retrieved_nodes: List[Dict]) -> str:
    filtered_contexts = [node for node in retrieved_nodes if node.get("score", 0) >= 0.7]
    if not filtered_contexts:
        return f"""User: {user_msg}

Rules:
- No relevant context found. Say you are unsure and suggest contacting 999 or 1195 if relevant.
- Be supportive and non‑judgmental.
- Avoid speculation or unrelated information.
"""

    ctx_lines = []
    for node in filtered_contexts:
        if any(keyword in user_msg.lower() for keyword in node["text"].lower().split()[:5]):  # Check first 5 words
            ctx_lines.append(f"- Q: {node['text'][:50]}... | Source: {node.get('metadata', {}).get('source', 'unknown')}")
    ctx = "\n".join(ctx_lines) if ctx_lines else "No directly relevant context found."

    return f"""Use ONLY the provided context to answer the user’s exact question safely and accurately.
Context:
{ctx}

User: {user_msg}

Rules:
- Answer directly based on the context, citing sources inline if used (e.g., [Source: unknown]).
- If the context does not address the question, say you are unsure and suggest contacting 999 or 1195 if relevant.
- Do not speculate, generate unrelated content, or provide information beyond the context.
- Be supportive and non‑judgmental.
- Apply safety-first principles: avoid sharing personal data, focus on empowerment, and redirect to professionals for complex issues.
"""

@app.post("/index")
async def index_documents(files: List[UploadFile] = File(...), user_lang: str = Form(None)):
    try:
        temp_dir = "temp_docs"
        os.makedirs(temp_dir, exist_ok=True)
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        
        # Load and index multiple documents
        documents = SimpleDirectoryReader(input_dir=temp_dir, recursive=True).load_data()
        index.insert_nodes(documents)
        
        # Clean up
        shutil.rmtree(temp_dir)
        return JSONResponse(content={"message": f"{len(files)} documents indexed successfully", "language": user_lang or "en"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_documents(req: QueryRequest):
    client_ip = "127.0.0.1"  # In production, use real IP
    if client_ip not in request_counts:
        request_counts[client_ip] = []
    request_counts[client_ip] = [t for t in request_counts[client_ip] if time.time() - t < 60]
    if len(request_counts[client_ip]) >= MAX_REQUESTS_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Too many requests")
    request_counts[client_ip].append(time.time())

    from safety import detect_emergency, emergency_response
    if detect_emergency(req.query):
        er = emergency_response()
        lang_key = "en"
        if req.user_lang and req.user_lang.lower().startswith("sw"):
            lang_key = "sw"
        elif req.user_lang and "sheng" in req.user_lang.lower():
            lang_key = "sheng"
        answer = er[lang_key]
        return QueryResponse(answer=answer, used_provider="rule/emergency", retrieved=[], ts=dt.datetime.utcnow().isoformat())

    query_engine = index.as_query_engine(similarity_top_k=req.top_k)
    response = query_engine.query(req.query)
    retrieved_nodes = [{"text": node.text, "score": node.score, "metadata": node.metadata} for node in response.source_nodes]
    
    if not retrieved_nodes:
        return QueryResponse(answer="I'm unsure. For help, contact 999 or 1195.", used_provider="llm", retrieved=[], ts=dt.datetime.utcnow().isoformat())

    prompt = build_prompt(req.query, retrieved_nodes)
    answer = _llm_answer(prompt)
    from safety import validate_safety_response
    is_safe, safety_msg = validate_safety_response(answer)
    if not is_safe:
        answer = f"I'm sorry, I can't assist with that due to safety concerns: {safety_msg}. Please contact 999 or 1195."
    user_keywords = set(req.query.lower().split())
    answer_keywords = set(answer.lower().split())
    if not user_keywords & answer_keywords and "unsure" not in answer.lower():
        answer = "I'm unsure. Please provide more details or contact 999 or 1195 for help."

    current_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S EAT")
    print(f"{current_time} - User: [redacted] | Answer: {answer}")
    return QueryResponse(answer=answer, used_provider="llm", retrieved=retrieved_nodes, ts=dt.datetime.utcnow().isoformat())

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)