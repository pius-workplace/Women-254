# gemini_embed.py
import os
import google.generativeai as genai
from typing import List, Optional
from llama_index.core.embeddings import BaseEmbedding

class GeminiEmbedding(BaseEmbedding):
    api_key: Optional[str] = None
    model_name: str = "models/embedding-001"

    def __init__(self, model_name: str = "models/embedding-001", api_key: str = None, **kwargs):
        super().__init__(model_name=model_name, **kwargs)
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)

    def _get_text_embedding(self, text: str) -> List[float]:
        result = genai.embed_content(model=self.model_name, content=text)
        return result['embedding']  # This is a list of floats

    def get_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    def get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return [self._get_text_embedding(t) for t in texts]

    def embed_query(self, query: str) -> List[float]:
        return self._get_text_embedding(query)

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        return self.get_text_embeddings(documents)

    def _get_query_embedding(self, query: str) -> List[float]:
        return self._get_text_embedding(query)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_text_embedding(query)
