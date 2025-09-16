import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI
import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure APIs if keys are available
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
else:
    print("Warning: GEMINI_API_KEY not set. Gemini LLM will not work.")

# Load CSV documents (run once on startup)
import pandas as pd
from llama_index.core import Document

# Load CSV files and convert to documents
csv_files = ["data/knowledge.csv", "data/shebot_dataset_2000.csv", "data/shebot_mental_health_1500.csv"]
documents = []

for csv_file in csv_files:
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        # Combine relevant columns into text
        for _, row in df.iterrows():
            text = f"Category: {row.get('Category', '')} | Question: {row.get('Question', '')} | Answer: {row.get('Bot Response', row.get('Answer', ''))} | Language: {row.get('Language', '')}"
            documents.append(Document(text=text))

# Set up ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db_new")
chroma_collection = chroma_client.get_or_create_collection(name="test_documents")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Use local HuggingFace embeddings
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Create index
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model)

# Initialize Gemini LLM if API key is available
if gemini_api_key:
    llm = GoogleGenAI(model="gemini-2.0-flash-exp", api_key=gemini_api_key)
else:
    llm = None

# Jinja2 templates for serving HTML
templates = Jinja2Templates(directory="templates")

# Serve the chat interface
@app.get("/", response_class=HTMLResponse)
async def get_chat_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoint for queries with custom logic
@app.get("/query")
async def query_document(query: str):
    if index is None or llm is None:
        # Default response if no index or LLM
        base_response = "I'm sorry, the AI service is currently unavailable. Please try again later or contact support."
    else:
        system_prompt = "You are She Bot, a helpful assistant for women in Kenya facing harassment and mental health challenges. Always respond in the same language as the user's query. Provide empathetic, supportive, and relevant advice based on the knowledge base."
        query_engine = index.as_query_engine(llm=llm, system_prompt=system_prompt)
        response = query_engine.query(query)
        base_response = str(response)

    # Check for greetings and respond accordingly
    greetings = ["hello", "hi", "hey", "greetings", "habari", "jambo"]  # Added Swahili greetings
    query_lower = query.lower().strip()
    if any(greeting in query_lower for greeting in greetings):
        # Detect language and respond in kind
        if any(word in query_lower for word in ["habari", "jambo", "niko", "sawa"]):
            base_response = "Habari! Mimi ni She Bot, hapa kusaidia wanawake nchini Kenya wanaokabiliwa na unyanyasaji na changamoto za afya ya akili. Ninawezaje kukusaidia leo?"
        else:
            base_response = "Hello! I am She Bot, here to support women in Kenya facing harassment and mental health challenges. How can I assist you today?"
    # No else needed, keep the base_response from above

    # Append developer credit only if asked about the developer
    developer_keywords = ["who made", "who developed", "who created", "developer", "creator"]
    if any(keyword in query_lower for keyword in developer_keywords):
        base_response += " (Developed by Denis Pius)"

    return {"query": query, "response": base_response}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)