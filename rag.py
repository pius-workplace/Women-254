import os
import numpy as np
import pandas as pd
from typing import List, Dict
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()

# Provider can be "openai" or "gemini"
PROVIDER = os.getenv("PROVIDER", "openai").lower()
OPENAI_EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-large")
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "models/embedding-001")
GEMINI_GEN_MODEL = os.getenv("GEMINI_GEN_MODEL", "gemini-1.5-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

_openai_client = None
_gemini_embed_model = None
_gemini_gen_model = None

def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        from openai import OpenAI
        _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _openai_client

def _embed_openai(texts: List[str]) -> np.ndarray:
    client = _get_openai_client()
    response = client.embeddings.create(model=OPENAI_EMBED_MODEL, input=texts)
    embeddings = [data.embedding for data in response.data]
    return np.array(embeddings, dtype=float)

def _configure_gemini():
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    return genai

def _get_gemini_embed_model():
    global _gemini_embed_model
    if _gemini_embed_model is None:
        genai = _configure_gemini()
        _gemini_embed_model = GEMINI_EMBED_MODEL  # Model name for embedding
    return _gemini_embed_model

def _embed_gemini(texts: List[str]) -> np.ndarray:
    genai = _configure_gemini()
    vecs = []
    model = _get_gemini_embed_model()
    try:
        for text in texts:
            response = genai.embed_content(model=model, content=text, task_type="retrieval_document")
            vecs.append(response["embedding"])
        return np.array(vecs, dtype=float)
    except Exception as e:
        raise Exception(f"Error generating embeddings with Gemini: {str(e)}")

def embed(texts: List[str]) -> np.ndarray:
    if PROVIDER == "gemini":
        return _embed_gemini(texts)
    else:
        return _embed_openai(texts)

def _get_gemini_gen_model():
    global _gemini_gen_model
    if _gemini_gen_model is None:
        genai = _configure_gemini()
        _gemini_gen_model = genai.GenerativeModel(GEMINI_GEN_MODEL)
    return _gemini_gen_model

def generate_answer(query: str, contexts: List[Dict]) -> str:
    if PROVIDER != "gemini":
        raise ValueError("Generation currently supported only for Gemini provider.")
    
    model = _get_gemini_gen_model()
    
    # Prepare contexts
    context_text = "\n\n".join([
        f"Relevant Q: {ctx['Question']}\nA: {ctx['Answer']}\nCategory: {ctx['Category']}\nLanguage: {ctx['Language']}\nSource: {ctx['Source']}"
        for ctx in contexts
    ])
    
    # Safety prompt
    safety_prompt = (
        "You are a helpful assistant focused on providing safe, supportive, and accurate information. "
        "Do not provide any harmful, illegal, or unethical advice. If the query involves danger or emergency, "
        "direct the user to appropriate authorities or helplines. Answer only based on the provided context "
        "and filter the response to directly address the specific question asked."
    )
    
    # Full prompt
    prompt = f"{safety_prompt}\n\nQuestion: {query}\n\nUse the following context to answer the question specifically and concisely:\n{context_text}"
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating answer: {str(e)}"

class CSVKnowledgeBase:
    def __init__(self, csv_path: str):
        print(f"[INFO] Loading CSV from: {csv_path}")
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)

        # Create a combined text field for embedding
        self.df['retrieval_text'] = self.df[['Category', 'Question', 'Bot Response', 'Language', 'Source']].astype(str).agg(' | '.join, axis=1)

        self.index_path = csv_path.replace(".csv", ".npz")
        if os.path.exists(self.index_path):
            print("[INFO] Loading cached embeddings...")
            data = np.load(self.index_path)
            self.embeddings = data['embeddings']
        else:
            print("[INFO] Generating new embeddings...")
            self.embeddings = embed(self.df['retrieval_text'].tolist())
            np.savez(self.index_path, embeddings=self.embeddings)

    def query(self, query_text: str, top_k: int = 5) -> List[Dict]:
        query_vec = embed([query_text])
        similarities = cosine_similarity(query_vec, self.embeddings)[0]
        top_indices = similarities.argsort()[::-1][:top_k]

        results = []
        for i in top_indices:
            if similarities[i] > 0.5:  # Add a relevance threshold to filter
                results.append({
                    "score": float(similarities[i]),
                    "Category": self.df.iloc[i]["Category"],
                    "Question": self.df.iloc[i]["Question"],
                    "Answer": self.df.iloc[i]["Bot Response"],
                    "Language": self.df.iloc[i]["Language"],
                    "Source": self.df.iloc[i]["Source"],
                })
        return results

# Run this file directly for testing
if __name__ == "__main__":
    kb = CSVKnowledgeBase("data/knowledge.csv")

    while True:
        query = input("\nAsk a question (or type 'exit'): ")
        if query.lower() == "exit":
            break
        contexts = kb.query(query)
        if contexts:
            answer = generate_answer(query, contexts)
            print("\nAnswer:")
            print(answer)
        else:
            print("\nNo relevant information found.")