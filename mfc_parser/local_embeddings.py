from typing import List
from openai import OpenAI

from config import Config

class CustomOllamaEmbeddings:
    def __init__(self):
        self.model = Config.EMBEDDING_MODEL
        self.client = OpenAI(
            base_url=Config.OPENAI_API_URL,
            api_key=Config.LLM_API_KEY,
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._get_embeddings(texts)

    def embed_query(self, text: str) -> List[float]:
        return self._get_embeddings([text])[0]

    def _get_embeddings(self, input_texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=input_texts
        )
        return [e.embedding for e in response.data]
