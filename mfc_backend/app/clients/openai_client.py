from typing import Any, Dict, List, Optional, Union

import requests
from openai import OpenAI
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.embeddings import Embeddings

from app.config.config import settings


class CustomLLM(LLM):
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        return self.get_response_from_server(prompt)

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model_name": "CustomChatModel",
        }

    @property
    def _llm_type(self) -> str:
        return "custom"

    def get_response_from_server(self, prompt: str) -> str:
        client = OpenAI(
            base_url=settings.OPENAI_API_URL,
            api_key=settings.LLM_API_KEY,
        )

        completion = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content


class CustomOllamaEmbeddings(Embeddings):
    def __init__(self):
        self.model = settings.EMBEDDING_MODEL
        self.client = OpenAI(
            base_url=settings.OPENAI_API_URL,
            api_key=settings.LLM_API_KEY,
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
