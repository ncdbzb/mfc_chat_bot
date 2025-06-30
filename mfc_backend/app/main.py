import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

from app.clients.parser_client import MFCParserClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    async def wait_for_parser_readiness():
        await asyncio.sleep(1)
        client = MFCParserClient()
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, client.wait_until_ready)

    await wait_for_parser_readiness()
    yield


app = FastAPI(lifespan=lifespan)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_text(req: PromptRequest):
    # Пробуем искать в ChromaDB
    client = MFCParserClient()
    results = client.search_chroma(req.prompt)

    return {
        "input_prompt": req.prompt,
        "found_situations": results
    }