from fastapi import FastAPI
from pydantic import BaseModel
from app.clients.openai_client import CustomLLM, CustomOllamaEmbeddings

app = FastAPI()

llm = CustomLLM()
embeddings = CustomOllamaEmbeddings()


class PromptRequest(BaseModel):
    prompt: str


@app.post("/generate")
def generate_text(req: PromptRequest):
    response = llm._call(prompt=req.prompt)
    embedding = embeddings.embed_query(req.prompt)
    return {
        "response": response,
        "embedding": embedding
    }
