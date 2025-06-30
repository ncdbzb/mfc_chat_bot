import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_DB = os.getenv("REDIS_DB")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    CHROMADB_HOST = os.getenv("CHROMADB_HOST", "localhost")
    CHROMADB_PORT = int(os.getenv("CHROMADB_PORT", 8800))
    CHROMA_COLLECTION_NAME = os.getenv("MFC_TICKETS_COLLECTION", "mfc_tickets")
    PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY")
    CHROMA_SERVER_AUTHN_CREDENTIALS = os.getenv("CHROMA_SERVER_AUTHN_CREDENTIALS")
    CHROMA_CLIENT_AUTH_PROVIDER = os.getenv("CHROMA_CLIENT_AUTH_PROVIDER")

    OPENAI_API_URL = os.getenv("OPENAI_API_URL")
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")