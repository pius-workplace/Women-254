# gemini_embed.py
import os
import google.generativeai as genai
from llama_index.core.embeddings.base import BaseEmbedding
from typing import List

class GeminiEmbedding(BaseEmbedding):
    def __init__(self, model_name: str = "models/embedding-001", api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self.model = genai.EmbeddingModel(model_name=self.model_name)

    def _get_text_embedding(self, text: str) -> List[float]:
        result = self.model.embed(content=text)
        return result.embedding  # This is a list of floats

    def get_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    def get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return [self._get_text_embedding(t) for t in texts]
