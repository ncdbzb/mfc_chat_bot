import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    MFC_PARSER_URL: str = os.getenv("MFC_PARSER_URL", "http://mfc_parser:5000")
    OPENAI_API_URL: str = os.getenv("OPENAI_API_URL")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY")
    LLM_MODEL: str = os.getenv("LLM_MODEL")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL")

settings = Settings()
